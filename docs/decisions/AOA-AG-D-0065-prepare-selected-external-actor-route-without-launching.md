# Prepare Selected External Actor Route Without Launching

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0065
- Original date: 2026-08-11
- Surface classes: owner skill home, external actor preparation, execution leaf
- Agent facets: obligation, role contract, incarnation, responsibility return
- Mechanic parents: cross-mechanic, boundary-bridge
- Guard families: owner boundary, model fit, evidence closure, task-local DAG, wake ABI
- Posture: admitted non-starting route compiler

## Context

The external CLI pilot proved the physical runtime, but assembling each route
still required a controller to hand-build and reconcile obligation, role,
mandate, model fit, SDK admission, runtime binding, task-local DAG,
responsibility transfer, domain procedure, and final summon artifacts. That
made a model-first launcher easier to reproduce than the intended role-first
path and allowed cross-owner drift to appear only after a costly actor run.

A real eval-selection writer and independent reviewer also exposed two concrete
preparation gaps: writer evidence could reference an immutable input that was
not forwarded to the reviewer, and a completed review could be bound to
`result.completed` even though the runtime ABI emits `result.validated`.

## Options Considered

- Keep hand-building task-local packets for every new duty.
- Move role, model, SDK, runtime, and domain decisions into one launcher.
- Compile only after those decisions exist, preserving every owner artifact and
  refusing incomplete or inconsistent routes before launch.

## Decision

Add strict preparation input and result schemas plus
`skills/aoa-summon/scripts/prepare_external_actor.py` as a passive,
non-starting compiler for an already selected external actor route.

The compiler may resolve and content-address settled inputs, invoke owner
compilers and non-starting binders, and emit the exact packet consumed by the
external runtime. It may not detect an obligation, select a role or model,
weaken permissions, start a process, interpret a returned result, or accept
work for an owner.

Writer preparation may predict one independent review branch. Independent
review preparation is terminal and may not recursively create another
reviewer. Writer report and selection references must be transitively closed
over the exact evidence inputs supplied to that reviewer. Validated reviewer
completion binds to `result.validated`; repair return binds to
`result.review_required`.

## Rationale

This keeps the public semantic entrance at obligation and role while making
the expensive physical route reproducible. Cross-owner contracts fail before
model execution, but model judgment remains free inside the granted mandate;
the guards constrain evidence identity and authority, not the reasoning path.

## Consequences

- Any suitable model realization can replace Luna without renaming the route.
- Domain procedures remain owner inputs rather than becoming `aoa-agents`
  workflow truth.
- Review evidence omissions and wake-event drift become preparation failures.
- The compiler still depends on current owner repositories and an admitted
  installed runtime binder; it is not a portable all-in-one launcher.
- Runtime success, independent review, owner acceptance, and global skill
  exposure remain separate proof stages.

## Source Surfaces

- `skills/aoa-summon/SKILL.md`
- `skills/aoa-summon/scripts/prepare_external_actor.py`
- `skills/aoa-summon/references/actor-route-preparation-v1.schema.json`
- `skills/aoa-summon/references/actor-route-preparation-result-v1.schema.json`
- `tests/test_external_actor_preparer.py`

## Follow-Up Route

Validate the owner source, build fresh decision and capability projections,
then exercise writer, independent-review, A2A export, and master-filter paths
through the installed `abyss-stack` interface before global profile rollout.

## Verification

Verification routes through focused preparer tests, schema validation,
decision-index regeneration, semantic and nested-agent validators, the full
repository test suite, and real separate-session external actor receipts.
