# AGENTS.md

## Guidance for `.agents/skills/`

`.agents/skills/` is an agent-facing companion surface for role-layer maintenance.

It may help a coding agent inspect profiles, role contracts, handoffs, memory posture, or evaluation posture, but it must not create new agent authority outside source-authored profiles and docs.

Do not hand-edit exported companion files before changing the source profile, model tier, orchestrator class, cohort pattern, or runtime seam that owns meaning.

Keep role language bounded. An agent is a role-bearing actor that uses skills; it is not a skill bundle and not a proof bundle.

Keep everything public-safe: no secrets, private operational prompts, hidden credentials, or unreduced operator traces.

Verify with:

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
