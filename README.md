# aoa-agents

`aoa-agents` is the role and persona layer of the AoA ecosystem.

It exists to make agents explicit as role-bearing actors rather than leaving them as vague prompt folklore or hidden orchestration assumptions.

This repository is not the main home of reusable techniques, skill bundles, proof bundles, or memory objects.
Its role is different: it should define who acts, under what contract, with what boundaries, preferred skills, memory posture, evaluation posture, and handoff rules.

## Start here

If you are new to this repository, use this path:

1. Read [CHARTER](CHARTER.md) for the role and boundaries of the agent layer.
2. Read [docs/AGENT_MODEL](docs/AGENT_MODEL.md) for the conceptual model.
3. Read [docs/AGENT_PROFILE_SURFACE](docs/AGENT_PROFILE_SURFACE.md) for the source-authored role-contract surface.
4. Read [docs/REGISTRY_SOURCE_SURFACES](docs/REGISTRY_SOURCE_SURFACES.md) for the source-authored machine-readable registry layer.
5. Read [docs/PUBLISHED_CONTRACT_COMPATIBILITY](docs/PUBLISHED_CONTRACT_COMPATIBILITY.md) for wire-shape and publication compatibility discipline.
6. Read [docs/AGENT_MEMORY_POSTURE](docs/AGENT_MEMORY_POSTURE.md) for role-level memory rights and posture.
7. Read [docs/MODEL_TIER_MODEL](docs/MODEL_TIER_MODEL.md) for the separate tier-oriented orchestration model.
8. Read [docs/AGENT_COHORT_PATTERNS](docs/AGENT_COHORT_PATTERNS.md) for the first bounded cohort composition surface.
9. Read [docs/AGENT_RUNTIME_SEAM](docs/AGENT_RUNTIME_SEAM.md) for the contract-first runtime seam.
10. Read [docs/REFERENCE_ROUTE_EXAMPLES](docs/REFERENCE_ROUTE_EXAMPLES.md) for example-only route packs over the public loop.
11. Read [docs/FEDERATION_CONSUMER_SEAMS](docs/FEDERATION_CONSUMER_SEAMS.md) for the current bounded cross-repo consumer seams.
12. Read [docs/RUNTIME_ARTIFACT_TRANSITIONS](docs/RUNTIME_ARTIFACT_TRANSITIONS.md) for artifact coverage and transition discipline.
13. Read [docs/RECURRENCE_DISCIPLINE](docs/RECURRENCE_DISCIPLINE.md) for explicit recurrence discipline and bounded return governance.
14. Read [docs/SELF_AGENT_CHECKPOINT_STACK](docs/SELF_AGENT_CHECKPOINT_STACK.md) for the bounded self-agent contract.
15. Read [docs/BOUNDARIES](docs/BOUNDARIES.md) for ownership rules.
16. Read [ROADMAP](ROADMAP.md) for the current direction.

## What this repository is for

`aoa-agents` should own agent-layer meaning about:
- agent profiles
- role contracts
- handoff postures
- preferred skill families
- memory access posture
- evaluation posture
- agent composition hints
- compact agent registries and validation

## What this repository is not for

This repository should not become the main home for:
- reusable techniques
- skill bundles
- eval bundles
- routing surfaces
- memory objects
- infrastructure implementation details
- giant prompt archives pretending to be role design

An agent is not a skill.
A skill is a bounded workflow.
An agent is a role-bearing actor that uses skills.

## Relationship to the AoA federation

Within AoA:
- `aoa-techniques` owns practice meaning
- `aoa-skills` owns execution meaning
- `aoa-evals` owns bounded proof meaning
- `aoa-routing` should own dispatch and navigation surfaces
- `aoa-memo` should own memory and recall meaning
- `aoa-agents` should own role and persona meaning

## Local validation

Canonical source-authored role contracts now live at:
- `profiles/*.profile.json`
- `schemas/agent-profile.schema.json`

Canonical source-authored machine-readable registry inputs now live at:
- `model_tiers/*.tier.json`
- `cohort_patterns/*.pattern.json`
- `runtime_seam/*.binding.json`
- `schemas/model-tier.schema.json`
- `schemas/cohort-pattern.schema.json`
- `schemas/runtime-seam-binding.schema.json`

This repository includes a compact machine-readable agent-layer registry at:
- `generated/agent_registry.min.json`
- `generated/model_tier_registry.json`

It also includes a compact machine-readable cohort composition surface at:
- `schemas/cohort-composition-registry.schema.json`
- `generated/cohort_composition_registry.json`

It also includes public contract schemas for bounded runtime-facing artifacts at:
- `schemas/artifact.route_decision.schema.json`
- `schemas/artifact.bounded_plan.schema.json`
- `schemas/artifact.work_result.schema.json`
- `schemas/artifact.verification_result.schema.json`
- `schemas/artifact.transition_decision.schema.json`
- `schemas/artifact.deep_synthesis_note.schema.json`
- `schemas/artifact.distillation_pack.schema.json`

It also includes inspectable runtime seam surfaces at:
- `examples/runtime_artifacts/*.example.json`
- `examples/runtime_artifacts/invalid/*.json`
- `schemas/runtime-seam-bindings.schema.json`
- `generated/runtime_seam_bindings.json`

It also includes self-agent checkpoint contract surfaces at:
- `schemas/self-agent-checkpoint.schema.json`
- `examples/self_agent_checkpoint/*.json`
- `examples/self_agent_checkpoint/invalid/*.json`

It also includes example-only reference route surfaces at:
- `schemas/reference-route.example.schema.json`
- `examples/reference_routes/*/manifest.json`
- `examples/reference_routes/*/*.json`

To validate the current agent-layer surface locally, run:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

Validation is self-contained by default.

Optional bounded consumer smoke checks may be enabled by setting:
- `AOA_PLAYBOOKS_ROOT`
- `AOA_EVALS_ROOT`
- `AOA_MEMO_ROOT`
- `AOA_ROUTING_ROOT`

When those roots are supplied, the same validator also performs federated smoke checks against published consumer seams.
Without those roots, validation stays local and autonomous.

These checks only confirm published contract reachability.
`AOA_MEMO_ROOT` additionally confirms object recall surface reachability.
`AOA_ROUTING_ROOT` additionally confirms doctrine-default memo recall entrypoints
plus the parallel `memory_objects` tiny-model recall family.
They do not move playbook, eval, memo, or routing meaning into `aoa-agents`.

## Current status

The bootstrap baseline is landed.
The current cycle hardens published contract compatibility, adds scenario-backed reference routes, and proves bounded consumer seams without turning `aoa-agents` into runtime or scenario canon.

## Principles

- agents should be explicit rather than magical
- roles should stay bounded and reviewable
- self-agent posture should be checkpointed rather than mythologized
- handoff should be a contract, not an accident
- memory posture should be named, not implied
- evaluation posture should be named, not retrofitted later
- the agent layer should not swallow neighboring AoA layers

## License

Apache-2.0
