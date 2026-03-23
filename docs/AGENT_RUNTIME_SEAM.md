# AGENT RUNTIME SEAM

## Purpose

This document defines the runtime seam at the agent layer.

It does not turn `aoa-agents` into the owner of runtime implementation.
It defines the contract that a future runtime may read from this repository.

## Source Seed

Source seed ref:

- `Dionysus/seed_expansion/seed.aoa.agents-runtime-pack.v0.md#aoa-seed-r1-agents-runtime-seam`

## Core Rule

`aoa-agents` may define role-and-tier binding plus public artifact contracts.

It does not own:

- routing logic
- playbook meaning
- memory object canon
- eval doctrine
- network protocol commitments
- runtime infrastructure implementation

## Runtime Formula

Keep the seam explicit and small:

```text
run
= task
+ route_hint
+ playbook
+ tier_state_machine
+ role_binding
+ skill_calls
+ eval_hooks
+ memory_writeback
```

This is a contract formula, not a runtime mandate.

The public loop remains:

`route -> plan -> do -> verify -> deep? -> distill`

## Role × Tier Binding

The public binding for the first planting slice is:

- `router + architect -> route_decision`
- `planner + architect -> bounded_plan`
- `executor + coder -> work_result`
- `verifier + reviewer -> verification_result`
- `conductor + architect/reviewer -> transition_decision`
- `deep + evaluator/architect -> deep_synthesis_note`
- `archivist + memory-keeper -> distillation_pack`

This keeps the role axis and tier axis visible without collapsing them into one mythic agent.

The official cohort composition surface sits beside this binding, not above it.
Use:

- `solo` for bounded single-role routes with explicit handoff posture
- `pair` for bounded dual-role collaboration without hidden orchestration
- `checkpoint_cohort` for governed self-agent routes
- `orchestrated_loop` for explicit coordination over the public loop

These are composition hints.
They do not move scenario composition into this repository.

## Public Artifact Surfaces

The first public runtime seam is schema-backed and code-free.
The public artifact contracts are:

- `schemas/artifact.route_decision.schema.json`
- `schemas/artifact.bounded_plan.schema.json`
- `schemas/artifact.work_result.schema.json`
- `schemas/artifact.verification_result.schema.json`
- `schemas/artifact.transition_decision.schema.json`
- `schemas/artifact.deep_synthesis_note.schema.json`
- `schemas/artifact.distillation_pack.schema.json`

These schemas define inspectable artifact names and minimal contract fields.
They do not define runtime execution, tool wiring, or vendor-specific transport.

Inspectable examples for each public artifact live under:

- `examples/runtime_artifacts/*.example.json`
- `examples/runtime_artifacts/invalid/*.json`

The role × tier binding is also published as a machine-readable surface:

- `schemas/runtime-seam-bindings.schema.json`
- `generated/runtime_seam_bindings.json`

The cohort composition surface is also published as a machine-readable surface:

- `schemas/cohort-composition-registry.schema.json`
- `generated/cohort_composition_registry.json`

## Reference Scenarios

Use these as reference scenarios and future example runs only:

- `AOA-P-0008 long-horizon-model-tier-orchestra`
- `AOA-P-0009 restartable-inquiry-loop`

They inform the seam.
They do not move scenario composition into this repository.

## Boundaries To Preserve

- runtime may read `generated/agent_registry.min.json` and `generated/model_tier_registry.json`
- `aoa-routing` still owns navigation and dispatch surfaces
- `aoa-playbooks` still owns scenario composition
- `aoa-skills` still owns bounded execution workflows
- `aoa-memo` still owns memory objects and writeback doctrine
- `aoa-evals` still owns proof doctrine and verdict logic
- `abyss-stack` still owns runtime and infrastructure implementation

## Optional Consumer Smoke Checks

`python scripts/validate_agents.py` stays self-contained by default.

When these environment variables are set, the validator may also confirm that
published neighboring surfaces still resolve back to the public artifact
contracts in this repository:

- `AOA_PLAYBOOKS_ROOT`
- `AOA_EVALS_ROOT`
- `AOA_MEMO_ROOT`

These checks verify published contract reachability only.
They do not move playbook meaning, eval doctrine, or memo object meaning into
`aoa-agents`.

## Minimal Landing Slice

This first landing slice is intentionally small:

- one human-readable contract note
- one schema pack for tier artifacts
- no `runtime/` implementation
- no MCP or A2A networking
- no internal router
- no direct memory canon writeback

That is enough to make the seam inspectable without overbuilding the runtime too early.
