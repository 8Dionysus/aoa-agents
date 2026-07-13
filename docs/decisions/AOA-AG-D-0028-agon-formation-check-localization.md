# 2026-05-26: Agon Formation Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0028
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, agon formation
- Mechanic parents: agon
- Guard families: part-local artifact, validation guard
- Posture: accepted

## Context

Agon formation contracts already live under
`mechanics/agon/parts/formation/`, but the Wave I formation builders,
Wave II.5 formation-trial builder, validators, and focused tests still lived
in root `scripts/` and `tests/`.

The generated formation readers stay root-published because they summarize
`agents/` source records for repo-wide consumers. That does not require the
support code to stay root-owned.

Sibling mechanics refactors in Agents-of-Abyss, `aoa-evals`, and `aoa-memo`
put part-specific scripts and tests next to the part that owns the operation.

## Decision

Move the Agon formation builders, validators, and focused tests into
`mechanics/agon/parts/formation/{scripts,tests}/`.

Keep:

- `generated/agent_agonic_formation_index.min.json`
- `generated/agent_formation_trial.min.json`

root-published, but update their `generated_by` fields to the part-local
builder paths.

`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
part-local formation contract validator directly. `scripts/release_check.py`
runs the part-local formation tests explicitly.

## Consequences

Formation operation changes now start in the owning Agon part. Root `scripts/`
keeps repo-level coordination and shared builders; root `tests/` keeps
repo-level route checks.

Old root script and test paths are provenance facts only and are checked for
absence by the part-local formation contract validator.

## Validation

Verification routes through the focused owner checks and the repository release gate.
