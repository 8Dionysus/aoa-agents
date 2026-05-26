# Formation Schemas

These schemas define candidate-only Agon actor formation and formation-trial
contracts. They do not grant live arena protocol, verdict, scar, retention, or
runtime authority.

| Schema | Contract |
| --- | --- |
| [agent-kind.schema.json](agent-kind.schema.json) | Wave I agonic kind adjunct |
| [subjectivity.schema.json](subjectivity.schema.json) | Wave I subjectivity adjunct |
| [office-overlay.schema.json](office-overlay.schema.json) | Wave I office overlay adjunct |
| [resistance-revision.schema.json](resistance-revision.schema.json) | Wave I resistance and revision adjunct |
| [formation-trial.schema.json](formation-trial.schema.json) | Wave II.5 formation-trial reader |

Arena eligibility lives in the adjacent
[arena-rank-school schema route](../../arena-rank-school/schemas/arena-eligibility.schema.json).

Validate with:

```bash
python mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py
```
