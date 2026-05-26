# Schema District

`schemas/` holds repo-wide machine-readable contracts for the source-authored
agent layer.

These root schemas constrain base role profiles, model tiers, orchestrator
classes, cohort patterns, runtime seam bindings, the checked `agents/` source
home manifest, and the generated registries published from those source
families. They are shared contracts, not mechanic payloads.

## Operating Card

| Field | Route |
| --- | --- |
| role | repo-wide agent-layer schema district |
| input | schema lookup, source-object contract edit, generated registry contract edit, or old schema reference |
| output | schema owner route, validator route, generated reader rebuild, or mechanic-local handoff |
| owner | `schemas/AGENTS.md` for root schema law; source family route for meaning |
| next route | `agents/<family>/`, owning builder, `generated/`, or mechanic part-local schema route |
| tools | `scripts/validate_agents.py`, `scripts/build_published_surfaces.py`, family validators |
| validation | `schemas/AGENTS.md#validation` and the source-family checks |

## Current Root Contracts

| Schema | Source family or reader |
| --- | --- |
| `agent-profile.schema.json` | `agents/profiles/*.profile.json` |
| `agent-registry.schema.json` | `generated/agent_registry.min.json` |
| `model-tier.schema.json` | `agents/model_tiers/*.tier.json` |
| `model-tier-registry.schema.json` | `generated/model_tier_registry.json` |
| `orchestrator-class.schema.json` | `agents/orchestrator_classes/*.class.json` and orchestrator readers |
| `cohort-pattern.schema.json` | `agents/cohort_patterns/*.pattern.json` |
| `cohort-composition-registry.schema.json` | `generated/cohort_composition_registry.json` |
| `runtime-seam-binding.schema.json` | `agents/runtime_seam/*.binding.json` |
| `runtime-seam-bindings.schema.json` | `generated/runtime_seam_bindings.json` |
| `agent-source-home.schema.json` | `agents/source_home.manifest.json` |

## Boundary

Mechanic-specific schemas live with the owning mechanic part after the target
part has local route cards and validators. Root schemas remain appropriate when
several source families, generated readers, tests, or public consumers share
the same contract.

Do not loosen a root schema to make a mechanic-local example pass. Move or fix
the mechanic-local contract instead.
