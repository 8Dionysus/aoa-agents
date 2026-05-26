# RPG Legacy Distillation Log

## 2026-05-26 Root Docs To Active Parts

Moved 2 mechanics-facing docs out of root `docs/` and into active part-local `docs/` directories. Git history preserves the verbatim file bodies; `PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.

| Part | Moved docs |
| --- | --- |
| `cohort-patterns` | 1 |
| `progression-model` | 1 |

## 2026-05-26 Root Progression Payloads To Active Part

Moved 1 schema and 1 example out of root support districts and into the active
`progression-model` part. Git history preserves the verbatim file bodies;
`PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.

| Part | Moved schemas | Moved examples |
| --- | ---: | ---: |
| `progression-model` | 1 | 1 |

## 2026-05-26 Root Progression Validator To Active Part

Moved the RPG progression validator out of root `scripts/` and into the active
`progression-model` part. Added part-local focused tests while keeping
`scripts/validate_agents.py` as the repo-wide coordinator.

| Part | Moved scripts | Added tests |
| --- | ---: | ---: |
| `progression-model` | 1 | 1 |
