"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
Chủ đề: Chatbot Định Hướng Sự Nghiệp (Career Orientation)
"""

# ============================================================
# MỐC 1: DANH SÁCH CÔNG CỤ DỰ KIẾN (Career Orientation)
# ============================================================
# 1. search_jobs(keyword, location)
#    - Tra cứu việc làm theo ngành nghề/kỹ năng/địa điểm.
#
# 2. get_career_info(career_name)
#    - Mô tả ngành, mức lương TB, nhu cầu tuyển dụng, yêu cầu học vấn.
#
# 3. get_skill_requirements(role)
#    - Liệt kê hard skills & soft skills cần cho vị trí.
#
# 4. get_certifications(domain)
#    - Đề xuất chứng chỉ, khóa học online theo lĩnh vực.
#
# 5. get_career_path(career_name)
#    - Lộ trình thăng tiến Fresher → Junior → Senior → Lead/Manager.
#
# 6. compare_careers(careers)
#    - So sánh lương, yêu cầu, triển vọng giữa các ngành.
#
# 7. get_market_trends(industry)
#    - Xu hướng thị trường: ngành hot, tỷ lệ cạnh tranh, top công ty.

# ============================================================
# MỐC 2: IMPLEMENTATION
# ============================================================

def search_jobs(keyword: str, location: str = "") -> str:
    return f"Kết quả tìm kiếm việc làm cho '{keyword}' tại {location or 'cả nước'}: Chưa có dữ liệu thực tế."


def get_career_info(career_name: str) -> str:
    return f"Thông tin ngành '{career_name}': Chưa có dữ liệu thực tế."


def get_skill_requirements(role: str) -> str:
    return f"Kỹ năng yêu cầu cho vị trí '{role}': Chưa có dữ liệu thực tế."


def get_certifications(domain: str) -> str:
    return f"Chứng chỉ / khóa học cho lĩnh vực '{domain}': Chưa có dữ liệu thực tế."


def get_career_path(career_name: str) -> str:
    return f"Lộ trình thăng tiến ngành '{career_name}': Chưa có dữ liệu thực tế."


def compare_careers(career1: str, career2: str) -> str:
    return f"So sánh giữa '{career1}' và '{career2}': Chưa có dữ liệu thực tế."


def get_market_trends(industry: str) -> str:
    return f"Xu hướng thị trường ngành '{industry}': Chưa có dữ liệu thực tế."


AVAILABLE_TOOLS = {
    "search_jobs": search_jobs,
    "get_career_info": get_career_info,
    "get_skill_requirements": get_skill_requirements,
    "get_certifications": get_certifications,
    "get_career_path": get_career_path,
    "compare_careers": compare_careers,
    "get_market_trends": get_market_trends,
}
