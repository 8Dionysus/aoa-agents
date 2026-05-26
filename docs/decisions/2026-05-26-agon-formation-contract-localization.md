# 2026-05-26: Agon Formation Contract Localization

## Status

Accepted.

## Context

Agon formation docs, generated readers, and validators already live around the
`mechanics/agon/parts/formation/` route, but Wave I formation adjunct schemas,
the arena eligibility schema, the Wave II.5 formation-trial schema, and their
examples still lived in root `schemas/` and `examples/`.

Those contracts are not shared profile schemas and not live Agon protocol
authority. They are candidate-only agent-layer support contracts for formation
reader paths and pre-protocol split-form judgment.

## Decision

Move these Agon formation contract payloads into their owning parts:

- kind, subjectivity, office overlay, resistance/revision, formation-trial
  schemas and Wave I / Wave II.5 examples move into
  `mechanics/agon/parts/formation/{schemas,examples}/`;
- arena eligibility moves into
  `mechanics/agon/parts/arena-rank-school/schemas/`;
- `scripts/validate_agon_formation_contracts.py` becomes the package-local
  contract validator and is called by `scripts/validate_agents.py`.

Generated formation readers remain derived surfaces under `generated/`; builder
scripts remain support surfaces under `scripts/`. Stable schema `$id` values
remain unchanged as public contract identifiers.

Former root paths are recorded only through Agon `PROVENANCE.md` and `legacy/`.

## Consequences

Formation contract edits now start in the Agon part that owns the operation.
Root `schemas/` and `examples/` no longer act as active homes for these
contracts. Wave II assistant civil contracts were intentionally left for a
separate Experience-owned localization slice, which later landed under
`mechanics/experience/`.

Validation for this route is:

```bash
python scripts/validate_agon_formation_contracts.py
python scripts/validate_agent_agonic_formation.py
python scripts/build_agent_formation_trial.py --check
python scripts/validate_agent_formation_trial.py
python scripts/validate_agents.py
python -m pytest -q tests/test_agon_formation_contracts.py tests/test_agent_agonic_formation.py tests/test_agent_formation_trial.py
```
