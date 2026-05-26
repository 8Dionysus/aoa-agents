# 2026-05-26: Checkpoint Check Localization

## Status

Accepted.

## Context

Checkpoint contract payloads already live in the `self-agent-checkpoint` and
`continuity-lane` parts, but their dedicated validator and focused tests still
lived in root `scripts/` and `tests/`.

The check spans more than one part, so placing it under only
`self-agent-checkpoint` or only `continuity-lane` would make the route lie
about ownership. The owning mechanic package is the narrower truthful home.

## Decision

Move the checkpoint contract validator and focused tests into
`mechanics/checkpoint/{scripts,tests}/`.

Make the package-local validator self-contained: it validates the active file
sets, draft 2020-12 schema surfaces, examples, and negative fixtures directly
instead of importing `scripts/validate_agents.py`. `scripts/validate_agents.py`
remains the repo-wide coordinator by loading this package-local validator
explicitly.

Run the package-local tests from `scripts/release_check.py` so the release gate
continues to cover the moved tests.

## Consequences

- `mechanics/checkpoint/` now owns the contract checks that span its parts.
- Former root validator/test paths are historical lookup facts preserved
  through Checkpoint provenance and legacy maps.
- `validate_agents.py` still owns repo-wide coherence checks that compare
  checkpoint examples against agent profiles and generated registries.
- The package-local validator duplicates the small fixture expectation list so
  it can stay independent from the repo-wide coordinator.

## Verification

```bash
python mechanics/checkpoint/scripts/validate_checkpoint_contracts.py
python -m unittest discover -s mechanics/checkpoint/tests -p 'test_*.py'
python scripts/validate_agents.py
python scripts/release_check.py
```
