# examples/AGENTS.md

## Purpose

`examples/` contains public-safe, schema-backed examples for inspectable agent-layer contracts.
These files illustrate published contracts. They are not the source-authored canon layer.

## Subtrees

- `mechanics/agon/parts/formation/examples/agent-agonic-formation.example.json`
  for the additive Wave I reader path across base role contract plus agonic
  companion surfaces
- `mechanics/experience/parts/assistant-civil-service/examples/civil-formation.example.json`
  for the additive Wave II reader path across base role contract plus assistant
  civil companion surfaces
- `mechanics/agon/parts/formation/examples/formation-trial.example.json` for
  the additive Wave II.5 reader path across base role house plus agonic and
  assistant split-form judgment
- `mechanics/checkpoint/parts/reference-routes/examples/` for manifest-driven
  reference route packs over the published public loop
- `mechanics/questbook/parts/alpha-reference-routes/examples/` for curated
  Alpha cohort reference-route surfaces used by the readiness proof lane

Mechanic-specific self-agent checkpoint examples and negative fixtures live
under `mechanics/checkpoint/parts/self-agent-checkpoint/examples/` and are
validated by `scripts/validate_checkpoint_contracts.py`. The adjacent
continuity-window example lives under
`mechanics/checkpoint/parts/continuity-lane/examples/`.

Mechanic-specific runtime artifact examples and negative fixtures live under
`mechanics/runtime-seam/parts/artifact-contracts/examples/` and are validated
by `scripts/validate_runtime_artifact_contracts.py`. Their schemas live beside
them under `mechanics/runtime-seam/parts/artifact-contracts/schemas/`.

Mechanic-specific Titan examples live under
`mechanics/titan/parts/*/examples/` and are validated by
`mechanics/titan/scripts/validate_titan_examples.py`. Their schemas live
beside them under `mechanics/titan/parts/*/schemas/`.

Mechanic-specific antifragility stress examples live under
`mechanics/antifragility/parts/stress-posture/examples/` and are validated by
`mechanics/antifragility/parts/stress-posture/scripts/validate_stress_posture.py`.
Their schemas live beside them under
`mechanics/antifragility/parts/stress-posture/schemas/`.

Mechanic-specific RPG progression examples live under
`mechanics/rpg/parts/progression-model/examples/` and are validated by
`scripts/validate_rpg_progression.py`. Their schemas live beside them under
`mechanics/rpg/parts/progression-model/schemas/`.

Mechanic-specific assistant projection resolver examples live under
`mechanics/codex-projection/parts/assistant-projection/examples/` and are
validated by `scripts/validate_assistant_projection_resolver.py`. Their
schemas live beside them under
`mechanics/codex-projection/parts/assistant-projection/schemas/`.

Mechanic-specific Codex refresh-law examples live under
`mechanics/codex-projection/parts/refresh-law/examples/` and are validated by
`scripts/validate_codex_refresh_law_contracts.py`.

Mechanic-specific recursor examples live under
`mechanics/recurrence/parts/recursor-readiness/examples/` and
`mechanics/recurrence/parts/agon-recursor-boundary/examples/`. They are
validated by `scripts/validate_recursor_contracts.py`. Their schemas live
beside them under the corresponding recurrence parts.

Mechanic-specific Agon rank, school, and epistemic actor examples live under
`mechanics/agon/parts/arena-rank-school/examples/` and
`mechanics/agon/parts/epistemic-actor/examples/`. They are validated by
`scripts/validate_agon_rank_epistemic_contracts.py`. Their schemas live beside
them under the corresponding Agon parts.

Mechanic-specific Agon formation examples live under
`mechanics/agon/parts/formation/examples/`. They are validated by
`scripts/validate_agon_formation_contracts.py`. Their schemas live beside them
under `mechanics/agon/parts/formation/schemas/`, with arena eligibility in the
adjacent `arena-rank-school` schema route.

Mechanic-specific Experience assistant civil examples live under
`mechanics/experience/parts/assistant-civil-service/examples/`. They are
validated by `scripts/validate_experience_assistant_civil_contracts.py`. Their
schemas live beside them under
`mechanics/experience/parts/assistant-civil-service/schemas/`, with arena
exclusion in the adjacent `arena-exclusion` schema route.

Mechanic-specific adoption and boundary bridge examples live under
`mechanics/agon/parts/adoption-retention/examples/`,
`mechanics/boundary-bridge/parts/*/examples/`, and
`mechanics/experience/parts/{adoption-and-regression,office-operations}/examples/`.
They are validated by `scripts/validate_adoption_boundary_contracts.py`.
Their schemas live beside them under the corresponding part-local `schemas/`
routes.

Mechanic-specific agent service examples live under
`mechanics/experience/parts/*/examples/`,
`mechanics/runtime-seam/parts/artifact-contracts/examples/`, and
`mechanics/release-support/parts/runtime-release-hold/examples/`. They are
validated by `scripts/validate_agent_service_contracts.py`. Their schemas live
beside them under the corresponding part-local `schemas/` routes.

Mechanic-specific reference-route examples live under
`mechanics/checkpoint/parts/reference-routes/examples/` and
`mechanics/questbook/parts/alpha-reference-routes/examples/`. They are
validated by `scripts/validate_reference_route_contracts.py`. Their schemas
live beside them under the corresponding part-local `schemas/` routes.

## Editing posture

Keep examples minimal, portable, and public-safe.
Do not invent new contract keys ahead of schema or runtime-seam changes.
Do not store real run history, secrets, or hidden transport assumptions.
Do not turn examples into live authority for arena seats, protocol packets, or
runtime state.

## Validation

Run `python -m pip install -r requirements-dev.txt` first. Then `python scripts/validate_agents.py` validates example alignment and negative fixtures.
For Titan part-local examples, also run `python mechanics/titan/scripts/validate_titan_examples.py`.
For antifragility stress part-local examples, also run `python mechanics/antifragility/parts/stress-posture/scripts/validate_stress_posture.py`.
For RPG progression part-local examples, also run `python scripts/validate_rpg_progression.py`.
For assistant projection resolver part-local examples, also run `python scripts/validate_assistant_projection_resolver.py`.
For Codex refresh-law part-local examples, also run `python scripts/validate_codex_refresh_law_contracts.py`.
For runtime artifact contract part-local examples, also run `python scripts/validate_runtime_artifact_contracts.py`.
For checkpoint contract part-local examples, also run `python scripts/validate_checkpoint_contracts.py`.
For recursor part-local examples, also run `python scripts/validate_recursor_contracts.py`.
For Agon formation part-local examples, also run `python scripts/validate_agon_formation_contracts.py`.
For Agon rank/school/epistemic part-local examples, also run `python scripts/validate_agon_rank_epistemic_contracts.py`.
For Experience assistant civil part-local examples, also run `python scripts/validate_experience_assistant_civil_contracts.py`.
For adoption and boundary bridge part-local examples, also run `python scripts/validate_adoption_boundary_contracts.py`.
For agent service part-local examples, also run `python scripts/validate_agent_service_contracts.py`.
For reference-route part-local examples, also run `python scripts/validate_reference_route_contracts.py`.
For the Wave I reader path example, also run `python scripts/validate_agent_agonic_formation.py`.
For the Wave II reader path example, also run `python scripts/validate_assistant_civil_formation.py`.
For the Wave II.5 reader path example, also run `python scripts/validate_agent_formation_trial.py`.
