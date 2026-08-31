# generated/AGENTS.md

## Role

`generated/` contains derived reader surfaces published from source-authored
agent objects, quests, and mechanic payloads. Use [README.md](README.md) for
the human reader-family inventory.

## Boundaries

- Do not hand edit anything under `generated/`.
- Source objects and builders own meaning; generated readers are projections.
- The source families include `agents/operating-model/cohorts/` and role,
  tier, orchestrator, runtime-seam, quest, and mechanic part inputs.
- `orchestrator_class_catalog.min.json` and sibling readers are derived
  outputs, not authority.

## Route

When a generated reader is stale, inspect its source owner and builder, then
use the repository [validation map](../VALIDATION.md). Preserve source,
builder, generated output, and validator as separate evidence classes.

## Closeout

Report the source owner, builder, generated outputs inspected, checks run,
checks skipped, and any stronger-owner handoff.
