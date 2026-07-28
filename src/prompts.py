"""
Prompts & safeguards for the career-orientation tool set.
"""

# Baseline Chatbot Prompt: no tool use, just direct LLM response.
CHATBOT_BASELINE_PROMPT = """Bạn là một chatbot tư vấn thông thường.
Hãy trả lời câu hỏi của người dùng một cách thân thiện, rõ ràng, dựa trên kiến thức sẵn có của bạn.
Nếu không biết thông tin thực tế hoặc thông tin có thể thay đổi theo thời gian, hãy nói rõ là bạn không chắc và tránh bịa dữ liệu.
"""

# ReAct Agent Prompt: use tools when needed, then answer from observations.
REACT_SYSTEM_PROMPT = """Bạn là một ReAct Agent thông minh có khả năng sử dụng công cụ (Tools).

Danh sách công cụ bạn có thể sử dụng:
1. search_jobs[keyword, location]: Tra cứu việc làm theo ngành nghề, kỹ năng hoặc địa điểm.
2. get_career_info[career_name]: Mô tả ngành, mức lương, nhu cầu tuyển dụng và yêu cầu học vấn.
3. get_skill_requirements[role]: Liệt kê hard skills và soft skills cần cho vị trí.
4. get_certifications[domain]: Đề xuất chứng chỉ hoặc khóa học online theo lĩnh vực.
5. get_career_path[career_name]: Mô tả lộ trình thăng tiến theo từng cấp độ.
6. compare_careers[career1, career2]: So sánh lương, yêu cầu và triển vọng giữa hai ngành.
7. get_market_trends[industry]: Tóm tắt xu hướng thị trường, ngành hot và mức độ cạnh tranh.

QUY TẮC BẮT BUỘC: Khi trả lời, bạn PHẢI tuân theo định dạng từng dòng sau:

Thought: Suy luận của bạn về bước tiếp theo cần làm.
Action: tên_công_cụ[tham_số]
(Sau đó dừng lại chờ hệ thống trả về kết quả Observation)

Khi đã có đủ thông tin để trả lời người dùng, hãy dùng định dạng:
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: Câu trả lời hoàn chỉnh cuối cùng gửi cho người dùng.

BẮT ĐẦU:
"""

# Guardrails configuration.
MAX_ITERATIONS = 3
TIMEOUT_SECONDS = 10


FAILURE_MODES = """Failure modes của các tool trong src/tools.py

1. search_jobs(keyword, location="")
- Nếu keyword rỗng, quá chung chung, hoặc location không được cung cấp thì kết quả trở nên rất mơ hồ.
- Tool không tra cứu dữ liệu việc làm thực tế, nên mọi câu trả lời đều là mô phỏng và không dùng để khẳng định thị trường tuyển dụng.
- Không có cơ chế chuẩn hóa tên địa điểm hoặc sửa lỗi chính tả, nên input sai dễ dẫn tới output kém hữu ích.

2. get_career_info(career_name)
- Không có dữ liệu ngành thực tế; luôn trả về chuỗi mô phỏng "Chưa có dữ liệu thực tế".
- Nếu career_name nhập sai, tool vẫn trả về kết quả chung chung thay vì tự sửa hoặc suy luận thêm.

3. get_skill_requirements(role)
- Không phân biệt đúng/sai giữa các vai trò tương đồng, nên output có thể quá rộng hoặc quá chung.
- Không có data nguồn thật để xác minh kỹ năng bắt buộc hay kỹ năng khuyến nghị.

4. get_certifications(domain)
- Không kiểm tra tính hợp lệ, độ mới, hay độ phổ biến của chứng chỉ.
- Output chỉ là mô tả placeholder, nên không nên dùng như danh sách chứng chỉ đáng tin cậy.

5. get_career_path(career_name)
- Không có lộ trình nghề nghiệp thật theo thị trường; chỉ trả về chuỗi mô phỏng.
- Không phân nhánh theo bối cảnh cá nhân như học vấn, kinh nghiệm, hoặc mục tiêu chuyển ngành.

6. compare_careers(career1, career2)
- Chỉ hỗ trợ đúng 2 tham số; nếu agent gọi thiếu hoặc thừa tham số thì sẽ lỗi ở tầng tích hợp.
- Không có dữ liệu so sánh thật về lương, nhu cầu tuyển dụng hoặc triển vọng.

7. get_market_trends(industry)
- Không dùng dữ liệu thời gian thực nên xu hướng thị trường có thể cũ hoặc không chính xác.
- Không có lớp xác thực nguồn, nên không thể xem như báo cáo thị trường thật.

8. Failure modes ở mức tích hợp
- AVAILABLE_TOOLS chỉ có 7 tool; câu hỏi ngoài phạm vi sẽ không có công cụ phù hợp.
- Gọi sai tên tool hoặc sai số lượng tham số sẽ làm agent không thực thi được hành động.
- Tất cả tool đều trả về string đơn giản, không có schema lỗi riêng, nên agent phải tự đọc chuỗi lỗi/placeholder.
- Vì không có validation mạnh, prompt cần nhắc agent dừng đúng lúc, không suy diễn quá mức từ output mô phỏng.
"""
