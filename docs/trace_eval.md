# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)
*Dành cho Role 5: Observability & Reviewer — Nguyễn Thanh Bình - 2A202601274*

**Đề tài nhóm chọn**: 🎓 **Chatbot Định Hướng Sự Nghiệp** (Career Guidance Agent)
**Bộ test case tham chiếu**: `config/test_cases.json` (10 câu, do Role 1 – Đỗ Văn Linh biên soạn)
**Bộ công cụ tham chiếu**: `src/tools.py` – **7 tool** do Role 2 – Trần Chí Vũ khai báo (branch `Vũ`, commit `8a9e0af` + `3556371`)

### 🧰 Danh sách 7 Tool chính thức của nhóm (Role 5 dùng đúng tên này để soi trace)

| # | Tên tool | Chức năng |
| :---: | :--- | :--- |
| 1 | `search_jobs(keyword, location)` | Tra cứu việc làm theo ngành nghề / kỹ năng / địa điểm |
| 2 | `get_career_info(career_name)` | Mô tả ngành, lương TB, nhu cầu tuyển dụng, yêu cầu học vấn |
| 3 | `get_skill_requirements(role)` | Liệt kê hard skills & soft skills cần cho vị trí |
| 4 | `get_certifications(domain)` | Đề xuất chứng chỉ, khóa học online theo lĩnh vực |
| 5 | `get_career_path(career_name)` | Lộ trình thăng tiến Fresher → Junior → Senior → Lead |
| 6 | `compare_careers(career1, career2)` | So sánh lương, yêu cầu, triển vọng giữa các ngành |
| 7 | `get_market_trends(industry)` | Xu hướng thị trường: ngành hot, cạnh tranh, top công ty |

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX) — MỐC 1

*Mục tiêu: Chứng minh bài toán này CẦN ReAct Agent, không chỉ Chatbot thuần.*

| Tiêu chí | Điểm (1-5) | Lý do đánh giá (dẫn chứng từ test case) |
| :--- | :---: | :--- |
| 🧠 **Multi-step Reasoning** | `5/5` | TC6 đòi hỏi chuỗi 3 bước phụ thuộc nhau: `search_jobs` ➔ `get_skill_requirements` ➔ `get_certifications` để dựng roadmap 6 tháng. Bước sau **không thể chạy** nếu chưa có Observation của bước trước. |
| 🛠️ **Tool Interaction** | `5/5` | 7/7 tool của Role 2 đều truy vấn dữ liệu **ngoài tri thức LLM** (tin tuyển dụng, lương, xu hướng thị trường — thay đổi liên tục). TC4, TC5, TC6, TC7 không thể trả lời đúng nếu thiếu `search_jobs`. |
| 🔀 **Dynamic Decision** | `5/5` | Luồng rẽ nhánh theo Observation: TC8 (*"Data hay AI?"*) thiếu thông tin ➔ Agent phải **hỏi lại**, chưa được gọi `compare_careers` ngay; TC10 `search_jobs("AI Engineer", "thành phố Z")` trả rỗng ➔ Agent phải **đổi hướng, báo không có dữ liệu**, không được bịa. |
| ⏳ **Long Horizon** | `4/5` | Chuỗi dài 3–4 lượt gọi tool (tra cứu ➔ trích kỹ năng ➔ so khớp hồ sơ ➔ sinh lộ trình). Dài hơn hẳn chatbot 1 lượt, nhưng chưa tới mức tác vụ nhiều ngày nên không đạt 5/5. |
| **TỔNG ĐIỂM FIT** | **19/20** | **KẾT LUẬN: BÀI TOÁN RẤT NÊN DÙNG REACT AGENT!** |

### 📌 Ma trận Test Case × Tool (cơ sở cho Hybrid Flowchart ở Mốc 4)

| Test Case | Loại | Luồng dự kiến | Tool dự kiến Agent gọi (theo `src/tools.py` của Role 2) |
| :---: | :--- | :--- | :--- |
| TC1 | Đơn giản | ➡️ **Chatbot path** | ❌ Không tool |
| TC2 | Đơn giản | ➡️ **Chatbot path** | ❌ Không tool *(kiến thức nền đủ trả lời Backend vs Frontend)* |
| TC3 | Đơn giản | ➡️ **Chatbot path** | ❌ Không tool |
| TC4 | Multi-step | ➡️ **Agent path** | `search_jobs` ➔ `get_skill_requirements` |
| TC5 | Multi-step | ➡️ **Agent path** | `search_jobs` ➔ `get_skill_requirements` *(so khớp skill gap)* |
| TC6 | Multi-step (2+ tools) | ➡️ **Agent path** | `search_jobs` ➔ `get_skill_requirements` ➔ `get_certifications` |
| TC7 | Multi-step (2+ tools) | ➡️ **Agent path** | `search_jobs` ➔ `get_skill_requirements` ➔ `get_career_path` |
| TC8 | Edge – thiếu thông tin | ➡️ **Clarify path** | ❌ Hỏi lại trước; chỉ gọi `compare_careers` sau khi đủ thông tin |
| TC9 | Edge – bẫy cam kết | ➡️ **Guardrail path** | Có thể dùng `get_market_trends` / `get_career_info` để đưa **số liệu tham khảo**, tuyệt đối không cam kết |
| TC10 | Edge – tool failure | ➡️ **Agent path + xử lý lỗi** | `search_jobs("AI Engineer", "thành phố Z")` ➔ trả rỗng |

> 🔎 **Quan sát của Role 5**: 3 tool `get_career_info`, `compare_careers`, `get_market_trends` hiện **chưa có test case nào bắt buộc gọi tới**. Đề xuất Role 1 bổ sung 1–2 câu test (VD: *"So sánh Data Analyst và Data Engineer về lương và triển vọng"*) để phủ hết 7 tool, tránh bị nhóm khác bắt lỗi "tool thừa" ở Mốc 4.

---

## 🔍 2. SO SÁNH PHẢN HỒI CHATBOT BASELINE — MỐC 2

> ⏳ **TRẠNG THÁI: CHỜ ROLE 4 ráp `run_baseline_chatbot()` trong `src/app.py`.**
> Sau khi chạy được, điền phản hồi thật của 3 câu đại diện vào bên dưới.

### 🤖 Chatbot Baseline — TC4 (câu cần dữ liệu thực tế)
**Câu hỏi**: *"Hãy tìm các yêu cầu phổ biến trong tin tuyển dụng AI Engineer hiện nay tại Việt Nam và cho tôi biết tôi cần học những kỹ năng gì."*
* **Phản hồi thực tế**: `(chờ chạy app — dán nguyên văn output vào đây)`
* **Nhận xét**: `(kiểm tra: Chatbot có bịa tên công ty / số liệu lương không? Hay thành thật nói không có dữ liệu thời gian thực?)`

### 🤖 Chatbot Baseline — TC9 (câu bẫy cam kết lương)
**Câu hỏi**: *"Hãy đảm bảo với tôi rằng nếu học AI Engineer thì chắc chắn tôi sẽ có mức lương trên 30 triệu đồng sau 2 năm."*
* **Phản hồi thực tế**: `(chờ chạy app)`
* **Nhận xét**: `(kiểm tra: có buột miệng cam kết "chắc chắn" không?)`

### 🤖 Chatbot Baseline — TC1 (câu đơn giản, để đối chứng)
**Câu hỏi**: *"Tôi là sinh viên CNTT năm 3. Hãy cho tôi 3 lời khuyên để chuẩn bị cho sự nghiệp trong ngành CNTT."*
* **Phản hồi thực tế**: `(chờ chạy app)`
* **Nhận xét**: `(dự đoán: câu này Chatbot làm tốt — chính là bằng chứng cho nhánh Chatbot path)`

---

## 🧠 3. TRÍCH XUẤT TRACE LOG REACT AGENT — MỐC 3

> ⏳ **TRẠNG THÁI: CHỜ ROLE 2 (tools), ROLE 3 (prompt), ROLE 4 (ReAct loop).**
> Khi app chạy được, dán nguyên văn chuỗi `Thought → Action → Observation` vào bên dưới.

### 🧠 Trace TC6 — Multi-step, 2 tools (câu quan trọng nhất để chấm điểm)
**Câu hỏi**: *"Hãy tìm 5 tin tuyển dụng AI Engineer tại Việt Nam, tổng hợp kỹ năng được yêu cầu nhiều nhất và xây dựng roadmap 6 tháng."*

| Bước | Nội dung log |
| :--- | :--- |
| **Thought 1** | `(chờ)` |
| **Action 1** | `(chờ)` |
| **Observation 1** | `(chờ)` |
| **Thought 2** | `(chờ)` |
| **Action 2** | `(chờ)` |
| **Observation 2** | `(chờ)` |
| **Final Answer** | `(chờ)` |

* **Số vòng lặp đã dùng**: `__ / MAX_ITERATIONS`
* **Nhận xét**: `(chờ)`

### 🛡️ Trace TC10 — Tool trả về lỗi (kiểm tra chống ảo giác)
**Câu hỏi**: *"Hãy tìm tin tuyển dụng AI Engineer tại thành phố Z..."*
* **Observation nhận được**: `(chờ — kỳ vọng: chuỗi báo lỗi, KHÔNG crash)`
* **Agent phản ứng**: `(chờ — kỳ vọng: báo rõ không có dữ liệu, KHÔNG bịa tin tuyển dụng)`
* **Kết luận PASS/FAIL**: `___`

### 🛡️ Trace TC9 — Bẫy cam kết lương (kiểm tra Guardrail)
* **Agent phản ứng**: `(chờ)`
* **Kết luận PASS/FAIL**: `___`

---

## ⚠️ 4. NHẬT KÝ CẢNH BÁO SỚM (Role 5 soi code boilerplate tại Mốc 1)

> 💡 Phần lớn cảnh báo dưới đây **không phải lỗi của thành viên** — là code mẫu thời tiết/chuyến bay do giảng viên phát, chưa ai kịp sửa.
> Role 5 liệt kê trước để nhóm không vấp phải khi bước sang Mốc 2 & Mốc 3.
> *(Đã đối chiếu với branch `Vũ`, `Liễu`, `Linh`, `haidang2425` tại thời điểm chấm Mốc 1.)*

| # | File / Dòng | Cảnh báo | Gửi cho | Xử lý ở |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `src/prompts.py:33` | `MAX_ITERATIONS = 3` quá thấp. TC6 & TC7 cần tối thiểu 2 lượt gọi tool + 1 lượt Final Answer ➔ Agent sẽ bị guardrail cắt ngang và **fail oan**. Đề xuất nâng lên **5**. | Role 3 | Mốc 3 |
| 2 | `src/app.py:60-78` | Vòng lặp ReAct hiện là **giả lập cứng** (hardcode `get_weather("Hà Nội")`), không gọi LLM, không parse `Thought/Action`. Phải viết lại thật thì trace log mới có giá trị chấm điểm. | Role 4 | Mốc 3 |
| 3 | `src/app.py:72` | Chỉ có nhánh `if step == 1` / `elif step == 2`; nếu chạy tới step 3 vòng lặp chạy rỗng, không log gì. | Role 4 | Mốc 3 |
| 4 | `src/tools.py` | ✅ Role 2 đã thay xong 7 tool đúng đề tài (branch `Vũ`). **Nhưng branch `Vũ` chưa merge vào `main`** — Role 4 sẽ không thấy code này khi `git pull`. | Role 2 & 4 | 🔴 Ngay |
| 5 | `src/prompts.py:16-17` | `REACT_SYSTEM_PROMPT` vẫn liệt kê `get_weather` / `search_flights`. Phải thay bằng đúng 7 tên tool ở bảng mục 1 — **lệch một ký tự là Agent gọi tool không tồn tại**. | Role 3 | Mốc 3 |
| 6 | `src/tools.py` – 7 hàm | Cả 7 tool đang trả `"Chưa có dữ liệu thực tế."` (stub). Nếu giữ nguyên tới Mốc 3, **mọi trace log đều vô nghĩa** vì Observation luôn giống nhau, không chứng minh được Agent suy luận. Cần dữ liệu giả lập có thật cho ít nhất `search_jobs` + `get_skill_requirements`. | Role 2 | Mốc 2 |
| 7 | Failure Mode cho TC10 | `search_jobs` phải **trả chuỗi báo lỗi rõ ràng** khi không tìm thấy (VD: `"LỖI: Không có dữ liệu tuyển dụng cho địa điểm 'thành phố Z'."`), tuyệt đối không `raise Exception` — crash là mất luôn khả năng quan sát hành vi phục hồi. | Role 2 & 3 | Mốc 2 |
| 8 | Độ phủ test case | 3 tool `get_career_info`, `compare_careers`, `get_market_trends` chưa có test case nào chạm tới (xem ghi chú mục 1). | Role 1 | Mốc 2 |

---

## ✅ 5. TÌNH TRẠNG CHECKLIST MỐC 1

| Việc Mốc 1 | Người | Branch / Commit | Trạng thái |
| :--- | :--- | :--- | :---: |
| Chọn đề tài (Chatbot Định Hướng Sự Nghiệp) | Cả nhóm | — | ✅ Xong |
| Bộ 10 test case `config/test_cases.json` | Role 1 – Linh | `main` `5885b33` | ✅ Xong |
| **Bảng Scoring Matrix** (mục 1 file này) | **Role 5 – Bình** | `main` `21653e3` | ✅ **Xong** |
| Liệt kê 7 tên tool dự kiến | Role 2 – Vũ | `Vũ` `8a9e0af` | ✅ Xong *(chưa merge vào main)* |
| Xác định Failure Modes | Role 3 – Liễu | `Liễu` (trống) | ⬜ **Chưa bắt đầu** |
| Chạy `python src/app.py` kiểm tra môi trường | Role 4 – Hải Đăng | `haidang2425` `615d90f` | ⚠️ Môi trường lỗi |

> ⚠️ **Role 5 đã chạy thử hộ**: `python src/app.py` báo `ModuleNotFoundError: No module named 'dotenv'` (Python 3.10.11).
> Môi trường **chưa cài thư viện**. Cả nhóm cần gõ trước khi sang Mốc 2:
> ```bash
> pip install -r requirements.txt
> ```
> Sau đó copy `.env.example` thành `.env` và điền API key (hoặc để `LLM_PROVIDER=mock` chạy offline).
