# Checkpoint Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

Open `legacy/` only for former path lookup, raw receipt intake, or distillation history. Former root file names stay historical here; active parts use their current route names.

## 2026-05-26 Root Docs Move

6 mechanics-facing docs moved from `docs/` into `checkpoint/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/SELF_AGENCY_CONTINUITY_LANE.md` | [parts/continuity-lane/docs/self-agency-continuity-lane.md](parts/continuity-lane/docs/self-agency-continuity-lane.md) | `continuity-lane` |
| `docs/WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md` | [parts/growth-checkpoint/docs/workspace-checkpoint-growth-role-posture.md](parts/growth-checkpoint/docs/workspace-checkpoint-growth-role-posture.md) | `growth-checkpoint` |
| `docs/REFERENCE_ROUTE_EXAMPLES.md` | [parts/reference-routes/docs/reference-route-examples.md](parts/reference-routes/docs/reference-route-examples.md) | `reference-routes` |
| `docs/REVIEWED_CLOSEOUT_ROLE_POSTURE_HOLD.md` | [parts/reviewed-closeout-hold/docs/reviewed-closeout-role-posture-hold.md](parts/reviewed-closeout-hold/docs/reviewed-closeout-role-posture-hold.md) | `reviewed-closeout-hold` |
| `docs/SELF_AGENT_CHECKPOINT_STACK.md` | [parts/self-agent-checkpoint/docs/self-agent-checkpoint-stack.md](parts/self-agent-checkpoint/docs/self-agent-checkpoint-stack.md) | `self-agent-checkpoint` |
| `docs/SELF_RECHARTER_RUNTIME_BLOCK.md` | [parts/self-agent-checkpoint/docs/self-recharter-runtime-block.md](parts/self-agent-checkpoint/docs/self-recharter-runtime-block.md) | `self-agent-checkpoint` |

## 2026-05-26 Checkpoint Contract Move

2 checkpoint schemas and 6 example-route, example, and fixture files moved
from root `schemas/` and `examples/` into checkpoint part-local routes.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/self-agent-checkpoint.schema.json` | [parts/self-agent-checkpoint/schemas/self-agent-checkpoint.schema.json](parts/self-agent-checkpoint/schemas/self-agent-checkpoint.schema.json) | `self-agent-checkpoint` |
| `examples/self_agent_checkpoint/AGENTS.md` | [parts/self-agent-checkpoint/examples/README.md](parts/self-agent-checkpoint/examples/README.md) | `self-agent-checkpoint` |
| `examples/self_agent_checkpoint/self_agent_checkpoint.example.json` | [parts/self-agent-checkpoint/examples/self-agent-checkpoint.example.json](parts/self-agent-checkpoint/examples/self-agent-checkpoint.example.json) | `self-agent-checkpoint` |
| `examples/self_agent_checkpoint/invalid/self_agent_checkpoint.missing_required_field.json` | [parts/self-agent-checkpoint/examples/invalid/self-agent-checkpoint.missing-required-field.json](parts/self-agent-checkpoint/examples/invalid/self-agent-checkpoint.missing-required-field.json) | `self-agent-checkpoint` |
| `examples/self_agent_checkpoint/invalid/self_agent_checkpoint.invalid_approval_mode.json` | [parts/self-agent-checkpoint/examples/invalid/self-agent-checkpoint.invalid-approval-mode.json](parts/self-agent-checkpoint/examples/invalid/self-agent-checkpoint.invalid-approval-mode.json) | `self-agent-checkpoint` |
| `examples/self_agent_checkpoint/invalid/self_agent_checkpoint.max_iterations_below_minimum.json` | [parts/self-agent-checkpoint/examples/invalid/self-agent-checkpoint.max-iterations-below-minimum.json](parts/self-agent-checkpoint/examples/invalid/self-agent-checkpoint.max-iterations-below-minimum.json) | `self-agent-checkpoint` |
| `schemas/self-agency-continuity-window.schema.json` | [parts/continuity-lane/schemas/self-agency-continuity-window.schema.json](parts/continuity-lane/schemas/self-agency-continuity-window.schema.json) | `continuity-lane` |
| `examples/self_agent_checkpoint/self_agency_continuity_window.example.json` | [parts/continuity-lane/examples/self-agency-continuity-window.example.json](parts/continuity-lane/examples/self-agency-continuity-window.example.json) | `continuity-lane` |

Stable schema `$id` values remain public contract identifiers, not active repo
path authority.
