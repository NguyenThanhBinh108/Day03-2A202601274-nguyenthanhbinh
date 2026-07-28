"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Security + Multi-Provider.
Pipeline: Input → Security Check → Intent Router → Chatbot | ReAct Agent → Response

Cách chạy:
    python src/app.py           # chạy test case mặc định (TC6)
    python src/app.py 10        # chạy riêng TC10
    python src/app.py 8 9 10    # chạy nhiều test case
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
    GUARDRAIL_MESSAGE,
    ADVERSARIAL_RESPONSE,
    REACT_STOP_SEQUENCES,
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

# Bộ nhận dạng các dòng trong giao thức ReAct
THOUGHT_RE = re.compile(r"^Thought:\s*(.+)$", re.MULTILINE)
ACTION_RE = re.compile(r"^Action:\s*(\w+)\s*\[(.*?)\]\s*$", re.MULTILINE)
FINAL_RE = re.compile(r"^Final Answer:\s*(.*)$", re.MULTILINE | re.DOTALL)


# ============================================================
# HELPERS
# ============================================================

def load_test_cases() -> list:
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    # Fallback kiểm tra nếu file ở thư mục hiện tại
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
        Action: tool_name(arg1, arg2)   ← format v2.0
        Action: tool_name[arg1, arg2]   ← format main branch
    Returns: (tool_name, [arg1, arg2, ...])
    """
    # Format: tool_name[args]  (main branch format — ưu tiên vì REACT_SYSTEM_PROMPT dùng format này)
    m = ACTION_RE.search(text)
    if m:
        name = m.group(1).strip()
        raw_args = m.group(2).strip()
        args = [a.strip().strip("\"'") for a in raw_args.split(",") if a.strip()]
        return name, args

    # Format: tool_name(args)  (fallback)
    m = re.search(r"Action\s*:\s*(\w+)\(([^)]*)\)", text)
    if m:
        name = m.group(1).strip()
        raw_args = m.group(2).strip()
        args = [a.strip().strip("\"'") for a in raw_args.split(",") if a.strip()]
        return name, args

    return None, []


def extract_thought(text: str) -> str:
    """Trích xuất nội dung Thought từ LLM output."""
    m = THOUGHT_RE.search(text)
    if m:
        return m.group(1).strip()
    m = re.search(r"Thought\s*:\s*(.+?)(?=\n(?:Action|Final Answer)|$)", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()[:200]


def extract_final_answer(text: str) -> str:
    """Trích xuất Final Answer từ LLM output."""
    m = FINAL_RE.search(text)
    if m:
        return m.group(1).strip()
    m = re.search(r"Final Answer\s*:\s*(.+)", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def _cut_hallucinated_observation(text: str) -> str:
    """
    🛡️ Cắt bỏ phần Agent TỰ BỊA dòng Observation.

    Provider hiện chưa hỗ trợ stop_sequences, nên ta cắt thủ công: mọi thứ từ
    'Observation:' trở đi đều bị bỏ, vì Observation là việc của hệ thống.
    """
    idx = text.find("Observation:")
    return text[:idx].strip() if idx != -1 else text.strip()


def execute_tool(tool_name: str, raw_args: str) -> str:
    """
    Thực thi một công cụ theo tên và chuỗi tham số Agent sinh ra.

    LUÔN trả về chuỗi, KHÔNG BAO GIỜ ném exception ra ngoài — nếu tool lỗi thì
    Agent phải đọc được thông báo lỗi để tự phục hồi (Failure Mode #1, #4).
    """
    # 🛡️ Guardrail: Agent gọi tool không tồn tại
    if tool_name not in AVAILABLE_TOOLS:
        ds = ", ".join(AVAILABLE_TOOLS)
        return f"LỖI: Không có công cụ tên '{tool_name}'. Các công cụ hợp lệ: {ds}."

    fn = AVAILABLE_TOOLS[tool_name]
    args = [a.strip().strip("'\"") for a in raw_args.split(",")] if raw_args.strip() else []

    try:
        return fn(*args)
    except TypeError:
        # 🛡️ Guardrail: Agent truyền sai số lượng tham số → thử gộp lại làm 1
        try:
            return fn(raw_args.strip())
        except Exception as e:
            return f"LỖI: Gọi '{tool_name}' sai tham số ({e})."
    except Exception as e:
        logger.error(f"Tool {tool_name} exception: {e}")
        return f"LỖI: Công cụ '{tool_name}' gặp sự cố: {e}"


def safe_execute_tool(tool_name: str, args: list[str]) -> str:
    """Wrapper cho execute_tool khi args đã parse thành list."""
    raw_args = ", ".join(args)
    return execute_tool(tool_name, raw_args)


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
        logger.info("[Security] Salary guarantee request detected")
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

    # Transcript-style history (tương thích với cả hai format)
    transcript = f"{REACT_SYSTEM_PROMPT}\nQuestion: {cleaned}\n"
    trace: list[dict] = []
    observations: list[str] = []
    start_time = time.time()
    used_actions: set[str] = set()  # Detect duplicate tool calls

    for step in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        # Gọi LLM
        raw = provider.generate(transcript, system_prompt="")
        output = _cut_hallucinated_observation(raw)

        if not output:
            logger.warning(f"[Agent] Step {step}: Empty LLM response")
            break

        step_trace: dict = {"step": step, "llm_output": output}

        thought_m = THOUGHT_RE.search(output)
        thought = thought_m.group(1).strip() if thought_m else extract_thought(output)
        print(f"🧠 Thought: {thought}")
        step_trace["thought"] = thought

        action_m = ACTION_RE.search(output)
        final_m = FINAL_RE.search(output)

        # --- Final Answer ---
        if final_m and not action_m:
            final_answer = final_m.group(1).strip()

            # Grounding check
            grounding = check_response_grounding(final_answer, observations)
            if not grounding["grounded"]:
                logger.warning(f"[Grounding] Ungrounded claims: {grounding['ungrounded_claims']}")
                print(f"⚠️ [Grounding Warning] Số liệu chưa xác thực: {grounding['ungrounded_claims']}")

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

        # --- Fallback: Final Answer without explicit action check ---
        if "Final Answer:" in output and not action_m:
            final_answer = extract_final_answer(output)
            grounding = check_response_grounding(final_answer, observations)
            step_trace["final_answer"] = final_answer
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

        # --- Action ---
        if not action_m:
            print(f"⚠️ Không đọc được Action lẫn Final Answer. Output thô:\n{output[:300]}")
            trace.append(step_trace)
            break

        tool_name = action_m.group(1)
        raw_args = action_m.group(2)
        signature = f"{tool_name}[{raw_args}]"

        # 🛡️ Guardrail: cấm lặp lại y hệt một Action đã gọi
        if signature in used_actions:
            print(f"🛠️ Action: {signature}")
            print("🛡️ GUARDRAIL: Action này đã gọi rồi, chặn để tránh lặp vô tận.")
            observation = (
                f"LỖI: Bạn đã gọi công cụ này với đúng tham số này rồi. "
                f"Hãy đổi cách tiếp cận hoặc trả lời luôn cho người dùng."
            )
        else:
            used_actions.add(signature)
            print(f"🛠️ Action: {signature}")
            observation = execute_tool(tool_name, raw_args)

        observations.append(observation)
        print(f"👁️ Observation: {observation[:300]}{'...' if len(observation) > 300 else ''}")

        step_trace["action"] = tool_name
        step_trace["args"] = [a.strip() for a in raw_args.split(",")]
        step_trace["observation"] = observation
        trace.append(step_trace)

        transcript += f"\nThought: {thought}\nAction: {signature}\nObservation: {observation}\n"

    # MAX_ITERATIONS reached without Final Answer
    elapsed = time.time() - start_time
    print(f"\n🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn {MAX_ITERATIONS} bước. Trả về safe fallback.")
    print(f"🏁 Final Answer: {GUARDRAIL_MESSAGE}")
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
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json")
    print(f"🛡️ Guardrail: MAX_ITERATIONS = {MAX_ITERATIONS}\n")

    # Cho phép chọn test case từ dòng lệnh: python src/app.py 8 9 10
    wanted = {tc["id"] for tc in tests if tc["id"] in {a for a in sys.argv[1:]}}
    if not wanted and len(sys.argv) > 1:
        # Thử parse số nguyên: python src/app.py 6
        nums = {int(a) for a in sys.argv[1:] if a.isdigit()}
        wanted = {tc["id"] for tc in tests if any(tc["id"].endswith(str(n)) for n in nums)}

    selected = [t for t in tests if t["id"] in wanted] if wanted else [tests[5]]

    for tc in selected:
        print("\n" + "=" * 60)
        print(f"📌 TEST CASE {tc['id']} — {tc.get('category', 'unknown')}")
        if tc.get("scenario"):
            print(f"📝 {tc['scenario']}")
        print("=" * 60)

        query = _get_query(tc)
        session = make_session_id(tc["id"])

        print("\n--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE (Cấp 2 — Không tool) ---")
        run_baseline_chatbot(query, provider, session)

        print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT (Cấp 3 — Có tool, có guardrails) ---")
        result = run_react_agent(query, provider, session)

        # Save trace log
        trace_path = os.path.join(_LOG_DIR, f"trace_{session}.json")
        with open(trace_path, "w", encoding="utf-8") as f:
            json.dump({
                "session_id": session,
                "tc_id": tc["id"],
                "query": query,
                "agent_result": result
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📝 Trace log saved: {trace_path}")
