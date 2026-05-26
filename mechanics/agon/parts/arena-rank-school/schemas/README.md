# Arena Rank School Schemas

These schemas define candidate-only Agon rank, jurisdiction, school, lineage,
and campaign posture contracts. They do not grant live verdict authority,
rank mutation, school canon, or campaign runtime.

| Schema | Contract |
| --- | --- |
| [rank-jurisdiction.schema.json](rank-jurisdiction.schema.json) | Wave XIV rank/jurisdiction entry |
| [rank-jurisdiction-registry.schema.json](rank-jurisdiction-registry.schema.json) | generated Wave XIV registry |
| [school-campaign-posture.schema.json](school-campaign-posture.schema.json) | Wave XVI school/campaign posture entry |
| [school-campaign-posture-registry.schema.json](school-campaign-posture-registry.schema.json) | generated Wave XVI registry |

Validate with:

```bash
python scripts/validate_agon_rank_epistemic_contracts.py
```
