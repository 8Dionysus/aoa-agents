# Recursor Readiness Config

## Operating Card

| Field | Route |
| --- | --- |
| role | source seed configs for recursor role readiness and pair separation |
| input | reviewed witness/executor role contracts and pair boundary law |
| output | generated readiness index, pair contract reader, and boundary report |
| owner | `mechanics/recurrence/parts/recursor-readiness/` |
| next route | recursor readiness docs, boundary validators, generated readiness surfaces |
| tools | `mechanics/recurrence/scripts/build_recursor_role_readiness.py`, `mechanics/recurrence/scripts/validate_recursor_role_readiness.py`, `mechanics/recurrence/scripts/validate_recursor_boundary.py` |
| validation | readiness builder with `--check` plus recursor validators |

## Active Seeds

- [roles.seed.json](roles.seed.json)
- [pair.seed.json](pair.seed.json)

## Boundaries

These seeds express readiness only. They do not create live recursor execution,
agent spawning, arena sessions, verdicts, scar writes, or hidden scheduling.
