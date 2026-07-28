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
    """
    Tra cứu danh sách việc làm theo ngành nghề, kỹ năng và địa điểm.

    Args:
        keyword (str): Từ khóa ngành nghề hoặc kỹ năng (VD: 'Python', 'Data Science')
        location (str, optional): Địa điểm làm việc (VD: 'Hà Nội', 'Hồ Chí Minh'). Mặc định '' (cả nước).

    Returns:
        str: Danh sách tin tuyển dụng phù hợp kèm thông tin công ty, lương, địa điểm.

    Error: Trả về chuỗi báo lỗi nếu không tìm thấy kết quả.
    """
    return f"Kết quả tìm kiếm việc làm cho '{keyword}' tại {location or 'cả nước'}: Chưa có dữ liệu thực tế."


def get_career_info(career_name: str) -> str:
    """
    Cung cấp thông tin tổng quan về một ngành nghề.

    Args:
        career_name (str): Tên ngành nghề (VD: 'Lập trình viên', 'Data Scientist').

    Returns:
        str: Mô tả ngành, mức lương trung bình, nhu cầu tuyển dụng, yêu cầu học vấn.

    Error: Trả về chuỗi báo lỗi nếu ngành nghề không tồn tại.
    """
    return f"Thông tin ngành '{career_name}': Chưa có dữ liệu thực tế."


def get_skill_requirements(role: str) -> str:
    """
    Liệt kê các kỹ năng cần thiết cho một vị trí công việc.

    Args:
        role (str): Tên vị trí công việc (VD: 'Frontend Developer', 'AI Engineer').

    Returns:
        str: Danh sách hard skills và soft skills yêu cầu kèm mức độ quan trọng.

    Error: Trả về chuỗi báo lỗi nếu vị trí không tồn tại.
    """
    return f"Kỹ năng yêu cầu cho vị trí '{role}': Chưa có dữ liệu thực tế."


def get_certifications(domain: str) -> str:
    """
    Đề xuất chứng chỉ chuyên môn và khóa học theo lĩnh vực.

    Args:
        domain (str): Lĩnh vực quan tâm (VD: 'Machine Learning', 'Cloud Computing').

    Returns:
        str: Danh sách chứng chỉ, khóa học online, thời gian và chi phí ước tính.

    Error: Trả về chuỗi báo lỗi nếu lĩnh vực không tồn tại.
    """
    return f"Chứng chỉ / khóa học cho lĩnh vực '{domain}': Chưa có dữ liệu thực tế."


def get_career_path(career_name: str) -> str:
    """
    Mô tả lộ trình thăng tiến trong một ngành nghề.

    Args:
        career_name (str): Tên ngành nghề (VD: 'Kỹ sư phần mềm').

    Returns:
        str: Các cấp bậc từ Fresher đến Lead/Manager, thời gian trung bình mỗi cấp.

    Error: Trả về chuỗi báo lỗi nếu ngành nghề không tồn tại.
    """
    return f"Lộ trình thăng tiến ngành '{career_name}': Chưa có dữ liệu thực tế."


def compare_careers(career1: str, career2: str) -> str:
    """
    So sánh hai ngành nghề dựa trên nhiều tiêu chí.

    Args:
        career1 (str): Ngành thứ nhất (VD: 'Data Scientist').
        career2 (str): Ngành thứ hai (VD: 'Software Engineer').

    Returns:
        str: Bảng so sánh lương, yêu cầu kỹ năng, triển vọng, độ khó đầu vào.

    Error: Trả về chuỗi báo lỗi nếu một trong hai ngành không tồn tại.
    """
    return f"So sánh giữa '{career1}' và '{career2}': Chưa có dữ liệu thực tế."


def get_market_trends(industry: str) -> str:
    """
    Tra cứu xu hướng thị trường lao động của một ngành.

    Args:
        industry (str): Tên ngành công nghiệp (VD: 'CNTT', 'Tài chính').

    Returns:
        str: Các ngành hot, tỷ lệ cạnh tranh, top công ty tuyển dụng nhiều.

    Error: Trả về chuỗi báo lỗi nếu không có dữ liệu cho ngành này.
    """
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
