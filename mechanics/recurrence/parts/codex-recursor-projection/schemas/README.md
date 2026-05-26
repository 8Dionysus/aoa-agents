# Codex Recursor Projection Schemas

This schema keeps Codex recursor projection candidate-only. It describes the
reviewable projection source, not an installed subagent or runtime authority.

| Schema | Contract |
| --- | --- |
| [projection-candidate.schema.json](projection-candidate.schema.json) | candidate projection source for `recursor.witness` and `recursor.executor` |

Validate with:

```bash
python mechanics/recurrence/scripts/validate_recursor_contracts.py
```
