# Checkpoint Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `self-agent-checkpoint` | self-agent posture, checkpoint schema, and example route | `docs/SELF_AGENT_CHECKPOINT.md`; `examples/self_agent_checkpoint/`; `schemas/self_agent_checkpoint/` |
| `continuity-lane` | agent continuity without claiming durable memory truth | `docs/AGENT_CONTINUITY.md`; continuity examples and schemas |
| `reviewed-closeout-hold` | role hold before reviewed closeout promotes memory, quest, or progression claims | reviewed closeout docs/examples; checkpoint note route surfaces |
| `reference-routes` | reference routes and alpha reference routes as checkpoint-readable surfaces | `examples/reference_routes/`; `examples/alpha_reference_routes/`; related docs |
| `growth-checkpoint` | checkpoint-facing progression and growth posture | `docs/WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md`; `agents/cohort_patterns/checkpoint_cohort.pattern.json`; cross-route to `mechanics/rpg/` |
| `stress-handoff` | stress posture where checkpoint needs reviewable survival boundaries | `docs/AGENT_STRESS_POSTURE.md`; `examples/agent_stress_posture.example.json`; cross-route to `mechanics/antifragility/` |

## Move Posture

Checkpoint files are intentionally split between docs, examples, schemas, and
cohort source objects. Do not collapse them into this package until memory,
proof, and playbook stop-lines are covered by validators.
