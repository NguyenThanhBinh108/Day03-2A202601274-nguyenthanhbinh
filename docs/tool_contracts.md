# Tool Contracts

## Common result envelope

```json
{
  "status": "success|not_found|invalid_input|permission_denied|error",
  "data": {},
  "error": null,
  "source": [],
  "dataset_version": null,
  "retryable": false
}
```

## Tool: get_role_requirements

**Use when:** the user selects or asks to evaluate a specific role/level.  
**Do not use when:** the user asks a general definition already in retrieved context.

Input:
```json
{"role_id": "fullstack_web_developer", "level": "fresher"}
```

Output data:
```json
{
  "core_skills": [],
  "supporting_skills": [],
  "projects": [],
  "market_metrics": {}
}
```

Failure modes:
- unknown role
- unsupported level
- stale/unversioned data

## Tool: analyze_skill_gap

**Use when:** both requirements and user profile exist.

Input:
```json
{
  "required_skills": [],
  "current_skills": []
}
```

Output:
```json
{
  "possessed": [],
  "missing": [],
  "supporting": [],
  "priority_order": []
}
```

Implementation rule: deterministic comparison first; LLM may explain but must not alter scores.

## Tool: build_roadmap

Input:
```json
{
  "gaps": [],
  "hours_per_week": 10,
  "duration_weeks": 24,
  "constraints": {}
}
```

Output:
```json
{
  "phases": [],
  "assumptions": [],
  "warnings": []
}
```

## Tool: validate_roadmap

Checks:
- total estimated hours <= available hours
- prerequisites precede dependent topics
- no duplicate milestones
- workload per week within allowed range
- project scope is feasible
