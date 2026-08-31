# Schema District

`schemas/` holds repo-wide machine-readable contracts for the source-authored
agent layer.

These root schemas constrain base role profiles, role specializations,
capability packs, model tiers, orchestrator classes, cohort patterns, runtime
seam bindings, the checked `agents/` source home manifest, and the generated
registries published from those source families. They are shared contracts,
not mechanic payloads.

## Operating Card

| Field | Route |
| --- | --- |
| role | repo-wide agent-layer schema district |
| input | schema lookup, source-object contract edit, generated registry contract edit, or old schema reference |
| output | schema owner route, validator route, generated reader rebuild, or mechanic-local handoff |
| owner | `schemas/AGENTS.md` for root schema law; source family route for meaning |
| next route | `agents/<family>/`, owning builder, `generated/`, or mechanic part-local schema route |
| tools | `scripts/validate_agents.py`, `scripts/build_published_surfaces.py`, family validators |
| validation | root [VALIDATION.md](../VALIDATION.md), with `schemas/AGENTS.md#validation` identifying the local route and source-family checks |

## Current Root Contracts

| Schema | Source family or reader |
| --- | --- |
| `agent-profile.schema.json` | `agents/roles/*/profile.json` |
| `role-specialization.schema.json` | `agents/roles/*/specializations/*/specialization.json` |
| `agent-registry.schema.json` | `generated/agent_registry.min.json` |
| `capability-pack.schema.json` | `agents/operating-model/capabilities/packs/*.capability.json` |
| `model-tier.schema.json` | `agents/operating-model/tiers/*.tier.json` |
| `model-tier-registry.schema.json` | `generated/model_tier_registry.json` |
| `orchestrator-class.schema.json` | `agents/operating-model/orchestrators/*.class.json` and orchestrator readers |
| `cohort-pattern.schema.json` | `agents/operating-model/cohorts/*.pattern.json` |
| `cohort-composition-registry.schema.json` | `generated/cohort_composition_registry.json` |
| `runtime-seam-binding.schema.json` | `agents/operating-model/runtime-seams/*.binding.json` |
| `runtime-seam-bindings.schema.json` | `generated/runtime_seam_bindings.json` |
| `agent-source-home.schema.json` | `agents/source_home.manifest.json` |
| `active-organ-agent-local-namespace-v0.schema.json` | optional agent-local episodic/procedural namespace posture and reviewed-promotion boundary |

The active-organ namespace contract and its cross-file role binding use the
schema route in `schemas/AGENTS.md` and executable checks in root
[VALIDATION.md](../VALIDATION.md).

## Mechanic-local Schema Families

Mechanic-specific schemas live beside the part that owns their meaning and
validator:

| Family | Schema route | Validator route |
| --- | --- | --- |
| runtime artifact contracts | `mechanics/runtime-seam/parts/artifact-contracts/schemas/` | artifact-contract validator |
| self-agent checkpoint and continuity | `mechanics/checkpoint/parts/{self-agent-checkpoint,continuity-lane}/schemas/` | checkpoint contract validator |
| checkpoint and Alpha reference routes | `mechanics/{checkpoint,questbook}/parts/*reference-routes*/schemas/` | reference-route contract validator |
| Titan | `mechanics/titan/parts/*/schemas/` | Titan schema validator |
| antifragility stress | `mechanics/antifragility/parts/stress-posture/schemas/` | stress-posture validator |
| RPG progression | `mechanics/rpg/parts/progression-model/schemas/` | RPG progression validator |
| assistant projection | `mechanics/codex-projection/parts/assistant-projection/schemas/` | assistant-projection validator |
| recurrence | `mechanics/recurrence/parts/{recursor-readiness,codex-recursor-projection,agon-recursor-boundary}/schemas/` | recurrence contract validators |
| Agon formation, rank, school, and epistemic actor | `mechanics/agon/parts/{formation,arena-rank-school,epistemic-actor}/schemas/` | Agon formation and rank/epistemic validators |
| assistant civil service and arena exclusion | `mechanics/experience/parts/{assistant-civil-service,arena-exclusion}/schemas/` | Experience assistant-civil validators |
| adoption and boundary bridge | Agon adoption-retention, boundary-bridge parts, and Experience adoption/office parts | adoption-boundary validator |
| agent service and release hold | Experience parts, runtime artifact contracts, and release-support runtime-release-hold | agent-service validator |

The executable commands for these families stay in root
[VALIDATION.md](../VALIDATION.md); the nearest mechanic and part route owns
applicability and stop-lines.

## Boundary

Mechanic-specific schemas live with the owning mechanic part after the target
part has local route cards and validators. Root schemas remain appropriate when
several source families, generated readers, tests, or public consumers share
the same contract.

Do not loosen a root schema to make a mechanic-local example pass. Move or fix
the mechanic-local contract instead.
