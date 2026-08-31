# RPG Parts

`mechanics/rpg/parts/` is the lower index for active progression and mastery
posture parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `progression-model/` | agent progression and mastery posture | `progression-model/README.md` |
| `cohort-patterns/` | role grouping and progression-readable cohorts | `cohort-patterns/README.md` |
| `quest-readable-status/` | progress posture exposed to quest surfaces | Route to Questbook/root quest sources and readers; no placeholder README is materialized. |
| `checkpoint-growth/` | growth status that must pass through reviewed checkpoint posture | Route to Checkpoint `growth-checkpoint/`; no placeholder README is materialized. |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
