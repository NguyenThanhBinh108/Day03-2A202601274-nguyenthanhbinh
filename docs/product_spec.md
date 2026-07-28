# Product Specification — EduPath Career Advisor

## North-star outcome

A user can choose or compare an IT career target, understand their evidence-based skill gap, and receive a feasible learning roadmap with clear assumptions and next actions.

## Primary jobs-to-be-done

1. "Help me understand which IT roles may fit my interests and current background."
2. "Show what I am missing for an intern/fresher target role."
3. "Create a realistic roadmap based on my available time."
4. "Explain why each skill/project is recommended."
5. "Update my plan after I complete a test or change goals."

## Features and acceptance criteria

### F-01 Career Q&A
- Answers definitions and comparisons from curated data.
- Uses retrieval, not agent loop, for one-step questions.
- Shows source/version for market claims.

### F-02 Role Discovery
- Returns up to 3 candidate roles.
- Explains match and mismatch.
- Asks clarifying questions when input is insufficient.
- Does not claim a role is objectively "the best".

### F-03 Skill Profile
- Supports self-assessment and test-derived evidence.
- Distinguishes user claim from verified test result.
- Allows user to correct/delete profile information.

### F-04 Skill Gap
- Separates `possessed`, `missing`, `supporting`.
- Prioritizes by role importance, prerequisite and market evidence.
- Every recommendation points to a requirement record.

### F-05 Roadmap
- Accepts hours/week and target duration/date.
- Produces phases, weekly outcomes, projects and checkpoints.
- Passes deterministic validation.
- Shows assumptions and warnings.

### F-06 ReAct Comparison Lab
- Baseline and agent run on identical inputs.
- At least 5 test cases.
- At least 1 multi-tool trace.
- At least 1 tool failure case.
- Includes hybrid decision flowchart and Agentic Fit conclusion.

## Non-goals

- Guaranteed recruitment outcomes.
- Psychological/personality diagnosis.
- Automatic job application.
- Unverified real-time salary prediction.
- Fully autonomous long-horizon career management in MVP.
