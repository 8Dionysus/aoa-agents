# Checkpoint Legacy Distillation Log

## 2026-05-26 Root Docs To Active Parts

Moved 6 mechanics-facing docs out of root `docs/` and into active part-local `docs/` directories. Git history preserves the verbatim file bodies; `PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.

| Part | Moved docs |
| --- | --- |
| `continuity-lane` | 1 |
| `growth-checkpoint` | 1 |
| `reference-routes` | 1 |
| `reviewed-closeout-hold` | 1 |
| `self-agent-checkpoint` | 2 |

## 2026-05-26 Checkpoint Contracts To Active Parts

Moved checkpoint contract payloads out of root `schemas/` and `examples/`
into active checkpoint part-local routes.

| Part | Moved schemas | Moved example route, examples, and fixtures |
| --- | ---: | ---: |
| `self-agent-checkpoint` | 1 | 5 |
| `continuity-lane` | 1 | 1 |

The former shared example `AGENTS.md` became an active README for the
`self-agent-checkpoint` examples. The continuity example now has its own
`continuity-lane` examples route. Git history preserves the file bodies;
`PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.
