# 2026-05-26: RPG Progression Payload Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0015
- Original date: 2026-05-26
- Surface classes: mechanic part, example/source
- Agent facets: mechanics atlas, progression/cohort
- Mechanic parents: rpg
- Guard families: part-local artifact, example validation
- Posture: accepted

## Context

The progression model doc already lives under
`mechanics/rpg/parts/progression-model/`, but the machine-readable progression
schema and example still lived in root `schemas/` and `examples/`.

The progression contract is not a shared profile schema and not live routing
policy. It is the `progression-model` part's own adjunct overlay for reviewed
mastery axes, rank posture, unlock posture, and evidence refs keyed by
`agent_id`.

## Decision

Move the progression schema and example into
`mechanics/rpg/parts/progression-model/{schemas,examples}/` using part-local
names. Keep the stable schema `$id` unchanged because it is a public contract
identifier, not active repository path authority.

Add an explicit RPG progression validator and wire it into
`scripts/validate_agents.py` so the active file set, schema validity, example
validation, and old-route absence are checked explicitly. The validator later
moved into the active part route:
`mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py`.

Preserve former root lookup only through RPG `PROVENANCE.md` and `legacy/`.

## Consequences

- The `progression-model` part now co-locates docs, schema, and example.
- Root `schemas/` and `examples/` remain active for shared or not-yet-localized
  contracts.
- Existing schema `$id` remains stable for consumers.
- Old root progression names remain historical lookup facts only.

## Verification

```bash
python mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python -m pytest -q tests/test_repo_validator.py
python -m pytest -q tests
python scripts/release_check.py
```
