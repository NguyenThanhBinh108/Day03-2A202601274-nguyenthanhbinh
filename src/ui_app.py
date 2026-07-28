"""
🎨 STREAMLIT UI — EduPath Career Advisor
Deploy: streamlit run src/ui_app.py
Hoặc: Streamlit Cloud (share.streamlit.io) từ GitHub repo
"""

import sys
import os
import json

# Thêm thư mục src vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import streamlit — cần cài: pip install streamlit
try:
    import streamlit as st
except ImportError:
    print("❌ Streamlit chưa được cài. Chạy: pip install streamlit")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()

from app import run_baseline_chatbot, run_react_agent, load_test_cases, _get_query
from providers import get_llm_provider
from security import make_session_id

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EduPath — Career Advisor for IT",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .stat-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .trace-step {
        background: #f0f2f6;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        font-family: monospace;
    }
    .badge-agent { background: #667eea; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; }
    .badge-chatbot { background: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; }
    .badge-blocked { background: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = make_session_id("ui")
if "provider" not in st.session_state:
    st.session_state.provider = None
if "mode" not in st.session_state:
    st.session_state.mode = "agent"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ⚙️ Cấu hình")

    # Provider selection
    provider_choice = st.selectbox(
        "🔌 LLM Provider",
        ["gemini", "groq", "openrouter", "openai", "anthropic", "mock"],
        help="mock = offline, không cần API key"
    )

    # Mode selection
    mode = st.radio(
        "🤖 Chế độ",
        ["agent", "chatbot"],
        format_func=lambda x: "🔬 ReAct Agent (có Tool)" if x == "agent" else "💬 Chatbot Baseline (không Tool)",
        help="Agent dùng dữ liệu thực tế từ ITviec VN 2025"
    )
    st.session_state.mode = mode

    # Init provider
    if st.button("🚀 Khởi động", type="primary", use_container_width=True):
        os.environ["LLM_PROVIDER"] = provider_choice
        st.session_state.provider = get_llm_provider(provider_choice)
        st.session_state.messages = []
        st.session_state.session_id = make_session_id("ui")
        st.success(f"✅ {provider_choice.upper()} sẵn sàng!")

    st.divider()
    st.markdown("### 👤 Profile (tùy chọn)")
    background = st.selectbox(
        "Bạn đang là:",
        ["-- Chọn --", "Sinh viên CNTT năm 1-2", "Sinh viên CNTT năm 3-4",
         "Người chuyển ngành (non-IT)", "Fresher đang đi làm", "Người tự học"]
    )
    current_skills = st.multiselect(
        "Kỹ năng hiện có:",
        ["Python", "JavaScript", "React", "Node.js", "SQL", "Java",
         "Docker", "TypeScript", "Vue.js", "Go", "C#", "Kotlin", "Swift"]
    )
    hours_per_week = st.slider("📅 Có thể học (giờ/tuần):", 2, 40, 10)

    st.divider()
    st.markdown("### 🧪 Quick Test")
    try:
        test_cases = load_test_cases()
        tc_options = [
            f"[{tc.get('id', tc.get('id','?'))}] {_get_query(tc)[:50]}..."
            for tc in test_cases[:10]
        ]
        selected_tc = st.selectbox("Chạy test case:", ["-- Chọn --"] + tc_options)
    except:
        selected_tc = "-- Chọn --"

    st.divider()
    st.markdown("### 📊 Dataset")
    st.markdown("""
    <div class="stat-card">
    <strong>ITviec & TopDev VN 2025</strong><br>
    📋 77 roles | 2795 JDs<br>
    🧠 92 skills ontology<br>
    📅 v2026-06-11
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN CONTENT
# ============================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 EduPath Career Advisor</h1>
    <p>Tư vấn nghề nghiệp IT dựa trên dữ liệu thực tế từ 2795 tin tuyển dụng · ITviec & TopDev VN 2025</p>
</div>
""", unsafe_allow_html=True)

# Check provider
if st.session_state.provider is None:
    st.info("👈 Chọn Provider và bấm **Khởi động** ở sidebar để bắt đầu. Chọn **mock** nếu không có API key.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **🆓 Miễn phí hoàn toàn**
        - Gemini: AI Studio, project không bật billing
        - Groq: Đăng ký tại console.groq.com
        - Mock: Không cần API key
        """)
    with col2:
        st.markdown("""
        **⚡ Model nên dùng**
        - Gemini: `gemini-1.5-flash-latest`
        - Groq: `llama-3.3-70b-versatile`
        - ⚠️ KHÔNG dùng `gemini-2.5-flash`
        """)
    with col3:
        st.markdown("""
        **🔑 Cấu hình .env**
        ```
        LLM_PROVIDER=gemini
        GEMINI_API_KEY=xxx
        LLM_MODEL=gemini-1.5-flash-latest
        ```
        """)
    st.stop()

# Chat history display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("trace"):
            result = msg.get("result_data", {})
            status = result.get("status", "unknown")
            steps = result.get("steps", 0)

            badge = ""
            if status == "success" and steps > 0:
                badge = f'<span class="badge-agent">🔬 Agent · {steps} steps · {result.get("elapsed_seconds", 0):.1f}s</span>'
            elif status == "success":
                badge = f'<span class="badge-chatbot">💬 Chatbot · {result.get("elapsed_seconds", 0):.1f}s</span>'
            elif status == "blocked":
                badge = '<span class="badge-blocked">🛡️ Blocked</span>'

            if badge:
                st.markdown(badge, unsafe_allow_html=True)

            with st.expander(f"🔍 Agent Trace ({len(msg['trace'])} steps)"):
                for step_data in msg["trace"]:
                    st.markdown(f"""
                    <div class="trace-step">
                    <strong>Step {step_data.get('step', '?')}</strong><br>
                    💭 <em>{step_data.get('thought', '')[:200]}</em><br>
                    🛠️ Action: <code>{step_data.get('action', 'N/A')}({', '.join(str(a) for a in step_data.get('args', []))})</code><br>
                    👁️ Observation: <code>{str(step_data.get('observation', ''))[:150]}...</code>
                    </div>
                    """, unsafe_allow_html=True)

# Quick test from sidebar
if selected_tc != "-- Chọn --":
    tc_idx = tc_options.index(selected_tc)
    quick_query = _get_query(test_cases[tc_idx])
    if st.button(f"▶️ Chạy: {quick_query[:60]}..."):
        st.session_state.messages.append({"role": "user", "content": quick_query})
        st.rerun()

# Chat input
placeholder_text = "Hỏi về nghề nghiệp IT... VD: 'Tôi biết Python, SQL. Thiếu gì để làm Data Scientist?'"
if prompt := st.chat_input(placeholder_text):
    # Enrich prompt with profile if provided
    enriched_prompt = prompt
    if background and background != "-- Chọn --":
        enriched_prompt = f"[Context: {background}"
        if current_skills:
            enriched_prompt += f", kỹ năng hiện có: {', '.join(current_skills)}"
        if hours_per_week:
            enriched_prompt += f", có thể học {hours_per_week}h/tuần"
        enriched_prompt += f"]\n\n{prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("🤔 Đang phân tích..."):
            session_id = st.session_state.session_id

            if st.session_state.mode == "agent":
                result = run_react_agent(enriched_prompt, st.session_state.provider, session_id)
            else:
                result = run_baseline_chatbot(enriched_prompt, st.session_state.provider, session_id)

        answer = result.get("answer", result.get("response", "Không có phản hồi"))
        st.write(answer)

        trace = result.get("trace", [])
        if trace:
            with st.expander(f"🔍 Xem trace ({len(trace)} steps · {result.get('elapsed_seconds', 0):.1f}s)"):
                for step_data in trace:
                    st.markdown(f"""
                    <div class="trace-step">
                    <strong>Step {step_data.get('step', '?')}</strong><br>
                    💭 {step_data.get('thought', '')[:200]}<br>
                    🛠️ <code>{step_data.get('action', 'N/A')}({', '.join(str(a) for a in step_data.get('args', []))})</code><br>
                    👁️ <code>{str(step_data.get('observation', ''))[:150]}</code>
                    </div>
                    """, unsafe_allow_html=True)

        # Grounding warning
        grounding = result.get("grounding", {})
        if grounding.get("ungrounded_claims"):
            st.warning(f"⚠️ Một số số liệu chưa được xác thực từ dataset: {grounding['ungrounded_claims']}")

        # Add to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "trace": trace,
            "result_data": result
        })
