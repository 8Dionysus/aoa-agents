# AGENTS.md

## Guidance for `schemas/`

`schemas/` holds shared contracts for profiles, model tiers, orchestrator classes, cohorts, checkpoints, and reference routes.

Mechanic-specific runtime artifact schemas live under
`mechanics/runtime-seam/parts/artifact-contracts/schemas/` and are validated by
`scripts/validate_runtime_artifact_contracts.py`.

Mechanic-specific self-agent checkpoint schemas live under
`mechanics/checkpoint/parts/self-agent-checkpoint/schemas/` and
`mechanics/checkpoint/parts/continuity-lane/schemas/`. They are validated by
`scripts/validate_checkpoint_contracts.py`.

Mechanic-specific Titan schemas live under `mechanics/titan/parts/*/schemas/`
and are validated by `scripts/validate_titan_schemas.py`.

Mechanic-specific antifragility stress schemas live under
`mechanics/antifragility/parts/stress-posture/schemas/` and are validated by
`scripts/validate_antifragility_stress.py`.

Mechanic-specific RPG progression schemas live under
`mechanics/rpg/parts/progression-model/schemas/` and are validated by
`scripts/validate_rpg_progression.py`.

Mechanic-specific assistant projection resolver schemas live under
`mechanics/codex-projection/parts/assistant-projection/schemas/` and are
validated by `scripts/validate_assistant_projection_resolver.py`.

Mechanic-specific recursor schemas live under
`mechanics/recurrence/parts/recursor-readiness/schemas/`,
`mechanics/recurrence/parts/codex-recursor-projection/schemas/`, and
`mechanics/recurrence/parts/agon-recursor-boundary/schemas/`. They are
validated by `scripts/validate_recursor_contracts.py`.

Mechanic-specific Agon rank, school, and epistemic actor schemas live under
`mechanics/agon/parts/arena-rank-school/schemas/` and
`mechanics/agon/parts/epistemic-actor/schemas/`. They are validated by
`scripts/validate_agon_rank_epistemic_contracts.py`.

Schema edits are role contract edits. Preserve `$schema`, stable `$id` or identifier posture, required fields, enums, and descriptions that keep role authority bounded.

Do not loosen a schema to pass a vague profile. Fix the profile or explicitly document the contract change.

Pair schema edits with examples, generated-surface rebuilds, and validation.

Verify with:

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
