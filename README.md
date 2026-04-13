# aoa-agents

`aoa-agents` is the role and persona layer of the AoA ecosystem. It exists to make agents explicit as role-bearing actors rather than leaving them as vague prompt folklore or hidden orchestration assumptions.

This repository does not own reusable techniques, skill bundles, proof bundles, or memory objects. Its job is different: it defines who acts, under what contract, with what boundaries, preferred skill families, memory posture, evaluation posture, and handoff rules.

An agent is not a skill. A skill is a bounded workflow. An agent is a role-bearing actor that uses skills.

> Current release: `v0.2.1`. See [CHANGELOG](CHANGELOG.md) for release notes.

## Start here

Use the shortest route by need:

- docs map: `docs/README.md`
- role and boundary charter: `CHARTER.md`
- conceptual model: `docs/AGENT_MODEL.md`
- future subject and kind-split preparation: `docs/AGENT_SUBJECT_PREP.md`
- source-authored role-contract surface: `docs/AGENT_PROFILE_SURFACE.md`
- source-authored orchestrator-class surface: `docs/ORCHESTRATOR_CLASS_MODEL.md`
- source-authored registry surface: `docs/REGISTRY_SOURCE_SURFACES.md`
- Codex custom-agent projection surface and owner refresh law: `docs/CODEX_SUBAGENT_PROJECTION.md`, `docs/CODEX_SUBAGENT_REFRESH_LAW.md`, `config/codex_subagent_wiring.v2.json`, and `generated/codex_agents/`
- role-level memory posture: `docs/AGENT_MEMORY_POSTURE.md`
- stress posture and stress handoff doctrine: `docs/AGENT_STRESS_POSTURE.md` and `docs/AGENT_STRESS_HANDOFFS.md`
- model-tier orchestration and cohort composition: `docs/MODEL_TIER_MODEL.md` and `docs/AGENT_COHORT_PATTERNS.md`
- runtime seam, consumer handoff, trigger posture, and transition posture: `docs/AGENT_RUNTIME_SEAM.md`, `docs/FEDERATION_CONSUMER_SEAMS.md`, `docs/WORKSPACE_SURFACE_TRIGGER_POSTURE.md`, and `docs/RUNTIME_ARTIFACT_TRANSITIONS.md`
- reviewed role-posture adjunct for the workspace checkpoint-growth closeout: `docs/WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md`
- ownership rules and current direction: `docs/BOUNDARIES.md` and `ROADMAP.md`

## Route by need

- canonical profiles and schemas: `profiles/*.profile.json` and `schemas/agent-profile.schema.json`
- model tiers, orchestrator classes, and bounded cohort composition: `model_tiers/*.tier.json`, `orchestrator_classes/*.class.json`, `cohort_patterns/*.pattern.json`, `schemas/model-tier.schema.json`, `schemas/orchestrator-class.schema.json`, `schemas/cohort-pattern.schema.json`, `generated/model_tier_registry.json`, `generated/orchestrator_class_catalog.min.json`, and `generated/cohort_composition_registry.json`
- published registries and consumer seams: `generated/agent_registry.min.json`, `generated/model_tier_registry.json`, `generated/cohort_composition_registry.json`, `generated/runtime_seam_bindings.json`, and `docs/FEDERATION_CONSUMER_SEAMS.md`
- Codex subagent projection, owner refresh law, and workspace install seam: `docs/CODEX_SUBAGENT_PROJECTION.md`, `docs/CODEX_SUBAGENT_REFRESH_LAW.md`, `generated/codex_agents/agents/*.toml`, `generated/codex_agents/config.subagents.generated.toml`, and `scripts/build_codex_subagents_v2.py`
- runtime seam bindings and runtime-facing artifact contracts: `runtime_seam/*.binding.json`, `generated/runtime_seam_bindings.json`, and `schemas/artifact.*.schema.json`
- additive stress posture and handoff adjuncts: `schemas/agent_stress_posture_v1.json`, `schemas/stress_handoff_envelope_v1.json`, `examples/agent_stress_posture.example.json`, `examples/stress_handoff_envelope.example.json`, `docs/AGENT_STRESS_POSTURE.md`, and `docs/AGENT_STRESS_HANDOFFS.md`
- via negativa pruning checklist: `docs/VIA_NEGATIVA_CHECKLIST.md`
- progression, recurrence, and self-agent surfaces: `docs/AGENT_PROGRESSION_MODEL.md`, `docs/RECURRENCE_DISCIPLINE.md`, `docs/SELF_AGENT_CHECKPOINT_STACK.md`, and `docs/SELF_AGENCY_CONTINUITY_LANE.md`
- example and bounded smoke surfaces: `examples/runtime_artifacts/*`, `examples/self_agent_checkpoint/*`, `docs/REFERENCE_ROUTE_EXAMPLES.md`, and `docs/RUNTIME_ARTIFACT_TRANSITIONS.md`
- adjunct quest and Alpha readiness surfaces: `docs/QUEST_EXECUTION_PASSPORT.md`, `generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`, `examples/alpha_reference_routes/*`, and `generated/alpha_reference_routes.min.json`

## What this repository is for

`aoa-agents` owns agent-layer meaning about:

- agent profiles
- role contracts
- orchestrator class identity and capsule law
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

Verify the current committed surfaces without rewriting files:

```bash
python scripts/validate_agents.py
python -m pytest -q tests
```

Optional bounded consumer smoke checks can be enabled with the documented `AOA_*_ROOT` variables when you want federated reachability checks against sibling repositories.

```bash
AOA_PLAYBOOKS_ROOT=/path/to/aoa-playbooks \
AOA_EVALS_ROOT=/path/to/aoa-evals \
AOA_MEMO_ROOT=/path/to/aoa-memo \
AOA_ROUTING_ROOT=/path/to/aoa-routing \
python scripts/validate_agents.py
```

Refresh published registries only after editing source-authored registry inputs under `profiles/`, `model_tiers/`, `orchestrator_classes/`, `cohort_patterns/`, or `runtime_seam/`:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
python scripts/validate_codex_subagents.py --profiles-root profiles --wiring config/codex_subagent_wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
```

## License

Apache-2.0
