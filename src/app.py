"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.

Cách chạy:
    python src/app.py           # chạy test case mặc định (TC6)
    python src/app.py 10        # chạy riêng TC10
    python src/app.py 8 9 10    # chạy nhiều test case
"""

import json
import os
import re
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import AVAILABLE_TOOLS
from prompts import (
    CHATBOT_BASELINE_PROMPT,
    REACT_SYSTEM_PROMPT,
    MAX_ITERATIONS,
    GUARDRAIL_MESSAGE,
)
from providers import get_llm_provider

load_dotenv()

# Bộ nhận dạng các dòng trong giao thức ReAct do Role 3 quy định
THOUGHT_RE = re.compile(r"^Thought:\s*(.+)$", re.MULTILINE)
ACTION_RE = re.compile(r"^Action:\s*(\w+)\s*\[(.*?)\]\s*$", re.MULTILINE)
FINAL_RE = re.compile(r"^Final Answer:\s*(.*)$", re.MULTILINE | re.DOTALL)

# 🚨 Các model nhóm đã test và XÁC NHẬN LỖI với REACT_SYSTEM_PROMPT dài.
# Cảnh báo ngay lúc khởi động để không ai mất thời gian debug màn hình trắng.
KNOWN_BAD_MODELS = {
    "gemini-flash-lite-latest": "trả về rỗng (MALFORMED_RESPONSE) khi gặp prompt ReAct dài",
    "gemini-2.5-flash": "Google đã ngừng cấp cho tài khoản mới (lỗi 404 NOT_FOUND)",
    "gemini-2.0-flash-lite": "đã hết hạn mức ngày ở gói free",
}
RECOMMENDED_MODEL = "gemini-3.1-flash-lite"


def check_model_config(provider):
    """
    Kiểm tra model đang cấu hình có nằm trong danh sách đã biết là lỗi không.
    In cảnh báo rõ ràng thay vì để người chạy tự đoán khi thấy output rỗng.
    """
    model = getattr(provider, "model_name", "") or ""
    if model in KNOWN_BAD_MODELS:
        print()
        print("=" * 66)
        print(f"⚠️  CẢNH BÁO: model '{model}' đã được nhóm test và XÁC NHẬN LỖI.")
        print(f"    Lý do: {KNOWN_BAD_MODELS[model]}")
        print(f"    ➜ Hãy sửa file .env thành: LLM_MODEL={RECOMMENDED_MODEL}")
        print("=" * 66)
        return False
    if provider.__class__.__name__ == "MockProvider":
        print()
        print("=" * 66)
        print("⚠️  CẢNH BÁO: đang chạy MockProvider (không có API key).")
        print("    Mọi câu hỏi sẽ trả về CÙNG một chuỗi -> không dùng để chấm điểm.")
        print("    ➜ Hãy copy .env.example thành .env rồi điền GEMINI_API_KEY.")
        print("=" * 66)
        return False
    return True


def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")

    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")

    # Gọi LLM Provider thực hiện sinh câu trả lời
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")
    return response


# =============================================================================
# 🛠️ TẦNG THỰC THI CÔNG CỤ
# =============================================================================

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
        # 🛡️ Guardrail: Agent truyền sai số lượng tham số -> thử gộp lại làm 1
        try:
            return fn(raw_args.strip())
        except Exception as e:
            return f"LỖI: Gọi '{tool_name}' sai tham số ({e})."
    except Exception as e:
        return f"LỖI: Công cụ '{tool_name}' gặp sự cố: {e}"


def _cut_hallucinated_observation(text: str) -> str:
    """
    🛡️ Cắt bỏ phần Agent TỰ BỊA dòng Observation.

    Provider hiện chưa hỗ trợ stop_sequences, nên ta cắt thủ công: mọi thứ từ
    'Observation:' trở đi đều bị bỏ, vì Observation là việc của hệ thống.
    """
    idx = text.find("Observation:")
    return text[:idx].strip() if idx != -1 else text.strip()


# =============================================================================
# 🤖 VÒNG LẶP REACT
# =============================================================================

def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails.

    Mỗi vòng:
      1. Gọi LLM với REACT_SYSTEM_PROMPT + toàn bộ lịch sử hội thoại
      2. Đọc ra Thought / Action / Final Answer
      3. Nếu có Action -> thực thi tool, nối Observation vào lịch sử, lặp tiếp
      4. Nếu có Final Answer -> dừng và trả lời người dùng
      5. Quá MAX_ITERATIONS -> guardrail cắt an toàn
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")

    transcript = f"{REACT_SYSTEM_PROMPT}\nQuestion: {user_query}\n"
    used_actions = set()

    for step in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        raw = provider.generate(transcript, system_prompt="")
        output = _cut_hallucinated_observation(raw)

        if not output:
            print("❌ LLM trả về RỖNG.")
            print(f"   ➜ Nguyên nhân thường gặp: model không xử lý được prompt dài.")
            print(f"   ➜ Hãy sửa .env thành: LLM_MODEL={RECOMMENDED_MODEL}")
            return None

        if output.startswith("[") and ("Error" in output[:40] or "Exception" in output[:40]):
            print(f"❌ Provider báo lỗi: {raw[:250]}")
            if "RESOURCE_EXHAUSTED" in raw or "429" in raw:
                print("   ➜ Hết hạn mức gọi API. Chờ 1 phút rồi chạy lại, "
                      "hoặc đổi LLM_MODEL / API key.")
            return None

        thought_m = THOUGHT_RE.search(output)
        thought = thought_m.group(1).strip() if thought_m else "(không sinh Thought)"
        action_m = ACTION_RE.search(output)
        final_m = FINAL_RE.search(output)

        print(f"🧠 Thought: {thought}")

        # --- Trường hợp Agent đã đủ thông tin để trả lời ---
        if final_m and not action_m:
            answer = final_m.group(1).strip()
            print(f"🏁 Final Answer: {answer}")
            return answer

        # --- Trường hợp Agent sinh sai định dạng ---
        if not action_m:
            print(f"⚠️ Không đọc được Action lẫn Final Answer. Output thô:\n{output[:300]}")
            return None

        tool_name, raw_args = action_m.group(1), action_m.group(2)
        signature = f"{tool_name}[{raw_args}]"

        # 🛡️ Guardrail: cấm lặp lại y hệt một Action đã gọi
        if signature in used_actions:
            print(f"🛠️ Action: {signature}")
            print("🛡️ GUARDRAIL: Action này đã gọi rồi, chặn để tránh lặp vô tận.")
            transcript += (
                f"\nThought: {thought}\nAction: {signature}\n"
                f"Observation: LỖI: Bạn đã gọi công cụ này với đúng tham số này rồi. "
                f"Hãy đổi cách tiếp cận hoặc trả lời luôn cho người dùng.\n"
            )
            continue

        used_actions.add(signature)

        # --- Thực thi tool và ghi nhận Observation ---
        print(f"🛠️ Action: {signature}")
        observation = execute_tool(tool_name, raw_args)
        print(f"👁️ Observation: {observation}")

        transcript += f"\nThought: {thought}\nAction: {signature}\nObservation: {observation}\n"

    # 🛡️ Guardrail: vượt quá số vòng lặp cho phép
    print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")
    print(f"🏁 Final Answer: {GUARDRAIL_MESSAGE}")
    return GUARDRAIL_MESSAGE


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")

    # Khởi tạo Multi-Provider LLM Adapter (Đọc từ biến môi trường LLM_PROVIDER)
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")

    # 🛡️ Chặn sớm các cấu hình đã biết là lỗi
    check_model_config(provider)

    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json")
    print(f"🛡️ Guardrail: MAX_ITERATIONS = {MAX_ITERATIONS}\n")

    # Cho phép chọn test case từ dòng lệnh: python src/app.py 8 9 10
    wanted = {int(a) for a in sys.argv[1:] if a.isdigit()}
    selected = [t for t in tests if t["id"] in wanted] if wanted else [tests[5]]

    for tc in selected:
        print("\n" + "=" * 60)
        print(f"📌 TEST CASE {tc['id']} — {tc['category']}")
        print("=" * 60)

        print("\n--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
        run_baseline_chatbot(tc["question"], provider)

        print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
        run_react_agent(tc["question"], provider)
