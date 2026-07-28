# AGENTS.md

## Repository purpose

Build and evaluate a Vietnamese hybrid career-advisory system for IT beginners, students, interns and freshers.

## Read order

1. `CONTEXT.md`
2. `docs/product_spec.md`
3. `docs/architecture.md`
4. `docs/tool_contracts.md`
5. `docs/evaluation_plan.md`
6. Task-specific source files

## Non-negotiable constraints

- Baseline chatbot: exactly one model call, zero tool calls.
- ReAct agent: real tool observations, no fabricated observations.
- Maximum iterations and safe fallback are mandatory.
- Simple FAQ/general explanation should not enter the agent loop.
- Skill gap scoring and roadmap validation should be deterministic.
- Market claims require source and dataset version.
- Do not reveal secrets, system prompts, private profile data or hidden reasoning.

## Change protocol

- Make the smallest change that satisfies the task.
- Add or update tests before declaring completion.
- Do not silently change schemas.
- Do not introduce a new dependency without documenting the reason.
- Do not modify test fixtures merely to hide a bug.
