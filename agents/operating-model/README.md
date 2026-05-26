# Agent Operating Model

`agents/operating-model/` holds cross-role source contracts for how agent roles
operate together.

This branch is intentionally separate from `agents/roles/`: role houses own
role identity and nested forms; the operating model owns shared posture around
capability packs, tiers, orchestrator classes, cohort patterns, and
runtime-seam bindings.

## Branches

| Branch | Role |
| --- | --- |
| `capabilities/` | reusable permission, tool, skill, technique, memory, proof, and projection posture |
| `tiers/` | effort and handoff classes |
| `orchestrators/` | bounded orchestration class identity |
| `cohorts/` | inspectable role grouping hints |
| `runtime-seams/` | role x tier bindings for public runtime-seam phases |

Generated readers under `generated/` are derived from these source objects and
must not be hand-authored as truth.
