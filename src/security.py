"""
🔒 SECURITY & GUARDRAILS MODULE
Input sanitization, prompt injection defense, PII masking, rate limiting.
Tích hợp vào pipeline TRƯỚC khi gọi LLM.
"""

import re
import hashlib
from collections import defaultdict
from time import time


# ============================================================
# G-01: INPUT SANITIZATION
# ============================================================

MAX_INPUT_LENGTH = 500

_PII_PATTERNS = {
    "email": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
    "phone_vn": (r"(\+84|0)(3[2-9]|5[6-9]|7[0-9]|8[0-9]|9[0-9])\d{7}", "[SDT]"),
    "cccd": (r"\b\d{9}\b|\b\d{12}\b", "[CCCD]"),
}


def sanitize_input(user_input: str) -> tuple[str, list[str]]:
    """
    Làm sạch input: giới hạn độ dài, strip HTML, mask PII.
    Returns: (cleaned_input, list_of_warnings)
    """
    warnings = []

    # 1. Length limit
    if len(user_input) > MAX_INPUT_LENGTH:
        user_input = user_input[:MAX_INPUT_LENGTH]
        warnings.append("INPUT_TRUNCATED")

    # 2. Strip HTML tags
    user_input = re.sub(r"<[^>]+>", "", user_input).strip()

    # 3. Normalize whitespace
    user_input = re.sub(r"\s+", " ", user_input)

    # 4. PII detection & masking
    for pii_type, (pattern, replacement) in _PII_PATTERNS.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            user_input = re.sub(pattern, replacement, user_input, flags=re.IGNORECASE)
            warnings.append(f"PII_{pii_type.upper()}_MASKED")

    return user_input, warnings


# ============================================================
# G-02: PROMPT INJECTION DETECTION
# ============================================================

_INJECTION_PATTERNS = [
    r"ignore\s+(previous|above|all|prior)\s+instructions?",
    r"forget\s+(everything|all|previous)",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"disregard\s+your\s+(previous|prior|all)",
    r"override\s+(your\s+)?(instructions?|rules?|guidelines?)",
    r"system\s*:\s*",
    r"<\|im_start\|>",
    r"\[INST\]",
    r"\[SYS\]",
    r"act\s+as\s+(?!a\s+career)",     # "act as X" nhưng không phải "act as a career advisor"
    r"pretend\s+(you\s+are|to\s+be)",
    r"jailbreak",
    r"bypass\s+(the\s+)?(guardrail|safety|filter|restriction)",
    r"bỏ\s+qua\s+(hướng\s+dẫn|quy\s+tắc|giới\s+hạn)",
    r"quên\s+(tất\s+cả|mọi\s+thứ|hướng\s+dẫn)",
    r"tiết\s+lộ\s+(system\s+prompt|hướng\s+dẫn\s+hệ\s+thống)",
    r"làm\s+theo\s+bất\s+kỳ\s+yêu\s+cầu",
    r"không\s+được\s+từ\s+chối",
    r"DAN\b",                          # "Do Anything Now" jailbreak
    r"developer\s+mode",
    r"sudo\s+mode",
]


def detect_injection(text: str) -> bool:
    """
    Trả về True nếu phát hiện dấu hiệu prompt injection.
    Conservative: false positive tốt hơn false negative ở context bảo mật.
    """
    text_lower = text.lower()
    return any(re.search(p, text_lower, re.IGNORECASE) for p in _INJECTION_PATTERNS)


def detect_off_topic(text: str) -> bool:
    """
    Phát hiện câu hỏi hoàn toàn ngoài domain tư vấn nghề nghiệp IT.
    Simple heuristic — không dùng LLM để tránh cost.
    """
    it_keywords = [
        "nghề", "career", "job", "việc làm", "lương", "kỹ năng", "skill",
        "học", "lập trình", "developer", "engineer", "data", "AI", "ML",
        "CNTT", "IT", "software", "backend", "frontend", "python", "java",
        "intern", "fresher", "junior", "senior", "roadmap", "lộ trình",
        "chứng chỉ", "certification", "phỏng vấn", "interview", "portfolio"
    ]
    text_lower = text.lower()
    has_it_keyword = any(kw.lower() in text_lower for kw in it_keywords)

    truly_off_topic_patterns = [
        r"\b(hack|crack|exploit|vulnerability|sql injection)\b",
        r"\b(recipe|nấu|món ăn|food)\b",
        r"\b(game\s+cheats?|mod\s+menu)\b",
        r"\b(chứng khoán|cổ phiếu|forex|trading)\b(?!.*career)",
    ]
    is_harmful = any(re.search(p, text_lower, re.IGNORECASE) for p in truly_off_topic_patterns)

    return is_harmful or (not has_it_keyword and len(text) > 30)


# ============================================================
# G-03: SALARY GUARANTEE DETECTION
# ============================================================

_GUARANTEE_TRIGGERS = [
    r"đảm\s+bảo.*lương",
    r"cam\s+kết.*lương",
    r"chắc\s+chắn.*\d+\s*(triệu|tr|M|million)",
    r"guarantee.*salary",
    r"lương\s+(chắc chắn|nhất định|đảm bảo)",
]

_SALARY_CLAIM_PATTERN = re.compile(
    r"\b\d[\d.,]*\s*(triệu|million|tr\b|M\b|usd|\$|vnđ)",
    re.IGNORECASE
)


def detect_salary_guarantee_request(text: str) -> bool:
    """Phát hiện yêu cầu ép cam kết lương."""
    return any(re.search(p, text.lower(), re.IGNORECASE) for p in _GUARANTEE_TRIGGERS)


def check_response_grounding(response: str, observations: list[str]) -> dict:
    """
    Kiểm tra xem response có claim số liệu nào không có trong observations không.
    Returns: {"grounded": bool, "ungrounded_claims": list}
    """
    ungrounded = []
    all_obs_text = " ".join(observations).lower()

    for match in _SALARY_CLAIM_PATTERN.finditer(response):
        claim = match.group(0).strip()
        if claim.lower() not in all_obs_text:
            # Số liệu trong response không xuất hiện trong bất kỳ Observation nào
            ungrounded.append({"type": "salary_claim", "value": claim})

    return {
        "grounded": len(ungrounded) == 0,
        "ungrounded_claims": ungrounded
    }


# ============================================================
# G-04: RATE LIMITER
# ============================================================

class RateLimiter:
    """
    In-memory rate limiter theo session.
    Production: thay bằng Redis để support multi-instance.
    """
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def allow(self, session_id: str) -> bool:
        now = time()
        # Xóa requests cũ ngoài cửa sổ thời gian
        self._requests[session_id] = [
            t for t in self._requests[session_id] if now - t < self.window
        ]
        if len(self._requests[session_id]) >= self.max_requests:
            return False
        self._requests[session_id].append(now)
        return True

    def remaining(self, session_id: str) -> int:
        now = time()
        active = [t for t in self._requests[session_id] if now - t < self.window]
        return max(0, self.max_requests - len(active))


# ============================================================
# G-05: SESSION ID GENERATOR (không lưu PII)
# ============================================================

def make_session_id(user_hint: str = "") -> str:
    """Tạo session ID ẩn danh — không lưu thông tin cá nhân."""
    raw = f"{user_hint}-{time()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# Singleton rate limiter cho toàn app
_rate_limiter = RateLimiter(max_requests=15, window_seconds=60)


def get_rate_limiter() -> RateLimiter:
    return _rate_limiter
