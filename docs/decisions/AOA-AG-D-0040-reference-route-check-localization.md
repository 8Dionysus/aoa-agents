# 2026-05-26: Reference Route Check Localization
## Index Metadata

- Decision ID: AOA-AG-D-0040
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard, generated/readout
- Agent facets: mechanics atlas, quest/alpha
- Mechanic parents: questbook, checkpoint
- Guard families: part-local artifact, validation guard, generated/read-model, quest dispatch
- Posture: accepted


## Context

Reference-route contracts had already moved into active mechanic homes:
public-loop route packs under `mechanics/checkpoint/parts/reference-routes/`
and Alpha readiness routes under
`mechanics/questbook/parts/alpha-reference-routes/`.

The remaining root helpers still mixed those owners:
`scripts/validate_reference_route_contracts.py` validated both Checkpoint route
packs and Questbook Alpha routes, while
`scripts/generate_alpha_reference_routes.py` rebuilt only the Questbook Alpha
part-local generated reader.

## Decision

Move reference-route checks into their owning mechanic routes:

- Checkpoint reference-route validation:
  `mechanics/checkpoint/scripts/validate_reference_route_contracts.py`
- Checkpoint reference-route focused tests:
  `mechanics/checkpoint/tests/test_reference_route_contracts.py`
- Questbook Alpha reference-route validation:
  `mechanics/questbook/scripts/validate_alpha_reference_routes.py`
- Questbook Alpha generated-reader builder:
  `mechanics/questbook/parts/alpha-reference-routes/scripts/generate_alpha_reference_routes.py`
- Questbook Alpha focused tests:
  `mechanics/questbook/tests/test_alpha_reference_routes.py`

`scripts/validate_agents.py` remains the repo-wide coordinator and still checks
both surfaces as part of full validation.

## Consequences

Root `scripts/` no longer owns mechanics-specific reference-route check
entrypoints. The Alpha builder now sits beside the examples and generated
reader it derives. Release validation must run Questbook package tests
explicitly, while the existing Checkpoint test discovery now covers
reference-route tests.

The split preserves the source-store boundary: root `quests/` remains the
quest source record lane, while `mechanics/questbook/` owns Alpha route
operation law and generated-reader discipline.

`generated/AGENTS.md` is a route card for generated-reader edit law, so the
release drift check now excludes that card while still checking generated data
outputs after `scripts/build_published_surfaces.py`.

## Validation

```bash
python mechanics/checkpoint/scripts/validate_reference_route_contracts.py
python mechanics/questbook/parts/alpha-reference-routes/scripts/generate_alpha_reference_routes.py --check
python mechanics/questbook/scripts/validate_alpha_reference_routes.py
python -m unittest discover -s mechanics/checkpoint/tests -p 'test_*.py'
python -m unittest discover -s mechanics/questbook/tests -p 'test_*.py'
python scripts/validate_agents.py
PYTHONDONTWRITEBYTECODE=1 python scripts/release_check.py
```
