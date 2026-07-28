"""
🌐 SERVER DEMO — nối giao diện presentation_ui.html với ReAct Agent thật.

Không dùng thư viện ngoài (chỉ http.server của Python), nên không cần cài thêm gì.
Giao diện bấm "Chạy" -> server gọi ĐÚNG hàm trong src/app.py -> trả trace thật về.

Cách chạy:
    python serve_ui.py
Rồi mở trình duyệt: http://localhost:8000
"""

import io
import json
import os
import sys
import threading
import webbrowser
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv  # noqa: E402
load_dotenv(os.path.join(ROOT, ".env"))

import app as agent_app  # noqa: E402  (dùng lại nguyên xi code của Role 4)
from providers import get_llm_provider  # noqa: E402

PORT = 8000
UI_FILE = os.path.join(ROOT, "presentation_ui.html")

# Khởi tạo provider một lần, dùng lại cho mọi request
_provider = get_llm_provider()
_lock = threading.Lock()  # LLM free tier có rate limit -> chạy tuần tự
LOCK_TIMEOUT = 180        # giây chờ tối đa khi có lượt chạy khác đang giữ lock


def run_case(case_id: int, mode: str) -> dict:
    """
    Chạy 1 test case qua Chatbot Baseline hoặc ReAct Agent.

    Bắt toàn bộ output in ra màn hình bằng redirect_stdout, nhờ vậy dùng lại
    CHÍNH XÁC hàm run_baseline_chatbot / run_react_agent trong src/app.py —
    kết quả trên web y hệt khi chạy `python src/app.py <id>` ở terminal.
    """
    tests = agent_app.load_test_cases()
    tc = next((t for t in tests if t["id"] == case_id), None)
    if tc is None:
        return {"ok": False, "error": f"Không có test case id={case_id}"}

    # Gói free có rate limit -> chỉ cho 1 lượt gọi LLM chạy tại một thời điểm.
    # Dùng timeout để không bao giờ chờ vô hạn nếu có request đang treo.
    if not _lock.acquire(timeout=LOCK_TIMEOUT):
        return {"ok": False,
                "error": "Đang có một lượt chạy khác chưa xong. Chờ chút rồi thử lại."}

    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            if mode == "baseline":
                agent_app.run_baseline_chatbot(tc["question"], _provider)
            else:
                agent_app.run_react_agent(tc["question"], _provider)
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "output": buf.getvalue()}
    finally:
        _lock.release()

    return {
        "ok": True,
        "id": tc["id"],
        "category": tc["category"],
        "question": tc["question"],
        "expected": tc["expected_behavior"],
        "mode": mode,
        "model": getattr(_provider, "model_name", "?"),
        "output": buf.getvalue().strip(),
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # tắt log mặc định cho đỡ rối terminal

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html", "/presentation_ui.html"):
            with open(UI_FILE, "r", encoding="utf-8") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")

        if self.path == "/api/config":
            return self._send(200, json.dumps({
                "provider": _provider.__class__.__name__,
                "model": getattr(_provider, "model_name", "?"),
                "max_iterations": agent_app.MAX_ITERATIONS,
                "tools": list(agent_app.AVAILABLE_TOOLS),
                "cases": [{"id": t["id"], "category": t["category"],
                           "question": t["question"]}
                          for t in agent_app.load_test_cases()],
            }, ensure_ascii=False))

        self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/run":
            return self._send(404, json.dumps({"error": "not found"}))
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n) or b"{}")
            result = run_case(int(payload.get("id", 6)),
                              payload.get("mode", "agent"))
            self._send(200, json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self._send(500, json.dumps({"ok": False, "error": str(e)},
                                       ensure_ascii=False))


if __name__ == "__main__":
    model = getattr(_provider, "model_name", "?")
    print("=" * 62)
    print("🌐 DASHBOARD CAREER REACT AGENT")
    print("=" * 62)
    print(f"🔌 Provider : {_provider.__class__.__name__} (Model: {model})")
    print(f"🛡️ Guardrail: MAX_ITERATIONS = {agent_app.MAX_ITERATIONS}")
    print(f"🛠️ Tools    : {len(agent_app.AVAILABLE_TOOLS)} công cụ")
    agent_app.check_model_config(_provider)
    print()
    print(f"➜ Mở trình duyệt tại: http://localhost:{PORT}")
    print("➜ Nhấn Ctrl+C để dừng server")
    print("=" * 62)

    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass

    try:
        # ThreadingHTTPServer: mỗi request một luồng riêng, nên một lượt gọi LLM
        # chậm KHÔNG làm treo cả server (HTTPServer thường sẽ bị treo).
        ThreadingHTTPServer(("localhost", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Đã dừng server.")
