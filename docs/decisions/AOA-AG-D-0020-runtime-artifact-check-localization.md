# 2026-05-26: Runtime Artifact Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0020
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, runtime seam
- Mechanic parents: runtime-seam
- Guard families: part-local artifact, validation guard, runtime seam
- Posture: accepted

## Context

The Runtime Seam `artifact-contracts` part already owned the runtime artifact
schemas, examples, invalid fixtures, and authority-claim adjunct. The dedicated
validator and focused tests still lived in root `scripts/` and `tests/`,
leaving the owning contract part dependent on a root utility posture.

AoA mechanics topology now treats package-specific validators and focused tests
as part-local once the mechanic has explicit route cards, provenance
accounting, and release-gate coverage.

## Decision

Move the runtime artifact contract validator and focused tests into
`mechanics/runtime-seam/parts/artifact-contracts/{scripts,tests}/`.

Make the part-local validator self-contained: it validates the active file set,
draft 2020-12 schema surfaces, artifact examples, authority-claim example, and
negative fixtures directly instead of importing `scripts/validate_agents.py`.
`scripts/validate_agents.py` remains the repo-wide coordinator by loading this
part-local validator explicitly.

Run the part-local tests from `scripts/release_check.py` so the move does not
weaken the release gate.

## Consequences

- `artifact-contracts` now owns its contract checks beside the payloads they
  protect.
- The former root validator/test paths are historical lookup facts preserved
  through Runtime Seam provenance and legacy maps.
- `validate_agents.py` still owns repo-wide orchestration and downstream
  coherence checks, but no longer has to be imported by this part-local
  validator.
- The part-local validator duplicates the small artifact-name list so it can
  break the former circular dependency cleanly.

## Verification

```bash
python mechanics/runtime-seam/parts/artifact-contracts/scripts/validate_artifact_contracts.py
python -m unittest discover -s mechanics/runtime-seam/parts/artifact-contracts/tests -p 'test_*.py'
python scripts/validate_agents.py
python scripts/release_check.py
```
