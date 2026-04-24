# AGENTS.md

## Guidance for `schemas/`

`schemas/` holds contracts for profiles, model tiers, orchestrator classes, cohorts, runtime artifacts, checkpoints, and reference routes.

Schema edits are role contract edits. Preserve `$schema`, stable `$id` or identifier posture, required fields, enums, and descriptions that keep role authority bounded.

Do not loosen a schema to pass a vague profile. Fix the profile or explicitly document the contract change.

Pair schema edits with examples, generated-surface rebuilds, and validation.

Verify with:

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
