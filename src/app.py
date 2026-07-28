"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Security + Multi-Provider.
Pipeline: Input → Security Check → Intent Router → Chatbot | ReAct Agent → Response
"""

import json
import os
import re
import sys
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Import các thành phần từ các Role
from tools import AVAILABLE_TOOLS
from prompts import (
    CHATBOT_BASELINE_PROMPT,
    REACT_SYSTEM_PROMPT,
    MAX_ITERATIONS,
    TIMEOUT_SECONDS,
    SAFE_FALLBACK_MESSAGE,
    ADVERSARIAL_RESPONSE,
)
from providers import get_llm_provider
from security import (
    sanitize_input,
    detect_injection,
    detect_off_topic,
    detect_salary_guarantee_request,
    check_response_grounding,
    get_rate_limiter,
    make_session_id,
)

load_dotenv()

# ============================================================
# LOGGING SETUP
# ============================================================

_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(_LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(_LOG_DIR, "app.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("edupath")


# ============================================================
# HELPERS
# ============================================================

def load_test_cases() -> list:
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_query(tc: dict) -> str:
    """Lấy câu hỏi từ test case — hỗ trợ cả Schema A ('question') và Schema B ('input')."""
    return tc.get("question") or tc.get("input") or "Hãy tư vấn nghề nghiệp IT cho tôi"


def parse_action(text: str) -> tuple[str | None, list[str]]:
    """
    Trích xuất Action và tham số từ LLM output.
    Hỗ trợ các format:
        Action: tool_name(arg1, arg2)
        Action: tool_name["arg1"]
        Action: tool_name[arg1, arg2]
    Returns: (tool_name, [arg1, arg2, ...])
    """
    # Format: tool_name(args)
    m = re.search(r"Action\s*:\s*(\w+)\(([^)]*)\)", text)
    if m:
        name = m.group(1).strip()
        raw_args = m.group(2).strip()
        args = [a.strip().strip("\"'") for a in raw_args.split(",") if a.strip()]
        return name, args

    # Format: tool_name["args"] or tool_name[args]
    m = re.search(r"Action\s*:\s*(\w+)\[([^\]]*)\]", text)
    if m:
        name = m.group(1).strip()
        raw_args = m.group(2).strip()
        args = [a.strip().strip("\"'") for a in raw_args.split(",") if a.strip()]
        return name, args

    return None, []


def extract_thought(text: str) -> str:
    """Trích xuất nội dung Thought từ LLM output."""
    m = re.search(r"Thought\s*:\s*(.+?)(?=\n(?:Action|Final Answer)|$)", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()[:200]


def extract_final_answer(text: str) -> str:
    """Trích xuất Final Answer từ LLM output."""
    m = re.search(r"Final Answer\s*:\s*(.+)", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def safe_execute_tool(tool_name: str, args: list[str]) -> str:
    """
    Gọi tool an toàn với timeout và error handling.
    Không crash app — luôn trả về string (kể cả khi lỗi).
    """
    if tool_name not in AVAILABLE_TOOLS:
        return json.dumps({
            "status": "error",
            "error": f"Tool '{tool_name}' không tồn tại. Các tool hợp lệ: {', '.join(AVAILABLE_TOOLS.keys())}",
            "retryable": False
        }, ensure_ascii=False)

    tool_fn = AVAILABLE_TOOLS[tool_name]
    try:
        # Call tool với timeout (signal-based trên Unix, threading trên Windows)
        result = tool_fn(*args)
        logger.info(f"Tool {tool_name}({args}) → {str(result)[:100]}...")
        return result
    except TypeError as e:
        return json.dumps({
            "status": "invalid_args",
            "error": f"Sai tham số cho tool '{tool_name}': {str(e)}",
            "retryable": False
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Tool {tool_name} exception: {e}")
        return json.dumps({
            "status": "error",
            "error": f"Lỗi khi chạy tool '{tool_name}': {str(e)}",
            "retryable": True
        }, ensure_ascii=False)


# ============================================================
# SECURITY PIPELINE
# ============================================================

def security_check(user_input: str, session_id: str) -> tuple[str | None, str | None]:
    """
    Chạy tất cả security checks TRƯỚC khi gọi LLM.
    Returns: (cleaned_input, error_response_or_None)
    None trong error_response_or_None = OK, tiếp tục.
    """
    rate_limiter = get_rate_limiter()
    if not rate_limiter.allow(session_id):
        return None, "⏳ Bạn đang gửi quá nhiều yêu cầu. Vui lòng chờ 1 phút và thử lại."

    cleaned, warnings = sanitize_input(user_input)
    if warnings:
        logger.info(f"[Security] Input sanitized: {warnings}")

    if detect_injection(cleaned):
        logger.warning(f"[Security] Prompt injection detected: {cleaned[:100]}")
        return None, ADVERSARIAL_RESPONSE

    if detect_salary_guarantee_request(cleaned):
        logger.info(f"[Security] Salary guarantee request detected")
        return cleaned, None  # Không block, nhưng flag để xử lý ở response level

    return cleaned, None


# ============================================================
# CHATBOT BASELINE (Cấp 2 — LLM only, không tool)
# ============================================================

def run_baseline_chatbot(user_query: str, provider, session_id: str = "") -> dict:
    """
    Chatbot gốc (Baseline) không có công cụ.
    Mốc 2: Chứng minh LLM thuần không thể đáp ứng câu hỏi cần data thực.
    """
    session_id = session_id or make_session_id()
    logger.info(f"[Chatbot] Session {session_id[:8]} | Query: {user_query[:80]}")

    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")

    # Security check
    cleaned, error = security_check(user_query, session_id + "_chatbot")
    if error:
        print(f"🛡️ [BLOCKED] {error}")
        return {"status": "blocked", "response": error, "session_id": session_id}

    start = time.time()
    response = provider.generate(cleaned, system_prompt=CHATBOT_BASELINE_PROMPT)
    elapsed = time.time() - start

    print(f"🤖 Chatbot trả lời:\n{response}")
    print(f"⏱️ Thời gian: {elapsed:.2f}s")

    return {
        "status": "success",
        "mode": "chatbot_baseline",
        "query": user_query,
        "response": response,
        "session_id": session_id,
        "elapsed_seconds": round(elapsed, 2),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================
# REACT AGENT (Cấp 3 — Thought → Action → Observation loop)
# ============================================================

def run_react_agent(user_query: str, provider, session_id: str = "") -> dict:
    """
    ReAct Agent thực với vòng lặp Thought → Action → Observation.
    Mốc 3: Agent gọi tool thực, nhận Observation thực, có Guardrails đầy đủ.

    Returns:
        dict với status, answer, trace, steps, elapsed_seconds
    """
    session_id = session_id or make_session_id()
    logger.info(f"[Agent] Session {session_id[:8]} | Query: {user_query[:80]}")

    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")

    # Security check
    cleaned, error = security_check(user_query, session_id + "_agent")
    if error:
        print(f"🛡️ [BLOCKED] {error}")
        return {"status": "blocked", "answer": error, "trace": [], "steps": 0, "session_id": session_id}

    # Build conversation history (multi-turn aware)
    history: list[dict] = [{"role": "user", "content": cleaned}]
    trace: list[dict] = []
    observations: list[str] = []
    start_time = time.time()
    seen_actions: set[str] = set()  # Detect duplicate tool calls

    for step in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        # Build full prompt from history
        full_prompt = "\n\n".join(
            f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}"
            for m in history
        )

        # Gọi LLM
        llm_response = provider.generate(full_prompt, system_prompt=REACT_SYSTEM_PROMPT)
        step_trace: dict = {"step": step, "llm_output": llm_response}

        thought = extract_thought(llm_response)
        print(f"🧠 Thought: {thought}")
        step_trace["thought"] = thought

        # Kiểm tra Final Answer
        if "Final Answer:" in llm_response:
            final_answer = extract_final_answer(llm_response)

            # Grounding check — cảnh báo nếu claim không có trong observations
            grounding = check_response_grounding(final_answer, observations)
            if not grounding["grounded"]:
                logger.warning(f"[Grounding] Ungrounded claims: {grounding['ungrounded_claims']}")
                print(f"⚠️ [Grounding Warning] Một số số liệu chưa được xác thực: {grounding['ungrounded_claims']}")

            print(f"🏁 Final Answer:\n{final_answer}")
            step_trace["final_answer"] = final_answer
            step_trace["grounding"] = grounding
            trace.append(step_trace)

            elapsed = time.time() - start_time
            return {
                "status": "success",
                "answer": final_answer,
                "trace": trace,
                "steps": step,
                "observations": observations,
                "grounding": grounding,
                "session_id": session_id,
                "elapsed_seconds": round(elapsed, 2),
                "timestamp": datetime.now().isoformat()
            }

        # Parse Action
        action_name, action_args = parse_action(llm_response)
        step_trace["action"] = action_name
        step_trace["args"] = action_args

        if not action_name:
            # LLM không ra Action cũng không ra Final Answer — fallback
            logger.warning(f"[Agent] Step {step}: No Action or Final Answer parsed")
            trace.append(step_trace)
            break

        print(f"🛠️ Action: {action_name}({', '.join(action_args)})")

        # Detect duplicate tool call (loop prevention)
        action_key = f"{action_name}({','.join(action_args)})"
        if action_key in seen_actions:
            observation = json.dumps({
                "status": "loop_detected",
                "error": f"Tool '{action_name}' đã được gọi với cùng tham số. Không lặp lại."
            }, ensure_ascii=False)
            logger.warning(f"[Agent] Duplicate action detected: {action_key}")
        else:
            seen_actions.add(action_key)
            observation = safe_execute_tool(action_name, action_args)

        observations.append(observation)
        print(f"👁️ Observation: {observation[:300]}{'...' if len(observation) > 300 else ''}")

        step_trace["observation"] = observation
        trace.append(step_trace)

        # Cập nhật conversation history
        history.append({"role": "assistant", "content": llm_response})
        history.append({"role": "user", "content": f"Observation: {observation}"})

    # MAX_ITERATIONS reached without Final Answer
    elapsed = time.time() - start_time
    print(f"\n🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn {MAX_ITERATIONS} bước. Trả về safe fallback.")
    logger.warning(f"[Agent] Session {session_id[:8]} hit MAX_ITERATIONS after {elapsed:.2f}s")

    return {
        "status": "max_iterations_reached",
        "answer": SAFE_FALLBACK_MESSAGE,
        "trace": trace,
        "steps": MAX_ITERATIONS,
        "observations": observations,
        "session_id": session_id,
        "elapsed_seconds": round(elapsed, 2),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================
# MAIN — Demo chạy thử
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🏫 VINUNI LAB 3 — CHATBOT VS REACT AGENT")
    print("📊 Dataset: ITviec & TopDev VN 2025 (77 roles, 2795 JDs)")
    print("=" * 60)

    # Khởi tạo LLM Provider từ biến môi trường
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock")
    print(f"\n🔌 Provider: {provider.__class__.__name__} | Model: {model_name}")

    # Load test cases
    tests = load_test_cases()
    print(f"✅ Loaded {len(tests)} test cases\n")

    # Demo với test case số 3 (index 2) — hỗ trợ cả 2 schema
    sample_query = _get_query(tests[2])

    session = make_session_id("demo")
    print(f"🔑 Session ID: {session}")

    print("\n" + "─" * 60)
    print("DEMO 1: CHATBOT BASELINE (Cấp 2 — Không tool)")
    print("─" * 60)
    chatbot_result = run_baseline_chatbot(sample_query, provider, session)

    print("\n" + "─" * 60)
    print("DEMO 2: REACT AGENT (Cấp 3 — Có tool, có guardrails)")
    print("─" * 60)
    agent_result = run_react_agent(sample_query, provider, session)

    print("\n" + "─" * 60)
    print("📊 SUMMARY")
    print("─" * 60)
    print(f"Chatbot: {chatbot_result.get('status')} | {chatbot_result.get('elapsed_seconds', 0):.2f}s")
    print(f"Agent:   {agent_result.get('status')} | {agent_result.get('steps', 0)} steps | {agent_result.get('elapsed_seconds', 0):.2f}s")

    # Save trace log
    trace_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "logs", f"trace_{session}.json"
    )
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump({
            "session_id": session,
            "query": sample_query,
            "chatbot_result": chatbot_result,
            "agent_result": agent_result
        }, f, ensure_ascii=False, indent=2)
    print(f"\n📝 Trace log saved: {trace_path}")
