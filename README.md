# aoa-agents

`aoa-agents` is the role and persona layer of the AoA ecosystem. It exists to make agents explicit as role-bearing actors rather than leaving them as vague prompt folklore or hidden orchestration assumptions.

This repository does not own reusable techniques, skill bundles, proof bundles, or memory objects. Its job is different: it defines who acts, under what contract, with what boundaries, preferred skill families, memory posture, evaluation posture, and handoff rules.

An agent is not a skill. A skill is a bounded workflow. An agent is a role-bearing actor that uses skills.

> Current release: `v0.2.3`. See [CHANGELOG](CHANGELOG.md) for release notes.

## Start here

Use the shortest route by need:

- docs map: `docs/README.md`
- repository design: `DESIGN.md`
- source object district: `agents/README.md`
- agent-facing companion lanes: `.agents/AGENTS.md`
- mechanics atlas: `mechanics/README.md`
- role and boundary charter: `CHARTER.md`
- conceptual model: `docs/AGENT_MODEL.md`
- subject prep boundary plus landed Agon actor and assistant recharters and the first formation trial: `mechanics/agon/parts/formation/docs/subject-prep.md`, `mechanics/agon/parts/formation/docs/actor-rechartering.md`, `mechanics/experience/parts/assistant-civil-service/docs/civil-rechartering.md`, `mechanics/agon/parts/formation/docs/formation-trial.md`, `generated/agent_agonic_formation_index.min.json`, `generated/assistant_civil_formation_index.min.json`, and `generated/agent_formation_trial.min.json`
- source-authored role-contract surface: `docs/AGENT_PROFILE_SURFACE.md`
- source-authored orchestrator-class surface: `docs/ORCHESTRATOR_CLASS_MODEL.md`
- source-authored registry surface: `mechanics/boundary-bridge/parts/source-surface-registry/docs/registry-source-surfaces.md`
- Codex custom-agent projection surface and owner refresh law: `mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md`, `mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md`, `mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json`, and `generated/codex_agents/`
- Wave 1 assistant projection resolver and no-self-rewrite posture: `mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md`, `mechanics/codex-projection/parts/assistant-projection/schemas/assistant-projection-resolver.schema.json`, and `mechanics/codex-projection/parts/assistant-projection/examples/assistant-projection-resolver.example.json`
- Titan service-cohort role, bearer lineage, and incarnation identity surfaces: `mechanics/titan/parts/service-cohort/docs/service-cohort.md`, `mechanics/titan/parts/summon-boundary/docs/summon-boundary.md`, `mechanics/titan/parts/role-bearing/docs/role-bearer-ontology.md`, `mechanics/titan/parts/lineage-ledger/docs/lineage-ledger.md`, `mechanics/titan/parts/incarnation-spine/docs/incarnation-spine.md`, `mechanics/titan/parts/incarnation-spine/docs/praxis-plane.md`, `mechanics/titan/parts/role-bearing/config/role-classes.v0.json`, `mechanics/titan/parts/role-bearing/config/bearers.v0.json`, `mechanics/titan/parts/lineage-ledger/config/ledger.v0.json`, `mechanics/titan/parts/incarnation-spine/schemas/incarnation-identity.schema.json`, and `mechanics/titan/parts/incarnation-spine/examples/incarnation-identity.example.json`
- role-level memory posture: `docs/AGENT_MEMORY_POSTURE.md`
- stress posture and stress handoff doctrine: `mechanics/antifragility/parts/stress-posture/docs/stress-posture.md` and `mechanics/antifragility/parts/stress-posture/docs/stress-handoffs.md`
- model-tier orchestration and cohort composition: `docs/MODEL_TIER_MODEL.md` and `mechanics/rpg/parts/cohort-patterns/docs/cohort-patterns.md`
- runtime seam, consumer handoff, trigger posture, and transition posture: `mechanics/runtime-seam/parts/role-tier-bindings/docs/agent-runtime-seam.md`, `mechanics/boundary-bridge/parts/federation-consumer-seams/docs/federation-consumer-seams.md`, `mechanics/boundary-bridge/parts/workspace-trigger/docs/workspace-surface-trigger-posture.md`, and `mechanics/runtime-seam/parts/transition-discipline/docs/runtime-artifact-transitions.md`
- reviewed role-posture adjunct for the workspace checkpoint-growth closeout: `mechanics/checkpoint/parts/growth-checkpoint/docs/workspace-checkpoint-growth-role-posture.md`
- ownership rules and current direction: [docs/BOUNDARIES.md](docs/BOUNDARIES.md) and [ROADMAP.md](ROADMAP.md)

## Route by need

- source-authored agent objects: `agents/README.md`, then the nearest `agents/**/AGENTS.md`
- agent-facing companion lanes: `.agents/AGENTS.md`; for Spark, `.agents/spark/AGENTS.md` and `.agents/spark/SWARM.md`
- repeatable agent-layer operations: `mechanics/README.md` and `mechanics/ARTIFACT_TOPOLOGY.md`
- canonical profiles and schemas: `agents/profiles/*.profile.json` and `schemas/agent-profile.schema.json`
- Agon-facing companion actor surfaces: `agents/profiles/adjuncts/*`, `mechanics/agon/parts/formation/schemas/agent-kind.schema.json`, `mechanics/agon/parts/formation/schemas/subjectivity.schema.json`, `mechanics/agon/parts/formation/schemas/office-overlay.schema.json`, `mechanics/agon/parts/arena-rank-school/schemas/arena-eligibility.schema.json`, `mechanics/agon/parts/formation/schemas/resistance-revision.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/assistant-variant.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-identity.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-contract.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-governance.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-certification.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/civil-formation.schema.json`, `mechanics/experience/parts/assistant-civil-service/examples/civil-formation.example.json`, `mechanics/experience/parts/arena-exclusion/schemas/arena-exclusion.schema.json`, `mechanics/agon/parts/formation/schemas/formation-trial.schema.json`, `mechanics/agon/parts/formation/examples/agent-agonic-formation.example.json`, `mechanics/agon/parts/formation/examples/formation-trial.example.json`, `mechanics/agon/parts/arena-rank-school/schemas/rank-jurisdiction.schema.json`, `mechanics/agon/parts/arena-rank-school/examples/rank-surface.example.json`, `mechanics/agon/parts/epistemic-actor/schemas/epistemic-actor-posture.schema.json`, `generated/agent_agonic_formation_index.min.json`, `generated/assistant_civil_formation_index.min.json`, and `generated/agent_formation_trial.min.json`
- Agon rank/school/epistemic generated companions: `mechanics/agon/parts/arena-rank-school/generated/rank-jurisdiction-registry.min.json`, `mechanics/agon/parts/arena-rank-school/generated/school-campaign-posture-registry.min.json`, and `mechanics/agon/parts/epistemic-actor/generated/epistemic-actor-posture-registry.min.json`
- pre-protocol formation-trial judgment and Codex boundary: `mechanics/agon/parts/formation/docs/formation-trial.md`, `mechanics/agon/parts/pre-protocol-boundary/docs/pre-protocol-agent-boundary.md`, `mechanics/agon/parts/pre-protocol-boundary/docs/formation-trial-readiness.md`, `mechanics/codex-projection/parts/agon-boundary/docs/projection-agon-boundary.md`, `mechanics/agon/parts/formation/docs/formation-trial-landing.md`, `mechanics/agon/parts/formation/schemas/formation-trial.schema.json`, and `generated/agent_formation_trial.min.json`
- model tiers, orchestrator classes, and bounded cohort composition: `agents/model_tiers/*.tier.json`, `agents/orchestrator_classes/*.class.json`, `agents/cohort_patterns/*.pattern.json`, `schemas/model-tier.schema.json`, `schemas/orchestrator-class.schema.json`, `schemas/cohort-pattern.schema.json`, `generated/model_tier_registry.json`, `generated/orchestrator_class_catalog.min.json`, and `generated/cohort_composition_registry.json`
- published registries and consumer seams: `generated/agent_registry.min.json`, `generated/model_tier_registry.json`, `generated/cohort_composition_registry.json`, `generated/runtime_seam_bindings.json`, and `mechanics/boundary-bridge/parts/federation-consumer-seams/docs/federation-consumer-seams.md`
- Codex subagent projection, owner refresh law, and workspace install seam: `mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md`, `mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md`, `mechanics/codex-projection/parts/refresh-law/examples/subagent-refresh-law.example.json`, `generated/codex_agents/agents/*.toml`, `generated/codex_agents/config.subagents.generated.toml`, and `mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py`
- Titan role classes, named bearers, runtime roster boundaries, incarnation identity, and generated Codex-agent identity projection: `mechanics/titan/parts/role-bearing/docs/role-bearer-ontology.md`, `mechanics/titan/parts/runtime-roster/docs/runtime-roster.md`, `mechanics/titan/parts/runtime-roster/docs/appserver-bridge-boundary.md`, `mechanics/titan/parts/incarnation-spine/docs/incarnation-spine.md`, `mechanics/titan/parts/incarnation-spine/docs/praxis-plane.md`, `mechanics/titan/parts/role-bearing/schemas/role-class.schema.json`, `mechanics/titan/parts/role-bearing/schemas/bearer-identity.schema.json`, `mechanics/titan/parts/lineage-ledger/schemas/lineage-ledger.schema.json`, `mechanics/titan/parts/incarnation-spine/schemas/incarnation-identity.schema.json`, `mechanics/titan/parts/incarnation-spine/examples/incarnation-identity.example.json`, and `mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py`
- runtime seam bindings and runtime-facing artifact contracts: `agents/runtime_seam/*.binding.json`, `generated/runtime_seam_bindings.json`, `mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.*.schema.json`, and `mechanics/runtime-seam/parts/artifact-contracts/schemas/agent-authority-claim.schema.json`
- additive stress posture and handoff adjuncts: `mechanics/antifragility/parts/stress-posture/schemas/agent-stress-posture.schema.json`, `mechanics/antifragility/parts/stress-posture/schemas/stress-handoff-envelope.schema.json`, `mechanics/antifragility/parts/stress-posture/examples/agent-stress-posture.example.json`, `mechanics/antifragility/parts/stress-posture/examples/stress-handoff-envelope.example.json`, `mechanics/antifragility/parts/stress-posture/docs/stress-posture.md`, and `mechanics/antifragility/parts/stress-posture/docs/stress-handoffs.md`
- via negativa pruning checklist: `mechanics/antifragility/parts/via-negativa/docs/via-negativa-checklist.md`
- progression, recurrence, and self-agent surfaces: `mechanics/rpg/parts/progression-model/docs/agent-progression-model.md`, `mechanics/rpg/parts/progression-model/schemas/agent-progression.schema.json`, `mechanics/rpg/parts/progression-model/examples/agent-progression.example.json`, `mechanics/recurrence/parts/anchor-return/docs/recurrence-discipline.md`, `mechanics/recurrence/parts/recursor-readiness/schemas/role-contract.schema.json`, `mechanics/recurrence/parts/recursor-readiness/examples/session-intent.example.json`, `mechanics/recurrence/parts/codex-recursor-projection/schemas/projection-candidate.schema.json`, `mechanics/recurrence/parts/agon-recursor-boundary/schemas/boundary-report.schema.json`, `mechanics/checkpoint/parts/self-agent-checkpoint/docs/self-agent-checkpoint-stack.md`, `mechanics/checkpoint/parts/self-agent-checkpoint/schemas/self-agent-checkpoint.schema.json`, `mechanics/checkpoint/parts/self-agent-checkpoint/examples/self-agent-checkpoint.example.json`, `mechanics/checkpoint/parts/continuity-lane/docs/self-agency-continuity-lane.md`, `mechanics/checkpoint/parts/continuity-lane/schemas/self-agency-continuity-window.schema.json`, and `mechanics/checkpoint/parts/continuity-lane/examples/self-agency-continuity-window.example.json`
- example and bounded smoke surfaces: `mechanics/runtime-seam/parts/artifact-contracts/examples/*`, `mechanics/checkpoint/parts/self-agent-checkpoint/examples/*`, `mechanics/checkpoint/parts/continuity-lane/examples/*`, `mechanics/checkpoint/parts/reference-routes/docs/reference-route-examples.md`, and `mechanics/runtime-seam/parts/transition-discipline/docs/runtime-artifact-transitions.md`
- adjunct quest and Alpha readiness surfaces: `QUESTBOOK.md`, `quests/`, `mechanics/questbook/parts/execution-passport/docs/quest-execution-passport.md`, `mechanics/questbook/parts/alpha-reference-routes/examples/*`, `mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json`, `generated/quest_catalog.min.json`, and `generated/quest_dispatch.min.json`

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
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
python mechanics/titan/scripts/validate_titan_schemas.py
python mechanics/titan/scripts/validate_titan_examples.py
python mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --out-dir generated/titan_codex_agents/agents --manifest generated/titan_codex_agents/projection_manifest.json --prune --check
python -m unittest discover -s mechanics/titan/parts/codex-projection/tests -p "test_*.py"
python mechanics/antifragility/parts/stress-posture/scripts/validate_stress_posture.py
python mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py
python mechanics/codex-projection/parts/assistant-projection/scripts/validate_assistant_projection_resolver.py
python mechanics/runtime-seam/parts/artifact-contracts/scripts/validate_artifact_contracts.py
python mechanics/checkpoint/scripts/validate_checkpoint_contracts.py
python mechanics/recurrence/scripts/validate_recursor_contracts.py
python mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py
python mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py
python mechanics/experience/scripts/validate_adoption_boundary_contracts.py
python -m pytest -q tests
```

Verify the additive agonic actor-formation surfaces explicitly:

```bash
python mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_agonic_formation.py
```

Verify the additive assistant civil surfaces explicitly:

```bash
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py
python -m pytest -q mechanics/experience/parts/assistant-civil-service/tests/test_assistant_civil_formation.py mechanics/experience/tests/test_experience_assistant_civil_contracts.py
```

Verify the additive formation trial surfaces explicitly:

```bash
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_formation_trial.py
```

Optional bounded consumer smoke checks can be enabled with the documented `AOA_*_ROOT` variables when you want federated reachability checks against sibling repositories.

```bash
AOA_PLAYBOOKS_ROOT=/path/to/aoa-playbooks \
AOA_EVALS_ROOT=/path/to/aoa-evals \
AOA_MEMO_ROOT=/path/to/aoa-memo \
AOA_ROUTING_ROOT=/path/to/aoa-routing \
python scripts/validate_agents.py
```

Refresh published registries only after editing source-authored registry inputs under `agents/profiles/`, `agents/model_tiers/`, `agents/orchestrator_classes/`, `agents/cohort_patterns/`, or `agents/runtime_seam/`:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/profiles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
```

## License

Apache-2.0
