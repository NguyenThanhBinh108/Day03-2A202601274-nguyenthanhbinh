# CLAUDE.md

Read `CONTEXT.md` first. It is the project source of truth.

## Operating rules

- Preserve the hybrid architecture: simple questions use retrieval chatbot; personalized multi-step tasks use the ReAct agent.
- Never hardcode or invent market figures, salaries, job counts, or skill percentages.
- Treat dataset year/version as part of every market claim.
- Keep business logic deterministic where possible, especially skill-gap scoring and roadmap validation.
- Do not expose hidden chain-of-thought. Log only decision summary, tool call, observation, errors, and stop reason.
- Never remove `MAX_ITERATIONS`, timeout, repeated-call detection, schema validation, or safe fallback.
- Do not commit `.env`, credentials, personal data, raw CVs, or private traces.
- Before editing: inspect relevant files and state a short plan.
- After editing: run the narrowest relevant tests, then full tests when practical.
- Update documentation whenever an API, schema, tool contract, data contract, or architecture decision changes.
- Prefer small, reviewable commits.

## Required commands

```bash
# install
pip install -r requirements.txt

# run
python src/app.py

# lint
# (add linter config if needed)
```

## Core files

- `CONTEXT.md`: product and engineering source of truth.
- `docs/product_spec.md`: user problem, features, scope and acceptance criteria.
- `docs/architecture.md`: components, flows, state and boundaries.
- `docs/tool_contracts.md`: tool schemas and failure modes.
- `docs/evaluation_plan.md`: test and metric contract.
- `config/test_cases.json`: executable behavior cases.
- `docs/trace_eval.md`: comparison and trace evidence required by Lab.
