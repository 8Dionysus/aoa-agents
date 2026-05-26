# Arena Rank School Schemas

These schemas define candidate-only Agon arena, rank, jurisdiction, school,
lineage, and campaign posture contracts. They do not grant live verdict
authority, rank mutation, school canon, or campaign runtime.

| Schema | Contract |
| --- | --- |
| [arena-eligibility.schema.json](arena-eligibility.schema.json) | candidate arena-seat posture |
| [rank-jurisdiction.schema.json](rank-jurisdiction.schema.json) | rank/jurisdiction entry |
| [rank-jurisdiction-registry.schema.json](rank-jurisdiction-registry.schema.json) | generated rank/jurisdiction registry |
| [school-campaign-posture.schema.json](school-campaign-posture.schema.json) | school/campaign posture entry |
| [school-campaign-posture-registry.schema.json](school-campaign-posture-registry.schema.json) | generated school/campaign posture registry |

Validate with:

```bash
python mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py
python mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py
```
