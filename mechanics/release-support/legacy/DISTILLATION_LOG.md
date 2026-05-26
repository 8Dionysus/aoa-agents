# Release Support Legacy Distillation Log

## 2026-05-26 Root Docs To Active Parts

Moved 2 mechanics-facing docs out of root `docs/` and into active part-local `docs/` directories. Git history preserves the verbatim file bodies; `PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.

| Part | Moved docs |
| --- | --- |
| `repo-release-gate` | 1 |
| `runtime-release-hold` | 1 |

## 2026-05-26 Agent Release Hold Contract To Active Part

Moved the release-hold schema and example out of root `schemas/` and
`examples/` into active `runtime-release-hold` part-local routes. Git history
preserves the file bodies; `PROVENANCE.md` and `legacy/INDEX.md` preserve
old-path lookup.

| Part | Moved schemas | Moved examples |
| --- | ---: | ---: |
| `runtime-release-hold` | 1 | 1 |
