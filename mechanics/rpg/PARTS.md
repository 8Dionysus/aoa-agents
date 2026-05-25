# RPG Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `progression-model` | agent progression and mastery posture | `docs/AGENT_PROGRESSION_MODEL.md`; progression schemas/examples if present |
| `cohort-patterns` | role grouping and progression-readable cohorts | `agents/cohort_patterns/*.pattern.json`; generated cohort registry |
| `quest-readable-status` | progress posture exposed to quest surfaces | `docs/QUEST_EXECUTION_PASSPORT.md`; `mechanics/questbook/` |
| `checkpoint-growth` | growth status that must pass through reviewed checkpoint posture | `docs/WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md`; `mechanics/checkpoint/` |

## Move Posture

This is a thin package. Keep it as a skeleton until progression has more
source contracts than public route language.
