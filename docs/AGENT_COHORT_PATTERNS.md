# AGENT COHORT PATTERNS

## Purpose

This document defines the first bounded cohort composition surface at the agent layer.

It exists to make composition hints explicit without turning `aoa-agents` into
the owner of scenario composition, routing policy, or runtime orchestration.

## Core rule

`aoa-agents` may name bounded cohort patterns.
It does not own scenario canon for how those patterns are run in the wild.

Composition hints do not replace `aoa-playbooks`.

## Official patterns

The first official cohort pattern set is:

- `solo`
- `pair`
- `checkpoint_cohort`
- `orchestrated_loop`
- `alpha_curated`

These patterns are composition hints.
They stay compact, inspectable, and role-facing.

### `solo`

Use `solo` when one role can carry a bounded route without pretending to own
every adjacent duty.

Allowed role sets:

- `["architect"]`
- `["coder"]`
- `["evaluator"]`

Preferred tier path:

- `router`
- `executor`
- `verifier`

Typical activation conditions:

- bounded low-risk route
- clear single-role ownership
- no mandatory multi-role review before the next step

Required handoff posture:

- hand off on ambiguity when the route exceeds the role contract
- hand off durable memory shaping to `memory-keeper`
- hand off high-cost arbitration to `deep` or `evaluator`

Boundary note:

`solo` is a bounded default, not permission for one role to silently become
planner, operator, reviewer, and memory canon owner at once.

### `pair`

Use `pair` when two roles should keep one another legible without escalating
into a larger orchestrated route.

Allowed role sets:

- `["architect","coder"]`
- `["coder","reviewer"]`
- `["architect","reviewer"]`

Preferred tier path:

- `planner`
- `executor`
- `verifier`

Typical activation conditions:

- moderate ambiguity or design pressure
- bounded implementation with an explicit review edge
- need for a second role before escalation becomes necessary

Required handoff posture:

- hand off to `reviewer` when execution risk rises
- hand off to `architect` when boundary-shaping decisions appear
- hand off durable provenance or recall design to `memory-keeper`

Boundary note:

`pair` keeps dual-role coordination explicit.
It does not become hidden orchestration or an implicit playbook.

### `checkpoint_cohort`

Use `checkpoint_cohort` for governed self-agent or system-shaping routes that
need explicit approval, rollback, health, and provenance posture.

Allowed role sets:

- `["architect","coder","reviewer","memory-keeper"]`

Preferred tier path:

- `planner`
- `executor`
- `verifier`
- `archivist`

Typical activation conditions:

- self-agent or system-shaping change
- approval, rollback, or health posture must be explicit
- provenance and improvement logging must remain reviewable

Required handoff posture:

- `architect` names constitutional fit and scope before the change
- `coder` executes only after approval is explicit
- `reviewer` checks post-change health and final boundedness
- `memory-keeper` preserves provenance and the improvement log

Boundary note:

`checkpoint_cohort` is the canonical governed self-agent pattern in
`aoa-agents`.
It names the actor cohort, not the runtime implementation beneath it.

### `orchestrated_loop`

Use `orchestrated_loop` when the public loop needs explicit coordination across
multiple steps, escalation surfaces, and possible distillation.

Allowed role sets:

- `["architect","coder","reviewer"]`
- `["architect","coder","reviewer","evaluator"]`
- `["architect","coder","reviewer","memory-keeper"]`
- `["architect","coder","reviewer","evaluator","memory-keeper"]`

Preferred tier path:

- `router`
- `planner`
- `executor`
- `verifier`
- `conductor`
- `deep`
- `archivist`

Typical activation conditions:

- non-trivial multi-step route
- escalation or arbitration may be needed
- durable distillation may follow execution

Required handoff posture:

- transition decisions stay explicit through conductor-facing surfaces
- `deep` activates only for named high-cost conditions
- `archivist` distills durable candidates without replacing source-owned canon

Boundary note:

`orchestrated_loop` is a coordination hint over the public loop.
It does not absorb scenario composition from `aoa-playbooks`.

### `alpha_curated`

Use `alpha_curated` when the local-runtime readiness lane needs all five
published roles under one explicit curator-facing cohort.

Allowed role sets:

- `["architect","coder","reviewer","evaluator","memory-keeper"]`

Preferred tier path:

- `router`
- `planner`
- `executor`
- `verifier`
- `conductor`
- `deep`
- `archivist`

Typical activation conditions:

- one-session readiness proof on the promoted local Qwen runtime
- explicit preflight, evaluation, and memo writeback are all mandatory
- the route must stay inside named playbook surfaces without inventing a new family

Required handoff posture:

- `architect` owns preflight, source-of-truth checks, boundary selection, and stop conditions
- `coder` executes only after explicit architect handoff
- `reviewer` closes verification and names rollback or re-entry posture
- `evaluator` runs the mapped eval bundles and interprets bounded verdicts
- `memory-keeper` prepares memo writeback and rerun recall posture

Boundary note:

`alpha_curated` is the curated readiness cohort for Phase Alpha only.
It does not replace `checkpoint_cohort`, does not replace
`orchestrated_loop`, and does not absorb scenario canon from
`aoa-playbooks`.

## Boundaries to preserve

- cohort patterns are not playbooks
- cohort patterns are not routing policy
- cohort patterns are not memory-object doctrine
- cohort patterns are not eval doctrine
- the agent layer may expose composition hints without owning scenario canon

## Minimal machine-readable contract

The machine-readable cohort registry should stay compact.
Each pattern entry should expose:

- `id`
- `status`
- `summary`
- `allowed_role_sets`
- `preferred_tier_ids`
- `activation_conditions`
- `required_handoffs`
- `boundary_note`
