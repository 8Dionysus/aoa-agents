# RPG Parts

`mechanics/rpg/parts/` is the lower index for active progression and mastery
posture parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `progression-model/` | agent progression and mastery posture | `progression-model/README.md` |
| `cohort-patterns/` | role grouping and progression-readable cohorts | `cohort-patterns/README.md` |
| `quest-readable-status/` | progress posture exposed to quest surfaces | `quest-readable-status/README.md` |
| `checkpoint-growth/` | growth status that must pass through reviewed checkpoint posture | `checkpoint-growth/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
