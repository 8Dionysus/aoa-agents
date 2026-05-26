# Recursor Readiness Examples

These examples demonstrate the part-local readiness contracts without creating
a live spawn, scheduler, arena, or durable memory write.

| Example | Schema |
| --- | --- |
| [session-intent.example.json](session-intent.example.json) | [../schemas/session-intent.schema.json](../schemas/session-intent.schema.json) |
| [witness-handoff.example.json](witness-handoff.example.json) | [../schemas/handoff-ledger.schema.json](../schemas/handoff-ledger.schema.json) |
| [executor-receipt.example.json](executor-receipt.example.json) | [../schemas/handoff-ledger.schema.json](../schemas/handoff-ledger.schema.json) |

Validate with:

```bash
python scripts/validate_recursor_contracts.py
```
