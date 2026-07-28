# 📘 PROJECT OVERVIEW — EDUPATH CAREER ADVISOR (Lab 3)
> **Tài liệu tổng hợp dành cho tất cả thành viên và người mới tham gia.**  
> Đọc file này để hiểu toàn bộ dự án từ mục tiêu, phân công vai trò, cấu trúc code, đến dữ liệu.

---

## 🎯 1. MỤC TIÊU DỰ ÁN

**Tên dự án**: EduPath Career Advisor — Chatbot Định Hướng Sự Nghiệp IT  
**Trường**: VinUniversity — Bài Lab 3: Chatbot vs ReAct Agent  
**Chủ đề bài toán**: Xây dựng hệ thống AI tư vấn nghề nghiệp IT lai (hybrid) dành cho sinh viên, intern và fresher người Việt Nam.

### Hệ thống phải làm được gì?

| Người dùng hỏi | Hệ thống làm gì |
|---|---|
| *"Frontend Developer là gì?"* | Trả lời ngay từ kiến thức LLM — **không dùng tool** |
| *"Fresher Fullstack cần kỹ năng gì?"* | Tra cứu dataset nội bộ → trả kết quả có nguồn gốc |
| *"Tôi biết HTML, CSS. Tôi thiếu gì để ứng tuyển Frontend?"* | Gọi tool `get_role_requirements` + `analyze_skill_gap` → phân tích có chứng cứ |
| *"Tôi muốn thành AI Engineer trong 6 tháng, học 10h/tuần"* | Chuỗi 4 tool calls → lộ trình học tập được validate |
| *"Tôi nên học gì?"* | Hỏi lại thêm thông tin — không tự bịa profile |
| *"Cam kết tôi lương 45tr sau 6 tháng đi"* | Từ chối cam kết — giải thích bất định — đưa dữ liệu tham khảo |

### Vì sao cần Agent, không chỉ Chatbot?

```
Chatbot thuần (Cấp 2): Chỉ biết kiến thức tĩnh, không tra được số liệu thực tế,
                        không so sánh hồ sơ cá nhân, không validate lộ trình.

ReAct Agent (Cấp 3): Suy luận Thought → Action → Observation theo vòng lặp,
                      gọi được tool thực, dừng khi đủ bằng chứng, có guardrail an toàn.
```

**Điểm Agentic Fit của nhóm: 19/20** — Xem chi tiết tại `docs/trace_eval.md`

---

## 👥 2. PHÂN CÔNG NHÓM VÀ TRÁCH NHIỆM TỪNG ROLE

> File chính thức: `docs/PHAN_CONG_CONG_VIEC.md`

### Role 1 — Product Architect
- **Người**: Đỗ Văn Linh — 2A202601190
- **File chính**: `config/test_cases.json`
- **Nhiệm vụ**:
  - Định hướng bài toán cho cả nhóm
  - Soạn bộ test cases đại diện cho các luồng: đơn giản, multi-step, edge case, failure
  - Kiểm tra xem Agent có vượt qua được câu bẫy (TC8, TC9, TC10) sau khi Role 3 cài guardrail
- **Đã làm**: ✅ Soạn 10 test cases tiếng Việt (id 1–10), bổ sung 7 test cases dạng chuẩn hóa (TC-01→TC-07)
- **Còn thiếu**: Bổ sung thêm test case cho 3 tool chưa được cover: `get_career_info`, `compare_careers`, `get_market_trends`

---

### Role 2 — Tool Engineer
- **Người**: Trần Chí Vũ — 2A202601044
- **File chính**: `src/tools.py`
- **Nhiệm vụ**:
  - Định nghĩa đầy đủ 7 tool với docstring chuẩn
  - Đảm bảo mỗi tool khi lỗi trả về chuỗi thông báo lỗi (không crash app)
  - Tuân thủ tool contract schema trong `docs/tool_contracts.md`
- **Đã làm**: ✅ Định nghĩa 7 tool với docstring, error handling cơ bản
- **Còn thiếu**: Kết nối tool với dữ liệu thực tế trong `data/real/` (hiện các tool trả về placeholder text)

---

### Role 3 — Prompt Engineer
- **Người**: Đỗ Thu Liễu — 2A202601898
- **File chính**: `src/prompts.py`
- **Nhiệm vụ**:
  - Soạn `CHATBOT_BASELINE_PROMPT` (không tool, không agent loop)
  - Soạn `REACT_SYSTEM_PROMPT` (ép AI sinh Thought → Action → Observation)
  - Đặt `MAX_ITERATIONS` và `TIMEOUT_SECONDS` (phanh an toàn)
- **Đã làm**: ✅ Cả hai prompt + `MAX_ITERATIONS = 3`, `TIMEOUT_SECONDS = 10`
- **Còn thiếu**: Cập nhật `REACT_SYSTEM_PROMPT` để liệt kê đủ 7 tool Career (hiện vẫn đang liệt kê `get_weather`, `search_flights` từ boilerplate)

---

### Role 4 — Core Developer / Integrator
- **Người**: Trịnh Hải Đăng — 2A202601602
- **File chính**: `src/app.py`
- **Nhiệm vụ** (đầu mối quan trọng nhất):
  - `git pull` kéo code của Role 1, 2, 3 về máy
  - Lắp ráp vòng lặp ReAct Agent hoàn chỉnh trong `app.py`
  - Đảm bảo app chạy được từ đầu đến cuối trên mọi provider (Gemini/OpenAI/offline)
- **Đã làm**: ✅ `load_test_cases()`, `run_baseline_chatbot()`, `run_react_agent()` skeleton
- **Còn thiếu**: Vòng lặp ReAct trong `run_react_agent()` vẫn là hardcode placeholder (chỉ gọi `get_weather`, không dùng LLM thực để chọn tool) — **cần Vibe Code hoàn thiện**

---

### Role 5 — Observability & Reviewer
- **Người**: Nguyễn Thanh Bình — 2A202601274 *(người quản lý repo này)*
- **File chính**: `docs/trace_eval.md`
- **Nhiệm vụ**:
  - Điền bảng Scoring Matrix (Agentic Fit)
  - Chạy test cases qua Chatbot Baseline, ghi lại phản hồi
  - Trích xuất chuỗi Thought → Action → Observation của Agent
  - Vẽ Hybrid Flowchart (phân luồng chatbot vs agent)
  - Kết luận "Agentic Fit" cuối cùng
- **Đã làm**: ✅ Scoring Matrix (19/20), chạy 10/10 test qua baseline, trace log đầy đủ
- **Còn thiếu**: Cập nhật trace log khi Role 4 hoàn thiện ReAct loop thực

---

## 🏗️ 3. KIẾN TRÚC HỆ THỐNG

> Chi tiết kỹ thuật: `docs/architecture.md`

### Luồng xử lý Hybrid

```
User Query
    │
    ▼
Safety + Normalize
    │
    ▼
Intent Router ─────────────────────────────────────────────────────┐
    │                                                               │
    ├──► General/FAQ ──► Retrieval Chatbot ──► Grounded Answer ◄───┤
    │                                                               │
    ├──► Skill Gap / Roadmap ──► ReAct Agent Loop                  │
    │         │                       │                            │
    │         ▼                       ▼                            │
    │    Tool Registry          Real Observation                    │
    │         │                       │                            │
    │         └───────────────────────┘                            │
    │                       │                                       │
    │                 Enough Evidence?                              │
    │                  ├── YES ──► Validate ──► Final Answer ───────┘
    │                  ├── NO (budget) ──► Loop again              │
    │                  └── NO (limit) ──► Safe Fallback ───────────┘
    │
    ├──► Missing info ──► Clarification Question
    │
    └──► Unsafe claim ──► Safe Fallback
```

### Các component chính

| Component | File | Trạng thái |
|---|---|---|
| LLM Provider Adapter | `src/providers.py` | ✅ Hỗ trợ Gemini, OpenAI, Mock offline |
| Tool Registry | `src/tools.py` | ✅ 7 tool, cần kết nối data thực |
| Prompts & Guardrails | `src/prompts.py` | ⚠️ Cần update tool list |
| Core App / ReAct Loop | `src/app.py` | ⚠️ Skeleton, cần hoàn thiện loop |
| Test Cases | `config/test_cases.json` | ✅ 17 test cases (10 + 7 chuẩn hóa) |
| Dataset - Career Maps | `data/real/career_maps/` | ✅ `all_roles.json` — 339KB |
| Dataset - Skills | `data/real/skills/` | ✅ 25 file JSON |
| Dataset - Question Bank | `data/real/question_bank/` | ✅ 83 file JSON |
| Dataset - Schedule Templates | `data/real/schedule_templates/` | ✅ 19 file JSON |
| Dataset - Resources | `data/real/resources/` | ✅ Tài liệu học theo ngành |
| Skill Ontology | `data/real/skill_ontology.json` | ✅ 101KB — Bản đồ kỹ năng |

---

## 📁 4. ĐÁNH GIÁ CHI TIẾT TỪNG FILE VÀ FOLDER

### 📄 Root Level

| File | Kích thước | Mô tả | Trạng thái |
|---|---|---|---|
| `README.md` | 6.5KB | Tổng quan Lab, bảng 4 cấp độ AI, scoring rubric, timeline thực hành | ✅ Hoàn chỉnh |
| `AGENTS.md` | 1.1KB | Quy tắc bắt buộc cho AI agent (non-negotiable constraints, read order) | ✅ Vừa thêm |
| `CLAUDE.md` | 1.6KB | Operating rules cho AI coding assistant khi làm việc với repo | ✅ Vừa thêm |
| `CONTEXT.md` | 14.7KB | Nguồn sự thật kỹ thuật của toàn dự án (product + engineering) | ⚠️ Cần copy từ new_folder |
| `.env.example` | 1.9KB | Template khai báo API keys (GEMINI_API_KEY, OPENAI_API_KEY, LLM_PROVIDER) | ✅ Hoàn chỉnh |
| `.gitignore` | 64B | Bỏ qua `.env`, `.venv`, `__pycache__` | ✅ Đủ |
| `requirements.txt` | 58B | Thư viện Python cần cài (`google-generativeai`, `openai`, `python-dotenv`) | ✅ Đủ |
| `ROLE4_HUONG_DAN_CHUAN.md` | 6.6KB | Hướng dẫn Vibe Code cho Role 4 — cách lắp ráp ReAct loop | ✅ Tài liệu hỗ trợ |
| `huong_dan_merge_va_chay.md` | 6.2KB | Hướng dẫn merge git và chạy app cho cả nhóm | ✅ Tài liệu hỗ trợ |
| `context_lba_3.docx` | 7.8MB | Tài liệu gốc của Lab (Word format) | ✅ Tham khảo |

---

### 📁 `config/`

#### `test_cases.json` (6.9KB — 155 dòng — **17 test cases**)

File trung tâm của Role 1. Định nghĩa bộ kiểm thử cho cả Chatbot lẫn ReAct Agent.

**Cấu trúc hai schema** (đã merge):

| Schema | ID | Dùng cho | Field chính |
|---|---|---|---|
| Schema A (Tiếng Việt) | `1`–`10` (số) | Chạy thủ công / demo | `question`, `expected_behavior` |
| Schema B (Chuẩn hóa) | `TC-01`–`TC-07` (chuỗi) | Evaluation tự động | `input`, `expected_route`, `expected_tools`, `checks` |

**Phân loại test cases:**

| Nhóm | TC | Mô tả | Expected Route |
|---|---|---|---|
| Đơn giản (LLM only) | 1, 2, 3, TC-01 | Giải thích khái niệm, so sánh role | `chatbot` |
| Retrieval | TC-02 | Hỏi dữ liệu dataset cụ thể | `chatbot_retrieval` |
| Multi-step (1-2 tool) | 4, 5, TC-03 | Skill gap cá nhân | `agent` |
| Multi-step (2+ tool) | 6, 7, TC-04 | Roadmap học tập | `agent` |
| Clarification | 8, TC-05 | Câu hỏi mơ hồ — cần hỏi lại | `clarify` |
| Adversarial / Bẫy | 9, TC-06 | Ép cam kết lương — bẫy đạo đức | `safe_fallback` |
| Failure / Not Found | 10, TC-07 | Role không tồn tại, địa điểm không có dữ liệu | `agent` + error handling |

---

### 📁 `src/`

#### `app.py` (4.1KB — 102 dòng) — **Role 4**

File điều phối chính của toàn hệ thống.

```python
load_test_cases()        # Đọc config/test_cases.json
run_baseline_chatbot()   # Gọi LLM với CHATBOT_BASELINE_PROMPT, không tool
run_react_agent()        # ⚠️ Hiện là placeholder — cần hoàn thiện vòng lặp thực
```

> ⚠️ **Vấn đề hiện tại**: Dòng 22 import `get_weather, search_flights` từ `tools` nhưng hai hàm này **không tồn tại** trong `tools.py` hiện tại. App sẽ **crash** khi chạy. **Role 4 cần sửa import này.**

#### `tools.py` (5.8KB — 151 dòng) — **Role 2**

Khai báo 7 tool chính thức cho Career Orientation Agent:

| Tool | Input | Output hiện tại | Cần làm |
|---|---|---|---|
| `search_jobs(keyword, location)` | Từ khóa, địa điểm | Placeholder string | Kết nối `data/real/career_maps/all_roles.json` |
| `get_career_info(career_name)` | Tên ngành | Placeholder string | Kết nối `data/real/career_maps/all_roles.json` |
| `get_skill_requirements(role)` | Tên vị trí | Placeholder string | Kết nối `data/real/skills/*.json` |
| `get_certifications(domain)` | Lĩnh vực | Placeholder string | Kết nối `data/real/resources/*.json` |
| `get_career_path(career_name)` | Tên ngành | Placeholder string | Kết nối `data/real/schedule_templates/` |
| `compare_careers(career1, career2)` | Hai ngành | Placeholder string | So sánh từ `data/real/career_maps/all_roles.json` |
| `get_market_trends(industry)` | Tên ngành | Placeholder string | Kết nối `data/real/index.json` |

#### `prompts.py` (1.8KB — 35 dòng) — **Role 3**

```python
CHATBOT_BASELINE_PROMPT  # ✅ Prompt đơn giản, không tool
REACT_SYSTEM_PROMPT      # ⚠️ Vẫn liệt kê get_weather/search_flights — cần update
MAX_ITERATIONS = 3       # ✅ Phanh an toàn: tối đa 3 vòng lặp
TIMEOUT_SECONDS = 10     # ✅ Timeout mỗi lần gọi tool
```

#### `providers.py` (6.9KB) — **Multi-Provider Adapter**

Hỗ trợ 3 chế độ LLM:
- `GeminiProvider` — dùng khi có `GEMINI_API_KEY`
- `OpenAIProvider` — dùng khi có `OPENAI_API_KEY`
- `MockProvider` — chạy offline, không cần API key (dùng cho demo/test)

---

### 📁 `docs/`

| File | Kích thước | Nội dung | Trạng thái |
|---|---|---|---|
| `CODELAB.md` | 23.7KB | Hướng dẫn thực hành từng bước theo format Codelab (LMS) | ✅ Hoàn chỉnh |
| `PHAN_CONG_CONG_VIEC.md` | 8KB | Phân công vai trò, checklist 4 mốc, hướng dẫn git workflow | ✅ Hoàn chỉnh |
| `DANH_SACH_DE_TAI.md` | 673B | 10 chủ đề gợi ý cho Lab | ✅ Tham khảo |
| `trace_eval.md` | 19.6KB | Scoring Matrix (19/20), log baseline 10 TC, trace Agent, kết luận | ✅ Khá đầy đủ |
| `baseline_log_raw.md` | 32.8KB | Raw log chi tiết khi chạy 10 TC qua Chatbot Baseline | ✅ Đã chạy thật |
| `architecture.md` | 2.6KB | Sơ đồ component, state TypedDict, lý do dùng hybrid | ✅ Vừa thêm |
| `product_spec.md` | 2.1KB | North-star outcome, features F-01→F-06, non-goals | ✅ Vừa thêm |
| `tool_contracts.md` | 1.5KB | Schema input/output chuẩn cho 4 tool chính, failure modes | ✅ Vừa thêm |
| `evaluation_plan.md` | 1.7KB | 12 chiều test, 9 metrics, trace format JSON chuẩn | ✅ Vừa thêm |
| `hybrid_flowchart.mermaid` | 604B | Sơ đồ Mermaid phân luồng chatbot / agent / clarify / fallback | ✅ Vừa thêm |
| `PROJECT_OVERVIEW.md` | *file này* | Tổng hợp toàn bộ dự án | ✅ Vừa tạo |

---

### 📁 `data/real/`

Toàn bộ dataset thực tế phục vụ các tool của Agent. **Đây là bộ dữ liệu quan trọng nhất** của hệ thống.

#### `career_maps/all_roles.json` — 339KB ⭐

Bản đồ nghề nghiệp IT tổng hợp. Mô tả **tất cả các role IT** với:
- Yêu cầu kỹ năng (core + supporting)
- Mức lương tham khảo
- Cấp bậc (intern → fresher → junior → senior → lead)
- Lộ trình thăng tiến

> **Tool cần dùng**: `search_jobs`, `get_career_info`, `get_career_path`, `compare_careers`

#### `skills/` — 25 file JSON

Mỗi file mô tả chi tiết một kỹ năng/công nghệ:

```
python.json (17KB)       — Python: levels, subtopics, projects, resources
java.json (13.7KB)       — Java: Spring Boot, enterprise patterns
react.json (13.2KB)      — React: hooks, state management, ecosystem
postgresql.json (9.7KB)  — PostgreSQL: queries, indexing, transactions
docker.json (8.9KB)      — Docker: containers, compose, networking
git.json (8.8KB)         — Git: workflow, branching, conflict resolution
... + 19 kỹ năng khác (aws, kubernetes, typescript, vue_js, v.v.)
```

> **Tool cần dùng**: `get_skill_requirements`, `analyze_skill_gap`

#### `question_bank/` — 83 file JSON ⭐

Ngân hàng câu hỏi phỏng vấn kỹ thuật theo từng công nghệ. Mỗi file có:
- Câu hỏi phân theo level (beginner/intermediate/advanced)
- Câu trả lời mẫu
- Tags và difficulty score

Các file lớn nhất (nội dung phong phú nhất):
```
nextjs_questions.json     (41KB)   — Next.js SSR, routing, optimization
vue_questions.json        (40KB)   — Vue 3, Composition API, Pinia
html_css_questions.json   (39KB)   — Semantic HTML, Flexbox, Grid
typescript_questions.json (38KB)   — Types, generics, decorators
angular_questions.json    (40KB)   — Modules, DI, RxJS
expressjs_questions.json  (37KB)   — Middleware, REST, security
```

> **Dùng để**: Tạo quiz kiểm tra kỹ năng người dùng tự đánh giá

#### `schedule_templates/` — 19 file JSON ⭐

Template lộ trình học tập chi tiết từng tuần cho từng role IT:

```
backend_developer_schedule.json      (294KB) — Lộ trình Backend
java_backend_developer_schedule.json (299KB) — Lộ trình Java Backend (chi tiết nhất)
full_stack_developer_schedule.json   (284KB) — Fullstack
ai_engineer_schedule.json            (277KB) — AI Engineer
frontend_developer_schedule.json     (238KB) — Frontend
devops_engineer_schedule.json        (224KB) — DevOps
data_engineer_schedule.json          (221KB) — Data Engineering
software_engineer_schedule.json      (234KB) — Software Engineer tổng quát
mobile_developer_schedule.json       (193KB) — Mobile (iOS/Android)
qa_engineer_schedule.json            (155KB) — QA/Testing
```

> **Tool cần dùng**: `build_roadmap`, `validate_roadmap`

#### `resources/` — 23 file JSON

Tài nguyên học tập (khóa học, sách, link) theo từng ngành:
`python_resources.json`, `react_resources.json`, `docker_resources.json`...

> **Tool cần dùng**: `get_certifications`, `search_learning_resources`

#### `skill_ontology.json` — 101KB ⭐

Bản đồ quan hệ giữa các kỹ năng — Skill Graph:
- Kỹ năng nào là prerequisite của kỹ năng nào
- Nhóm kỹ năng theo domain
- Trọng số tầm quan trọng theo role

> **Dùng để**: Đảm bảo prerequisite order khi validate roadmap, `validate_roadmap` tool

#### `index.json` — 32.5KB

File index tổng hợp:
- Danh sách tất cả role trong hệ thống
- Mapping role ↔ skills ↔ resources

---

## 📊 5. TIẾN ĐỘ 4 MỐC

### Mốc 1 — Định hình & Agentic Fit ✅ XONG

- [x] Chọn chủ đề: **Career Orientation**
- [x] Scoring Matrix: **19/20**
- [x] Liệt kê 7 tool (Role 2)
- [x] Xác định failure modes (Role 3)
- [x] Git sync commit Mốc 1

### Mốc 2 — Baseline Chatbot & Tool Specs ⚠️ CẦN HOÀN THIỆN

- [x] Soạn 10 test cases (Role 1)
- [x] Viết docstring 7 tool (Role 2)
- [x] Soạn `CHATBOT_BASELINE_PROMPT` (Role 3)
- [x] Chạy baseline 10/10 test case (Role 5) — xem `baseline_log_raw.md`
- [ ] **Sửa import lỗi trong `app.py`** (Role 4) ← **URGENT**

### Mốc 3 — ReAct Loop & Safeguards ❌ CHƯA XONG

- [x] `MAX_ITERATIONS = 3` đã đặt
- [ ] **Update `REACT_SYSTEM_PROMPT` với 7 career tools** (Role 3)
- [ ] **Hoàn thiện vòng lặp ReAct thực trong `app.py`** (Role 4)
- [ ] Tools kết nối data thực từ `data/real/` (Role 2)
- [ ] Trích xuất Trace Log (Role 5)

### Mốc 4 — Hybrid Flowchart & Cross-Audit ⚠️ CÒN THIẾU

- [x] `hybrid_flowchart.mermaid` đã có
- [ ] Cross-audit với nhóm khác
- [ ] Git final push

---

## ⚠️ 6. VẤN ĐỀ CẦN SỬA NGAY

### 🔴 URGENT — App crash khi chạy

**File `src/app.py` — Dòng 22:**
```python
# ❌ SAI (get_weather và search_flights không tồn tại trong tools.py):
from tools import AVAILABLE_TOOLS, get_weather, search_flights

# ✅ SỬA THÀNH:
from tools import AVAILABLE_TOOLS
```

**File `src/app.py` — Dòng 95:**
```python
# ❌ SAI nếu TC dùng schema B (TC-01..TC-07 không có field "question"):
sample_query = tests[2]["question"]

# ✅ SỬA THÀNH:
sample_query = tests[2].get("question") or tests[2].get("input", "")
```

### 🟡 MEDIUM — Cần update để demo đúng

**File `src/prompts.py`:**
```python
# REACT_SYSTEM_PROMPT hiện liệt kê sai tool (weather, flights)
# → Cần update thành 7 career tools của nhóm
```

---

## 📋 7. BẢNG CHẤM ĐIỂM

| Tiêu chí | Trọng số | Artifacts cần nộp | Trạng thái |
|---|---|---|---|
| Agentic Fit & Test Design | 20% | `docs/trace_eval.md` + `config/test_cases.json` | ✅ 19/20 |
| ReAct Implementation & Tools | 30% | `src/tools.py` + `src/app.py` | ⚠️ Chưa hoàn thiện loop |
| Guardrails & Observability | 20% | `src/prompts.py` + trace log | ⚠️ Prompt cần update |
| Inter-group Attack & Defense | 20% | Biên bản cross-audit | ❌ Chưa làm |
| Hybrid Decision Flowchart | 10% | `docs/hybrid_flowchart.mermaid` | ✅ Có file |
| **BONUS**: Autonomous Agent | +10% | Demo planning/memory | ❌ Chưa làm |

---

## 🚀 8. HƯỚNG DẪN CHẠY DỰ ÁN

```bash
# 1. Pull code mới nhất
git pull origin main

# 2. Tạo và kích hoạt virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Tạo file .env
copy .env.example .env
# Điền API key vào .env

# 5. Chạy app
cd src
python app.py
```

**Chạy offline (không cần API key)** — Sửa `.env`:
```env
LLM_PROVIDER=mock
```

---

## 🔗 9. MAP TÀI LIỆU

| Chủ đề | File |
|---|---|
| Kiến trúc tổng thể | `docs/architecture.md` |
| Đặc tả sản phẩm | `docs/product_spec.md` |
| Schema tool | `docs/tool_contracts.md` |
| Kế hoạch đánh giá | `docs/evaluation_plan.md` |
| Luồng hybrid (diagram) | `docs/hybrid_flowchart.mermaid` |
| Log trace & scoring | `docs/trace_eval.md` |
| Raw baseline log | `docs/baseline_log_raw.md` |
| Phân công thành viên | `docs/PHAN_CONG_CONG_VIEC.md` |
| Hướng dẫn merge & chạy | `huong_dan_merge_va_chay.md` |
| Quy tắc AI agent | `AGENTS.md` |

---

*Tài liệu này được tổng hợp bởi repo maintainer — cập nhật lần cuối: 2026-07-28.*  
*Nếu có thay đổi schema, tool, hoặc kiến trúc — cập nhật file này trước khi commit.*
