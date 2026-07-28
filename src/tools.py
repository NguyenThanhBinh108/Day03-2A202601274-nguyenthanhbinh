"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
Chủ đề: Chatbot Định Hướng Sự Nghiệp (Career Orientation)
"""

import json
import os

_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "real")


def _load_json(relative_path: str):
    path = os.path.join(_BASE_DIR, relative_path)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def _find_role(roles: dict, keyword: str):
    if keyword in roles:
        return keyword, roles[keyword]
    for name in roles:
        if keyword.lower() in name.lower():
            return name, roles[name]
    return None, None


def search_jobs(keyword: str, location: str = "") -> str:
    """
    Tra cứu danh sách việc làm theo ngành nghề, kỹ năng và địa điểm.

    Args:
        keyword (str): Từ khóa ngành nghề hoặc kỹ năng (VD: 'Python', 'Data Science')
        location (str, optional): Địa điểm làm việc (VD: 'Hà Nội', 'Hồ Chí Minh'). Mặc định '' (cả nước).

    Returns:
        str: Danh sách tin tuyển dụng phù hợp kèm thông tin công ty, lương, địa điểm.
    """
    if not keyword or not keyword.strip():
        return "Vui lòng nhập từ khóa tìm kiếm."
    try:
        data = _load_json("career_maps/all_roles.json")
        if not data or "roles" not in data:
            return "Dữ liệu việc làm hiện chưa khả dụng."
        kw = keyword.strip().lower()
        matched = []
        for name, info in data["roles"].items():
            if kw in name.lower():
                matched.append((name, info))
                continue
            for s in info.get("top_skills", []):
                if kw in s.get("skill", "").lower():
                    matched.append((name, info))
                    break
        if not matched:
            return f"Không tìm thấy việc làm nào liên quan đến '{keyword}'."
        lines = [f"Kết quả cho '{keyword}' ({len(matched)} vị trí):"]
        for name, info in matched[:10]:
            skills = ", ".join(s["skill"] for s in info.get("top_skills", [])[:5])
            lines.append(f"\n• {name}: {info.get('total_jds', '?')} tin — {skills}")
        if location:
            lines.append(f"\n(Lưu ý: chưa hỗ trợ lọc địa điểm '{location}')")
        return "\n".join(lines)
    except Exception as e:
        return f"Đã xảy ra lỗi khi tra cứu việc làm: {str(e)}"


def get_career_info(career_name: str) -> str:
    """
    Cung cấp thông tin tổng quan về một ngành nghề.

    Args:
        career_name (str): Tên ngành nghề (VD: 'Lập trình viên', 'Data Scientist').

    Returns:
        str: Mô tả ngành, mức lương trung bình, nhu cầu tuyển dụng, yêu cầu học vấn.
    """
    if not career_name or not career_name.strip():
        return "Vui lòng nhập tên ngành nghề."
    try:
        roles_data = _load_json("career_maps/all_roles.json")
        idx_data = _load_json("index.json")
        if not roles_data or "roles" not in roles_data:
            return "Dữ liệu ngành nghề chưa khả dụng."
        name, info = _find_role(roles_data["roles"], career_name.strip())
        if not info:
            return f"Không tìm thấy ngành '{career_name}'."
        salary = "Chưa có dữ liệu"
        if idx_data and "roles" in idx_data:
            for r in idx_data["roles"]:
                if r.get("role") == name:
                    if r.get("avg_salary_usd"):
                        salary = f"${r['avg_salary_usd']}/năm"
                    elif r.get("salary_range_usd", {}).get("min"):
                        sal = r["salary_range_usd"]
                        salary = f"${sal['min']} - ${sal['max']}/năm"
                    break
        lines = [
            f"📌 {name}",
            f"📊 Tin tuyển dụng: {info.get('total_jds', '?')}",
            f"💰 Lương: {salary}",
            "\n🎯 Top kỹ năng:",
        ]
        for s in info.get("top_skills", [])[:10]:
            tag = "🔴 BẮT BUỘC" if s.get("priority") == "should_have" else "🟢 NÊN CÓ"
            lines.append(f"  {tag} {s['skill']}: {s.get('frequency_percent', '?')}%")
        return "\n".join(lines)
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"


def get_skill_requirements(role: str) -> str:
    """
    Liệt kê các kỹ năng cần thiết cho một vị trí công việc.

    Args:
        role (str): Tên vị trí công việc (VD: 'Frontend Developer', 'AI Engineer').

    Returns:
        str: Danh sách hard skills và soft skills yêu cầu kèm mức độ quan trọng.
    """
    if not role or not role.strip():
        return "Vui lòng nhập tên vị trí."
    try:
        freq = _load_json("processed/skill_frequency_by_role.json")
        if not freq:
            return "Dữ liệu kỹ năng chưa khả dụng."
        matched_name = None
        for key in freq:
            if role.strip().lower() == key.lower() or role.strip().lower() in key.lower():
                matched_name = key
                break
        if not matched_name:
            return f"Không tìm thấy vị trí '{role}'."
        skills = freq[matched_name].get("skills", [])
        should = [s for s in skills if s.get("priority") == "should_have"]
        nice = [s for s in skills if s.get("priority") == "nice_to_have"]
        lines = [
            f"📋 {matched_name} ({freq[matched_name].get('total_jds', '?')} JD phân tích)",
            f"\n🔴 BẮT BUỘC:",
        ]
        for s in should[:8]:
            lines.append(f"  • {s['skill']}: {s.get('frequency_percent', '?')}% ({s.get('count', '?')} JD)")
        lines.append(f"\n🟢 NÊN CÓ:")
        for s in nice[:8]:
            lines.append(f"  • {s['skill']}: {s.get('frequency_percent', '?')}%")
        return "\n".join(lines) if len(lines) > 2 else f"Không có dữ liệu kỹ năng cho '{role}'."
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"


def get_certifications(domain: str) -> str:
    """
    Đề xuất chứng chỉ chuyên môn và khóa học theo lĩnh vực.

    Args:
        domain (str): Lĩnh vực quan tâm (VD: 'Machine Learning', 'Cloud Computing').

    Returns:
        str: Danh sách chứng chỉ, khóa học online, thời gian và chi phí ước tính.
    """
    if not domain or not domain.strip():
        return "Vui lòng nhập lĩnh vực."
    try:
        key = _normalize_name(domain)
        skill = _load_json(f"skills/{key}.json")
        if not skill:
            return f"Không tìm thấy lĩnh vực '{domain}'."
        lines = [f"📚 {skill.get('skill', domain)} — {skill.get('total_learning_hours', '?')}h học"]
        if skill.get("market_frequency"):
            lines.append(f"📊 {skill['market_frequency']}")
        if skill.get("market_role"):
            lines.append(f"🎯 Phù hợp: {skill['market_role']}")
        modules = skill.get("modules", [])
        if modules:
            lines.append(f"\n📖 Lộ trình ({len(modules)} module):")
            for mod in modules:
                lines.append(f"\n  {mod.get('order', '?')}. {mod.get('title', '')} ({mod.get('hours', '?')}h)")
                for t in mod.get("topics", [])[:3]:
                    lines.append(f"     - {t.get('title', '')} ({t.get('hours', '?')}h)")
                    for res in t.get("academic", {}).get("resources", [])[:2]:
                        tag = "🆓" if res.get("is_free") else "💰"
                        lines.append(f"       {tag} {res.get('title', '')}")
        resources = _load_json(f"resources/{key}_resources.json")
        if resources and resources.get("resources"):
            lines.append(f"\n📎 Tài nguyên ({len(resources['resources'])} items):")
            for r in resources["resources"][:5]:
                tag = "🆓" if r.get("is_free") else "💰"
                lines.append(f"  {tag} {r.get('title', '')} ({r.get('type', '')}, {r.get('duration_hours', '?')}h)")
        return "\n".join(lines)
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"


def get_career_path(career_name: str) -> str:
    """
    Mô tả lộ trình thăng tiến trong một ngành nghề.

    Args:
        career_name (str): Tên ngành nghề (VD: 'Kỹ sư phần mềm').

    Returns:
        str: Các cấp bậc từ Fresher đến Lead/Manager, thời gian trung bình mỗi cấp.
    """
    if not career_name or not career_name.strip():
        return "Vui lòng nhập tên ngành nghề."
    try:
        slug = _normalize_name(career_name)
        sched = _load_json(f"schedule_templates/{slug}_schedule.json")
        if not sched:
            alt_slug = slug.replace("_schedule", "")
            sched = _load_json(f"schedule_templates/{alt_slug}_schedule.json")
        if not sched:
            return f"Không tìm thấy lộ trình cho '{career_name}'."
        lines = [f"🗺️ {sched.get('role', career_name)}"]
        if sched.get("role_description"):
            lines.append(f"📝 {sched['role_description']}")
        skills_order = sched.get("skills_order", [])
        if skills_order:
            lines.append(f"\n📌 Thứ tự học ({len(skills_order)} kỹ năng):")
            for i, sk in enumerate(skills_order, 1):
                lines.append(f"  {i}. {sk}")
        variants = sched.get("variants", {})
        if variants:
            lines.append(f"\n⏱️ Lộ trình theo thời gian:")
            for speed, v in variants.items():
                label = speed.replace("_", " ").replace("per", "/")
                lines.append(f"  • {label}: {v.get('total_weeks', '?')} tuần, {v.get('hours_per_week', '?')}h/tuần")
        return "\n".join(lines)
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"


def compare_careers(career1: str, career2: str) -> str:
    """
    So sánh hai ngành nghề dựa trên nhiều tiêu chí.

    Args:
        career1 (str): Ngành thứ nhất (VD: 'Data Scientist').
        career2 (str): Ngành thứ hai (VD: 'Software Engineer').

    Returns:
        str: Bảng so sánh lương, yêu cầu kỹ năng, triển vọng, độ khó đầu vào.
    """
    if not career1 or not career2:
        return "Vui lòng nhập 2 ngành để so sánh."
    try:
        roles_data = _load_json("career_maps/all_roles.json")
        if not roles_data or "roles" not in roles_data:
            return "Dữ liệu chưa khả dụng."
        roles = roles_data["roles"]
        n1, r1 = _find_role(roles, career1.strip())
        n2, r2 = _find_role(roles, career2.strip())
        if not r1 or not r2:
            missing = [c for c, r in [(career1, r1), (career2, r2)] if not r]
            return f"Không tìm thấy: {', '.join(missing)}."
        s1 = {s["skill"]: s for s in r1.get("top_skills", [])}
        s2 = {s["skill"]: s for s in r2.get("top_skills", [])}
        common = set(s1.keys()) & set(s2.keys())
        only1 = set(s1.keys()) - set(s2.keys())
        only2 = set(s2.keys()) - set(s1.keys())
        lines = [
            f"📊 SO SÁNH: {n1} vs {n2}",
            f"📌 {'Tiêu chí':<25} {n1:<30} {n2}",
            f"   {'Số JD':<25} {r1.get('total_jds', '?'):<30} {r2.get('total_jds', '?')}",
            f"   {'Số kỹ năng yêu cầu':<25} {len(r1.get('top_skills', [])):<30} {len(r2.get('top_skills', []))}",
        ]
        if common:
            lines.append(f"\n✅ Chung ({len(common)}):")
            for sk in sorted(common)[:6]:
                lines.append(f"  • {sk}: {s1[sk].get('frequency_percent', '?')}% vs {s2[sk].get('frequency_percent', '?')}%")
        if only1:
            lines.append(f"\n🔵 Riêng {n1} ({len(only1)}): {', '.join(sorted(only1)[:6])}")
        if only2:
            lines.append(f"\n🟠 Riêng {n2} ({len(only2)}): {', '.join(sorted(only2)[:6])}")
        return "\n".join(lines)
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"


def get_market_trends(industry: str) -> str:
    """
    Tra cứu xu hướng thị trường lao động của một ngành.

    Args:
        industry (str): Tên ngành công nghiệp (VD: 'CNTT', 'Tài chính').

    Returns:
        str: Các ngành hot, tỷ lệ cạnh tranh, top công ty tuyển dụng nhiều.
    """
    if not industry or not industry.strip():
        return "Vui lòng nhập lĩnh vực."
    try:
        ontology = _load_json("skill_ontology.json")
        if not ontology or "skills" not in ontology:
            return "Dữ liệu xu hướng chưa khả dụng."
        ind = industry.strip().lower()
        matched = [
            s for s in ontology["skills"]
            if ind in s.get("domain", "").lower() or ind in s.get("canonical_name", "").lower()
        ]
        if not matched:
            return f"Không tìm thấy xu hướng cho '{industry}'."
        matched.sort(key=lambda s: s.get("frequency_in_jds_percent", 0), reverse=True)
        lines = [f"📈 Xu hướng thị trường — {industry}"]
        for s in matched[:10]:
            demand = s.get("market_demand_vn", "N/A")
            freq = s.get("frequency_in_jds_percent", 0)
            diff = s.get("difficulty", "N/A")
            lines.append(f"  • {s['canonical_name']}: {freq}% JD — Nhu cầu: {demand} — Độ khó: {diff}")
        return "\n".join(lines)
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"


AVAILABLE_TOOLS = {
    "search_jobs": search_jobs,
    "get_career_info": get_career_info,
    "get_skill_requirements": get_skill_requirements,
    "get_certifications": get_certifications,
    "get_career_path": get_career_path,
    "compare_careers": compare_careers,
    "get_market_trends": get_market_trends,
}
