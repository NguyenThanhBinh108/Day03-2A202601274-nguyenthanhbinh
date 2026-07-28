"""
Local live UI for Day03 chatbot/agent demo.

Run:
    python live_ui_server.py

This file does not change the existing chatbot/agent code. It imports the
current src/app.py functions, runs them on demand, captures terminal output,
and displays the result in a browser.
"""

import contextlib
import io
import json
import os
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from app import load_test_cases, run_baseline_chatbot, run_react_agent  # noqa: E402
from providers import get_llm_provider  # noqa: E402

HOST = "127.0.0.1"
PORT = int(os.getenv("LIVE_UI_PORT", "8501"))


def _json_response(handler, status, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _html_response(handler):
    data = HTML.encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _run_case(case_id, mode):
    tests = load_test_cases()
    test = next((item for item in tests if int(item.get("id")) == int(case_id)), None)
    if not test:
        return {"ok": False, "error": f"Không tìm thấy test case {case_id}."}

    provider = get_llm_provider()
    provider = SafeProvider(provider)
    provider_name = provider.__class__.__name__
    model_name = getattr(provider, "model_name", "Offline Mock Mode")

    result = {
        "ok": True,
        "case": test,
        "provider": provider_name,
        "model": model_name,
        "baseline": None,
        "agent": None,
    }

    if mode in ("baseline", "both"):
        stream = io.StringIO()
        try:
            with contextlib.redirect_stdout(stream):
                answer = run_baseline_chatbot(test["question"], provider)
        except Exception as exc:
            answer = f"[Live UI Error]: Baseline gặp lỗi: {exc}"
            stream.write(answer)
        result["baseline"] = {
            "answer": answer,
            "log": stream.getvalue(),
        }

    if mode in ("agent", "both"):
        stream = io.StringIO()
        try:
            with contextlib.redirect_stdout(stream):
                answer = run_react_agent(test["question"], provider)
        except Exception as exc:
            answer = f"[Live UI Error]: ReAct Agent gặp lỗi: {exc}"
            stream.write(answer)
        result["agent"] = {
            "answer": answer,
            "log": stream.getvalue(),
        }

    return result


class SafeProvider:
    """Small UI-side wrapper: retry transient provider disconnects without editing src/."""

    def __init__(self, provider, retries=2, delay=1.0):
        self.provider = provider
        self.retries = retries
        self.delay = delay
        self.model_name = getattr(provider, "model_name", "Offline Mock Mode")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        last = ""
        for attempt in range(1, self.retries + 2):
            try:
                text = self.provider.generate(prompt, system_prompt=system_prompt)
            except Exception as exc:
                text = f"[Provider Exception]: {exc}"
            last = text or ""
            lowered = last.lower()
            transient = (
                "server disconnected without sending a response" in lowered
                or "connection aborted" in lowered
                or "temporarily unavailable" in lowered
                or "timeout" in lowered
            )
            if not transient or attempt > self.retries:
                return last
            time.sleep(self.delay * attempt)
        return last


class LiveUiHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            _html_response(self)
            return
        if self.path == "/api/tests":
            try:
                _json_response(self, 200, {"ok": True, "tests": load_test_cases()})
            except Exception as exc:
                _json_response(self, 500, {"ok": False, "error": str(exc)})
            return
        _json_response(self, 404, {"ok": False, "error": "Not found"})

    def do_POST(self):
        if self.path != "/api/run":
            _json_response(self, 404, {"ok": False, "error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(body) if body else {}
            case_id = int(payload.get("case_id", 6))
            mode = payload.get("mode", "both")
            if mode not in ("baseline", "agent", "both"):
                raise ValueError("mode phải là baseline, agent hoặc both")
            _json_response(self, 200, _run_case(case_id, mode))
        except Exception as exc:
            _json_response(self, 500, {"ok": False, "error": str(exc)})


HTML = r"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Day03 Live AI Demo</title>
  <style>
    :root {
      --ink: #172033;
      --muted: #65758b;
      --line: #d8e1ec;
      --paper: #f5f7fb;
      --panel: #ffffff;
      --navy: #122033;
      --blue: #2364aa;
      --green: #2f8f6f;
      --red: #c2414b;
      --yellow: #b7791f;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      background: var(--paper);
      color: var(--ink);
      line-height: 1.5;
    }

    header {
      background: var(--navy);
      color: #fff;
      padding: 28px;
      border-bottom: 5px solid var(--green);
    }

    header h1 {
      margin: 0;
      font-size: clamp(28px, 4vw, 48px);
      letter-spacing: 0;
    }

    header p {
      margin: 10px 0 0;
      color: #cbd7e8;
      max-width: 840px;
    }

    main {
      padding: 24px;
      max-width: 1280px;
      margin: 0 auto;
    }

    .toolbar,
    .panel,
    .answer {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(20, 35, 60, .06);
    }

    .toolbar {
      padding: 16px;
      display: grid;
      grid-template-columns: minmax(220px, 1fr) 170px auto;
      gap: 12px;
      align-items: end;
    }

    label {
      display: grid;
      gap: 6px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    select,
    button {
      min-height: 42px;
      border-radius: 8px;
      border: 1px solid var(--line);
      padding: 9px 12px;
      font: inherit;
    }

    button {
      cursor: pointer;
      color: #fff;
      background: var(--blue);
      border-color: var(--blue);
      font-weight: 800;
    }

    button.secondary {
      background: #fff;
      color: var(--ink);
      border-color: var(--line);
    }

    button:disabled {
      cursor: wait;
      opacity: .65;
    }

    .meta {
      margin-top: 14px;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }

    .metric {
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
    }

    .metric b {
      display: block;
      font-size: 13px;
      color: var(--muted);
    }

    .metric span {
      display: block;
      margin-top: 4px;
      font-weight: 800;
      overflow-wrap: anywhere;
    }

    .question {
      margin-top: 14px;
      padding: 16px;
      background: #10192a;
      color: #edf5ff;
      border-radius: 8px;
    }

    .question h2 {
      margin: 0 0 8px;
      font-size: 18px;
    }

    .question p {
      margin: 0;
      color: #dbe7f7;
    }

    .grid {
      margin-top: 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }

    .answer {
      min-width: 0;
      overflow: hidden;
    }

    .answer-head {
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .answer-head h2 {
      margin: 0;
      font-size: 18px;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      border-radius: 999px;
      padding: 4px 9px;
      background: #eef4fb;
      color: #1b5291;
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }

    .pill.green { background: #e7f6ee; color: #166245; }
    .pill.red { background: #ffe9ec; color: #9b1c2a; }

    pre {
      margin: 0;
      padding: 16px;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      color: #233047;
      max-height: 560px;
      overflow-y: auto;
      background: #fbfcfe;
    }

    .final {
      padding: 16px;
      border-top: 1px solid var(--line);
      background: #f7fbf9;
    }

    .final h3 {
      margin: 0 0 8px;
      font-size: 15px;
      color: var(--green);
    }

    .final div {
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }

    .status {
      margin-top: 12px;
      color: var(--muted);
      font-size: 14px;
    }

    .error {
      color: var(--red);
      font-weight: 800;
    }

    @media (max-width: 900px) {
      .toolbar,
      .grid,
      .meta {
        grid-template-columns: 1fr;
      }
      main { padding: 14px; }
      header { padding: 22px 16px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Day03 Live AI Demo</h1>
    <p>Bấm chạy để giao diện gọi trực tiếp code chatbot/agent hiện có. Kết quả AI và trace log sẽ hiện ngay trên web, không cần copy từ terminal.</p>
  </header>

  <main>
    <section class="toolbar">
      <label>
        Chọn test case
        <select id="caseSelect"></select>
      </label>
      <label>
        Chế độ chạy
        <select id="modeSelect">
          <option value="both">Baseline + Agent</option>
          <option value="baseline">Chỉ Baseline</option>
          <option value="agent">Chỉ ReAct Agent</option>
        </select>
      </label>
      <div>
        <button id="runBtn" type="button">Chạy AI</button>
        <button class="secondary" id="refreshBtn" type="button">Tải lại test</button>
      </div>
    </section>

    <div class="meta">
      <div class="metric"><b>Provider</b><span id="provider">Chưa chạy</span></div>
      <div class="metric"><b>Model</b><span id="model">Chưa chạy</span></div>
      <div class="metric"><b>Test case</b><span id="caseId">-</span></div>
      <div class="metric"><b>Trạng thái</b><span id="runStatus">Sẵn sàng</span></div>
    </div>

    <section class="question">
      <h2 id="caseTitle">Câu hỏi</h2>
      <p id="caseQuestion">Đang tải...</p>
    </section>

    <div class="grid">
      <article class="answer">
        <div class="answer-head">
          <h2>Chatbot Baseline</h2>
          <span class="pill" id="baselinePill">tool_calls = 0</span>
        </div>
        <pre id="baselineLog">Chưa chạy.</pre>
        <div class="final">
          <h3>Câu trả lời cuối</h3>
          <div id="baselineFinal">Chưa có.</div>
        </div>
      </article>

      <article class="answer">
        <div class="answer-head">
          <h2>ReAct Agent</h2>
          <span class="pill green" id="agentPill">Thought → Action → Observation</span>
        </div>
        <pre id="agentLog">Chưa chạy.</pre>
        <div class="final">
          <h3>Câu trả lời cuối</h3>
          <div id="agentFinal">Chưa có.</div>
        </div>
      </article>
    </div>

    <div class="status" id="helpText">Server local đang chạy. Dừng bằng Ctrl+C trong terminal.</div>
  </main>

  <script>
    const caseSelect = document.getElementById("caseSelect");
    const modeSelect = document.getElementById("modeSelect");
    const runBtn = document.getElementById("runBtn");
    const refreshBtn = document.getElementById("refreshBtn");
    const provider = document.getElementById("provider");
    const model = document.getElementById("model");
    const caseId = document.getElementById("caseId");
    const runStatus = document.getElementById("runStatus");
    const caseTitle = document.getElementById("caseTitle");
    const caseQuestion = document.getElementById("caseQuestion");
    const baselineLog = document.getElementById("baselineLog");
    const baselineFinal = document.getElementById("baselineFinal");
    const agentLog = document.getElementById("agentLog");
    const agentFinal = document.getElementById("agentFinal");

    let tests = [];

    function selectedCase() {
      return tests.find(item => Number(item.id) === Number(caseSelect.value));
    }

    function renderSelectedCase() {
      const item = selectedCase();
      if (!item) return;
      caseId.textContent = `TC${item.id}`;
      caseTitle.textContent = `TC${item.id} - ${item.category}`;
      caseQuestion.textContent = item.question;
    }

    async function loadTests() {
      runStatus.textContent = "Đang tải test...";
      const res = await fetch("/api/tests");
      const data = await res.json();
      if (!data.ok) throw new Error(data.error);
      tests = data.tests;
      caseSelect.innerHTML = tests.map(item => {
        const selected = item.id === 6 ? "selected" : "";
        return `<option value="${item.id}" ${selected}>TC${item.id} - ${item.category}</option>`;
      }).join("");
      renderSelectedCase();
      runStatus.textContent = "Sẵn sàng";
    }

    async function runAi() {
      const item = selectedCase();
      if (!item) return;
      runBtn.disabled = true;
      refreshBtn.disabled = true;
      runStatus.textContent = "Đang gọi AI...";
      baselineLog.textContent = "Đang chạy...";
      agentLog.textContent = "Đang chạy...";
      baselineFinal.textContent = "Đang chờ...";
      agentFinal.textContent = "Đang chờ...";

      try {
        const res = await fetch("/api/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            case_id: Number(caseSelect.value),
            mode: modeSelect.value
          })
        });
        const data = await res.json();
        if (!data.ok) throw new Error(data.error);

        provider.textContent = data.provider;
        model.textContent = data.model;
        caseId.textContent = `TC${data.case.id}`;
        caseTitle.textContent = `TC${data.case.id} - ${data.case.category}`;
        caseQuestion.textContent = data.case.question;

        if (data.baseline) {
          baselineLog.textContent = data.baseline.log || "(Không có log)";
          baselineFinal.textContent = data.baseline.answer || "(Không có câu trả lời cuối)";
        } else {
          baselineLog.textContent = "Không chạy ở chế độ này.";
          baselineFinal.textContent = "Không chạy.";
        }

        if (data.agent) {
          agentLog.textContent = data.agent.log || "(Không có log)";
          agentFinal.textContent = data.agent.answer || "(Không có câu trả lời cuối)";
        } else {
          agentLog.textContent = "Không chạy ở chế độ này.";
          agentFinal.textContent = "Không chạy.";
        }

        runStatus.textContent = "Hoàn thành";
      } catch (err) {
        runStatus.innerHTML = `<span class="error">Lỗi</span>`;
        baselineLog.textContent = String(err.message || err);
        agentLog.textContent = String(err.message || err);
      } finally {
        runBtn.disabled = false;
        refreshBtn.disabled = false;
      }
    }

    caseSelect.addEventListener("change", renderSelectedCase);
    runBtn.addEventListener("click", runAi);
    refreshBtn.addEventListener("click", loadTests);
    loadTests().catch(err => {
      runStatus.innerHTML = `<span class="error">Không tải được test</span>`;
      caseQuestion.textContent = err.message;
    });
  </script>
</body>
</html>
"""


def main():
    url = f"http://{HOST}:{PORT}"
    server = ThreadingHTTPServer((HOST, PORT), LiveUiHandler)
    print(f"Live UI đang chạy tại: {url}")
    print("Nhấn Ctrl+C để dừng server.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng Live UI.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
