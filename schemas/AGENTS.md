# AGENTS.md

## Guidance for `schemas/`

Use [README.md](README.md) as the root schema district index. This card owns
edit posture, root-vs-mechanic schema boundaries, and validation route.

`schemas/` holds shared contracts for profiles, model tiers, orchestrator classes, cohorts, and runtime-seam registry bindings.

Mechanic-specific runtime artifact schemas live under
`mechanics/runtime-seam/parts/artifact-contracts/schemas/` and are validated by
`mechanics/runtime-seam/parts/artifact-contracts/scripts/validate_artifact_contracts.py`.

Mechanic-specific self-agent checkpoint schemas live under
`mechanics/checkpoint/parts/self-agent-checkpoint/schemas/` and
`mechanics/checkpoint/parts/continuity-lane/schemas/`. They are validated by
`mechanics/checkpoint/scripts/validate_checkpoint_contracts.py`.

Mechanic-specific reference-route schemas live under
`mechanics/checkpoint/parts/reference-routes/schemas/` and
`mechanics/questbook/parts/alpha-reference-routes/schemas/`. They are
validated by `scripts/validate_reference_route_contracts.py`.

Mechanic-specific Titan schemas live under `mechanics/titan/parts/*/schemas/`
and are validated by `mechanics/titan/scripts/validate_titan_schemas.py`.

Mechanic-specific antifragility stress schemas live under
`mechanics/antifragility/parts/stress-posture/schemas/` and are validated by
`mechanics/antifragility/parts/stress-posture/scripts/validate_stress_posture.py`.

Mechanic-specific RPG progression schemas live under
`mechanics/rpg/parts/progression-model/schemas/` and are validated by
`mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py`.

Mechanic-specific assistant projection resolver schemas live under
`mechanics/codex-projection/parts/assistant-projection/schemas/` and are
validated by
`mechanics/codex-projection/parts/assistant-projection/scripts/validate_assistant_projection_resolver.py`.

Mechanic-specific recursor schemas live under
`mechanics/recurrence/parts/recursor-readiness/schemas/`,
`mechanics/recurrence/parts/codex-recursor-projection/schemas/`, and
`mechanics/recurrence/parts/agon-recursor-boundary/schemas/`. They are
validated by `mechanics/recurrence/scripts/validate_recursor_contracts.py`.

Mechanic-specific Agon rank, school, and epistemic actor schemas live under
`mechanics/agon/parts/arena-rank-school/schemas/` and
`mechanics/agon/parts/epistemic-actor/schemas/`. They are validated by
`mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py`.

Mechanic-specific Agon formation schemas live under
`mechanics/agon/parts/formation/schemas/`, with arena eligibility in
`mechanics/agon/parts/arena-rank-school/schemas/`. They are validated by
`mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py`.

Mechanic-specific Experience assistant civil schemas live under
`mechanics/experience/parts/assistant-civil-service/schemas/`, with arena
exclusion in `mechanics/experience/parts/arena-exclusion/schemas/`. They are
validated by `mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py`.

Mechanic-specific adoption and boundary bridge schemas live under
`mechanics/agon/parts/adoption-retention/schemas/`,
`mechanics/boundary-bridge/parts/*/schemas/`, and
`mechanics/experience/parts/{adoption-and-regression,office-operations}/schemas/`.
They are validated by `scripts/validate_adoption_boundary_contracts.py`.

Mechanic-specific agent service schemas live under
`mechanics/experience/parts/*/schemas/`,
`mechanics/runtime-seam/parts/artifact-contracts/schemas/`, and
`mechanics/release-support/parts/runtime-release-hold/schemas/`. They are
validated by `scripts/validate_agent_service_contracts.py`.

Schema edits are role contract edits. Preserve `$schema`, stable `$id` or identifier posture, required fields, enums, and descriptions that keep role authority bounded.

Root schema payloads stay here when they constrain repo-wide agent source
families or generated registries. Mechanic-specific schemas belong under the
owning mechanic part once that part has route cards and validators.

Do not loosen a schema to pass a vague profile. Fix the profile or explicitly document the contract change.

Pair schema edits with examples, generated-surface rebuilds, and validation.

Verify with:

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
