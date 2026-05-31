# 2026-05-26: Experience Assistant Civil Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0030
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, assistant civil
- Mechanic parents: experience
- Guard families: part-local artifact, validation guard
- Posture: accepted

## Context

Wave II assistant civil schemas and examples already live under their owning
Experience parts. The generated assistant civil formation reader intentionally
remains root-published because it summarizes source adjunct records under
`agents/roles/*/forms/`.

The dedicated builder, validator, and focused tests still lived in root
`scripts/` and `tests/`, which made the active Experience part depend on root
check paths after the payload contracts had moved.

## Decision

Move the Wave II assistant civil checks into Experience-owned routes:

- the formation builder, formation validator, and focused formation test move
  into `mechanics/experience/parts/assistant-civil-service/{scripts,tests}/`;
- the cross-part assistant civil contract validator and focused contract test
  move into `mechanics/experience/{scripts,tests}/`, because they validate
  `assistant-civil-service` and `arena-exclusion` together.

`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
package-local validator directly. `scripts/release_check.py` runs the new
package and part-local Experience tests explicitly.

## Consequences

Assistant civil check edits now start in the Experience package or the
`assistant-civil-service` part. Root `scripts/` keeps repository-level
coordination and shared builders; root `tests/` keeps repository-level route
guards.

Old root script and test paths are provenance facts only and are checked for
absence by the package-local contract validator.

## Validation

```bash
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py
python -m unittest discover -s mechanics/experience/tests -p 'test_*.py'
python -m unittest discover -s mechanics/experience/parts/assistant-civil-service/tests -p 'test_*.py'
python scripts/validate_agents.py
```
