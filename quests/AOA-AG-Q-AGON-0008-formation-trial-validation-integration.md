# AOA-AG-Q-AGON-0008: Formation Trial Validation Integration

## Objective

Decide how the Formation Trial validator enters the normal repo validation contour.

## Suggested integration

After owner review, call:

```bash
python scripts/validate_agent_formation_trial.py
```

from the main validation route or release check path.

## Stop-line

Do not make this integration silently open arena protocol work inside `aoa-agents`.
