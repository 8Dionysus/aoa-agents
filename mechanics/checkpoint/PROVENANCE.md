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

## 2026-05-26 Reference Route Contract Move

1 reference-route manifest schema and 18 route-pack example files moved from
root `schemas/` and `examples/` into the checkpoint `reference-routes` part.
Active route-pack directories use kebab-case package names while stable
manifest `route_id` values remain contract identifiers.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/reference-route.example.schema.json` | [parts/reference-routes/schemas/reference-route-manifest.schema.json](parts/reference-routes/schemas/reference-route-manifest.schema.json) | `reference-routes` |
| `examples/reference_routes/AGENTS.md` | [parts/reference-routes/examples/README.md](parts/reference-routes/examples/README.md) | `reference-routes` |
| `examples/reference_routes/solo_bounded_route/manifest.json` | [parts/reference-routes/examples/solo-bounded-route/manifest.json](parts/reference-routes/examples/solo-bounded-route/manifest.json) | `reference-routes` |
| `examples/reference_routes/solo_bounded_route/route_decision.json` | [parts/reference-routes/examples/solo-bounded-route/route_decision.json](parts/reference-routes/examples/solo-bounded-route/route_decision.json) | `reference-routes` |
| `examples/reference_routes/pair_change_route/manifest.json` | [parts/reference-routes/examples/pair-change-route/manifest.json](parts/reference-routes/examples/pair-change-route/manifest.json) | `reference-routes` |
| `examples/reference_routes/pair_change_route/verification_result.json` | [parts/reference-routes/examples/pair-change-route/verification_result.json](parts/reference-routes/examples/pair-change-route/verification_result.json) | `reference-routes` |
| `examples/reference_routes/pair_change_route/work_result.json` | [parts/reference-routes/examples/pair-change-route/work_result.json](parts/reference-routes/examples/pair-change-route/work_result.json) | `reference-routes` |
| `examples/reference_routes/checkpoint_self_change_route/bounded_plan.json` | [parts/reference-routes/examples/checkpoint-self-change-route/bounded_plan.json](parts/reference-routes/examples/checkpoint-self-change-route/bounded_plan.json) | `reference-routes` |
| `examples/reference_routes/checkpoint_self_change_route/distillation_pack.json` | [parts/reference-routes/examples/checkpoint-self-change-route/distillation_pack.json](parts/reference-routes/examples/checkpoint-self-change-route/distillation_pack.json) | `reference-routes` |
| `examples/reference_routes/checkpoint_self_change_route/manifest.json` | [parts/reference-routes/examples/checkpoint-self-change-route/manifest.json](parts/reference-routes/examples/checkpoint-self-change-route/manifest.json) | `reference-routes` |
| `examples/reference_routes/checkpoint_self_change_route/verification_result.json` | [parts/reference-routes/examples/checkpoint-self-change-route/verification_result.json](parts/reference-routes/examples/checkpoint-self-change-route/verification_result.json) | `reference-routes` |
| `examples/reference_routes/checkpoint_self_change_route/work_result.json` | [parts/reference-routes/examples/checkpoint-self-change-route/work_result.json](parts/reference-routes/examples/checkpoint-self-change-route/work_result.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/bounded_plan.json` | [parts/reference-routes/examples/orchestrated-loop-route/bounded_plan.json](parts/reference-routes/examples/orchestrated-loop-route/bounded_plan.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/deep_synthesis_note.json` | [parts/reference-routes/examples/orchestrated-loop-route/deep_synthesis_note.json](parts/reference-routes/examples/orchestrated-loop-route/deep_synthesis_note.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/distillation_pack.json` | [parts/reference-routes/examples/orchestrated-loop-route/distillation_pack.json](parts/reference-routes/examples/orchestrated-loop-route/distillation_pack.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/manifest.json` | [parts/reference-routes/examples/orchestrated-loop-route/manifest.json](parts/reference-routes/examples/orchestrated-loop-route/manifest.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/route_decision.json` | [parts/reference-routes/examples/orchestrated-loop-route/route_decision.json](parts/reference-routes/examples/orchestrated-loop-route/route_decision.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/transition_decision.json` | [parts/reference-routes/examples/orchestrated-loop-route/transition_decision.json](parts/reference-routes/examples/orchestrated-loop-route/transition_decision.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/verification_result.json` | [parts/reference-routes/examples/orchestrated-loop-route/verification_result.json](parts/reference-routes/examples/orchestrated-loop-route/verification_result.json) | `reference-routes` |
| `examples/reference_routes/orchestrated_loop_route/work_result.json` | [parts/reference-routes/examples/orchestrated-loop-route/work_result.json](parts/reference-routes/examples/orchestrated-loop-route/work_result.json) | `reference-routes` |
