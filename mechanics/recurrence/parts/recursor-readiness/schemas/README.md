# Recursor Readiness Schemas

These schemas define the part-local recurrence contracts for the witness/executor
readiness lane.

| Schema | Contract |
| --- | --- |
| [role-contract.schema.json](role-contract.schema.json) | candidate-only witness/executor role contract |
| [pair-contract.schema.json](pair-contract.schema.json) | witness/executor separation and handoff-order contract |
| [readiness-index.schema.json](readiness-index.schema.json) | generated readiness reader contract |
| [handoff-ledger.schema.json](handoff-ledger.schema.json) | example handoff/receipt envelope contract |
| [session-intent.schema.json](session-intent.schema.json) | example recursor session-intent contract |

Stable `$id` values remain public contract identifiers. Active lookup for these
files is this part-local `schemas/` route.

Validate with:

```bash
python mechanics/recurrence/scripts/validate_recursor_contracts.py
```
