# Evaluation Plan

## Lab-required evidence

- Chatbot baseline.
- ReAct agent using the same use case.
- Minimum 5 shared test cases.
- One safe trace: decision summary → action → observation → stop reason.
- One hybrid flowchart.
- Clear conclusion: when chatbot is enough and when the agent adds value.

## Test dimensions

1. Simple direct question.
2. Retrieval-only question.
3. Personalized skill-gap request.
4. Multi-step roadmap request.
5. Ambiguous request requiring clarification.
6. Unknown role.
7. Missing profile.
8. Tool timeout.
9. Repeated tool call/loop trap.
10. Prompt injection in retrieved content.
11. Unsupported salary claim.
12. Unrealistic roadmap constraint.

## Metrics

| Metric | Definition |
|---|---|
| Route accuracy | Correct simple/agent/clarify/fallback path |
| Tool selection accuracy | Correct tool used when needed |
| Argument accuracy | Valid role, level and constraints |
| Grounding | Claims supported by tool/retrieved data |
| Constraint pass rate | Roadmap passes validator |
| Safe fallback rate | Correct behavior under missing/error data |
| Step efficiency | No unnecessary calls |
| Hallucination rate | Unsupported facts or market claims |
| Task success | User receives a usable next action |

## Trace format

```json
{
  "case_id": "TC-03",
  "route": "agent",
  "steps": [
    {
      "step": 1,
      "decision_summary": "Need role requirements for target level.",
      "action": "get_role_requirements",
      "arguments": {},
      "observation_summary": "Requirements returned with dataset version."
    }
  ],
  "stop_reason": "sufficient_evidence",
  "final_status": "success"
}
```
