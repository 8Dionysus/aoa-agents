# aoa-agents

`aoa-agents` is the role and persona layer of the AoA ecosystem. It exists to make agents explicit as role-bearing actors rather than leaving them as vague prompt folklore or hidden orchestration assumptions.

This repository does not own reusable techniques, skill bundles, proof bundles, or memory objects. Its job is different: it defines who acts, under what contract, with what boundaries, preferred skill families, memory posture, evaluation posture, and handoff rules.

An agent is not a skill. A skill is a bounded workflow. An agent is a role-bearing actor that uses skills.

## Start here

Use the shortest route by need:

- docs map: `docs/README.md`
- role and boundary charter: `CHARTER.md`
- conceptual model: `docs/AGENT_MODEL.md`
- source-authored role-contract surface: `docs/AGENT_PROFILE_SURFACE.md`
- source-authored registry surface: `docs/REGISTRY_SOURCE_SURFACES.md`
- role-level memory posture: `docs/AGENT_MEMORY_POSTURE.md`
- model-tier orchestration and cohort composition: `docs/MODEL_TIER_MODEL.md` and `docs/AGENT_COHORT_PATTERNS.md`
- runtime seam, consumer handoff, and transition posture: `docs/AGENT_RUNTIME_SEAM.md`, `docs/FEDERATION_CONSUMER_SEAMS.md`, and `docs/RUNTIME_ARTIFACT_TRANSITIONS.md`
- ownership rules and current direction: `docs/BOUNDARIES.md` and `ROADMAP.md`

## Route by need

- canonical profiles and schemas: `profiles/*.profile.json` and `schemas/agent-profile.schema.json`
- model tiers and bounded cohort composition: `model_tiers/*.tier.json`, `cohort_patterns/*.pattern.json`, `schemas/model-tier.schema.json`, `schemas/cohort-pattern.schema.json`, `generated/model_tier_registry.json`, and `generated/cohort_composition_registry.json`
- published registries and consumer seams: `generated/agent_registry.min.json`, `generated/model_tier_registry.json`, `generated/cohort_composition_registry.json`, `generated/runtime_seam_bindings.json`, and `docs/FEDERATION_CONSUMER_SEAMS.md`
- runtime seam bindings and runtime-facing artifact contracts: `runtime_seam/*.binding.json`, `generated/runtime_seam_bindings.json`, and `schemas/artifact.*.schema.json`
- progression, recurrence, and self-agent surfaces: `docs/AGENT_PROGRESSION_MODEL.md`, `docs/RECURRENCE_DISCIPLINE.md`, and `docs/SELF_AGENT_CHECKPOINT_STACK.md`
- example and bounded smoke surfaces: `examples/runtime_artifacts/*`, `examples/self_agent_checkpoint/*`, `docs/REFERENCE_ROUTE_EXAMPLES.md`, and `docs/RUNTIME_ARTIFACT_TRANSITIONS.md`

## What this repository is for

`aoa-agents` owns agent-layer meaning about:

- agent profiles
- role contracts
- handoff posture
- preferred skill families
- memory access posture
- evaluation posture
- bounded cohort composition hints
- compact registries and validation

## What this repository is not for

This repository should not become the main home for:

- reusable techniques
- skill bundles
- eval bundles
- routing surfaces
- memory objects
- infrastructure implementation details
- giant prompt archives pretending to be role design

## Relationship to the AoA federation

- `aoa-techniques` owns practice meaning
- `aoa-skills` owns execution meaning
- `aoa-evals` owns bounded proof meaning
- `aoa-routing` owns dispatch and navigation
- `aoa-memo` owns memory and recall meaning
- `aoa-agents` owns role and persona meaning

## Local validation

Install local dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Build published surfaces and validate them:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

Optional bounded consumer smoke checks can be enabled with the documented `AOA_*_ROOT` variables when you want federated reachability checks against sibling repositories.

## License

Apache-2.0
