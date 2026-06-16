# Current Contour

This document keeps the shipped `aoa-agents` surface contour discoverable
without making `README.md` or `ROADMAP.md` carry every path.

It is a route map, not a source of role meaning. Source objects, mechanic
packages, generated builders, tests, and sibling owners keep authority.

## Operating Card

| Field | Route |
| --- | --- |
| role | compact shipped-surface contour for the role layer |
| input | "where is the current surface for this role-layer family?" |
| output | route family, owner surface, generated reader, or validation lane |
| owner | this map for discoverability; named source or mechanic owns meaning |
| next route | source object, mechanic package, generated reader, builder, validator, or sibling owner |
| validation | root `AGENTS.md#verify` and the owning route-family `AGENTS.md` when this map moves |

## Release Marker

Current release: `v0.4.0`.

The current release line is `v0.4.x`: role-layer topology hardening over an
already-landed bootstrap baseline.

## Source And Generated Spine

| Family | Source | Generated / reader |
| --- | --- | --- |
| base role houses | `agents/roles/*/profile.json` | `generated/agent_registry.min.json` |
| agonic and assistant companion forms | `agents/roles/*/forms/` | `generated/agent_agonic_formation_index.min.json`, `generated/assistant_civil_formation_index.min.json`, `generated/agent_formation_trial.min.json` |
| role specializations | `agents/roles/*/specializations/*/specialization.json` | `generated/role_specialization_catalog.min.json` |
| capability packs | `agents/operating-model/capabilities/packs/*.capability.json` | `generated/capability_pack_registry.min.json` |
| model tiers | `agents/operating-model/tiers/*.tier.json` | `generated/model_tier_registry.json` |
| orchestrator classes | `agents/operating-model/orchestrators/*.class.json` | `generated/orchestrator_class_catalog.min.json`, `generated/orchestrator_class_capsules.json`, `generated/orchestrator_class_sections.full.json` |
| cohort patterns | `agents/operating-model/cohorts/*.pattern.json` | `generated/cohort_composition_registry.json` |
| runtime seam bindings | `agents/operating-model/runtime-seams/*.binding.json` | `generated/runtime_seam_bindings.json` |

## Codex Projection

| Surface | Route |
| --- | --- |
| source projection law | `mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md` |
| refresh law | `mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md` |
| refresh example | `mechanics/codex-projection/parts/refresh-law/examples/subagent-refresh-law.example.json` |
| projection wiring | `mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json` |
| generated workspace config | `generated/codex_agents/config.subagents.generated.toml` |
| generated agents | `generated/codex_agents/agents/*.toml` |
| projection manifest | `generated/codex_agents/projection_manifest.json` |
| validator script | `mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py` |
| validation route | `mechanics/codex-projection/AGENTS.md` and the subagent projection part route |

Codex custom-agent projection remains `base_role_profiles_only`.
Specializations are visible through source and generated catalogs, but they do
not become installed agents unless an eligibility record promotes them.

## Specialization Eligibility

| Surface | Route |
| --- | --- |
| gate docs | `mechanics/codex-projection/parts/specialization-eligibility/docs/specialization-eligibility.md` |
| records | `mechanics/codex-projection/parts/specialization-eligibility/records/` |
| readiness reader | `mechanics/codex-projection/parts/specialization-eligibility/generated/specialization-eligibility-readiness.min.json` |
| builder script | `mechanics/codex-projection/parts/specialization-eligibility/scripts/build_specialization_eligibility_readiness.py` |
| validator script | `mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py` |
| validation route | `mechanics/codex-projection/AGENTS.md` and the specialization eligibility part route |

Eligibility is candidate-only and non-installing.

## Agonic Actor Rechartering

| Surface | Route |
| --- | --- |
| subject prep | `mechanics/agon/parts/formation/docs/subject-prep.md` |
| rechartering doctrine | `mechanics/agon/parts/formation/docs/actor-rechartering.md` |
| landing | `mechanics/agon/parts/formation/docs/agonic-actor-rechartering-landing.md` |
| kind model | `mechanics/agon/parts/formation/docs/kind-model.md` |
| subjectivity model | `mechanics/agon/parts/formation/docs/subjectivity-model.md` |
| office overlay | `mechanics/experience/parts/office-operations/docs/agent-office-model.md` |
| arena eligibility | `mechanics/agon/parts/arena-rank-school/docs/arena-eligibility-model.md` |
| resistance and revision | `mechanics/agon/parts/formation/docs/resistance-revision-posture.md` |
| schemas | `mechanics/agon/parts/formation/schemas/agent-kind.schema.json`, `mechanics/agon/parts/formation/schemas/subjectivity.schema.json`, `mechanics/agon/parts/formation/schemas/office-overlay.schema.json`, `mechanics/agon/parts/arena-rank-school/schemas/arena-eligibility.schema.json`, `mechanics/agon/parts/formation/schemas/resistance-revision.schema.json` |
| generated reader | `generated/agent_agonic_formation_index.min.json` |
| example | `mechanics/agon/parts/formation/examples/agent-agonic-formation.example.json` |
| builder script | `mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py` |
| validator script | `mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py` |
| test route | `mechanics/agon/parts/formation/tests/test_agent_agonic_formation.py` |
| validation route | `mechanics/agon/AGENTS.md` and the formation part route |

Agonic Actor Rechartering has now landed as an additive companion-form turn.

## Assistant Civil Rechartering

| Surface | Route |
| --- | --- |
| civil rechartering | `mechanics/experience/parts/assistant-civil-service/docs/civil-rechartering.md` |
| landing | `mechanics/agon/parts/formation/docs/assistant-civil-rechartering-landing.md` |
| assistant kind | `mechanics/experience/parts/assistant-civil-service/docs/assistant-kind-model.md` |
| service identity | `mechanics/experience/parts/assistant-civil-service/docs/service-identity-model.md` |
| service contract | `mechanics/experience/parts/assistant-civil-service/docs/service-contract-model.md` |
| service governance | `mechanics/experience/parts/assistant-civil-service/docs/service-governance-model.md` |
| service certification | `mechanics/experience/parts/assistant-civil-service/docs/service-certification-model.md` |
| arena exclusion | `mechanics/experience/parts/arena-exclusion/docs/arena-exclusion-model.md` |
| escalation | `mechanics/experience/parts/arena-exclusion/docs/escalation-to-agon.md` |
| schemas | `mechanics/experience/parts/assistant-civil-service/schemas/assistant-variant.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-identity.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-contract.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-governance.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/service-certification.schema.json`, `mechanics/experience/parts/assistant-civil-service/schemas/civil-formation.schema.json`, `mechanics/experience/parts/arena-exclusion/schemas/arena-exclusion.schema.json` |
| generated reader | `generated/assistant_civil_formation_index.min.json` |
| example | `mechanics/experience/parts/assistant-civil-service/examples/civil-formation.example.json` |
| builder script | `mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py` |
| validator script | `mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py`, `mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py` |
| test route | `mechanics/experience/parts/assistant-civil-service/tests/test_assistant_civil_formation.py`, `mechanics/experience/tests/test_experience_assistant_civil_contracts.py` |
| validation route | `mechanics/experience/AGENTS.md` and the assistant civil service part route |

Assistant Civil Rechartering has now landed as a civil/service companion-form
turn, not as contestant or judge authority.

## Formation Trial

| Surface | Route |
| --- | --- |
| trial doctrine | `mechanics/agon/parts/formation/docs/formation-trial.md` |
| pre-protocol boundary | `mechanics/agon/parts/pre-protocol-boundary/docs/pre-protocol-agent-boundary.md` |
| readiness | `mechanics/agon/parts/pre-protocol-boundary/docs/formation-trial-readiness.md` |
| Codex boundary | `mechanics/codex-projection/parts/agon-boundary/docs/projection-agon-boundary.md` |
| landing | `mechanics/agon/parts/formation/docs/formation-trial-landing.md` |
| schema | `mechanics/agon/parts/formation/schemas/formation-trial.schema.json` |
| generated reader | `generated/agent_formation_trial.min.json` |
| example | `mechanics/agon/parts/formation/examples/formation-trial.example.json` |
| builder script | `mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py` |
| validator script | `mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py` |
| test route | `mechanics/agon/parts/formation/tests/test_agent_formation_trial.py` |
| validation route | `mechanics/agon/AGENTS.md` and the formation part route |

Formation Trial has now landed as pre-protocol readability judgment.

## Titan Role Bearing

| Surface | Route |
| --- | --- |
| service cohort | `mechanics/titan/parts/service-cohort/docs/service-cohort.md` |
| summon boundary | `mechanics/titan/parts/summon-boundary/docs/summon-boundary.md` |
| role bearer ontology | `mechanics/titan/parts/role-bearing/docs/role-bearer-ontology.md` |
| lineage ledger | `mechanics/titan/parts/lineage-ledger/docs/lineage-ledger.md` |
| incarnation spine | `mechanics/titan/parts/incarnation-spine/docs/incarnation-spine.md` |
| praxis plane | `mechanics/titan/parts/incarnation-spine/docs/praxis-plane.md` |
| source config | `mechanics/titan/parts/role-bearing/config/role-classes.v0.json`, `mechanics/titan/parts/role-bearing/config/bearers.v0.json`, `mechanics/titan/parts/lineage-ledger/config/ledger.v0.json` |
| incarnation schema/example | `mechanics/titan/parts/incarnation-spine/schemas/incarnation-identity.schema.json`, `mechanics/titan/parts/incarnation-spine/examples/incarnation-identity.example.json` |
| runtime roster docs | `mechanics/titan/parts/runtime-roster/docs/runtime-roster.md`, `mechanics/titan/parts/runtime-roster/docs/appserver-bridge-boundary.md`, `mechanics/titan/parts/runtime-roster/docs/agent-report-boundary.md` |
| Titan Codex projection part | `mechanics/titan/parts/codex-projection/README.md` |
| Titan Codex projection output | `generated/titan_codex_agents/agents/*.toml`, `generated/titan_codex_agents/projection_manifest.json` |
| Titan Codex projection validation | `mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py`, `mechanics/titan/parts/codex-projection/tests/test_titan_codex_projection.py` |

Titan surfaces are role-bearing and lineage posture inside `aoa-agents`; AoA
center and runtime owners keep their stronger authority.

## Stress, Runtime, Workspace, And Quest Surfaces

| Family | Route |
| --- | --- |
| Agent Stress Posture | `mechanics/antifragility/parts/stress-posture/docs/stress-posture.md` |
| Agent Stress Handoffs | `mechanics/antifragility/parts/stress-posture/docs/stress-handoffs.md` |
| runtime role-tier bindings | `mechanics/runtime-seam/parts/role-tier-bindings/docs/agent-runtime-seam.md` |
| runtime artifact transitions | `mechanics/runtime-seam/parts/transition-discipline/docs/runtime-artifact-transitions.md` |
| workspace trigger posture | `mechanics/boundary-bridge/parts/workspace-trigger/docs/workspace-surface-trigger-posture.md` |
| federation consumer seams | `mechanics/boundary-bridge/parts/federation-consumer-seams/docs/federation-consumer-seams.md` |
| Quest execution passport | `mechanics/questbook/parts/execution-passport/docs/quest-execution-passport.md` |
| Alpha reference routes | `mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json` |
| quest readers | `generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json` |
| workspace checkpoint-growth role posture | `mechanics/checkpoint/parts/growth-checkpoint/docs/workspace-checkpoint-growth-role-posture.md` |

## Root Validation Route

Use root `AGENTS.md#verify` for exact commands. This contour names shipped
surface families and owner routes; it does not own executable validation blocks.

When generated readers or source objects move, add the relevant builder checks
from the owning source or mechanic `AGENTS.md`.
