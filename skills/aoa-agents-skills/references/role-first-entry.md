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

For an ordinary step or convenience split, return to native Codex work without
compiling a negative receipt. When the request identifies an existing actor or
mandate, inspect and continue that lifecycle instead of running new formation.
Do not widen authority because a stronger model or runtime is available.

## Input

Normalize the request to role-first-intent-v1:

- goal: the anchored Goal in plain language;
- independent_duty: the one duty whose responsibility will move;
- authority: permissions, allowed effects, prohibited effects, and the
  explicit stop line;
- expected_result: one or more named semantic outcomes.
- execution_intent: optional `prepare` or `execute`; a direct current-holder
  imperative to form, assign, launch, or delegate the actor means `execute`,
  while planning, exploration, or a request to inspect the route means
  `prepare`.

This is the only caller-facing packet. All current-holder, workspace, domain,
return-owner, continuation, and runtime facts are resolved from the active
session and stronger owner contracts. Never ask the caller to supply a
summon-request-v4, owner roots, digests, or a model-specific command.

## Make the semantic choices once

Preserve Goal, holder, duty, authority, expected outputs, return owner, and the
stop line. Use the request and available context; ask only for a missing choice
that materially changes the mandate. A complete instruction to execute
supplies apply authority within that scope; a planning request does not.

Resolve the owner once through [source-return.md](source-return.md). Compare
the authored role and specialization candidates with the duty, choose a tier
from the role's `preferred_tier_ids`, and retain the specialization's exact
`capability_pack_ref` when present. Selection belongs to the holder, not list
order or a generated graph. Choose a current model-fit candidate for the
mandate's required behavior; preserve an explicit operator model choice and
report incompatibility instead of silently substituting another model.

The obligation and mandate carry responsibility meaning. Model, runtime,
process, and budget fields belong to the incarnation and execution bindings.
The current environment supplies exact owner roots, runtime profile,
workspace, and continuation evidence; missing bindings are integration gaps,
not fields for the user to invent.

## Compile the technical chain once

Use the existing passive preparer in the resolved `aoa-agents` owner:

```bash
python <aoa-agents-root>/skills/aoa-summon/scripts/prepare_external_actor.py \
  --spec <actor-route-preparation.json> --output-dir <new-preparation-dir>
```

The internal spec is `actor-route-preparation-v1`: semantic obligation,
`role_selection`, mandate, selected model fit, domain-procedure refs, and exact
execution-context inputs. Read the preparer's `--help` and linked schema when
building that spec, not every downstream packet schema.

The preparer already calls the obligation/mandate compiler, role resolver,
model-fit query, SDK transport and incarnation compilers, and final request
compiler. It derives their IDs, digests, provenance, DAG, transfer packet, and
launch-manifest input. Do not assemble those outputs by hand or invoke the
individual compilers first to reproduce what the preparer does. A focused
repair of an existing packet may still use the corresponding leaf compiler.

Preparation performs no launch. Preserve its outputs and any exact missing
owner input; do not rerun the chain with invented authority to make it pass.

## Apply and receive through supported runtime interfaces

Review the resulting role/model binding, permitted effects, outputs, stop
line, return owner, and external runtime against the request. For `prepare`,
return `awaiting_apply`. For an authorized `execute`, continue in the same
turn without requesting the same authority again.

Use `aoa-summon` only with the complete compiled packet and inspected external
binding. Actual execution must expose a separate process, persistent session,
and runtime-owned continuation/event handles. A native Codex child is not a
replacement for this external lane.

Keep the parent Goal and existing duty identity. Use the runtime's supported
wait/return/wake interface and [receive-return.md](receive-return.md) for the
result. An unavailable integration returns its exact blocker; do not emulate
Goal pause/resume, create a second observer, or interpret process exit as
responsibility acceptance.

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

Return the useful result or exact blocker, the current holder and next action,
actual effects, named-output checks, and unresolved uncertainty. Link the
typed artifacts for stages actually reached; do not repeat the technical
assembly transcript or claim that prepared handles prove execution.

## Verification and stop

- The caller-facing request contains no low-level JSON, digest, owner-root, or
  model-brand requirement.
- The role is an existing owner-authored role or specialization; model
  realization remains replaceable.
- The selected tier is declared by the selected base role, and a selected
  specialization's capability pack is the exact authored source ref rather
  than a task-derived or generated name.
- The selected model has current fit evidence and explicit current-holder
  selection authority.
- The SDK and runtime bind the exact mandate and environment; configuration is
  not reported as a launch.
- The compiled route is previewed and explicit apply is recorded before any
  runtime mutation. `prepare` awaits a later apply; a complete explicit
  `execute` request supplies apply authority in the same request. An
  awaiting-apply result has no process effect.
- External execution has separate process/session evidence and does not use
  built-in Codex spawn.
- Responsibility, actual effects, named outputs, review, return, and usage
  observations are separately evidenced.
- Stop when a required semantic choice or stronger-owner binding remains
  unresolved after bounded inspection. Preserve the obligation and name its
  next owner; missing execution infrastructure does not forbid unrelated
  native Codex work already in scope.
