# 2026-05-26: Assistant Projection Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0033
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, assistant civil, codex projection
- Mechanic parents: experience, codex-projection
- Guard families: part-local artifact, validation guard, projection guard
- Posture: accepted

## Context

The assistant projection resolver payloads already lived in
`mechanics/codex-projection/parts/assistant-projection/`, but their validator
still lived in root `scripts/` and the focused resolver test still lived in
root `tests/` as a pytest-style function.

That left the active contract in the right part while its check surface stayed
root-level. It also meant the focused test was outside the current
`release_check.py` `unittest` route.

## Decision

Move the validator to
`mechanics/codex-projection/parts/assistant-projection/scripts/` and move the
focused resolver test to
`mechanics/codex-projection/parts/assistant-projection/tests/`.

Keep `scripts/validate_agents.py` as the repo-wide coordinator by loading the
part-local validator explicitly. Add the part-local resolver tests to
`scripts/release_check.py`.

## Consequences

- The `assistant-projection` part owns both payloads and the focused check.
- Root `scripts/` keeps only repo-level coordination for this contract.
- Root `tests/` keeps broader repo tests; the resolver-specific test now runs
  in the part-local release route.
- Former root paths remain discoverable only through `PROVENANCE.md` and
  `legacy/`.

## Verification

```bash
python mechanics/codex-projection/parts/assistant-projection/scripts/validate_assistant_projection_resolver.py
python -m unittest discover -s mechanics/codex-projection/parts/assistant-projection/tests -p 'test_*.py'
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/release_check.py
```
