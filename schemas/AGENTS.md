# AGENTS.md

## Guidance for `schemas/`

`schemas/` holds shared contracts for profiles, model tiers, orchestrator classes, cohorts, runtime artifacts, checkpoints, and reference routes.

Mechanic-specific Titan schemas live under `mechanics/titan/parts/*/schemas/`
and are validated by `scripts/validate_titan_schemas.py`.

Mechanic-specific antifragility stress schemas live under
`mechanics/antifragility/parts/stress-posture/schemas/` and are validated by
`scripts/validate_antifragility_stress.py`.

Schema edits are role contract edits. Preserve `$schema`, stable `$id` or identifier posture, required fields, enums, and descriptions that keep role authority bounded.

Do not loosen a schema to pass a vague profile. Fix the profile or explicitly document the contract change.

Pair schema edits with examples, generated-surface rebuilds, and validation.

Verify with:

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
