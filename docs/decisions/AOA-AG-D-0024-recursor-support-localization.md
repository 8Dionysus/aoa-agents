# 2026-05-26: Recursor Support Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0024
- Original date: 2026-05-26
- Surface classes: mechanic part, generated/readout
- Agent facets: mechanics atlas, recurrence
- Mechanic parents: recurrence
- Guard families: part-local artifact, generated/read-model
- Posture: accepted

## Context

Recursor payloads and generated readers already live under
`mechanics/recurrence/parts/*`, but the common helper, builders, validators,
and focused tests still lived in root `scripts/` and `tests/`.

The helper and checks serve only the Recurrence recursor package. Keeping them
at root made the active contract look repo-wide even though the owning
operation is package-local.

## Decision

Move recursor support into `mechanics/recurrence/{scripts,tests}/`:

- `_recursor_common.py`
- recursor readiness and projection builders
- recursor contract, role-readiness, and boundary validators
- focused recursor contract and readiness tests

Keep `scripts/validate_agents.py` as the repo-wide coordinator by loading the
package-local recursor contract validator explicitly. Keep release validation
explicit by running the package-local recurrence tests from
`scripts/release_check.py`.

## Consequences

- Recurrence now owns the helper and checks beside the parts they protect.
- Former root script/test paths are provenance facts, not active routes.
- Component manifests and docs name the package-local commands directly.
- Root `scripts/` remains for repo-wide builders, validators, and publication
  helpers.

## Verification

```bash
python mechanics/recurrence/scripts/build_recursor_role_readiness.py --check
python mechanics/recurrence/scripts/build_recursor_projection_candidates.py --check
python mechanics/recurrence/scripts/validate_recursor_contracts.py
python mechanics/recurrence/scripts/validate_recursor_role_readiness.py
python mechanics/recurrence/scripts/validate_recursor_boundary.py
python -m unittest discover -s mechanics/recurrence/tests -p 'test_*.py'
python scripts/validate_agents.py
python scripts/release_check.py
```
