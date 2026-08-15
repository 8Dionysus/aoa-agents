### Mode: role-first-entry

Turn one explicit semantic request into the smallest valid external actor
route. This mode is the ordinary front door for the sentence:

> In this Goal an independent obligation has appeared; form and embody the
> appropriate actor.

It is an explicit delegation of one bounded branch, not keyword autospawn and
not a request to launch whatever model happens to be available.

## Applicability

Use this mode when the current holder supplies a Goal, an independent duty,
an authority envelope, and an expected result, and intends responsibility to
move to a separately addressable actor. The current Codex session supplies
the current holder, session, workspace, and phase context; the caller does not
need to know owner roots, digests, JSON packet shapes, or CLI assembly.

Return not_applicable or stop for clarification when the work is an ordinary
step, a convenience split, or a model-launch request without an independent
responsibility boundary. Do not widen authority because a stronger model or
runtime is available.

## Input

Normalize the request to role-first-intent-v1:

- goal: the anchored Goal in plain language;
- independent_duty: the one duty whose responsibility will move;
- authority: permissions, allowed effects, prohibited effects, and the
  explicit stop line;
- expected_result: one or more named semantic outcomes.

This is the only caller-facing packet. All current-holder, workspace, domain,
return-owner, continuation, and runtime facts are resolved from the active
session and stronger owner contracts. Never ask the caller to supply a
summon-request-v4, owner roots, digests, or a model-specific command.

## Procedure

1. Preserve the four semantic fields and identify the current responsibility
   holder from the active Goal/session. Reject an absent or contradictory
   authority envelope before any route is formed.
2. Convert the intent into the internal goal-pressure-v1 context and run
   detect-obligation. Require explicit positive and negative independence
   signals, a trigger strength, the missed consequence, a return owner, and a
   stop line. If the duty is not independent, stop with the typed disposition.
3. Execute the bounded owner-source route for `role-first-entry` in
   references/source-return.md. Read the admitted `aoa-agents` orientation
   surfaces first, then inspect only the exact authored role and
   specialization sources needed for the semantic choice. Resolve stronger
   owners through their own gates; do not broaden a missing ref into a
   repository-wide search.
4. Form one bounded agent-obligation-v1, then choose an existing aoa-agents
   role or specialization whose authored meaning bears that duty. Do not mint
   a task-named role. Use the exact role resolver only after the semantic
   choice and preserve the role's owner refs.
5. Form actor-mandate-v1 from the obligation, selected role chain, domain
   procedure, authority, continuity, named outputs, refusal, review, and wake
   posture. Keep model names, reasoning modes, process handles, and budgets
   out of the obligation, role, and mandate.
6. Ask aoa-models for current fit candidates for the mandate's behavioral
   properties. The current holder selects one candidate using its evidence and
   records the selection authority; the model owner does not route, launch, or
   grant permissions. If fit is absent or ambiguous, stop rather than silently
   choosing a brand or the first catalog entry.
7. Ask aoa-sdk to compile the caller-selected RunPlan and
   agent-incarnation-binding-v2, then resolve the specialized environment,
   permissions, continuation, and external runtime profile through
   abyss-stack. Usage is an observation only; this mode adds no budget gate.
8. Materialize the internal actor-route-preparation-v1 spec and invoke the
   passive aoa-summon preparer. It must create the obligation, mandate, role,
   model-fit query, SDK binding, task-local DAG, transfer, and
   summon-request-v4 artifacts without starting a process. Keep these
   artifacts in the active task-local state root, not in owner skill source.
9. Present a bounded preview to the current holder before any runtime
   mutation. The preview includes the selected role and owner refs, fit
   projection and selection authority, SDK/runtime binding, permissions,
   expected effects, prohibited effects, stop line, named outputs, rollback,
   return owner, and the exact external execution lane. Do not launch while
   the preview is awaiting review. Require a separate explicit apply
   confirmation from the current holder; the initial semantic request is not
   itself apply confirmation. Without that confirmation, return
   `awaiting_apply` with the prepared handles and no process effect.
10. Select aoa-summon only after the packet is complete and the inspected
   abyss-stack binding is available. Execute the external CLI lane through
   that runtime so the actor has a separate OS process, session, state root,
   continuation, and usage receipts. Do not use built-in Codex child agents or
   equate a transport handle with A2A responsibility.
11. Record responsibility movement from the current holder to the actor and
   leave the parent Goal/DAG reference intact. On pause, resume, refusal,
   failure, or return, use the runtime event and receive-return procedure to
   filter named outputs, actual effects, review state, open uncertainty, and
   the next holder. A return is not accepted merely because a process exited.

## Owner handoffs

| Concern | Owner | Role-first action |
| --- | --- | --- |
| obligation, role, mandate, responsibility, return | aoa-agents | detect, form, transfer, and filter meaning |
| fit evidence and realization | aoa-models | query current candidates; preserve selection authority |
| RunPlan and incarnation v2 | aoa-sdk | compile the exact caller-selected binding |
| process, session, state, resume, events, usage | abyss-stack | inspect and execute the external runtime |
| domain procedure and acceptance | named domain owner | supply the procedure and review route |
| task-local DAG grammar | aoa-skills | validate composition without owning actor meaning |

No owner handoff may turn a model, runtime, domain procedure, transport, or
generated graph into the source of responsibility.

## Output

Return one typed lifecycle result that preserves, when the route reaches each
stage, the semantic intent, goal-pressure disposition, obligation, mandate,
   exact role resolution, model-fit query and selected projection, SDK
   incarnation binding v2, runtime/environment binding, responsibility
   transfer, preview and explicit-apply evidence, external
   process/session/continuation handles, summon request/result, named outputs,
   filtered return, next holder, usage observations, uncertainty, and stop
   line. A shorter result must name the exact missing owner input and next
   route.

## Verification and stop

- The caller-facing request contains no low-level JSON, digest, owner-root, or
  model-brand requirement.
- The role is an existing owner-authored role or specialization; model
  realization remains replaceable.
- The selected model has current fit evidence and explicit current-holder
  selection authority.
- The SDK and runtime bind the exact mandate and environment; configuration is
  not reported as a launch.
- The compiled route is previewed and explicit apply is recorded before any
  runtime mutation; an awaiting-apply result has no process effect.
- External execution has separate process/session evidence and does not use
  built-in Codex spawn.
- Responsibility, actual effects, named outputs, review, return, and usage
  observations are separately evidenced.
- Stop at the first missing goal, duty, authority, expected result, role,
  domain procedure, fit, SDK binding, runtime binding, return owner, or
  validation input. Preserve the unresolved obligation for the current holder.
