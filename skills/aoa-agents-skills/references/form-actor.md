### Mode: form-actor

Turn one admitted obligation into a bounded role mandate. Preserve the role's
stable meaning separately from its replaceable model and process body.

## Input

Require one `agent-obligation-v1` plus exact owner refs for candidate base
roles, specializations, tiers, capability packs, and domain procedures. Missing
domain procedure truth is a handoff, not permission for `aoa-agents` to invent
it.

## Procedure

1. Resolve the smallest existing base role that can bear the obligation.
2. Add an existing specialization and capability pack when they narrow the
   mandate. Create neither merely to name the current task.
3. State required executor properties behaviorally: procedure discipline,
   initiative, scope control, handoff quality, tool competence, context span,
   latency, or other testable properties. Do not name a vendor or model.
4. Attach the domain skill or procedure by exact owner ref. It remains owned
   by that domain.
5. Define authority, permissions, effects, stop lines, named outputs, review,
   refusal, escalation, return, and wake posture.
6. Decide continuity posture:
   - `task-instance`: no identity beyond this obligation;
   - `role-continuity`: role identity and accumulated context may survive;
   - `persistent-office`: stable duty and relationships survive while process
     and model instances may disappear and later be restored.
7. Return an `actor-mandate-v1`. Do not bind a model or start a process.

## Output

The mandate records obligation and goal refs, actor identity posture, base role,
specialization, tier, capability packs, domain procedure refs, required
executor properties, authority/effects, specialized-environment requirements,
continuity and state roots, named outputs, return owner, review/refusal/wake
rules, expiry/review posture, uncertainty, and stop line.

For the first landing proof, existing `coder.repo-refactor` with
`repo-refactor.workspace-write` may bear bounded repo-local preparation, while
`evaluator.release-readiness` with `release-readiness.readonly` provides an
independent review. Neither becomes a permanent `landing-agent`, and remote
publication remains with its domain owner.
