# Self-Agency Continuity Lane

## Purpose

This note hardens the agent-layer landing for self-agency continuity.

The agent layer does not own runtime retries, memory canon, or proof truth.
It owns the role-facing contract for explicit continuity, bounded revision, and
return through named anchor artifacts.

## Core rule

A continuity route is valid only when the acting role can still name:

- the active continuity thread
- the current revision window
- the last valid anchor artifact
- the reanchor path to that artifact if drift appears

If those cannot be named, the route should return rather than improvise.

## Public continuity window

The schema-backed continuity window lives at
`schemas/self-agency-continuity-window.schema.json`.

The inspectable example lives at
`examples/self_agent_checkpoint/self_agency_continuity_window.example.json`.

At the current baseline, a public continuity window should be able to state:

- `continuity_ref`
- `revision_window_ref`
- `reanchor_ref`
- `anchor_artifact_ref`
- `continuity_status`
- `agent_id`
- `role`
- `memory_scope`
- `approval_mode`
- `rollback_marker`
- `max_iterations`

## Continuity status posture

Keep `continuity_status` inside a small explicit grammar:

- `active`
- `reanchor_needed`
- `reanchored`
- `closed`

This status names route posture.
It does not claim runtime success or final object quality.

## Return discipline

Return is legitimate when:

- the current actor can no longer state the active bounded route
- source-of-truth fit has drifted
- verification posture was lost
- the revision window widened without a new bounded plan
- repeated contradiction makes forward motion theatrical

Return must target a prior valid public artifact.
It must not target vague chat continuity.

## Cohort posture

A portable continuity route should usually keep:

- `architect` for route and anchor naming
- `coder` for bounded mutation only after approval
- `reviewer` for boundedness and health
- `memory-keeper` for provenance-thread legibility

No new role family is required.
The portable route still maps to `checkpoint_cohort`.

## Boundaries to preserve

- `aoa-playbooks` owns recurring continuity choreography
- `aoa-memo` owns continuity support writeback through existing memory kinds
- `aoa-evals` owns proof about continuity quality
- `aoa-sdk` may carry continuity hints, but not reviewed continuity truth
- `abyss-stack` still owns runtime context rebuild, retries, and wrapper policy

## One-line rule

The agent layer may publish continuity posture and anchor-return contracts, but
it does not turn self-agency into free runtime autonomy.
