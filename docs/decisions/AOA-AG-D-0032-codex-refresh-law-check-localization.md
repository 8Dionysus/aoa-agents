# 2026-05-26: Codex Refresh Law Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0032
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, codex projection
- Mechanic parents: codex-projection
- Guard families: part-local artifact, validation guard, projection guard
- Posture: accepted

## Context

The Codex refresh-law document and example already live in
`mechanics/codex-projection/parts/refresh-law/`, but their validator and
focused tests still lived under root `scripts/` and `tests/`.

That made root helper districts responsible for a single part's contract and
kept the refresh-law operation package from owning its own check surface.

## Decision

Move the Codex refresh-law validator to
`mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py`.
Move the focused tests to
`mechanics/codex-projection/parts/refresh-law/tests/`.

Keep `scripts/validate_agents.py` as the repo-wide coordinator by loading the
part-local validator explicitly. Keep `scripts/release_check.py` responsible
for running the focused part tests in the release gate.

## Consequences

- The `refresh-law` part now owns its document, example, validator, and focused
  tests together.
- Root `scripts/` remains active for repo-wide orchestration and shared
  builders, not this part's local refresh-law contract.
- Former root lookup survives only through Codex Projection `PROVENANCE.md`
  and `legacy/`.

## Verification

```bash
python mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py
python -m unittest discover -s mechanics/codex-projection/parts/refresh-law/tests -p 'test_*.py'
python scripts/validate_agents.py
python scripts/release_check.py
```
