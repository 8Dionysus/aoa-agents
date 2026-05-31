# 2026-05-26: RPG Progression Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0016
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, progression/cohort
- Mechanic parents: rpg
- Guard families: part-local artifact, validation guard
- Posture: accepted

## Context

The RPG progression schema, example, and model doc already live in
`mechanics/rpg/parts/progression-model/`, but their validator still lived at
root `scripts/validate_rpg_progression.py`.

That kept the repo-wide helper district responsible for a single part's active
contract and left focused validation outside the part it protects.

## Decision

Move the RPG progression validator to
`mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py`.
Add focused part-local tests under
`mechanics/rpg/parts/progression-model/tests/`.

Keep `scripts/validate_agents.py` as the repo-wide coordinator by loading the
part-local validator explicitly. Keep `scripts/release_check.py` responsible
for running the focused part tests in the release gate.

## Consequences

- The `progression-model` part now owns its docs, schema, example, validator,
  and focused tests together.
- Root `scripts/` remains active for repo-wide orchestration and shared
  builders, not for this part's local contract.
- Former root lookup survives only through RPG `PROVENANCE.md` and `legacy/`.

## Verification

```bash
python mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py
python -m unittest discover -s mechanics/rpg/parts/progression-model/tests -p 'test_*.py'
python scripts/validate_agents.py
python scripts/release_check.py
```
