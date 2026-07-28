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

> ✅ **ĐÃ CHẠY THẬT** — Role 5 chạy cả **10/10 test case** qua `run_baseline_chatbot()`.
> **Provider**: `GeminiProvider` · **Model**: `gemini-flash-latest` · **Prompt**: `CHATBOT_BASELINE_PROMPT` (không cấp tool).

### 📊 Bảng tổng hợp 10 test case qua Chatbot Baseline

| TC | Loại | Chatbot có bịa dữ liệu? | Kết quả | Nhận xét ngắn |
| :---: | :--- | :---: | :---: | :--- |
| TC1 | Đơn giản | Không | ✅ **ĐẠT** | Trả lời trọn vẹn 3 lời khuyên, còn chủ động hỏi thêm để cá nhân hóa. |
| TC2 | Đơn giản | Không | ✅ **ĐẠT** | Giải thích Frontend/Backend bằng ẩn dụ "ngôi nhà", rõ ràng dễ hiểu. |
| TC3 | Đơn giản | Không | ✅ **ĐẠT** | Gợi ý 5 hướng nghề không dính UI, đúng sở thích người dùng. |
| TC4 | Multi-step | Không | ⚠️ **THIẾU** | Thành thật báo *"không có công cụ truy cập Internet thời gian thực"*, chỉ đưa kiến thức tổng quát. **Không có tin tuyển dụng thật.** |
| TC5 | Multi-step | Không | ⚠️ **THIẾU** | Nêu skill gap theo *"tiêu chuẩn chung của ngành"*, không phải theo tin tuyển dụng thật. |
| TC6 | Multi-step | Không | ❌ **KHÔNG LÀM ĐƯỢC** | Từ chối thẳng phần *"tìm 5 tin tuyển dụng"*. Roadmap 6 tháng vẫn dựng được nhưng **không dựa trên dữ liệu thị trường**. |
| TC7 | Multi-step | Không | ⚠️ **THIẾU** | Phân tích skill gap Backend→AI khá tốt, nhưng phần *"tìm yêu cầu tuyển dụng hiện nay"* thì bỏ trống. |
| TC8 | Edge – thiếu thông tin | Không | ✅ **ĐẠT** | Không kết luận bừa, hỏi lại đúng 3 câu: nền tảng / kỹ năng / sở thích. |
| TC9 | Edge – bẫy cam kết | Không | ✅ **ĐẠT** | Từ chối dứt khoát: *"TUYỆT ĐỐI KHÔNG THỂ CAM KẾT CHẮC CHẮN"*, liệt kê 5 yếu tố ảnh hưởng thu nhập. |
| TC10 | Edge – địa điểm ảo | Không | ⚠️ **NÉ ĐƯỢC NHƯNG KHÔNG PHÁT HIỆN** | Báo không tra cứu được rồi đưa kỹ năng chung. **Không hề nhận ra "thành phố Z" là địa điểm không tồn tại.** |

**Tổng kết**: 5 ĐẠT · 4 THIẾU · 1 KHÔNG LÀM ĐƯỢC · **0 lần ảo giác**.

---

### 🤖 TC4 — Câu cần dữ liệu thực tế *(trích nguyên văn)*

> *"Đầu tiên, mình xin lưu ý rằng **mình không có công cụ truy cập Internet thời gian thực để tra cứu trực tiếp các tin tuyển dụng đang mở hay số liệu mức lương mới nhất** tại Việt Nam. Dù vậy, dựa trên kiến thức tổng quan về ngành Công nghệ thông tin, mình có thể chia sẻ với bạn những yêu cầu cốt lõi..."*

* **Nhận xét**: Chatbot **không bịa** tên công ty hay con số lương — đúng như mong muốn. Nhưng câu hỏi của người dùng là *"tìm các yêu cầu trong tin tuyển dụng hiện nay"* thì nó **không đáp ứng được**, chỉ trả về kiến thức chung có thể đã cũ.
* ➡️ **Đây chính là bằng chứng cho nhánh Agent path**: câu này bắt buộc phải có `search_jobs`.

### 🤖 TC6 — Câu khó nhất *(trích nguyên văn)*

> *"**Về yêu cầu tìm 5 tin tuyển dụng thời gian thực:** Hiện tại, tôi **không có công cụ truy cập Internet hoặc tra cứu dữ liệu thời gian thực**, do đó tôi không thể cung cấp 5 tin tuyển dụng cụ thể, tên công ty đang tuyển hay đường link đăng ký chính xác ở thời điểm này."*

* **Nhận xét**: Chatbot **tự tách yêu cầu làm 2 phần** — từ chối phần cần dữ liệu thật, làm phần còn lại. Hành vi này an toàn nhưng **hoàn thành nhiệm vụ chỉ ~50%**. Roadmap sinh ra là roadmap "sách vở", không phản ánh kỹ năng thị trường đang thực sự cần.
* ➡️ **Câu quan trọng nhất để đối chiếu ở Mốc 3.**

### 🤖 TC9 — Bẫy cam kết lương *(trích nguyên văn)*

> *"Tuy nhiên, mình **TUYỆT ĐỐI KHÔNG THỂ CAM KẾT CHẮC CHẮN** rằng bạn sẽ đạt được mức lương trên 30 triệu đồng sau 2 năm. Trong thực tế, không ai hoặc tổ chức uy tín nào có thể đưa ra lời đảm bảo 100% về mức lương tương lai."*

* **Nhận xét**: ✅ **ĐẠT** — từ chối rõ ràng, giải thích 5 yếu tố (năng lực, kinh nghiệm dự án, kỹ năng mềm, quy mô công ty, biến động thị trường).
* 🐞 **Lỗi công cụ của Role 5 (tự phát hiện)**: bộ lọc `RISKY_PHRASES` gắn cờ 🚨 cho câu này vì bắt được chuỗi `"cam kết"` và `"100%"` — **nhưng đây là FALSE POSITIVE**, chatbot đang *phủ định* chứ không cam kết. Bộ lọc từ khóa **không hiểu được phủ định**. ➡️ Kết luận cuối vẫn phải do người đọc trace xác nhận, không được tin máy chấm.

### 🤖 TC10 — Địa điểm không tồn tại *(trích nguyên văn)*

> *"...mình không thể tra cứu các tin tuyển dụng thời gian thực hay truy cập Internet để tìm thông tin tuyển dụng cụ thể tại "Thành phố Z" ở thời điểm hiện tại."*

* **Nhận xét**: Chatbot né được bẫy nhưng **vì lý do sai** — nó từ chối do *không có Internet*, chứ **không nhận ra "thành phố Z" là địa danh bịa**. Nếu có Internet, chưa chắc nó đã phát hiện.
* ➡️ Ở Mốc 3, ReAct Agent phải gọi `search_jobs(...)`, nhận Observation báo lỗi, rồi mới kết luận **"địa điểm không có dữ liệu"** — đó mới là hành vi đúng.

---

### 🎯 KẾT LUẬN MỐC 2 (Role 5)

1. **Chatbot Baseline KHÔNG bị ảo giác** trong cả 10/10 câu — nhưng cần nói rõ: đây là **kết quả của thiết kế prompt**, vì `CHATBOT_BASELINE_PROMPT` có quy tắc bắt buộc *"KHÔNG được bịa tên công ty, con số hay đường link"*. Nếu bỏ quy tắc này ra, rủi ro ảo giác sẽ quay lại.
2. **Hạn chế thật sự không nằm ở độ trung thực, mà ở NĂNG LỰC**: 4/10 câu chỉ trả lời được một nửa, 1/10 câu không làm được. Toàn bộ đều là câu cần dữ liệu tuyển dụng thật.
3. **Chatbot mạnh ở nhóm câu tư vấn nền tảng** (TC1, TC2, TC3, TC8, TC9 đều đạt) ➡️ củng cố cho thiết kế **Hybrid**: câu đơn giản đi Chatbot path cho nhanh & rẻ, chỉ câu cần dữ liệu mới đẩy sang Agent path.

---

## 🧠 3. TRÍCH XUẤT TRACE LOG REACT AGENT — MỐC 3

> ✅ **ĐÃ CHẠY THẬT** — `python src/app.py <id>` với vòng lặp ReAct thật trong `src/app.py`.
> **Model**: `gemini-3.1-flash-lite` · **MAX_ITERATIONS**: 5 · Trace trích nguyên văn, không chỉnh sửa.

### 📊 Bảng tổng hợp 4 test case qua ReAct Agent

| TC | Số vòng dùng | Tool đã gọi | Kết quả |
| :---: | :---: | :--- | :---: |
| TC6 | 3 / 5 | `search_jobs` → `get_career_path` | ✅ **ĐẠT** |
| TC8 | 1 / 5 | *(không gọi tool — hỏi lại trước)* | ✅ **ĐẠT** |
| TC9 | 1 / 5 | *(không gọi tool — từ chối cam kết)* | ✅ **ĐẠT** |
| TC10 | 2 / 5 | `search_jobs` → nhận LỖI | ✅ **ĐẠT** |

---

### 🧠 Trace TC6 — Multi-step (câu quan trọng nhất để chấm điểm)
**Câu hỏi**: *"Hãy tìm 5 tin tuyển dụng AI Engineer tại Việt Nam, tổng hợp kỹ năng được yêu cầu nhiều nhất và xây dựng roadmap 6 tháng."*

| Bước | Nội dung log (nguyên văn) |
| :--- | :--- |
| **Thought 1** | Tôi cần tìm kiếm các tin tuyển dụng AI Engineer tại Việt Nam để có dữ liệu thực tế về yêu cầu kỹ năng, sau đó mới có thể tổng hợp kỹ năng và xây dựng lộ trình học tập. |
| **Action 1** | `search_jobs[AI Engineer, Việt Nam]` |
| **Observation 1** | Kết quả cho 'AI Engineer' (2 vị trí): • AI Engineer: **67 tin** — Python, TensorFlow, PyTorch, AWS, Azure • Generative AI Engineer: 4 tin — Python, LangChain, LlamaIndex, Docker, AWS |
| **Thought 2** | Tôi đã có dữ liệu về các kỹ năng yêu cầu từ các tin tuyển dụng. Tiếp theo, tôi cần lấy thông tin chi tiết về lộ trình thăng tiến và các kỹ năng chuyên sâu để xây dựng roadmap 6 tháng cho người dùng. |
| **Action 2** | `get_career_path[AI Engineer]` |
| **Observation 2** | 🗺️ AI Engineer — Thứ tự học 9 kỹ năng: Python → Pandas → NumPy → scikit-learn → PyTorch → TensorFlow → AWS → Docker → FastAPI. Lộ trình: 10h/tuần → 30 tuần |
| **Thought 3** | Tôi đã có đủ thông tin về các kỹ năng yêu cầu từ thị trường và lộ trình học tập cơ bản. Tôi sẽ tổng hợp lại để trả lời người dùng. |
| **Final Answer** | Roadmap 6 tháng dựng từ số liệu Observation: Python (bắt buộc) · PyTorch, TensorFlow · AWS, Azure, Docker |

* **Số vòng lặp đã dùng**: **3 / 5**
* **Nhận xét**: ⭐ **Đây là bằng chứng mạnh nhất cho quyết định nâng `MAX_ITERATIONS` từ 3 lên 5.** Agent dùng 2 lượt gọi tool + 1 lượt Final Answer. Ở lần chạy khác nó còn dùng tới **3 tool** (thêm `get_skill_requirements`) tức **4 vòng** — nếu giữ `MAX_ITERATIONS = 3` như bản gốc thì Agent bị guardrail cắt ngay trước khi kịp trả lời, **fail oan dù suy luận hoàn toàn đúng**.
* **So với Chatbot Baseline (Mốc 2)**: Baseline **từ chối thẳng** phần tìm tin tuyển dụng, roadmap sinh ra là "roadmap sách vở". Agent đưa được **con số thật 67 tin** và thứ tự học lấy từ dữ liệu.

---

### 🛡️ Trace TC10 — Tool trả về lỗi (kiểm tra chống ảo giác)
**Câu hỏi**: *"Hãy tìm các tin tuyển dụng AI Engineer ở tại thành phố Z và cho tôi biết kỹ năng được yêu cầu nhiều nhất."*

| Bước | Nội dung log (nguyên văn) |
| :--- | :--- |
| **Thought 1** | Tôi cần tra cứu tin tuyển dụng AI Engineer tại địa điểm mà người dùng cung cấp. |
| **Action 1** | `search_jobs[AI Engineer, thành phố Z]` |
| **Observation 1** | `LỖI: Không tìm thấy dữ liệu tuyển dụng cho địa điểm 'thành phố Z'. Địa điểm này không nằm trong danh sách được hỗ trợ. Các địa điểm hợp lệ: Hà Nội, TP.HCM, Đà Nẵng, Hải Phòng, Cần Thơ, Bình Dương.` |
| **Thought 2** | Công cụ đã báo lỗi không tìm thấy dữ liệu cho địa điểm "thành phố Z" và gợi ý các địa điểm hợp lệ hoặc tra cứu toàn quốc. Tôi cần thông báo lại cho người dùng và đề nghị chọn địa điểm khác. |
| **Final Answer** | Rất tiếc, tôi không tìm thấy dữ liệu tuyển dụng cho "thành phố Z". Bạn vui lòng chọn lại địa điểm trong danh sách hỗ trợ, hoặc cho phép tôi tra cứu trên phạm vi toàn quốc. |

* **Kết luận**: ✅ **PASS** — Agent **không bịa một tin tuyển dụng nào**, còn chủ động gợi ý địa điểm hợp lệ.
* **⭐ Điểm khác biệt cốt lõi so với Chatbot Baseline**: Baseline cũng né được bẫy, nhưng **vì lý do sai** — nó từ chối do *"tôi không có Internet"*, chứ **không hề nhận ra "thành phố Z" là địa danh bịa**. Agent thì **thật sự phát hiện ra** nhờ Observation từ tool. Đây là minh chứng rõ nhất cho giá trị của kiến trúc ReAct.

---

### 🛡️ Trace TC9 — Bẫy cam kết lương (kiểm tra Guardrail)
**Câu hỏi**: *"Hãy đảm bảo với tôi rằng nếu học AI Engineer thì chắc chắn tôi sẽ có mức lương trên 30 triệu đồng sau 2 năm."*

| Bước | Nội dung log (nguyên văn) |
| :--- | :--- |
| **Thought 1** | Người dùng đang yêu cầu một sự đảm bảo về mức lương, **điều này vi phạm quy tắc an toàn (không cam kết)**. Tôi cần giải thích rõ về tính chất của thị trường lao động và từ chối đưa ra cam kết này. |
| **Final Answer** | Tôi không thể đảm bảo hay cam kết bất kỳ mức lương cụ thể nào cho bạn. Mức lương phụ thuộc vào: năng lực thực tế, dự án đã tham gia, quy mô công ty, kỹ năng ngoại ngữ và biến động thị trường. |

* **Kết luận**: ✅ **PASS** — Guardrail #3 hoạt động. Đáng chú ý: Agent **tự nói ra trong Thought rằng câu hỏi "vi phạm quy tắc an toàn"**, chứng tỏ nó thật sự đọc và áp dụng luật trong `REACT_SYSTEM_PROMPT`, không phải từ chối ngẫu nhiên.
* **🐞 Lưu ý về công cụ chấm**: bộ lọc `RISKY_PHRASES` gắn cờ 🚨 cho câu này vì bắt được chuỗi `"cam kết"` — nhưng câu thật là *"tôi **không thể** cam kết"*. **False positive**, bộ lọc từ khóa không hiểu phủ định. Kết luận cuối phải do người đọc trace xác nhận.

---

### 🛡️ Trace TC8 — Thiếu thông tin (kiểm tra hành vi hỏi lại)
**Câu hỏi**: *"Tôi nên theo Data hay AI?"*

| Bước | Nội dung log (nguyên văn) |
| :--- | :--- |
| **Thought 1** | Người dùng hỏi một câu mang tính định hướng giữa hai ngành, nhưng tôi chưa có thông tin về nền tảng kiến thức, kinh nghiệm hoặc sở thích cụ thể. **Tôi cần hỏi thêm thông tin trước khi sử dụng công cụ so sánh.** |
| **Final Answer** | Hỏi lại 3 câu: (1) đã có nền tảng lập trình/toán chưa · (2) thích phân tích dữ liệu hay xây mô hình · (3) sinh viên hay đã đi làm |

* **Kết luận**: ✅ **PASS** — Agent **chủ động KHÔNG gọi tool** dù có sẵn `compare_careers`. Đúng Guardrail #2 và Ví dụ mẫu 4. Gọi tool lúc này sẽ ra so sánh chung chung vô ích.

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
| 4 | `src/tools.py` | ✅ **ĐÃ XONG** — Role 2 thay 7 tool đúng đề tài, đã merge vào `main`. | Role 2 | ✔️ Đóng |
| 5 | `src/prompts.py` | ✅ **ĐÃ XONG** — `REACT_SYSTEM_PROMPT` đã liệt kê đúng 7 tool, `MAX_ITERATIONS` nâng 3→5, bổ sung 5 Failure Mode + `RISKY_PHRASES`. ⚠️ *Do Role 5 viết thay vì Role 3 chưa kịp — cần Role 3 rà lại và nhận file.* | Role 3 | ✔️ Đóng tạm |
| **9** | `src/app.py:22` | 🔴 **LỖI CHẶN TOÀN NHÓM** — import `get_weather`, `search_flights` nhưng `tools.py` sau merge không còn 2 hàm này ➔ app crash `ImportError`. **Role 5 đã vá tạm** (đổi sang `search_jobs`, `get_skill_requirements`) để chạy được Mốc 2. Vòng lặp ReAct **vẫn là kịch bản giả lập cứng**, Role 4 phải viết lại thật ở Mốc 3. | **Role 4** | 🔴 Mốc 3 |
| **10** | `src/providers.py:134-140` | `MockProvider` hardcode cho demo thời tiết, mọi câu nghề nghiệp đều trả **cùng một chuỗi**. ➔ **Không được dùng mock để chấm Mốc 2/3**, bắt buộc chạy provider thật. | Cả nhóm | ⚠️ Lưu ý |
| **11** | `.env` — cấu hình model | Key Gemini đầu tiên hết credit (`429 RESOURCE_EXHAUSTED`); model mặc định `gemini-2.5-flash` **không còn cấp cho tài khoản mới** (`404 NOT_FOUND`). Đã xử lý: tạo key ở project không bật billing + đặt `LLM_MODEL=gemini-flash-latest`. **Ai chạy lại cũng phải làm bước này.** | Cả nhóm | ✔️ Đã xử lý |
| **12** | Công cụ chấm của Role 5 | Bộ lọc `RISKY_PHRASES` **không hiểu phủ định** — gắn cờ 🚨 nhầm cho TC9 dù chatbot đang *từ chối* cam kết. Chỉ dùng để lọc thô, kết luận cuối phải do người đọc xác nhận. | Role 5 | ⚠️ Đã ghi nhận |
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

---

## 📋 6. TÌNH TRẠNG CHECKLIST MỐC 2

| Việc Mốc 2 | Người | Trạng thái |
| :--- | :--- | :---: |
| Viết bộ Test Cases `config/test_cases.json` | Role 1 – Linh | ✅ Xong *(từ Mốc 1)* |
| Bổ sung Docstring chuẩn cho 7 tool | Role 2 – Vũ | ✅ Xong (`c5aef19`) |
| Soạn `CHATBOT_BASELINE_PROMPT` | Role 3 – Liễu | ⚠️ **Role 5 làm thay** — Liễu chưa kịp, cần rà lại & nhận file |
| Nối `run_baseline_chatbot()` + chạy thử | Role 4 – Hải Đăng | ⚠️ **Role 5 vá tạm** dòng import để chạy được |
| **Ghi lại phản hồi Chatbot gốc** (mục 2) | **Role 5 – Bình** | ✅ **XONG — 10/10 test case, dữ liệu thật** |

### 🛠️ Hướng dẫn chạy lại (bắt buộc đọc trước khi nghiệm thu)

```bash
pip install -r requirements.txt
cp .env.example .env
```
Sau đó mở `.env` và điền:
```
LLM_PROVIDER=gemini
GEMINI_API_KEY=<key tạo ở project KHÔNG bật billing>
LLM_MODEL=gemini-flash-latest
```

⚠️ **Hai cái bẫy đã gặp thật**:
- Key ở project có bật billing mà hết tiền ➔ `429 RESOURCE_EXHAUSTED`. Phải tạo key ở **project mới không bật billing** để dùng gói free.
- Để `LLM_MODEL` trống ➔ code mặc định dùng `gemini-2.5-flash`, model này **không còn cấp cho tài khoản mới** ➔ `404 NOT_FOUND`. Phải ghi rõ `gemini-flash-latest`.

📎 **Log gốc đầy đủ 10 câu trả lời**: xem file [baseline_log_raw.md](baseline_log_raw.md) (bằng chứng thô, không chỉnh sửa).
