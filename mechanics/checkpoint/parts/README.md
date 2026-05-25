# Checkpoint Parts

`mechanics/checkpoint/parts/` is the lower index for active checkpoint and
continuity operation parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `self-agent-checkpoint/` | self-agent posture, checkpoint schema, and example route | `self-agent-checkpoint/README.md` |
| `continuity-lane/` | agent continuity without claiming durable memory truth | `continuity-lane/README.md` |
| `reviewed-closeout-hold/` | role hold before reviewed closeout promotes claims | `reviewed-closeout-hold/README.md` |
| `reference-routes/` | reference routes and alpha reference routes | `reference-routes/README.md` |
| `growth-checkpoint/` | checkpoint-facing progression and growth posture | `growth-checkpoint/README.md` |
| `stress-handoff/` | stress posture that needs reviewable survival boundaries | `stress-handoff/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
