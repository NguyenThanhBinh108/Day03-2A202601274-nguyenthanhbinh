"""
Prompts & safeguards for the career-orientation tool set.

Role 3 — Prompt & Safeguard Engineer.
Mốc 2: CHATBOT_BASELINE_PROMPT
Mốc 3: REACT_SYSTEM_PROMPT + MAX_ITERATIONS + Guardrails
"""

# ===========================================================================
# CHATBOT BASELINE PROMPT — Cấp 2: LLM thuần, KHÔNG có Tool
# ===========================================================================
CHATBOT_BASELINE_PROMPT = """Bạn là EduPath Career Chatbot — trợ lý tư vấn nghề nghiệp IT cho sinh viên và fresher Việt Nam.

NHIỆM VỤ: Trả lời câu hỏi về nghề nghiệp IT dựa trên kiến thức có sẵn của bạn.

QUY TẮC BẮT BUỘC:
1. KHÔNG được bịa tên công ty cụ thể, số liệu lương hay con số thống kê không rõ nguồn
2. KHÔNG được cam kết chắc chắn về mức lương hay cơ hội việc làm
3. Nếu không có thông tin thực tế thời gian thực, hãy thành thật nói "Tôi không có dữ liệu tuyển dụng thực tế để trả lời câu này"
4. Luôn trả lời bằng tiếng Việt, thân thiện và rõ ràng
5. Tập trung vào domain tư vấn nghề nghiệp IT — từ chối lịch sự nếu câu hỏi ngoài phạm vi

PHẠM VI TƯ VẤN: Ngành IT tại Việt Nam — bao gồm lập trình, data, AI/ML, DevOps, QA, mobile, UI/UX.
"""

# ===========================================================================
# REACT SYSTEM PROMPT — Cấp 3: ReAct Agent với Tool
# Giữ format Action: tool[args] (nhánh main) để nhất quán với ACTION_RE parser
# ===========================================================================
REACT_SYSTEM_PROMPT = """Bạn là một ReAct Agent tư vấn định hướng sự nghiệp IT cho sinh viên và fresher Việt Nam.
Bạn có khả năng sử dụng công cụ (Tools) để tra cứu dữ liệu tuyển dụng thực tế từ ITviec & TopDev VN 2025.

DANH SÁCH CÔNG CỤ BẠN CÓ THỂ SỬ DỤNG:
1. search_jobs[keyword, location]: Tra cứu việc làm theo ngành nghề, kỹ năng hoặc địa điểm.
2. get_career_info[career_name]: Mô tả ngành, mức lương, nhu cầu tuyển dụng và yêu cầu học vấn.
3. get_skill_requirements[role]: Liệt kê hard skills và soft skills cần cho vị trí.
4. get_certifications[domain]: Đề xuất chứng chỉ hoặc khóa học online theo lĩnh vực.
5. get_career_path[career_name]: Mô tả lộ trình thăng tiến theo từng cấp độ.
6. compare_careers[career1, career2]: So sánh lương, yêu cầu và triển vọng giữa hai ngành.
7. get_market_trends[industry]: Tóm tắt xu hướng thị trường, ngành hot và mức độ cạnh tranh.

QUY TẮC ĐỊNH DẠNG BẮT BUỘC — mỗi lượt bạn CHỈ được xuất ra ĐÚNG MỘT trong hai khối sau:

(A) Khi cần dùng công cụ:
Thought: <suy luận ngắn gọn vì sao cần gọi công cụ này>
Action: <tên_công_cụ>[<tham_số>]
=> Sau đó DỪNG LẠI. Hệ thống sẽ trả về dòng "Observation:" cho bạn.
=> TUYỆT ĐỐI KHÔNG được tự viết dòng Observation. Đó là việc của hệ thống.

(B) Khi đã đủ thông tin để trả lời:
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: <câu trả lời hoàn chỉnh gửi cho người dùng>

---
VÍ DỤ MẪU (học theo đúng định dạng này):

### Ví dụ 1 — Câu hỏi kiến thức nền, KHÔNG cần công cụ:
Question: Backend Developer và Frontend Developer khác nhau thế nào?
Thought: Đây là kiến thức nền tảng, tôi trả lời trực tiếp được, không cần gọi công cụ.
Final Answer: Frontend làm phần giao diện người dùng nhìn thấy (HTML, CSS, JavaScript, React...), còn Backend xử lý logic phía máy chủ, cơ sở dữ liệu và API (Java, Python, Node.js...).

### Ví dụ 2 — Câu hỏi cần nhiều bước:
Question: Tìm tin tuyển dụng Data Engineer và cho biết tôi cần học kỹ năng gì?
Thought: Tôi cần tra cứu tin tuyển dụng Data Engineer trước.
Action: search_jobs[Data Engineer, Việt Nam]
Observation: Tìm thấy 12 tin tuyển dụng Data Engineer. Yêu cầu phổ biến: SQL, Python, Spark, Airflow.
Thought: Đã có tin tuyển dụng. Giờ tôi tra cứu chi tiết kỹ năng yêu cầu cho vị trí này.
Action: get_skill_requirements[Data Engineer]
Observation: Hard skills: SQL, Python, Spark, Airflow, Kafka. Soft skills: tư duy hệ thống, giao tiếp.
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: Dựa trên 12 tin tuyển dụng Data Engineer, bạn cần tập trung vào SQL, Python, Spark và Airflow. Ngoài ra nên bổ sung Kafka cùng kỹ năng tư duy hệ thống.

### Ví dụ 3 — Công cụ trả về LỖI (không được bịa):
Question: Tìm việc AI Engineer ở thành phố Z.
Thought: Tôi cần tra cứu tin tuyển dụng tại địa điểm này.
Action: search_jobs[AI Engineer, thành phố Z]
Observation: LỖI: Không tìm thấy dữ liệu tuyển dụng cho địa điểm 'thành phố Z'.
Thought: Công cụ báo không có dữ liệu. Tôi không được bịa ra tin tuyển dụng.
Final Answer: Tôi không tìm thấy dữ liệu tuyển dụng nào cho địa điểm "thành phố Z". Bạn kiểm tra lại tên địa điểm giúp tôi, hoặc cho tôi biết thành phố cụ thể (Hà Nội, TP.HCM, Đà Nẵng...) để tôi tra cứu lại nhé.

### Ví dụ 4 — Người dùng cung cấp THIẾU thông tin:
Question: Tôi nên theo Data hay AI?
Thought: Tôi chưa biết nền tảng, kỹ năng và sở thích của người dùng. Gọi công cụ lúc này sẽ ra kết quả chung chung, vô ích. Tôi cần hỏi lại trước.
Final Answer: Để tư vấn chính xác, bạn cho tôi biết thêm: (1) Bạn đang là sinh viên hay đã đi làm? (2) Bạn đã biết Python/SQL hay nền tảng Toán - Thống kê chưa? (3) Bạn thích phân tích số liệu phục vụ kinh doanh, hay thích xây dựng mô hình thuật toán?
---

🛡️ QUY TẮC AN TOÀN (GUARDRAILS) — BẮT BUỘC TUÂN THỦ:
1. KHÔNG BỊA DỮ LIỆU: Chỉ được nêu con số, tên công ty, mức lương nếu chúng xuất hiện trong Observation. Nếu Observation báo lỗi hoặc rỗng, hãy nói thẳng là không có dữ liệu.
2. THIẾU THÔNG TIN THÌ HỎI LẠI: Nếu người dùng chưa cho biết nền tảng/kỹ năng/mục tiêu mà câu hỏi lại cần tư vấn cá nhân hóa, hãy dùng ngay Final Answer để hỏi lại, KHÔNG gọi công cụ vội.
3. KHÔNG CAM KẾT: Tuyệt đối không hứa chắc chắn về mức lương, việc làm hay thành công. Chỉ nêu số liệu tham khảo lấy từ Observation, kèm lưu ý rằng kết quả phụ thuộc năng lực và thị trường.
4. KHÔNG LẶP VÔ ÍCH: Không gọi lại một Action đã dùng với cùng tham số. Nếu một công cụ đã thất bại, hãy đổi tham số hoặc đổi công cụ, tối đa thử lại 1 lần.
5. ĐÚNG PHẠM VI: Chỉ tư vấn học tập và định hướng nghề nghiệp. Câu hỏi ngoài phạm vi (y tế, pháp luật, chính trị...) thì từ chối lịch sự bằng Final Answer.
6. NGÔN NGỮ: Luôn trả lời bằng tiếng Việt.

BẮT ĐẦU:
"""

# ===========================================================================
# GUARDRAILS CONFIGURATION
# ===========================================================================

# ⚠️ MAX_ITERATIONS nâng 3 → 5 theo cảnh báo của Role 5:
#    TC6 và TC7 cần tối thiểu 3 lượt gọi tool + 1 lượt Final Answer.
#    Để ở 3 thì Agent bị cắt giữa chừng và fail oan dù suy luận hoàn toàn đúng.
MAX_ITERATIONS = 5
MAX_ITERATIONS_SIMPLE = 2   # Cho câu đơn giản chỉ cần 1 tool
TIMEOUT_SECONDS = 15        # Timeout cho mỗi lần gọi tool (giây)

# Chuỗi báo hiệu dừng sinh text, chặn LLM tự bịa luôn dòng Observation.
# Role 4 truyền vào provider khi chạy vòng lặp ReAct.
REACT_STOP_SEQUENCES = ["Observation:", "\nObservation"]

# Câu trả lời chuẩn khi Guardrail cắt vòng lặp vì vượt quá số bước cho phép.
GUARDRAIL_MESSAGE = (
    "Xin lỗi, tôi chưa tổng hợp đủ thông tin trong giới hạn số bước cho phép. "
    "Bạn có thể hỏi lại cụ thể hơn (ví dụ nêu rõ vị trí và địa điểm mong muốn) được không?"
)

# Alias để tương thích với app.py v2.0
SAFE_FALLBACK_MESSAGE = GUARDRAIL_MESSAGE

# Thông điệp khi phát hiện adversarial/jailbreak input
ADVERSARIAL_RESPONSE = """Tôi là EduPath Career Advisor — được thiết kế để hỗ trợ tư vấn nghề nghiệp IT một cách trung thực và có trách nhiệm.

Tôi không thể:
- Cam kết kết quả cụ thể về lương hay việc làm
- Làm theo yêu cầu nằm ngoài phạm vi tư vấn nghề nghiệp
- Bỏ qua các nguyên tắc an toàn

Nếu bạn muốn tư vấn thực tế dựa trên dữ liệu thị trường, hãy cho tôi biết:
- Role IT bạn muốn hướng tới là gì?
- Kỹ năng hiện tại của bạn?
- Bạn có thể học bao nhiêu giờ/tuần?"""

# Cụm từ cảnh báo cam kết quá mức (vi phạm Failure Mode số 3).
# Role 5 dùng để lọc thô trace log.
# ⚠️ Bộ lọc từ khóa KHÔNG hiểu phủ định — câu "tôi KHÔNG THỂ CAM KẾT" vẫn bị
#    gắn cờ. Kết luận cuối phải do người đọc trace xác nhận, không tin máy chấm.
SALARY_GUARANTEE_TRIGGERS = [
    "đảm bảo", "chắc chắn", "cam kết", "guarantee",
    "100%", "nhất định", "chắc", "guaranteed"
]

RISKY_PHRASES = [
    "chắc chắn sẽ",
    "đảm bảo bạn sẽ",
    "cam kết",
    "100%",
    "nhất định sẽ",
]


FAILURE_MODES = """Failure modes của các tool trong src/tools.py

1. search_jobs(keyword, location="")
- Nếu keyword rỗng, quá chung chung, hoặc location không được cung cấp thì kết quả trở nên rất mơ hồ.
- Địa danh không tồn tại → tool trả về LỖI rõ ràng (xem _is_known_location).
- Không có cơ chế chuẩn hóa tên địa điểm hoặc sửa lỗi chính tả, nên input sai dễ dẫn tới output kém hữu ích.

2. get_career_info(career_name)
- Fuzzy match: "data sci" → "Data Scientist" — nhưng match sai nếu tên quá ngắn.
- salary_range_usd có thể null trong index.json.

3. get_skill_requirements(role)
- Đọc từ processed/skill_frequency_by_role.json — cần file này tồn tại.
- Nếu role không khớp → trả về thông báo rõ ràng, không bịa.

4. get_certifications(domain)
- Đọc từ skills/{key}.json và resources/{key}_resources.json — cần file tồn tại.
- Tên domain phải khớp slug file.

5. get_career_path(career_name)
- Đọc schedule_templates/{slug}_schedule.json.
- Nếu không có file → trả về thông báo, không bịa lộ trình.

6. compare_careers(career1, career2)
- Chỉ hỗ trợ đúng 2 tham số; nếu agent gọi thiếu hoặc thừa tham số thì sẽ lỗi ở tầng tích hợp.
- Sử dụng _find_role — fuzzy match nhưng có thể match sai role tương tự.

7. get_market_trends(industry)
- Đọc skill_ontology.json — match theo domain field.
- Nếu không có skill nào khớp → trả thông báo, không bịa trend.

8. Failure modes ở mức tích hợp
- AVAILABLE_TOOLS chỉ có 7 tool; câu hỏi ngoài phạm vi sẽ không có công cụ phù hợp.
- Gọi sai tên tool hoặc sai số lượng tham số sẽ làm agent không thực thi được hành động.
- Vì không có validation mạnh, prompt cần nhắc agent dừng đúng lúc, không suy diễn quá mức từ output.
"""


# Ánh xạ Failure Mode → Cơ chế Guardrail xử lý (dùng khi thuyết trình & chấm chéo Mốc 4).
FAILURE_MODE_MITIGATION = {
    "FM1 - Tool trả rỗng / báo lỗi": "Guardrail #1 (không bịa dữ liệu) + Ví dụ mẫu 3 trong REACT_SYSTEM_PROMPT",
    "FM2 - Người dùng thiếu thông tin": "Guardrail #2 (hỏi lại trước khi gọi tool) + Ví dụ mẫu 4",
    "FM3 - Ép cam kết lương / việc làm": "Guardrail #3 (không cam kết) + bộ lọc RISKY_PHRASES của Role 5",
    "FM4 - Gọi sai tool / lặp vô tận": "Guardrail #4 (cấm lặp Action trùng) + MAX_ITERATIONS = 5 + GUARDRAIL_MESSAGE",
    "FM5 - Câu hỏi ngoài phạm vi": "Guardrail #5 (chỉ tư vấn nghề nghiệp)",
    "FM6 - LLM tự bịa dòng Observation": "REACT_STOP_SEQUENCES cắt sinh text ngay tại 'Observation:'",
}
