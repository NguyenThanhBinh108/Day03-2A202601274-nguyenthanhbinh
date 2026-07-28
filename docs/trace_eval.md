# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)
*Dành cho Role 5: Observability & Reviewer — Nguyễn Thanh Bình - 2A202601274*

**Đề tài nhóm chọn**: 🎓 **Chatbot Định Hướng Sự Nghiệp** (Career Guidance Agent)
**Bộ test case tham chiếu**: `config/test_cases.json` (10 câu, do Role 1 biên soạn)

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX) — MỐC 1

*Mục tiêu: Chứng minh bài toán này CẦN ReAct Agent, không chỉ Chatbot thuần.*

| Tiêu chí | Điểm (1-5) | Lý do đánh giá (dẫn chứng từ test case) |
| :--- | :---: | :--- |
| 🧠 **Multi-step Reasoning** | `5/5` | TC6 đòi hỏi chuỗi 3 bước phụ thuộc nhau: tìm tin tuyển dụng ➔ thống kê kỹ năng xuất hiện nhiều nhất ➔ dựng roadmap 6 tháng. Bước sau không thể làm nếu chưa có kết quả bước trước. |
| 🛠️ **Tool Interaction** | `5/5` | Yêu cầu tuyển dụng & mức lương thị trường IT thay đổi liên tục, nằm ngoài dữ liệu huấn luyện của LLM. TC4, TC5, TC6, TC7 đều bắt buộc phải tra cứu dữ liệu tuyển dụng thực tế. |
| 🔀 **Dynamic Decision** | `5/5` | Luồng xử lý rẽ nhánh theo dữ liệu: TC8 (*"Tôi nên theo Data hay AI?"*) thiếu thông tin ➔ Agent phải **hỏi lại** thay vì gọi tool; TC10 (thành phố Z) tool trả về rỗng ➔ Agent phải **đổi hướng và báo không có dữ liệu**, không được bịa. |
| ⏳ **Long Horizon** | `4/5` | Quy trình dài 3–4 bước (tra cứu ➔ trích xuất kỹ năng ➔ so khớp hồ sơ ➔ sinh lộ trình). Dài hơn hẳn chatbot 1 lượt, nhưng chưa tới mức tác vụ nhiều ngày nên không đạt 5/5. |
| **TỔNG ĐIỂM FIT** | **19/20** | **KẾT LUẬN: BÀI TOÁN RẤT NÊN DÙNG REACT AGENT!** |

### 📌 Phân luồng dự kiến của 10 test case (cơ sở cho Hybrid Flowchart ở Mốc 4)

| Test Case | Loại | Luồng dự kiến | Tool cần gọi |
| :---: | :--- | :--- | :--- |
| TC1, TC2, TC3 | Đơn giản | ➡️ **Chatbot path** (trả lời trực tiếp) | Không |
| TC4, TC5 | Multi-step | ➡️ **Agent path** | 1 tool (tra cứu tuyển dụng) |
| TC6, TC7 | Multi-step | ➡️ **Agent path** | 2 tools (tra cứu + phân tích/roadmap) |
| TC8 | Edge – thiếu thông tin | ➡️ **Clarify path** (hỏi lại người dùng) | Không |
| TC9 | Edge – bẫy cam kết | ➡️ **Guardrail path** (từ chối cam kết lương) | Không / tham khảo dữ liệu |
| TC10 | Edge – tool failure | ➡️ **Agent path + xử lý lỗi** | 1 tool (trả về rỗng) |

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

> 💡 Đây **không phải lỗi của thành viên** — toàn bộ là code mẫu thời tiết/chuyến bay do giảng viên phát.
> Role 5 liệt kê trước để nhóm không vấp phải khi bước sang Mốc 2 & Mốc 3.

| # | File / Dòng | Cảnh báo | Gửi cho | Xử lý ở |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `src/prompts.py:33` | `MAX_ITERATIONS = 3` quá thấp. TC6 & TC7 cần tối thiểu 2 lượt gọi tool + 1 lượt Final Answer ➔ Agent sẽ bị guardrail cắt ngang và **fail oan**. Đề xuất nâng lên **5**. | Role 3 | Mốc 3 |
| 2 | `src/app.py:60-78` | Vòng lặp ReAct hiện là **giả lập cứng** (hardcode `get_weather("Hà Nội")`), không gọi LLM, không parse `Thought/Action`. Phải viết lại thật thì trace log mới có giá trị chấm điểm. | Role 4 | Mốc 3 |
| 3 | `src/app.py:72` | Chỉ có nhánh `if step == 1` / `elif step == 2`; nếu chạy tới step 3 vòng lặp chạy rỗng, không log gì. | Role 4 | Mốc 3 |
| 4 | `src/tools.py` | Cần thay `get_weather` / `search_flights` bằng tool tra cứu tuyển dụng & phân tích kỹ năng cho đúng đề tài. | Role 2 | Mốc 2 |
| 5 | `src/prompts.py:16-17` | `REACT_SYSTEM_PROMPT` đang liệt kê tool thời tiết/chuyến bay. Tên tool trong prompt **phải khớp tuyệt đối** với tên hàm của Role 2, lệch một ký tự là Agent gọi tool không tồn tại. | Role 3 | Mốc 3 |
| 6 | Failure Mode cho TC10 | Tool của Role 2 phải **trả về chuỗi báo lỗi**, tuyệt đối không `raise Exception` — nếu crash thì cả app chết, không quan sát được hành vi phục hồi của Agent. | Role 2 & 3 | Mốc 2 |

---

## ✅ 5. TÌNH TRẠNG CHECKLIST MỐC 1

| Việc | Người | Trạng thái |
| :--- | :--- | :---: |
| Chọn đề tài (Chatbot Định Hướng Sự Nghiệp) | Cả nhóm | ✅ Xong |
| Bộ 10 test case `config/test_cases.json` | Role 1 | ✅ Xong (commit `5885b33`) |
| **Bảng Scoring Matrix** (mục 1 file này) | **Role 5** | ✅ **Xong** |
| Liệt kê tên tool sẽ tạo | Role 2 | ⬜ Chưa |
| Xác định Failure Modes | Role 3 | ⬜ Chưa |
| Chạy `python src/app.py` kiểm tra môi trường | Role 4 | ⚠️ Chưa sẵn sàng |

> ⚠️ **Role 5 đã chạy thử hộ**: `python src/app.py` báo `ModuleNotFoundError: No module named 'dotenv'` (Python 3.10.11).
> Môi trường **chưa cài thư viện**. Cả nhóm cần gõ trước khi sang Mốc 2:
> ```bash
> pip install -r requirements.txt
> ```
> Sau đó copy `.env.example` thành `.env` và điền API key (hoặc để `LLM_PROVIDER=mock` chạy offline).
