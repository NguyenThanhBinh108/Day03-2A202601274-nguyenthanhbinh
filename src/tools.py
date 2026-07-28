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
# MỐC 2: IMPLEMENT (Sẽ code sau)
# ============================================================

def get_weather(location: str) -> str:
    loc_lower = location.lower()
    if "hà nội" in loc_lower or "ha noi" in loc_lower:
        return "Thời tiết Hà Nội: 28°C, Nắng nhẹ, Độ ẩm 65%."
    elif "hồ chí minh" in loc_lower or "tp.hcm" in loc_lower or "hcm" in loc_lower:
        return "Thời tiết TP.HCM: 33°C, Nắng nóng, Có mây."
    elif "đà nẵng" in loc_lower or "da nang" in loc_lower:
        return "Thời tiết Đà Nẵng: 30°C, Gió nhẹ, Mát mẻ."
    else:
        return f"LỖI: Không tìm thấy dữ liệu thời tiết cho địa điểm '{location}'."


def search_flights(origin: str, destination: str) -> str:
    return (
        f"Chuyến bay từ {origin} -> {destination} ngày mai:\n"
        f"1. VN123 (08:00) - Giá: 1,500,000 VNĐ (Còn vé)\n"
        f"2. VJ456 (14:30) - Giá: 1,200,000 VNĐ (Còn vé)"
    )


AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "search_flights": search_flights,
}
