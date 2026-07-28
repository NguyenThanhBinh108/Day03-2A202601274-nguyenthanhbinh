# 🏗️ Architecture — EduPath Career Advisor
**Version 2.0 | Production-ready | Dataset: ITviec & TopDev VN 2025**

---

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                              │
│          (chat message, max 500 chars, UTF-8)                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYER  (src/security.py)            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. Rate Limiter    (15 req/min per session)             │    │
│  │ 2. Input Sanitizer (strip HTML, mask PII, limit length) │    │
│  │ 3. Injection Detector (20+ regex patterns EN+VI)        │    │
│  │ 4. Off-topic Classifier (keyword + pattern heuristics)  │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                BLOCKED?     │ PASS                              │
│          ┌──────────────────┤                                    │
│          ▼                  ▼                                    │
│   ADVERSARIAL_RESPONSE   Continue                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTENT ROUTER  (src/app.py)                  │
│  Simple keyword + context heuristics (no extra LLM call)       │
│                                                                 │
│  ┌─────────────┬──────────────────┬──────────────┐             │
│  │  Simple/FAQ │  Skill Gap /     │  Missing     │             │
│  │  Concept    │  Roadmap /       │  Info        │             │
│  │  Explanation│  Market Research │              │             │
│  └──────┬──────┴────────┬─────────┴──────┬───────┘             │
└─────────┼───────────────┼────────────────┼─────────────────────┘
          │               │                │
          ▼               ▼                ▼
   ┌─────────────┐ ┌──────────────┐ ┌─────────────┐
   │  RETRIEVAL  │ │  REACT AGENT │ │ CLARIFY     │
   │  CHATBOT    │ │  LOOP        │ │ FLOW        │
   │ (LLM only)  │ │              │ │             │
   └──────┬──────┘ └──────┬───────┘ └──────┬──────┘
          │               │                │
          │        ┌──────▼───────┐        │
          │        │ TOOL REGISTRY│        │
          │        │ (src/tools.py│        │
          │        │  7 tools)    │        │
          │        └──────┬───────┘        │
          │               │                │
          │        ┌──────▼───────┐        │
          │        │  DATA LAYER  │        │
          │        │ data/real/   │        │
          │        │ (77 roles,   │        │
          │        │  2795 JDs,   │        │
          │        │  92 skills)  │        │
          │        └──────┬───────┘        │
          │               │                │
          ▼               ▼                ▼
     ┌─────────────────────────────────────────┐
     │            RESPONSE VALIDATOR           │
     │  - Grounding check (no hallucinated #s) │
     │  - Salary guarantee detection           │
     │  - dataset_version citation required    │
     └──────────────────────┬──────────────────┘
                            │
                            ▼
                   FINAL RESPONSE + TRACE LOG
```

---

## 2. ReAct Loop State Machine

```
START → [SECURITY_CHECK] →→ BLOCKED → ADVERSARIAL_RESPONSE
                ↓ PASS
        [STEP = 1]
                ↓
        [LLM CALL] ← system_prompt = REACT_SYSTEM_PROMPT
                ↓
        Parse LLM output
                ↓
        ┌────────────────────────────────────────────────┐
        │  Contains "Final Answer:" ?                    │
        │  YES → extract_final_answer()                  │
        │       → check_response_grounding()             │
        │       → RETURN success + trace                 │
        │                                                │
        │  Contains "Action:" ?                          │
        │  YES → parse_action() → action_name, args      │
        │       → Duplicate action? → ERROR:loop_detected│
        │       → safe_execute_tool(name, args)          │
        │       → OBSERVATION (from data/real/)          │
        │       → Append to conversation history         │
        │       → STEP++                                 │
        │                                                │
        │  Neither? → step++ (malformed output)          │
        └────────────────────────────────────────────────┘
                ↓
        STEP > MAX_ITERATIONS (5)?
        YES → SAFE_FALLBACK_MESSAGE
        NO  → Loop back to [LLM CALL]
```

---

## 3. Component Inventory

| Component | File | Role Owner | Status |
|---|---|---|---|
| Intent Router + ReAct Loop | `src/app.py` | Role 4 | ✅ v2.0 |
| Tool Registry + Data Layer | `src/tools.py` | Role 2 | ✅ v2.0 — 7 tools connected to data/real/ |
| System Prompts + Constants | `src/prompts.py` | Role 3 | ✅ v2.0 — 7 career tools, MAX_ITERATIONS=5 |
| Security Module | `src/security.py` | Role 3+4 | ✅ v2.0 — NEW |
| LLM Provider Adapter | `src/providers.py` | Role 4 | ✅ 4 providers + smart MockProvider |
| Career Maps Dataset | `data/real/career_maps/all_roles.json` | Data | ✅ 77 roles, 2795 JDs |
| Skills Ontology | `data/real/skill_ontology.json` | Data | ✅ 92 skills, prerequisites |
| Schedule Templates | `data/real/schedule_templates/` | Data | ✅ 19 role schedules |
| Resources | `data/real/resources/` | Data | ✅ 23 skill resource files |
| Question Bank | `data/real/question_bank/` | Data | ✅ 83 tech interview Q&A files |
| Test Cases | `config/test_cases.json` | Role 1 | ✅ 20 TCs, all 7 tools covered |
| Trace Evaluation | `docs/trace_eval.md` | Role 5 | ⚠️ Mốc 3 pending |

---

## 4. Agent State TypedDict

```python
from typing import TypedDict, Literal

class AgentState(TypedDict):
    session_id: str
    query: str                          # Sanitized user query
    mode: Literal["chatbot", "agent"]
    history: list[dict]                 # [{"role": "user"|"assistant", "content": str}]
    trace: list[dict]                   # Per-step: thought, action, args, observation
    observations: list[str]             # Raw tool outputs for grounding check
    seen_actions: set[str]              # Dedup: prevent same tool+args twice
    steps: int
    status: Literal["success", "max_iterations_reached", "blocked", "error"]
    answer: str
    grounding: dict                     # {"grounded": bool, "ungrounded_claims": list}
    elapsed_seconds: float
    timestamp: str
```

---

## 5. Data Flow: User Query → Tool Observation

```
User: "Tôi biết Python và SQL. Thiếu gì để làm Data Scientist?"
    │
    ▼ sanitize → "Tôi biết Python và SQL. Thiếu gì để làm Data Scientist?"
    ▼ detect_injection → False (safe)
    │
    ▼ LLM (REACT_SYSTEM_PROMPT + user query)
    │
    → "Thought: Cần lấy yêu cầu kỹ năng cho Data Scientist.
       Action: get_skill_requirements(Data Scientist)"
    │
    ▼ parse_action → ("get_skill_requirements", ["Data Scientist"])
    ▼ safe_execute_tool
    ▼ tools.get_skill_requirements("Data Scientist")
    ▼ _normalize_role("Data Scientist") → "Data Scientist" ✓
    ▼ _load_roles()["roles"]["Data Scientist"]
    │
    Observation: {
      "status": "success",
      "data": {
        "role": "Data Scientist",
        "total_jds_analyzed": 147,
        "must_have": [{"skill": "Python", "frequency_percent": 87.1}, ...],
        "should_have": [{"skill": "Machine Learning", "frequency_percent": 72.1}, ...]
      },
      "dataset_version": "2026-06-11",
      "source": "ITviec & TopDev Vietnam 2025"
    }
    │
    ▼ LLM receives Observation in history
    → "Thought: Có đủ dữ liệu. User có Python ✓, SQL ✓. Thiếu: ML (72%), Tensorflow (45%)...
       Final Answer: Dựa trên 147 JDs Data Scientist (ITviec 2025):
       ✅ Đã có: Python (87%), SQL
       ❌ Thiếu ưu tiên: Machine Learning (72%), TensorFlow/PyTorch (45%), Statistics (41%)..."
    │
    ▼ extract_final_answer → response
    ▼ check_response_grounding → grounded=True (all numbers from observation)
    ▼ Return to user
```

---

## 6. Security Layer Details

| Guard | Trigger | Response |
|---|---|---|
| Rate Limit | >15 req/60s per session | "Chờ 1 phút" |
| PII Masking | Email / Phone VN / CCCD | Masked before logging |
| Injection Detection | 20+ patterns (EN+VI) | ADVERSARIAL_RESPONSE |
| Off-topic | Non-IT + harmful keywords | Polite redirect |
| Salary Guarantee | Cam kết / đảm bảo + số tiền | Soft block → explain uncertainty |
| Grounding | LLM claims number not in observations | Warning log (not hard block) |
| Loop Detection | Same tool + same args twice | ERROR:loop_detected → skip |
| Max Iterations | Steps > MAX_ITERATIONS (5) | SAFE_FALLBACK_MESSAGE |

---

## 7. Why Hybrid (Not Pure Agent)?

| Câu hỏi | Hybrid | Pure Agent |
|---|---|---|
| "Backend là gì?" | ✅ Chatbot → instant, free | ❌ Overkill, 3x slower, higher cost |
| "Tôi thiếu kỹ năng gì?" | ✅ Agent → grounded in 2795 JDs | ❌ Chatbot → generic answer, no evidence |
| "Tôi nên học gì?" (mơ hồ) | ✅ Clarify → ask 2 questions | ❌ Both fail without info |
| "Cam kết lương 50tr?" | ✅ Guardrail → safe refusal | ❌ Without guardrail: might comply |

---

## 8. Dataset Stats (Source: data/real/)

| Dataset | File | Entries | Source |
|---|---|---|---|
| Career Maps | `career_maps/all_roles.json` | 77 roles, 2795 JDs | ITviec, TopDev VN |
| Skill Ontology | `skill_ontology.json` | 92 skills, prerequisites | ITviec VN 2025 |
| Skill Details | `skills/*.json` | 25 skills deep-dive | Generated |
| Resources | `resources/*.json` | 23 domains | Curated |
| Question Bank | `question_bank/*.json` | 83 tech domains | Generated |
| Schedule Templates | `schedule_templates/*.json` | 19 roles | Generated |
| Index | `index.json` | 77 roles summary | Generated 2026-06-11 |
| Skill Frequency | `processed/skill_frequency_by_role.json` | 427KB | Generated |

**Dataset Version**: `2026-06-11` — Cite này trong mọi tool output.
