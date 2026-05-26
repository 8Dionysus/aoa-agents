# 2026-05-26: Codex Refresh Law Example Localization

## Status

Accepted.

## Context

The Codex subagent refresh-law doc and wiring config already lived in
`mechanics/codex-projection/parts/*`, but the public refresh-law example still
lived in root `examples/`. That made a mechanic-owned route example look like
a shared root example even though its operation owner was the
`refresh-law` part.

## Decision

Move the Codex subagent projection refresh-law example into
`mechanics/codex-projection/parts/refresh-law/examples/` and preserve old root
lookup through Codex Projection `PROVENANCE.md` and `legacy/`.

Add an explicit Codex refresh-law validator so repo validation checks the
part-local example, former root-path absence, live surface patterns, refresh
routes, drift route classes, and rollback anchors. The validator later moved
into the active part route:
`mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py`.

## Consequences

Root `examples/` no longer owns the Codex refresh-law example.

The example remains a route contract for generated Codex projection refresh;
it is not generated output and not installed workspace state.

Validation for this route is:

```bash
python mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py
python -m unittest discover -s mechanics/codex-projection/parts/refresh-law/tests -p 'test_*.py'
python scripts/validate_agents.py
```
