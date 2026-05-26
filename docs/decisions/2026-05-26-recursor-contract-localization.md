# 2026-05-26: Recursor Contract Localization

## Status

Accepted.

## Context

Recursor readiness already had part-local docs, configs, generated readers, and
boundary validators, but its schema-backed contracts still lived in root
`schemas/` and `examples/`. That kept the active lookup topology split across
root districts even though the operation is recurrence-local: witness/executor
readiness, candidate-only Codex projection, and Agon boundary stop-lines.

## Decision

Move recursor contract payloads into their owning recurrence parts:

- readiness role, pair, index, ledger, and session-intent contracts move into
  `mechanics/recurrence/parts/recursor-readiness/{schemas,examples}/`;
- projection-candidate schema moves into
  `mechanics/recurrence/parts/codex-recursor-projection/schemas/`;
- boundary-report schema and example move into
  `mechanics/recurrence/parts/agon-recursor-boundary/{schemas,examples}/`;
- `mechanics/recurrence/scripts/validate_recursor_contracts.py` becomes the package-local contract
  validator and is called by `scripts/validate_agents.py`.

Stable schema `$id` values remain unchanged as public contract identifiers.
Former root paths are recorded only through recurrence `PROVENANCE.md` and
`legacy/`.

## Consequences

Recursor schema/example edits now start in the recurrence part that owns the
operation. Root `schemas/` and `examples/` no longer act as active homes for
these contracts, while generated recursor readers remain derived surfaces under
`generated/`.

Validation for this route is:

```bash
python mechanics/recurrence/scripts/validate_recursor_contracts.py
python mechanics/recurrence/scripts/build_recursor_role_readiness.py --check
python mechanics/recurrence/scripts/build_recursor_projection_candidates.py --check
python mechanics/recurrence/scripts/validate_recursor_role_readiness.py
python mechanics/recurrence/scripts/validate_recursor_boundary.py
python scripts/validate_agents.py
python -m unittest discover -s mechanics/recurrence/tests -p 'test_*.py'
```
