# Formation Schemas

These schemas define candidate-only Agon actor formation and formation-trial
contracts. They do not grant live arena protocol, verdict, scar, retention, or
runtime authority.

| Schema | Contract |
| --- | --- |
| [agent-kind.schema.json](agent-kind.schema.json) | agonic kind adjunct |
| [subjectivity.schema.json](subjectivity.schema.json) | agonic subjectivity adjunct |
| [office-overlay.schema.json](office-overlay.schema.json) | agonic office overlay adjunct |
| [resistance-revision.schema.json](resistance-revision.schema.json) | agonic resistance and revision adjunct |
| [formation-trial.schema.json](formation-trial.schema.json) | formation-trial reader |

Arena eligibility lives in the adjacent
[arena-rank-school schema route](../../arena-rank-school/schemas/arena-eligibility.schema.json).

Validate with:

```bash
python mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py
```
