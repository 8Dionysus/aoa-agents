# Agent Source District

`agents/` is the source-authored district for role-bearing agent objects in
`aoa-agents`.

The district exists so the repo has one obvious home for agent-layer objects
instead of scattering profile, tier, cohort, class, and seam source inputs at
the repository root.

## Operating Card

| Field | Route |
| --- | --- |
| role | source district for agent-layer objects |
| input | source JSON edits and adjacent docs/schema pressure |
| output | source object, generated reader, or stronger-owner handoff |
| owner | nearest `agents/<family>/AGENTS.md` |
| next route | target family, builder, generated reader, validator |
| tools | `scripts/build_published_surfaces.py` and family-specific builders |
| validation | `python scripts/validate_agents.py` plus family-specific checks |

## Active Source Families

| Family | Path | Publishes To |
| --- | --- | --- |
| role profiles | `agents/profiles/*.profile.json` | `generated/agent_registry.min.json` |
| agonic and assistant adjuncts | `agents/profiles/adjuncts/` | formation indexes under `generated/` |
| model tiers | `agents/model_tiers/*.tier.json` | `generated/model_tier_registry.json` |
| orchestrator classes | `agents/orchestrator_classes/*.class.json` | orchestrator generated readers |
| cohort patterns | `agents/cohort_patterns/*.pattern.json` | `generated/cohort_composition_registry.json` |
| runtime seam bindings | `agents/runtime_seam/*.binding.json` | `generated/runtime_seam_bindings.json` |

## Traversal

Start from the family that owns the source object, then follow its local
`AGENTS.md`.

Use `docs/` for public explanation, `schemas/` for shared contract shape,
`examples/` for schema-backed examples, `generated/` for derived readers, and
`mechanics/` for repeatable operation topology around these source families.

## Stop Lines

- `agents/` is not `.agents/`.
- `agents/` is not a runtime worker home.
- `agents/` is not a proof, memo, route, playbook, or skill owner.
- `agents/` does not make generated readers authoritative over source objects.
