"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
Chủ đề: Chatbot Định Hướng Sự Nghiệp (Career Orientation)
Dataset: ITviec & TopDev Vietnam IT Market Report 2025 (version 2026-06-11)
"""

import json
import os
import re

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


# ============================================================
# XÁC THỰC ĐỊA ĐIỂM (phục vụ Edge Case TC10 - địa điểm không tồn tại)
# ============================================================
# Bộ dữ liệu data/real/ tổng hợp theo VỊ TRÍ CÔNG VIỆC, không có chiều địa
# điểm -> không thể lọc thật theo tỉnh/thành. Nhưng vẫn PHẢI xác thực địa
# điểm người dùng nhập: nếu là địa danh không có thật thì báo lỗi rõ ràng,
# tuyệt đối không trả về kết quả toàn quốc như thể đã lọc.

_KNOWN_LOCATIONS = {
    # Toàn quốc / không giới hạn
    "việt nam", "viet nam", "vietnam", "toàn quốc", "toan quoc",
    "cả nước", "ca nuoc", "remote", "toàn cầu",
    # Các tỉnh/thành có thị trường IT
    "hà nội", "ha noi", "hanoi",
    "hồ chí minh", "ho chi minh", "tp hcm", "tphcm", "hcm",
    "sài gòn", "sai gon", "saigon",
    "đà nẵng", "da nang", "danang",
    "hải phòng", "hai phong",
    "cần thơ", "can tho",
    "bình dương", "binh duong",
    "đồng nai", "dong nai",
    "bắc ninh", "bac ninh",
    "huế", "hue", "thừa thiên huế",
    "nha trang", "khánh hòa", "khanh hoa",
    "vũng tàu", "vung tau", "bà rịa",
    "quảng ninh", "quang ninh", "hạ long",
    "thanh hóa", "thanh hoa", "nghệ an", "nghe an", "vinh",
}

# Tiền tố hành chính cần bỏ trước khi đối chiếu ("thành phố Hà Nội" -> "hà nội")
_LOCATION_PREFIXES = ("thành phố ", "thanh pho ", "tp. ", "tp.", "tp ",
                      "tỉnh ", "tinh ", "quận ", "huyện ")


def _clean_location(location: str) -> str:
    """Chuẩn hóa tên địa điểm: bỏ khoảng trắng thừa và tiền tố hành chính."""
    loc = " ".join(location.strip().lower().split())
    changed = True
    while changed:
        changed = False
        for p in _LOCATION_PREFIXES:
            if loc.startswith(p):
                loc = loc[len(p):].strip()
                changed = True
    return loc


def _is_known_location(location: str) -> bool:
    """True nếu địa điểm nằm trong danh sách tỉnh/thành được hỗ trợ."""
    return _clean_location(location) in _KNOWN_LOCATIONS


def search_jobs(keyword: str, location: str = "") -> str:
    """
    Tra cứu danh sách việc làm theo ngành nghề, kỹ năng và địa điểm.

    Args:
        keyword (str): Từ khóa ngành nghề hoặc kỹ năng (VD: 'Python', 'Data Science')
        location (str, optional): Địa điểm làm việc (VD: 'Hà Nội', 'Hồ Chí Minh'). Mặc định '' (cả nước).

    Returns:
        str: Danh sách tin tuyển dụng phù hợp kèm số lượng tin và kỹ năng yêu cầu.

    Error:
        - Trả về chuỗi báo lỗi nếu keyword rỗng.
        - Trả về chuỗi báo lỗi nếu location không phải tỉnh/thành được hỗ trợ.
        - Trả về chuỗi báo lỗi nếu không tìm thấy vị trí nào khớp keyword.
    """
    if not keyword or not keyword.strip():
        return "Vui lòng nhập từ khóa tìm kiếm."

    # 🛡️ Xác thực địa điểm TRƯỚC khi tra cứu (Edge Case TC10).
    # Địa danh không có thật -> báo lỗi ngay, không trả kết quả toàn quốc.
    if location and location.strip():
        if not _is_known_location(location):
            goi_y = "Hà Nội, TP.HCM, Đà Nẵng, Hải Phòng, Cần Thơ, Bình Dương"
            return (
                f"LỖI: Không tìm thấy dữ liệu tuyển dụng cho địa điểm '{location}'. "
                f"Địa điểm này không nằm trong danh sách được hỗ trợ. "
                f"Các địa điểm hợp lệ: {goi_y}. "
                f"Hoặc để trống địa điểm để tra cứu trên toàn quốc."
            )

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
            # Địa điểm hợp lệ nhưng dữ liệu không tách theo tỉnh/thành.
            # Nói rõ để Agent không hiểu nhầm là đã lọc theo địa điểm.
            lines.append(
                f"\n(Lưu ý: số liệu trên là tổng hợp TOÀN QUỐC. "
                f"Bộ dữ liệu chưa tách riêng theo địa điểm '{location}'.)"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Đã xảy ra lỗi khi tra cứu việc làm: {str(e)}"


def get_career_info(career_name: str) -> str:
    """
    Cung cấp thông tin tổng quan về một ngành nghề.

    Args:
        career_name (str): Tên ngành nghề (VD: 'Data Scientist', 'Backend Developer').

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
        domain (str): Lĩnh vực quan tâm (VD: 'Python', 'Machine Learning', 'Docker').

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
        career_name (str): Tên ngành nghề (VD: 'Software Engineer', 'Data Scientist').

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
    So sánh hai ngành nghề dựa trên nhiều tiêu chí từ dữ liệu thực tế.

    Args:
        career1 (str): Ngành thứ nhất (VD: 'Data Analyst').
        career2 (str): Ngành thứ hai (VD: 'Data Engineer').

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
    Tra cứu xu hướng thị trường lao động IT Việt Nam theo ngành.

    Args:
        industry (str): Tên ngành/lĩnh vực (VD: 'AI/ML', 'Cloud', 'Mobile', 'Backend').

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

    try:
        data = _load_roles()
        index_data = _load_index()
        roles = data.get("roles", {})
        ind_lower = industry.lower()

        # Domain keyword mapping
        domain_keywords = {
            "ai": ["AI Engineer", "Machine Learning Engineer", "Data Scientist", "NLP Engineer"],
            "ml": ["Machine Learning Engineer", "Data Scientist", "AI Engineer"],
            "data": ["Data Engineer", "Data Scientist", "Data Analyst", "Business Intelligence"],
            "backend": ["Backend Developer", "Java Developer", "Python Developer", "Node.js Developer"],
            "frontend": ["Frontend Developer", "React Developer", "Vue Developer", "Angular Developer"],
            "fullstack": ["Full-stack Developer", "MEAN Stack Developer", "MERN Stack Developer"],
            "mobile": ["Mobile Developer", "iOS Developer", "Android Developer", "Flutter Developer"],
            "devops": ["DevOps Engineer", "Cloud Engineer", "SRE Engineer", "Platform Engineer"],
            "cloud": ["Cloud Engineer", "AWS Engineer", "DevOps Engineer", "SRE Engineer"],
            "security": ["Security Engineer", "Penetration Tester", "SOC Analyst"],
        }

        # Tìm keyword phù hợp nhất
        matched_roles_names = []
        for kw, role_names in domain_keywords.items():
            if kw in ind_lower or ind_lower in kw:
                matched_roles_names = role_names
                break

        if not matched_roles_names:
            # Fallback: tìm tất cả roles có tên chứa keyword
            matched_roles_names = [r for r in roles if ind_lower in r.lower()][:10]

        if not matched_roles_names:
            available_domains = list(domain_keywords.keys())
            return _err(
                "not_found",
                f"Không có dữ liệu trend cho '{industry}'. "
                f"Các lĩnh vực có sẵn: {', '.join(available_domains)}"
            )

        # Thu thập stats cho các roles tìm được
        trends = []
        all_skills = {}
        for role_name in matched_roles_names:
            matched_key, _ = _normalize_role(role_name)
            if matched_key and matched_key in roles:
                rd = roles[matched_key]
                trends.append({
                    "role": matched_key,
                    "total_jds": rd.get("total_jds", 0),
                    "top_skill": rd["top_skills"][0]["skill"] if rd.get("top_skills") else "N/A"
                })
                for s in rd.get("top_skills", [])[:5]:
                    sk = s["skill"]
                    all_skills[sk] = all_skills.get(sk, 0) + 1

        trends.sort(key=lambda x: x["total_jds"], reverse=True)
        top_cross_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:8]

        total_jds = sum(t["total_jds"] for t in trends)
        index_stats = index_data.get("stats", {})

        return _ok({
            "industry": industry,
            "total_roles_found": len(trends),
            "total_jds_in_industry": total_jds,
            "market_share_of_total": f"{total_jds / max(index_stats.get('total_jds_analyzed', 2795), 1) * 100:.1f}%",
            "top_roles_by_demand": trends[:6],
            "most_demanded_cross_skills": [
                {"skill": sk, "appears_in_n_roles": count}
                for sk, count in top_cross_skills
            ],
            "data_summary": {
                "total_jds_in_dataset": index_stats.get("total_jds_analyzed", 2795),
                "total_roles_in_dataset": index_stats.get("total_roles", 77),
                "data_date": DATASET_VERSION
            }
        })

    except Exception as e:
        return _err("error", f"Lỗi hệ thống: {str(e)}", retryable=True)


# ============================================================
# TOOL REGISTRY — Agent dùng dict này để lookup và gọi tool
# ============================================================

AVAILABLE_TOOLS = {
    "search_jobs": search_jobs,
    "get_career_info": get_career_info,
    "get_skill_requirements": get_skill_requirements,
    "get_certifications": get_certifications,
    "get_career_path": get_career_path,
    "compare_careers": compare_careers,
    "get_market_trends": get_market_trends,
}
