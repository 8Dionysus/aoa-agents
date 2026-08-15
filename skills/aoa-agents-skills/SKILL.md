---
name: aoa-agents-skills
description: Detect when a goal creates or predicts an independently owned obligation, or when an explicit role-first request asks to form and embody an appropriate actor; form a bounded role mandate, bind a currently supported incarnation and specialized environment, transfer responsibility to a separately addressable actor, or receive and filter its return. Use when planning, execution, or closeout pressure may require an actor with its own identity, authority, continuity, and lifecycle. Do not use merely because a model or launcher is available, for ordinary task decomposition, to own a domain procedure, to select a model brand without fit evidence, or to equate CLI transport with A2A responsibility.
---

# aoa-agents-skills

Turn one real or anticipated obligation into an independently addressable
role-bearing actor without making a model, process, transport, or domain skill
the source of that actor's meaning.

## Applicability preflight

Inspect the goal, current plan, execution pressure, or closeout residue first.
Use this bundle only when at least one duty may need a distinct bearer of
responsibility rather than an ordinary step performed by the current actor.

Positive pressure includes:

- a future landing, CI, eval, memo, stats, review, or other domain duty that
  needs an independent owner, lifecycle, authority envelope, or return gate;
- work that should remain addressable and resumable after one process exits;
- a result that must return through an explicit reviewer, filter, or wake rule;
- a pre-authorized persistent role whose exact reflex condition may have fired.

Return `not_applicable` when the work is only a local step, a faster model is
available, a generic helper could shorten the task, or no responsibility needs
to move. Do not create an actor to justify available compute.

## Role-first entry

When the current holder explicitly says:

> In this Goal an independent obligation has appeared; form and embody the
> appropriate actor.

and supplies the Goal, independent duty, authority envelope, and expected
result, select the role-first-entry mode. Read
references/role-first-entry.md and normalize only the semantic
role-first-intent-v1 fields. The mode is the one public semantic entry for
the full lifecycle; it composes the existing internal modes and aoa-summon
leaf, and stops closed when any stronger-owner input is missing. The caller
must not hand-build summon packets or choose a model by brand.

## Start

1. Record `<bundle_dir>` as the absolute directory containing this loaded
   `SKILL.md`.
2. Read `references/contract.yaml`, `references/source-return.md`, and
   `references/task-local-dag.md` to EOF.
3. Select the smallest internal mode or task-local chain required now:

   | Mode | Use when | Read |
   | --- | --- | --- |
   | role-first-entry | An explicit semantic request asks this Goal to form and embody one appropriate actor. | references/role-first-entry.md |
   | `detect-obligation` | Pressure must be tested and assigned a trigger strength. | `references/detect-obligation.md` |
   | `form-actor` | An admitted obligation needs a stable role, mandate, required executor properties, and continuity posture. | `references/form-actor.md` |
   | `bind-incarnation` | A complete mandate needs a current model realization, specialized environment, permissions, and resumable runtime binding. | `references/bind-incarnation.md` |
   | `transfer-responsibility` | A complete actor and incarnation binding are ready for a bounded A2A handoff and external execution leaf. | `references/transfer-responsibility.md` |
   | `receive-return` | A return, event, refusal, pause, or failure must be filtered and responsibility reassigned or a role woken. | `references/receive-return.md` |

4. Read only the selected mode references. A compound request may select
   several modes only through the task-local DAG rule; do not hide a fixed
   workflow inside the root bundle.
5. Execute the owner-source gate before reading owner-relative role, tier,
   specialization, capability-pack, or handoff sources.
6. Return the typed output for every executed node and the exact stop or next
   owner route.

## Organ boundary

`aoa-agents` owns:

- whether pressure warrants a distinct responsibility bearer;
- the role, specialization, mandate, authority, continuity, and return posture;
- the required properties of an acceptable incarnation;
- responsibility transfer, pause, refusal, return, and wake meaning.

It does not own:

- landing, CI, eval, memo, stats, review, or other domain procedures;
- model-fit evidence or model research, which belong to `aoa-models`;
- runtime planning and incarnation binding, which belong to `aoa-sdk`;
- CLI process, session, persistence, and event transport, which belong to
  `abyss-stack`;
- A2A transport or protocol merely because it carries the handoff;
- task-local DAG persistence, routing policy, proof verdicts, or memory truth.

The domain skill remains an input to the actor mandate. The model realization
remains a replaceable binding. A persistent role may retain identity,
obligation, continuity, and relationships while no process or model instance
is running.

## Execution leaf

An external execution leaf may be selected only after obligation, mandate,
incarnation, environment, authority, named outputs, return owner, and stop
line are complete. `aoa-summon` is the current candidate leaf only where its
actual host binding launches a separate CLI process/session and returns a real
runtime handle. Its built-in Codex child-agent lanes do not satisfy this
bundle's external-incarnation path.

## Verification and stop

- Preserve the chain from goal pressure through obligation, mandate, required
  properties, model-fit evidence, runtime binding, handoff, and return.
- Resolve an already selected role chain through the bundled passive resolver;
  never guess owner-relative role paths or treat the resolver as role-selection
  authority.
- For role-first-entry, make the semantic role and current-holder model-fit
  decisions before invoking passive resolvers and compilers; preserve the
  resulting selection authority instead of hiding it in a launcher.
- Compile an admitted obligation and mandate through the bundled passive
  compiler so exact digests, lifecycle, stop line, output identities, and the
  current-holder-authorized duty-to-fit-family relation survive downstream;
  the compiler does not detect duties or select roles, models, or runtimes.
- Keep model name and reasoning mode out of the stable role and obligation.
- Count usage from runtime receipts; never convert usage counting into a
  pre-emptive budget gate.
- Treat plans, schemas, graph nodes, bindings, process handles, outputs, and
  proof as distinct evidence classes.
- Stop when the next owner input is absent, a responsibility holder is
  unresolved, the selected model lacks current fit evidence, the external
  binding cannot be inspected, or return validation cannot identify the next
  holder.
- Keep raw trials, live process state, and task-local DAG instances outside
  the owner skill source.
