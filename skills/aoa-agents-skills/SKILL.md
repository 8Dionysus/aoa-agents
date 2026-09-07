---
name: aoa-agents-skills
description: Form, transfer, continue, or receive an independent AoA responsibility with a role-bearing actor. Use when an obligation needs its own holder, mandate, or continuity across incarnations. Ordinary tasks and native Codex helpers do not need this skill.
---

# aoa-agents-skills

Turn an independent obligation into a role-bearing actor with a bounded
mandate, replaceable incarnation, and explicit return owner. A role may retain
identity and responsibility while no process or model instance is running.

## When responsibility needs its own holder

Use judgment about the work, not the presence of an agent tool. A distinct
holder is useful when a branch must be carried autonomously to a return gate,
has its own authority envelope, or needs continuity beyond one process. A
convenient parallel read or bounded helper does not acquire that lifecycle.

For ordinary work, continue with Codex's native workflow and delegation rules.
Do not call the SDK router, mint a negative classification, or route a native
helper through summon merely to establish that this skill is unnecessary.
An instruction to work alone remains in force.

Before forming anything, check whether the request already identifies an
obligation, actor, mandate, or return. Reuse that identity. Session resumption
alone does not create a new obligation or require semantic reclassification.

## Work at the current lifecycle boundary

| Situation | Relevant procedure |
| --- | --- |
| A new independent duty needs an actor | [role-first-entry.md](references/role-first-entry.md) |
| An existing duty needs its incarnation inspected or replaced | [bind-incarnation.md](references/bind-incarnation.md) |
| A complete mandate must move to another holder | [transfer-responsibility.md](references/transfer-responsibility.md) |
| An actor returns, pauses, refuses, fails, or requests wake | [receive-return.md](references/receive-return.md) |

For a new duty, start with Goal, obligation, authority, and expected result
from the request and available context. Resolve only missing facts that change
the decision. Use [detect-obligation.md](references/detect-obligation.md) for
uncertain independence and [form-actor.md](references/form-actor.md) for role
and mandate detail; neither is a compulsory extra stage for every helper.

The model chooses the role, mandate, and current model fit. Existing owner
compilers assemble the exact technical packets and check their relations.
Read [source-return.md](references/source-return.md) before owner-relative
reads, resolving from the directory of this loaded skill. Keep that binding
for the operation; do not rediscover every owner at each semantic step.

Read [contract.yaml](references/contract.yaml) when exact ABI details matter,
and [task-local-dag.md](references/task-local-dag.md) when several duties need
composition. The explicit legacy classification operation is documented in
[responsibility-classification.md](references/responsibility-classification.md);
its receipt is not permission for ordinary Codex delegation.

## Continue without recreating the actor

Recover the existing obligation, mandate, holder, incarnation, and latest
runtime/return refs. Check the current authority and whether the observed
runtime can continue that incarnation. Changed credentials or an unavailable
runtime may require a new binding, not a new role or obligation. Changed duty
or authority requires the corresponding owner decision before more effects.

Use only the runtime's supported continuation and event interfaces. If a
required start, wait, or wake binding is unavailable, report that concrete
integration gap while preserving the duty. Do not create a second scheduler
or claim a Goal transition from an instruction, observer, or prepared packet.

## Keep ownership separate

`aoa-agents` owns responsibility, role/specialization, mandate, continuity,
required executor properties, and return meaning. Domain procedures stay with
their named skills; model fit with `aoa-models`; planning and incarnation
binding with `aoa-sdk`; process, persistence, and event transport with
`abyss-stack`; task-local graph grammar with `aoa-skills`.

Select roles from authored candidates. A tier must belong to the base role's
`preferred_tier_ids`; a specialization's exact `capability_pack_ref` remains
part of the selected chain. Then use the passive role resolver and obligation/
mandate compiler to preserve exact identities and current-holder authority.
Neither a resolver nor a model brand makes the semantic choice.

`aoa-summon` is the execution leaf for the independent external actor. It runs
only after obligation, mandate, incarnation, environment, authority, named
outputs, return owner, and stop line are complete. That lane exposes a real
separate CLI process/session; a native Codex child is not its substitute.

## Stop and evidence

Stop at an unresolved holder, missing owner input, absent current fit evidence,
unavailable external binding, or a return that cannot identify its next holder.
Do not widen the mandate to make a route pass.

Plans, bindings, handles, output validation, review, and owner acceptance are
different evidence. Count usage from runtime receipts without turning it into
a pre-emptive budget gate. Keep raw trials, live state, and task-local DAG
instances outside the skill source.

Return the useful result, actual effects, checks and unresolved uncertainty,
the current holder, and the next action. Link exact artifacts instead of
repeating their assembly history. Stop at that bounded handoff; stats, memo,
proof, progression, and new branches are separate owner operations, not an
automatic closeout cascade.
