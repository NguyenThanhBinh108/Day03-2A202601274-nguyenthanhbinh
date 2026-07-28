"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
Chủ đề: Chatbot Định Hướng Sự Nghiệp (Career Orientation)
Dataset: ITviec & TopDev Vietnam IT Market Report 2025 (version 2026-06-11)
"""

import json
import os
import re

# ============================================================
# DATA LOADING — Lazy load để tránh overhead khi import
# ============================================================

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BASE_DIR, "data", "real")

_ROLES_DATA = None
_INDEX_DATA = None
_RESOURCES_CACHE = {}

DATASET_VERSION = "2026-06-11"
DATASET_SOURCE = "ITviec & TopDev Vietnam 2025"


def _load_roles() -> dict:
    global _ROLES_DATA
    if _ROLES_DATA is None:
        path = os.path.join(_DATA_DIR, "career_maps", "all_roles.json")
        with open(path, encoding="utf-8") as f:
            _ROLES_DATA = json.load(f)
    return _ROLES_DATA


def _load_index() -> dict:
    global _INDEX_DATA
    if _INDEX_DATA is None:
        path = os.path.join(_DATA_DIR, "index.json")
        with open(path, encoding="utf-8") as f:
            _INDEX_DATA = json.load(f)
    return _INDEX_DATA


def _load_resource(skill_key: str) -> dict | None:
    if skill_key not in _RESOURCES_CACHE:
        path = os.path.join(_DATA_DIR, "resources", f"{skill_key}_resources.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                _RESOURCES_CACHE[skill_key] = json.load(f)
        else:
            _RESOURCES_CACHE[skill_key] = None
    return _RESOURCES_CACHE[skill_key]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _ok(data: dict | list | str, source: str = DATASET_SOURCE) -> str:
    """Chuẩn envelope thành công — luôn kèm dataset_version."""
    return json.dumps({
        "status": "success",
        "data": data,
        "error": None,
        "source": source,
        "dataset_version": DATASET_VERSION,
        "retryable": False
    }, ensure_ascii=False, indent=2)


def _err(code: str, msg: str, retryable: bool = False) -> str:
    """Chuẩn envelope lỗi — Agent đọc status để biết phải làm gì."""
    return json.dumps({
        "status": code,
        "data": None,
        "error": msg,
        "source": DATASET_SOURCE,
        "dataset_version": DATASET_VERSION,
        "retryable": retryable
    }, ensure_ascii=False)


def _normalize_role(role: str) -> tuple[str | None, list[str]]:
    """
    Tìm role chính xác hoặc gợi ý role tương tự.
    Returns: (matched_role_key, suggestions)
    """
    data = _load_roles()
    roles = data.get("roles", {})

    # Exact match (case-insensitive)
    for key in roles:
        if key.lower() == role.lower():
            return key, []

    # Partial match
    role_lower = role.lower()
    suggestions = [k for k in roles if role_lower in k.lower() or k.lower() in role_lower]
    if suggestions:
        return None, suggestions[:5]

    # Keyword match
    keywords = re.split(r"[\s/_-]+", role_lower)
    keyword_matches = [k for k in roles if any(kw in k.lower() for kw in keywords if len(kw) > 2)]
    return None, keyword_matches[:5]


def _sanitize_param(value: str, max_len: int = 100) -> str:
    """Strip HTML tags và giới hạn độ dài tham số tool."""
    value = re.sub(r"<[^>]+>", "", str(value)).strip()
    return value[:max_len]


# ============================================================
# MỐC 2: 7 TOOLS IMPLEMENTATION — Kết nối với data/real/
# ============================================================

def search_jobs(keyword: str, location: str = "") -> str:
    """
    Tra cứu danh sách việc làm theo ngành nghề, kỹ năng và địa điểm.

    Args:
        keyword (str): Từ khóa ngành nghề hoặc kỹ năng (VD: 'Python', 'Data Science')
        location (str, optional): Địa điểm làm việc (VD: 'Hà Nội', 'Hồ Chí Minh'). Mặc định '' (cả nước).

    Returns:
        str: JSON envelope với danh sách role phù hợp và kỹ năng yêu cầu.

    Error codes:
        - not_found: Không có role nào khớp với keyword
        - invalid_input: Keyword rỗng hoặc không hợp lệ
    """
    keyword = _sanitize_param(keyword)
    location = _sanitize_param(location, 50)

    if not keyword:
        return _err("invalid_input", "Keyword không được để trống.")

    try:
        data = _load_roles()
        roles = data.get("roles", {})
        kw_lower = keyword.lower()

        # Tìm các role có top_skills chứa keyword
        matched = []
        for role_name, role_data in roles.items():
            skills_in_role = [s["skill"].lower() for s in role_data.get("top_skills", [])]
            if kw_lower in role_name.lower() or any(kw_lower in s for s in skills_in_role):
                top3 = role_data.get("top_skills", [])[:3]
                matched.append({
                    "role": role_name,
                    "total_jds": role_data.get("total_jds", 0),
                    "top_required_skills": [s["skill"] for s in top3],
                    "location_note": location if location else "Toàn quốc"
                })

        if not matched:
            return _err(
                "not_found",
                f"Không tìm thấy tin tuyển dụng cho '{keyword}'"
                + (f" tại '{location}'" if location else "")
                + f". Gợi ý: thử từ khóa khác như tên role (Backend Developer, Data Scientist...)"
            )

        # Sắp xếp theo số JDs giảm dần
        matched.sort(key=lambda x: x["total_jds"], reverse=True)
        return _ok({
            "keyword": keyword,
            "location": location or "Toàn quốc",
            "total_matching_roles": len(matched),
            "results": matched[:10],
            "note": f"Dữ liệu từ {data.get('total_roles', 0)} roles, {sum(r['total_jds'] for r in matched)} JDs phân tích"
        })

    except Exception as e:
        return _err("error", f"Lỗi hệ thống khi tìm kiếm: {str(e)}", retryable=True)


def get_career_info(career_name: str) -> str:
    """
    Cung cấp thông tin tổng quan về một ngành nghề.

    Args:
        career_name (str): Tên ngành nghề (VD: 'Data Scientist', 'Backend Developer').

    Returns:
        str: JSON envelope với mô tả ngành, số JDs, top skills, market demand.

    Error codes:
        - not_found: Ngành nghề không có trong dataset
        - invalid_input: Tên ngành rỗng
    """
    career_name = _sanitize_param(career_name)
    if not career_name:
        return _err("invalid_input", "Tên ngành nghề không được để trống.")

    try:
        matched_key, suggestions = _normalize_role(career_name)

        if not matched_key:
            suggestion_str = ", ".join(suggestions) if suggestions else "Không tìm thấy role tương tự"
            return _err(
                "not_found",
                f"Ngành '{career_name}' không có trong dataset. "
                f"Các ngành tương tự: {suggestion_str}"
            )

        data = _load_roles()
        role_data = data["roles"][matched_key]
        index_data = _load_index()

        # Tìm thêm thông tin từ index nếu có
        index_role = next((r for r in index_data.get("roles", []) if r["role"] == matched_key), {})

        top_skills = role_data.get("top_skills", [])
        must_have = [s for s in top_skills if s.get("priority") in ("must_have",)]
        should_have = [s for s in top_skills if s.get("priority") == "should_have"]

        return _ok({
            "role": matched_key,
            "total_jds_analyzed": role_data.get("total_jds", 0),
            "market_demand": "high" if role_data.get("total_jds", 0) > 200 else "medium",
            "must_have_skills": [
                {"skill": s["skill"], "frequency": f"{s['frequency_percent']}%", "category": s.get("category", "")}
                for s in must_have[:5]
            ],
            "should_have_skills": [
                {"skill": s["skill"], "frequency": f"{s['frequency_percent']}%"}
                for s in should_have[:5]
            ],
            "top_skills_from_index": index_role.get("top_skills", [])[:5],
            "description": f"Role {matched_key} có {role_data.get('total_jds', 0)} tin tuyển dụng thực tế được phân tích từ ITviec & TopDev VN."
        })

    except Exception as e:
        return _err("error", f"Lỗi hệ thống: {str(e)}", retryable=True)


def get_skill_requirements(role: str) -> str:
    """
    Liệt kê các kỹ năng cần thiết cho một vị trí công việc.

    Args:
        role (str): Tên vị trí công việc (VD: 'Frontend Developer', 'AI Engineer').

    Returns:
        str: JSON envelope với danh sách must_have/should_have/nice_to_have skills kèm frequency từ JDs thực tế.

    Error codes:
        - not_found: Role không có trong dataset, kèm gợi ý role tương tự
        - invalid_input: Tên role rỗng
    """
    role = _sanitize_param(role)
    if not role:
        return _err("invalid_input", "Tên role không được để trống.")

    try:
        matched_key, suggestions = _normalize_role(role)

        if not matched_key:
            suggestion_str = ", ".join(suggestions) if suggestions else "Không tìm thấy"
            return _err(
                "not_found",
                f"Role '{role}' không có trong dataset (version {DATASET_VERSION}). "
                f"Các role tương tự: {suggestion_str}"
            )

        data = _load_roles()
        role_data = data["roles"][matched_key]
        top_skills = role_data.get("top_skills", [])

        must_have = [s for s in top_skills if s.get("priority") == "must_have"]
        should_have = [s for s in top_skills if s.get("priority") == "should_have"]
        nice_to_have = [s for s in top_skills if s.get("priority") == "nice_to_have"]

        return _ok({
            "role": matched_key,
            "total_jds_analyzed": role_data.get("total_jds", 0),
            "must_have": [
                {
                    "skill": s["skill"],
                    "frequency_percent": s["frequency_percent"],
                    "category": s.get("category", "")
                } for s in must_have
            ],
            "should_have": [
                {
                    "skill": s["skill"],
                    "frequency_percent": s["frequency_percent"],
                    "category": s.get("category", "")
                } for s in should_have[:8]
            ],
            "nice_to_have": [
                {
                    "skill": s["skill"],
                    "frequency_percent": s["frequency_percent"]
                } for s in nice_to_have[:5]
            ],
            "interpretation": (
                f"must_have = xuất hiện trong >60% JDs; "
                f"should_have = 30-60% JDs; "
                f"nice_to_have = <30% JDs"
            )
        })

    except Exception as e:
        return _err("error", f"Lỗi hệ thống: {str(e)}", retryable=True)


def get_certifications(domain: str) -> str:
    """
    Đề xuất chứng chỉ chuyên môn và khóa học theo lĩnh vực.

    Args:
        domain (str): Lĩnh vực quan tâm (VD: 'Python', 'Machine Learning', 'Docker').

    Returns:
        str: JSON envelope với danh sách resource có is_free, duration_hours, rating, url.

    Error codes:
        - not_found: Không có resource cho lĩnh vực này
        - invalid_input: Tên lĩnh vực rỗng
    """
    domain = _sanitize_param(domain)
    if not domain:
        return _err("invalid_input", "Tên lĩnh vực không được để trống.")

    try:
        # Tìm file resource khớp (fuzzy)
        resources_dir = os.path.join(_DATA_DIR, "resources")
        domain_key = domain.lower().replace(" ", "_").replace("/", "_").replace("-", "_")

        # Thử tìm file khớp
        found_path = None
        found_key = None
        if os.path.exists(resources_dir):
            for fname in os.listdir(resources_dir):
                if fname.endswith("_resources.json"):
                    fkey = fname.replace("_resources.json", "")
                    if domain_key in fkey or fkey in domain_key:
                        found_path = os.path.join(resources_dir, fname)
                        found_key = fkey
                        break

        if not found_path:
            # List available domains
            available = []
            if os.path.exists(resources_dir):
                available = [f.replace("_resources.json", "")
                             for f in os.listdir(resources_dir)
                             if f.endswith("_resources.json")]
            return _err(
                "not_found",
                f"Không có resource cho '{domain}'. "
                f"Các lĩnh vực có sẵn: {', '.join(available[:10])}"
            )

        with open(found_path, encoding="utf-8") as f:
            res_data = json.load(f)

        resources = res_data.get("resources", [])
        free_resources = [r for r in resources if r.get("is_free", False)]
        paid_resources = [r for r in resources if not r.get("is_free", True)]

        return _ok({
            "domain": res_data.get("skill", domain),
            "total_resources": res_data.get("total_resources", len(resources)),
            "free_resources": [
                {
                    "title": r["title"],
                    "url": r.get("url", ""),
                    "type": r.get("type", ""),
                    "level": r.get("level", ""),
                    "duration_hours": r.get("duration_hours"),
                    "rating": r.get("rating"),
                    "best_for": r.get("best_for", "")
                } for r in free_resources[:5]
            ],
            "paid_resources": [
                {
                    "title": r["title"],
                    "url": r.get("url", ""),
                    "level": r.get("level", ""),
                    "duration_hours": r.get("duration_hours"),
                    "rating": r.get("rating")
                } for r in paid_resources[:3]
            ]
        })

    except Exception as e:
        return _err("error", f"Lỗi hệ thống: {str(e)}", retryable=True)


def get_career_path(career_name: str) -> str:
    """
    Mô tả lộ trình thăng tiến trong một ngành nghề.

    Args:
        career_name (str): Tên ngành nghề (VD: 'Software Engineer', 'Data Scientist').

    Returns:
        str: JSON envelope với các cấp bậc, thời gian trung bình, kỹ năng cần phát triển.

    Error codes:
        - not_found: Không có template cho ngành này
        - invalid_input: Tên ngành rỗng
    """
    career_name = _sanitize_param(career_name)
    if not career_name:
        return _err("invalid_input", "Tên ngành nghề không được để trống.")

    try:
        templates_dir = os.path.join(_DATA_DIR, "schedule_templates")
        career_key = career_name.lower().replace(" ", "_")

        found_path = None
        if os.path.exists(templates_dir):
            for fname in os.listdir(templates_dir):
                fkey = fname.replace(".json", "").replace("_schedule", "")
                if career_key in fkey or fkey in career_key:
                    found_path = os.path.join(templates_dir, fname)
                    break

        # Fallback: kiểm tra all_roles.json
        matched_key, suggestions = _normalize_role(career_name)

        if not found_path and not matched_key:
            suggestion_str = ", ".join(suggestions) if suggestions else "Không tìm thấy"
            return _err(
                "not_found",
                f"Không có lộ trình cho '{career_name}'. "
                f"Các ngành tương tự trong dataset: {suggestion_str}"
            )

        # Trả về thông tin cấp bậc từ dataset nếu có
        career_levels = [
            {"level": "Intern/Fresher", "years_experience": "0-1 năm", "focus": "Học nền tảng, thực hành project nhỏ"},
            {"level": "Junior", "years_experience": "1-2 năm", "focus": "Làm việc độc lập task medium, fix bug, code review"},
            {"level": "Mid-level", "years_experience": "2-4 năm", "focus": "Lead feature, mentor junior, thiết kế module"},
            {"level": "Senior", "years_experience": "4-7 năm", "focus": "Architect solution, technical leadership, cross-team"},
            {"level": "Lead/Manager", "years_experience": "7+ năm", "focus": "Team building, strategy, business impact"}
        ]

        role_info = {}
        if matched_key:
            data = _load_roles()
            role_data = data["roles"][matched_key]
            top_skills = [s["skill"] for s in role_data.get("top_skills", [])[:5]]
            role_info = {
                "role": matched_key,
                "key_skills_to_master": top_skills,
                "total_jds": role_data.get("total_jds", 0)
            }

        return _ok({
            "career": career_name,
            "career_levels": career_levels,
            "role_market_info": role_info,
            "note": "Thời gian có thể rút ngắn tùy năng lực cá nhân và loại công ty (startup vs enterprise).",
            "schedule_template_available": found_path is not None
        })

    except Exception as e:
        return _err("error", f"Lỗi hệ thống: {str(e)}", retryable=True)


def compare_careers(career1: str, career2: str) -> str:
    """
    So sánh hai ngành nghề dựa trên nhiều tiêu chí từ dữ liệu thực tế.

    Args:
        career1 (str): Ngành thứ nhất (VD: 'Data Analyst').
        career2 (str): Ngành thứ hai (VD: 'Data Engineer').

    Returns:
        str: JSON envelope với bảng so sánh JD count, skills, market demand.

    Error codes:
        - not_found: Một hoặc cả hai ngành không có trong dataset
        - invalid_input: Thiếu tên ngành
    """
    career1 = _sanitize_param(career1)
    career2 = _sanitize_param(career2)

    if not career1 or not career2:
        return _err("invalid_input", "Cần cung cấp tên của cả hai ngành nghề.")

    try:
        key1, sug1 = _normalize_role(career1)
        key2, sug2 = _normalize_role(career2)

        errors = []
        if not key1:
            errors.append(f"'{career1}' không tìm thấy. Gợi ý: {', '.join(sug1[:3])}")
        if not key2:
            errors.append(f"'{career2}' không tìm thấy. Gợi ý: {', '.join(sug2[:3])}")
        if errors:
            return _err("not_found", " | ".join(errors))

        data = _load_roles()
        r1 = data["roles"][key1]
        r2 = data["roles"][key2]

        def summarize(role_data: dict) -> dict:
            skills = role_data.get("top_skills", [])
            must = [s["skill"] for s in skills if s.get("priority") == "must_have"]
            should = [s["skill"] for s in skills if s.get("priority") == "should_have"][:4]
            return {
                "total_jds": role_data.get("total_jds", 0),
                "market_demand": "high" if role_data.get("total_jds", 0) > 200 else "medium",
                "must_have_skills": must,
                "should_have_skills": should,
                "top_skill": skills[0]["skill"] if skills else "N/A",
                "top_skill_frequency": f"{skills[0]['frequency_percent']}%" if skills else "N/A"
            }

        comparison = {
            key1: summarize(r1),
            key2: summarize(r2),
            "comparison_summary": {
                "more_jds": key1 if r1.get("total_jds", 0) >= r2.get("total_jds", 0) else key2,
                "jd_ratio": f"{r1.get('total_jds',0)} vs {r2.get('total_jds',0)}",
                "shared_skills": list(
                    set(s["skill"] for s in r1.get("top_skills", [])[:10]) &
                    set(s["skill"] for s in r2.get("top_skills", [])[:10])
                )
            },
            "recommendation_note": "Chọn dựa trên sở thích cá nhân và background hiện có. Dữ liệu JDs phản ánh nhu cầu thị trường VN 2025."
        }

        return _ok(comparison)

    except Exception as e:
        return _err("error", f"Lỗi hệ thống: {str(e)}", retryable=True)


def get_market_trends(industry: str) -> str:
    """
    Tra cứu xu hướng thị trường lao động IT Việt Nam theo ngành.

    Args:
        industry (str): Tên ngành/lĩnh vực (VD: 'AI/ML', 'Cloud', 'Mobile', 'Backend').

    Returns:
        str: JSON envelope với top roles, JD counts, top skills đang được yêu cầu nhiều nhất.

    Error codes:
        - not_found: Không có dữ liệu cho ngành này
        - invalid_input: Tên ngành rỗng
    """
    industry = _sanitize_param(industry)
    if not industry:
        return _err("invalid_input", "Tên ngành không được để trống.")

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
