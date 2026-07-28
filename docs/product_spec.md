# 📦 Product Specification — EduPath Career Advisor
**Version 2.0 | Lab 3 — VinUniversity × GDGoC**

---

## 1. North-Star Outcome

Một sinh viên CNTT năm 3 hoặc người đang chuyển ngành có thể gõ câu hỏi bằng tiếng Việt tự nhiên và nhận được **tư vấn nghề nghiệp IT có căn cứ từ dữ liệu tuyển dụng thực tế** (không phải ý kiến cá nhân), bao gồm:
- Skill gap được định lượng theo % xuất hiện trong JDs thực
- Lộ trình học tập khả thi dựa trên constraints của người dùng (giờ/tuần)
- Nguồn tham khảo rõ ràng (tên dataset, version, số JDs phân tích)

---

## 2. User Personas & Pain Points

### Persona A: Sinh viên CNTT năm 1-2 🎓
**Tuổi**: 18-20 | **Đặc điểm**: Chưa biết lập trình nhiều, mới tiếp xúc với ngành

| Pain Point | Ví dụ cụ thể | Hệ thống giải quyết thế nào |
|---|---|---|
| Không biết học gì trước | "Python hay JavaScript trước?" | `get_skill_requirements` → % JDs từ data thực |
| Sợ chọn sai hướng | "Game dev hay Web dev tốt hơn?" | `compare_careers` + `get_market_trends` → số JDs thực |
| Không biết roadmap thực tế | "Syllabus trường vs thị trường khác nhau thế nào?" | `get_career_path` + `get_certifications` |

**Kịch bản điển hình**:
```
User: "Em học CNTT năm 1, thích game nhưng không biết có nên theo không"
Agent: [get_market_trends("Mobile/Game")] → "Game Dev VN: ~50 JDs/năm vs Backend: 552 JDs/năm"
→ Trả lời có data: "Game Dev VN có ít cơ hội hơn Web Dev 10x, nhưng nếu đam mê..."
```

---

### Persona B: Sinh viên CNTT năm 3-4 🎓🎓
**Tuổi**: 21-23 | **Đặc điểm**: Biết code cơ bản, đang tìm intern/fresher

| Pain Point | Ví dụ cụ thể |
|---|---|
| "Mình đủ điều kiện ứng tuyển chưa?" | So skill gap vs yêu cầu JD thực |
| "Nên làm project gì thêm?" | Skills thiếu phổ biến nhất trong JDs |
| "React hay Vue, cái nào dễ xin việc?" | JD count React vs Vue từ data |

**Kịch bản điển hình**:
```
User: "Em biết HTML/CSS/JS, React cơ bản. Ứng Frontend Intern được chưa?"
Agent: [get_skill_requirements("Frontend Developer")] 
→ must_have: HTML/CSS 92% ✅, JS 89% ✅, React 74% ✅ (cơ bản)
→ should_have: TypeScript 61% ❌, Testing 45% ❌
→ "Đủ để ứng intern! Điểm yếu cần học trước: TypeScript (61% JDs)"
```

---

### Persona C: Người chuyển ngành từ non-IT 🔄
**Tuổi**: 25-35 | **Đặc điểm**: Đang làm kế toán/marketing/giáo viên, muốn vào IT

| Pain Point | Cách xử lý |
|---|---|
| "Có quá muộn không?" | Không cam kết, đưa data về distribution age in JDs nếu có |
| "Cần bao lâu để có việc?" | `get_career_path` → timeline thực tế theo timeline học |
| "Bằng cấp không có CNTT có xin được không?" | % JDs yêu cầu bằng CNTT từ data |

---

### Persona D: Fresher đang đi làm, muốn lên level 📈
**Tuổi**: 22-26 | **Đặc điểm**: 6-18 tháng kinh nghiệm, muốn switch company/role

| Pain Point | Tool giải quyết |
|---|---|
| "Mình đang ở level nào so với thị trường?" | `get_skill_requirements` + skill gap analysis |
| "Cần học thêm skill nào để tăng lương?" | Skills có `salary_impact: high` trong skill_ontology |
| "Switch từ outsource sang product cần gì?" | `search_jobs` + `get_market_trends` |

---

### Persona E: Người tự học (Autodidact) 📚
**Tuổi**: Mọi độ tuổi | **Đặc điểm**: Không học chính quy, học qua YouTube/freeCodeCamp

| Pain Point | Tool giải quyết |
|---|---|
| "Không có bằng CNTT có xin được không?" | `get_career_info` — % JDs có/không yêu cầu bằng |
| "Portfolio của mình đủ chưa?" | `get_skill_requirements` so sánh với portfolio |
| "Nên có certifications nào?" | `get_certifications` — list kèm is_free, duration_hours |

---

## 3. Features (F-01 → F-08)

### F-01: Multi-turn Career Counseling (Chatbot Path)
**Mô tả**: Trả lời câu hỏi khái niệm và tư vấn tổng quát không cần data thực  
**Acceptance Criteria**:
- [x] Trả lời trong <3s
- [x] Không bịa số liệu/tên công ty
- [x] Hỏi lại khi thiếu thông tin (không tự bịa profile)
- [x] Từ chối ngoài domain IT bằng cách redirect lịch sự

### F-02: Skill Gap Analysis (Agent Path)
**Mô tả**: So sánh skills người dùng tự khai vs yêu cầu từ JDs thực  
**Acceptance Criteria**:
- [x] Phân loại: possessed / missing / supporting
- [x] Mỗi skill missing có % frequency từ JDs thực
- [x] Cite dataset_version và source
- [ ] *Bonus*: Link tới learning resource cho skills thiếu

### F-03: Role Requirements Lookup
**Mô tả**: Liệt kê kỹ năng must_have / should_have / nice_to_have cho bất kỳ role nào  
**Acceptance Criteria**:
- [x] Cover 77 roles từ dataset
- [x] Fuzzy matching (user gõ "backend dev" → "Backend Developer")
- [x] Gợi ý role tương tự khi không tìm thấy (không crash)
- [x] Trả kết quả trong <2s (local data, no network)

### F-04: Career Comparison
**Mô tả**: So sánh hai ngành về JD count, skills, market demand  
**Acceptance Criteria**:
- [x] Cả hai role phải có trong dataset
- [x] Output có shared_skills và unique differences
- [x] Không đề xuất một ngành "tốt hơn" không có căn cứ

### F-05: Learning Roadmap Generation
**Mô tả**: Tạo lộ trình học theo constraints người dùng (giờ/tuần)  
**Acceptance Criteria**:
- [x] 5 career levels (Intern → Lead) với timeline
- [x] Key skills per level từ data
- [x] Không cam kết timeline cụ thể — luôn note "tùy năng lực cá nhân"

### F-06: Market Trend Lookup
**Mô tả**: Xu hướng thị trường IT VN theo ngành/lĩnh vực  
**Acceptance Criteria**:
- [x] Top roles by JD count từ data thực (ITviec VN 2025)
- [x] Cross-skills phổ biến nhất trong lĩnh vực
- [x] Market share % của lĩnh vực trong tổng dataset

### F-07: Security & Guardrails ⭐ NEW
**Mô tả**: Bảo vệ hệ thống khỏi abuse và bảo vệ user khỏi thông tin sai  
**Acceptance Criteria**:
- [x] Prompt injection blocked TRƯỚC khi gọi LLM (rate: >95% detection)
- [x] PII (email, phone, CCCD) không được log — masked trước khi process
- [x] Rate limit: 15 req/min per session
- [x] Salary guarantee request → explain uncertainty, không cam kết
- [x] MAX_ITERATIONS=5 → safe fallback, không infinite loop
- [x] Grounding check: warn khi LLM claim số liệu không có trong observations

### F-08: Observability & Trace Logging ⭐ NEW
**Mô tả**: Ghi lại toàn bộ trace cho mục đích đánh giá và debugging  
**Acceptance Criteria**:
- [x] Mỗi session có JSON trace file: `logs/trace_{session_id}.json`
- [x] Trace gồm: thought, action, args, observation, elapsed_time per step
- [x] Grounding check result trong trace
- [x] Không log PII — session_id là hash anonymous

---

## 4. Non-Goals (Explicit Out of Scope)

| Non-Goal | Lý do |
|---|---|
| Lưu trữ profile người dùng giữa các session | Privacy — không có persistent storage trong Lab |
| Real-time job scraping từ ITviec/TopDev | Data đã được pre-processed vào `data/real/` — không cần live crawl |
| Cam kết lương hoặc xác suất xin được việc | Ethically và legally không thể |
| Tư vấn cho ngành ngoài IT | Out of domain — politely declined |
| Tạo CV hoặc cover letter | Scope quá rộng cho Lab 3 |
| Multi-language support (English) | Vietnamese only — dataset có VN context |

---

## 5. Non-Functional Requirements

| Requirement | Target | Đo bằng cách nào |
|---|---|---|
| Response latency (chatbot) | < 3s | Đo elapsed_seconds trong trace |
| Response latency (agent, 2 tool calls) | < 15s | Đo elapsed_seconds trong trace |
| Tool execution latency | < 0.5s (local JSON reads) | Đo per-step trong trace |
| Injection detection accuracy | > 95% True Positive | Manual test với 20 injection TCs |
| Grounding rate (no hallucinated #s) | > 90% | check_response_grounding() |
| Uptime (Streamlit Cloud deploy) | > 95% trong giờ demo | Manual monitoring |
| Memory footprint | < 500MB RAM | Không load tất cả data vào RAM cùng lúc (lazy load) |

---

## 6. API Provider Recommendations

| Provider | Model | Free Tier | Best Use |
|---|---|---|---|
| 🥇 **Google Gemini** | `gemini-1.5-flash-latest` | 15 RPM, 1.5M TPD | Primary (tạo key ở project KHÔNG bật billing) |
| 🥈 **Groq** | `llama-3.3-70b` | 30 RPM, 500K TPD | Fastest backup, good quality |
| 🔧 **Ollama (Local)** | `qwen2.5:7b` | Unlimited | Demo offline, no internet needed |
| 🔄 **OpenRouter** | Nhiều model | $1 free credit | Access to many models via single API |

**⚠️ Known pitfalls** (từ kinh nghiệm thực tế của nhóm):
- `gemini-2.5-flash` → `404`: Không available cho tài khoản mới. Dùng `gemini-1.5-flash-latest`
- Project có bật billing mà hết tiền → `429`. Tạo project mới, KHÔNG bật billing
- Groq: context window nhỏ hơn — tránh system prompt quá dài (>2000 tokens)
