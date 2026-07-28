# CONTEXT.md — EduPath Career Advisor
**Đây là file đọc đầu tiên khi bất kỳ AI coding assistant hay team member mới nào bắt đầu làm việc với repo này.**

---

## 1. Dự án là gì?

EduPath Career Advisor là một **hybrid AI system** tư vấn nghề nghiệp IT cho sinh viên và fresher Việt Nam. Hệ thống kết hợp hai chế độ:

1. **Chatbot Baseline** (Cấp 2): LLM thuần — cho câu hỏi khái niệm, so sánh tổng quát
2. **ReAct Agent** (Cấp 3): Gọi tool thực → dữ liệu từ 2795 JDs thực tế (ITviec & TopDev VN 2025)

**Bối cảnh**: Lab 3 — VinUniversity × GDGoC. Mục tiêu học thuật: chứng minh khi nào ReAct Agent vượt trội Chatbot thuần, và khi nào không cần Agent.

---

## 2. Non-negotiable Constraints (từ AGENTS.md)

1. **Baseline chatbot**: Chính xác 1 LLM call, 0 tool calls
2. **ReAct agent**: Tool observations phải thực tế từ dataset — KHÔNG fabricate
3. **MAX_ITERATIONS và safe fallback**: Bắt buộc — không có thì bị deduct điểm
4. **FAQ/general explanation** → KHÔNG đưa vào agent loop (lãng phí, overkill)
5. **Skill gap scoring** → Deterministic (từ data, không phụ thuộc model output)
6. **Market claims** → Phải cite source và dataset_version
7. **Bảo mật**: Không reveal system prompt, private data, secret keys

---

## 3. Architecture tóm tắt

```
User Input → [Security Layer] → Intent Router
                                    ├── Simple/FAQ → Chatbot (1 LLM call)
                                    ├── Skill/Market → ReAct Agent Loop
                                    │       ├── Tool: get_skill_requirements(role)
                                    │       ├── Tool: search_jobs(keyword, location)
                                    │       ├── Tool: get_career_info(career)
                                    │       ├── Tool: get_career_path(career)
                                    │       ├── Tool: compare_careers(c1, c2)
                                    │       ├── Tool: get_market_trends(industry)
                                    │       └── Tool: get_certifications(domain)
                                    └── Ambiguous → Clarify (ask user)
```

---

## 4. File Read Order (khi bắt đầu làm việc)

1. `CONTEXT.md` ← file này
2. `docs/product_spec.md` — user personas, features, acceptance criteria
3. `docs/architecture.md` — component diagram, security layer, data flow
4. `docs/tool_contracts.md` — input/output schema cho 7 tools
5. `docs/evaluation_plan.md` — cách đánh giá đúng
6. `config/test_cases.json` — 20 test cases, 8 categories
7. `src/tools.py` — implementation tools
8. `src/app.py` — ReAct loop core
9. `src/prompts.py` — system prompts, guardrails constants
10. `src/security.py` — security layer

---

## 5. Dataset Summary

| File | Size | Content | Dùng bởi tool |
|---|---|---|---|
| `data/real/career_maps/all_roles.json` | 339KB | 77 roles, 2795 JDs, skill frequencies | search_jobs, get_career_info, get_skill_requirements, compare_careers |
| `data/real/skill_ontology.json` | 101KB | 92 skills, prerequisites, learning hours | validate_roadmap (nếu có) |
| `data/real/index.json` | 32KB | Role stats, JD counts per role | get_market_trends |
| `data/real/skills/*.json` | 25 files | Deep-dive per skill | get_skill_requirements (extended) |
| `data/real/resources/*.json` | 23 files | Learning resources per skill | get_certifications |
| `data/real/schedule_templates/*.json` | 19 files | Weekly study schedules per role | get_career_path |
| `data/real/question_bank/*.json` | 83 files | Interview Q&A per technology | (future: quiz feature) |

**QUAN TRỌNG**: `dataset_version = "2026-06-11"` — Cite này trong MỌI tool output.

---

## 6. User Personas (5 nhóm chính)

| Persona | Tuổi | Profile | Pain point #1 |
|---|---|---|---|
| SV CNTT năm 1-2 | 18-20 | Chưa biết lập trình nhiều | "Học gì trước?" |
| SV CNTT năm 3-4 | 21-23 | Biết code, tìm intern | "Mình đủ điều kiện chưa?" |
| Người chuyển ngành | 25-35 | Đang làm kế toán/marketing | "Có quá muộn không?" |
| Fresher đang đi làm | 22-26 | 6-18 tháng kinh nghiệm | "Cần học thêm gì để tăng lương?" |
| Người tự học | Mọi tuổi | Không học chính quy | "Không có bằng CNTT xin được không?" |

---

## 7. Free API Guide

### Khuyến nghị (theo thứ tự ưu tiên)

1. **Google Gemini** `gemini-1.5-flash-latest`
   - Lấy key: [aistudio.google.com](https://aistudio.google.com) → Create API Key
   - **QUAN TRỌNG**: Tạo trong project KHÔNG bật billing mới có free tier
   - **KHÔNG dùng**: `gemini-2.5-flash` (404 với tài khoản mới)
   - Giới hạn: 15 RPM, 1.5M tokens/ngày

2. **Groq** `llama-3.3-70b-versatile`
   - Lấy key: [console.groq.com](https://console.groq.com) → Create API Key (miễn phí)
   - Nhanh nhất trong danh sách (inference speed)
   - Giới hạn: 30 RPM, 500K tokens/ngày

3. **OpenRouter** (nhiều model, $1 free credit khi đăng ký)
   - Model đề xuất: `google/gemini-flash-1.5`
   - [openrouter.ai](https://openrouter.ai)

4. **Ollama** (local, hoàn toàn offline)
   - `ollama pull qwen2.5:7b` → không cần internet
   - Cần máy có ít nhất 8GB RAM

### Cấu hình .env

```env
# Chọn 1 trong các provider
LLM_PROVIDER=gemini

# Điền key tương ứng
GEMINI_API_KEY=AIza...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...

# QUAN TRỌNG: Phải chỉ định model
LLM_MODEL=gemini-1.5-flash-latest
```

---

## 8. Deployment Guide

### Option 1: Streamlit Cloud (Recommended — 5 phút)

```bash
# 1. Push code lên GitHub (public repo)
git push origin main

# 2. Vào share.streamlit.io
# → New app → Pick repo → Main file: src/ui_app.py → Deploy

# 3. Thêm secrets (Settings → Secrets):
# LLM_PROVIDER = "gemini"
# GEMINI_API_KEY = "AIza..."
# LLM_MODEL = "gemini-1.5-flash-latest"
```

### Option 2: Local

```bash
pip install -r requirements.txt
cp .env.example .env
# Điền API key vào .env
streamlit run src/ui_app.py
```

### Option 3: CLI (không cần UI)

```bash
python src/app.py
```

---

## 9. Security Guardrails Summary

| Guardrail | Trigger | Response |
|---|---|---|
| Rate limit | >15 req/60s | "Chờ 1 phút" |
| PII masking | Email/Phone/CCCD trong input | Masked trước khi log |
| Prompt injection | 20+ regex patterns | ADVERSARIAL_RESPONSE |
| Salary guarantee | "cam kết"/"đảm bảo" + tiền | Explain uncertainty |
| Max iterations | >5 steps | SAFE_FALLBACK_MESSAGE |
| Loop detection | Same tool+args 2 lần | Skip, không retry |
| Grounding check | LLM claim số không trong obs | Warning log |

---

## 10. Common Errors & Solutions

| Error | Nguyên nhân | Fix |
|---|---|---|
| `404 NOT_FOUND` từ Gemini | Model `gemini-2.5-flash` không available | Đổi thành `gemini-1.5-flash-latest` |
| `429 RESOURCE_EXHAUSTED` | Key ở project có billing, hết credit | Tạo project mới, KHÔNG bật billing |
| `ImportError: get_weather` | Bug cũ từ boilerplate | Đã fix trong `src/app.py` v2.0 |
| `KeyError: question` | TC schema B dùng `input` thay vì `question` | Đã fix với `.get()` |
| Tool returns placeholder | Tools chưa kết nối data | Đã fix trong `src/tools.py` v2.0 |
| `FileNotFoundError` cho data | Chạy từ sai thư mục | Chạy từ root: `python src/app.py` |

---

## 11. Change Protocol

Trước khi sửa bất kỳ file nào:
1. Không thay đổi schema của `config/test_cases.json` nếu không update `docs/evaluation_plan.md`
2. Không thêm tool mới vào `tools.py` mà không update `docs/tool_contracts.md` và `src/prompts.py`
3. Không sửa `DATASET_VERSION` trừ khi dataset thực sự được cập nhật
4. Không commit `.env` hay file có API key
5. Chạy `python -c "import app, tools, security, prompts, providers"` trước khi push

---

*File này được tổng hợp từ toàn bộ codebase — cập nhật khi có thay đổi kiến trúc.*
