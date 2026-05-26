# examples/AGENTS.md

## Purpose

`examples/` contains public-safe, schema-backed examples for inspectable agent-layer contracts.
These files illustrate published contracts. They are not the source-authored canon layer.

## Subtrees

- `agent_agonic_formation.example.json` for the additive Wave I reader path
  across base role contract plus agonic companion surfaces
- `assistant_civil_formation.example.json` for the additive Wave II reader path
  across base role contract plus assistant civil companion surfaces
- `agent_formation_trial.example.json` for the additive Wave II.5 reader path
  across base role house plus agonic and assistant split-form judgment
- `reference_routes/` for manifest-driven reference route packs over the published public loop
- `alpha_reference_routes/` for curated Alpha cohort reference-route surfaces used by the readiness proof lane

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
`scripts/validate_titan_examples.py`. Their schemas live beside them under
`mechanics/titan/parts/*/schemas/`.

Mechanic-specific antifragility stress examples live under
`mechanics/antifragility/parts/stress-posture/examples/` and are validated by
`scripts/validate_antifragility_stress.py`. Their schemas live beside them
under `mechanics/antifragility/parts/stress-posture/schemas/`.

Mechanic-specific RPG progression examples live under
`mechanics/rpg/parts/progression-model/examples/` and are validated by
`scripts/validate_rpg_progression.py`. Their schemas live beside them under
`mechanics/rpg/parts/progression-model/schemas/`.

Mechanic-specific assistant projection resolver examples live under
`mechanics/codex-projection/parts/assistant-projection/examples/` and are
validated by `scripts/validate_assistant_projection_resolver.py`. Their
schemas live beside them under
`mechanics/codex-projection/parts/assistant-projection/schemas/`.

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

## Editing posture

Keep examples minimal, portable, and public-safe.
Do not invent new contract keys ahead of schema or runtime-seam changes.
Do not store real run history, secrets, or hidden transport assumptions.
Do not turn examples into live authority for arena seats, protocol packets, or
runtime state.

## Validation

Run `python -m pip install -r requirements-dev.txt` first. Then `python scripts/validate_agents.py` validates example alignment and negative fixtures.
For Titan part-local examples, also run `python scripts/validate_titan_examples.py`.
For antifragility stress part-local examples, also run `python scripts/validate_antifragility_stress.py`.
For RPG progression part-local examples, also run `python scripts/validate_rpg_progression.py`.
For assistant projection resolver part-local examples, also run `python scripts/validate_assistant_projection_resolver.py`.
For runtime artifact contract part-local examples, also run `python scripts/validate_runtime_artifact_contracts.py`.
For checkpoint contract part-local examples, also run `python scripts/validate_checkpoint_contracts.py`.
For recursor part-local examples, also run `python scripts/validate_recursor_contracts.py`.
For Agon rank/school/epistemic part-local examples, also run `python scripts/validate_agon_rank_epistemic_contracts.py`.
For the Wave I reader path example, also run `python scripts/validate_agent_agonic_formation.py`.
For the Wave II reader path example, also run `python scripts/validate_assistant_civil_formation.py`.
For the Wave II.5 reader path example, also run `python scripts/validate_agent_formation_trial.py`.
