# 📋 Tool Contracts — EduPath Career Advisor
**Version 2.0 | Tất cả 7 tools | Dataset version: 2026-06-11**

---

## Error Envelope Schema (chuẩn cho tất cả tools)

Mọi tool đều trả về **JSON string** với envelope sau:

```json
{
  "status": "success | not_found | invalid_input | loop_detected | error",
  "data": { ... },
  "error": null,
  "source": "ITviec & TopDev Vietnam 2025",
  "dataset_version": "2026-06-11",
  "retryable": false
}
```

**Agent rules when reading Observation:**
- `status == "success"` → dùng `data` để trả lời
- `status == "not_found"` → báo người dùng không có trong dataset, gợi ý alternatives (trong `error`)
- `status == "invalid_input"` → KHÔNG thử lại với cùng params, hỏi lại người dùng
- `status == "error"` + `retryable: true` → có thể thử lại 1 lần
- `status == "loop_detected"` → dừng ngay, chuyển sang Final Answer với thông tin đã có

---

## Tool 1: `search_jobs(keyword, location)`

**Mô tả**: Tra cứu roles phù hợp với keyword (tên ngành/kỹ năng) và địa điểm  
**Sử dụng khi**: Người dùng hỏi về cơ hội việc làm theo ngành/skill/địa điểm  
**Không dùng khi**: Câu hỏi là định nghĩa khái niệm

| Param | Type | Bắt buộc | Ví dụ | Validation |
|---|---|---|---|---|
| keyword | string | ✅ | `"Python Developer"` | max 100 chars, non-empty |
| location | string | ❌ | `"Hà Nội"` | max 50 chars, default = "Toàn quốc" |

**Success output:**
```json
{
  "status": "success",
  "data": {
    "keyword": "Python",
    "location": "Hà Nội",
    "total_matching_roles": 5,
    "results": [
      {
        "role": "Backend Developer",
        "total_jds": 552,
        "top_required_skills": ["Java", "Docker", "MySQL"],
        "location_note": "Hà Nội"
      }
    ],
    "note": "Dữ liệu từ 77 roles, 2795 JDs phân tích"
  },
  "dataset_version": "2026-06-11"
}
```

**Failure modes:**
1. `not_found`: Không có role nào khớp keyword → gợi ý thử tên role cụ thể hơn
2. `invalid_input`: keyword rỗng → KHÔNG retry, hỏi lại người dùng

---

## Tool 2: `get_career_info(career_name)`

**Mô tả**: Tổng quan về một ngành: JD count, market demand, top skills  
**Sử dụng khi**: Người dùng muốn biết tổng quan về một ngành nghề

| Param | Type | Bắt buộc | Ví dụ |
|---|---|---|---|
| career_name | string | ✅ | `"Data Scientist"` |

**Success output:**
```json
{
  "status": "success",
  "data": {
    "role": "Data Scientist",
    "total_jds_analyzed": 147,
    "market_demand": "medium",
    "must_have_skills": [
      {"skill": "Python", "frequency": "87.1%", "category": "language"}
    ],
    "should_have_skills": [...],
    "description": "Role Data Scientist có 147 tin..."
  }
}
```

**Failure modes:**
1. `not_found`: Role không có → error message chứa suggestions từ fuzzy match
2. Fuzzy match logic: "data sci" → matches "Data Scientist"

---

## Tool 3: `get_skill_requirements(role)`

**Mô tả**: Danh sách kỹ năng must_have / should_have / nice_to_have với tần suất từ JDs thực  
**Sử dụng khi**: Cần skill gap analysis, interview prep, learning plan

| Priority | Threshold | Ý nghĩa |
|---|---|---|
| `must_have` | >60% JDs | Thiếu là out ngay |
| `should_have` | 30-60% JDs | Nên có để cạnh tranh |
| `nice_to_have` | <30% JDs | Điểm cộng |

**Success output:**
```json
{
  "status": "success",
  "data": {
    "role": "Backend Developer",
    "total_jds_analyzed": 552,
    "must_have": [
      {"skill": "Java", "frequency_percent": 43.7, "category": "language"}
    ],
    "should_have": [...],
    "nice_to_have": [...]
  }
}
```

**Failure modes:**
1. `not_found` + suggestions: "backend dev" → không tìm thấy → suggestions: ["Backend Developer", "Java Backend Developer"]
2. `invalid_input`: role name rỗng

---

## Tool 4: `get_certifications(domain)`

**Mô tả**: Danh sách resource học tập (khóa học, tutorial, docs) theo lĩnh vực  
**Sử dụng khi**: Người dùng hỏi về chứng chỉ hoặc tài nguyên học cụ thể

| Param | Ví dụ | Ghi chú |
|---|---|---|
| domain | `"Python"`, `"Machine Learning"`, `"Docker"` | Tên skill/lĩnh vực |

**Success output:**
```json
{
  "status": "success",
  "data": {
    "domain": "Python",
    "total_resources": 10,
    "free_resources": [
      {
        "title": "freeCodeCamp Python",
        "url": "https://...",
        "type": "course",
        "level": "beginner",
        "duration_hours": 40,
        "rating": 5,
        "best_for": "Beginners wanting structured path"
      }
    ],
    "paid_resources": [...]
  }
}
```

**Available domains**: python, react, javascript, java, docker, git, typescript, postgresql, sql, node_js, ...  
**Failure modes**: `not_found` với list available domains

---

## Tool 5: `get_career_path(career_name)`

**Mô tả**: Lộ trình thăng tiến từ Intern → Fresher → Junior → Senior → Lead  
**Sử dụng khi**: Người dùng hỏi về timeline career hoặc cần lộ trình học

**Success output:**
```json
{
  "status": "success",
  "data": {
    "career": "Software Engineer",
    "career_levels": [
      {"level": "Intern/Fresher", "years_experience": "0-1 năm", "focus": "Học nền tảng..."},
      {"level": "Junior", "years_experience": "1-2 năm", "focus": "Lead feature nhỏ..."},
      ...
    ],
    "role_market_info": {
      "role": "Software Engineer",
      "key_skills_to_master": ["Java", "Docker", "..."],
      "total_jds": 400
    },
    "note": "Thời gian có thể rút ngắn tùy năng lực cá nhân..."
  }
}
```

**QUAN TRỌNG**: Tool này KHÔNG cam kết timeline — luôn có note "tùy năng lực cá nhân"

---

## Tool 6: `compare_careers(career1, career2)`

**Mô tả**: So sánh hai ngành về JD count, skills, market demand  
**Sử dụng khi**: Người dùng phân vân giữa 2 hướng nghề nghiệp

| Param | Bắt buộc | Ví dụ |
|---|---|---|
| career1 | ✅ | `"Data Analyst"` |
| career2 | ✅ | `"Data Engineer"` |

**Success output:**
```json
{
  "status": "success",
  "data": {
    "Data Analyst": {
      "total_jds": 89,
      "market_demand": "medium",
      "must_have_skills": ["Python", "SQL", "Excel"],
      "top_skill": "Python",
      "top_skill_frequency": "78.5%"
    },
    "Data Engineer": {
      "total_jds": 134,
      "market_demand": "high",
      "must_have_skills": ["Python", "SQL", "Spark"]
    },
    "comparison_summary": {
      "more_jds": "Data Engineer",
      "jd_ratio": "89 vs 134",
      "shared_skills": ["Python", "SQL"]
    },
    "recommendation_note": "Chọn dựa trên sở thích cá nhân..."
  }
}
```

**Failure modes:**
1. `not_found` với danh sách suggestions cho mỗi role không tìm thấy
2. `invalid_input`: thiếu 1 trong 2 tên role

---

## Tool 7: `get_market_trends(industry)`

**Mô tả**: Xu hướng thị trường IT VN — top roles theo JD count, cross-skills  
**Sử dụng khi**: Người dùng hỏi ngành IT nào đang hot, ngành nào nhiều việc

| Param | Ví dụ lĩnh vực | Keyword mapping |
|---|---|---|
| industry | `"AI/ML"` | → AI Engineer, ML Engineer, Data Scientist |
| industry | `"Backend"` | → Backend Developer, Java Developer, Python Developer |
| industry | `"Frontend"` | → Frontend Developer, React Developer, ... |
| industry | `"DevOps"` | → DevOps Engineer, Cloud Engineer, SRE |
| industry | `"Mobile"` | → Mobile Developer, iOS, Android, Flutter |
| industry | `"Data"` | → Data Engineer, Data Scientist, Data Analyst |
| industry | `"Security"` | → Security Engineer, Penetration Tester, SOC |

**Success output:**
```json
{
  "status": "success",
  "data": {
    "industry": "AI/ML",
    "total_roles_found": 4,
    "total_jds_in_industry": 392,
    "market_share_of_total": "14.0%",
    "top_roles_by_demand": [
      {"role": "AI Engineer", "total_jds": 145, "top_skill": "Python"},
      {"role": "Data Scientist", "total_jds": 147, "top_skill": "Python"}
    ],
    "most_demanded_cross_skills": [
      {"skill": "Python", "appears_in_n_roles": 4},
      {"skill": "Machine Learning", "appears_in_n_roles": 3}
    ],
    "data_summary": {
      "total_jds_in_dataset": 2795,
      "total_roles_in_dataset": 77,
      "data_date": "2026-06-11"
    }
  }
}
```

**Failure modes:**
1. `not_found` với list available industry keywords

---

## Versioning Policy

- `dataset_version: "2026-06-11"` là constant trong mọi tool output
- Khi dataset được cập nhật, bump version string này và update `data/real/index.json`
- Agent PHẢI cite version trong Final Answer: *"Theo dữ liệu ITviec VN 2025 (v2026-06-11)..."*

---

## Anti-patterns (NEVER DO in tools)

```python
# ❌ Raise exception — làm crash Agent loop
raise ValueError("Role not found")

# ❌ Return None hoặc empty string
return None

# ❌ Return không có status
return json.dumps({"skills": [...]})

# ✅ ĐÚNG — Luôn dùng _ok() hoặc _err()
return _err("not_found", "Role 'X' không có trong dataset. Gợi ý: ...")
return _ok({"role": ..., "skills": ...})
```
