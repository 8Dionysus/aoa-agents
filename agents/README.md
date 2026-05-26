# Agent Source Home

`agents/` is the source-authored home for role-bearing agent objects in
`aoa-agents`.

The home exists so the repo has one obvious source body for agent-layer objects
instead of scattering profile, tier, cohort, class, adjunct, and seam inputs at
the repository root or inside operation mechanics.

Its checked contract is `source_home.manifest.json`. The manifest names every
active source family, the family owner route, publication targets, validation
routes, and stronger-owner stop lines.

## Operating Card

| Field | Route |
| --- | --- |
| role | source home for agent-layer objects |
| input | source JSON edits and adjacent docs/schema pressure |
| output | source object, generated reader, checked home manifest, or stronger-owner handoff |
| owner | `agents/source_home.manifest.json` plus nearest `agents/<family>/AGENTS.md` |
| next route | target family, builder, generated reader, validator |
| tools | `scripts/validate_agent_source_home.py`, `scripts/build_published_surfaces.py`, and family-specific builders |
| validation | `python scripts/validate_agent_source_home.py`, `python scripts/validate_agents.py`, plus family-specific checks |

## Active Source Families

| Family | Path | Publishes To |
| --- | --- | --- |
| base role houses | `agents/profiles/*.profile.json` | `generated/agent_registry.min.json` |
| agonic and assistant companions | `agents/profiles/adjuncts/` | formation indexes under `generated/` |
| model tiers | `agents/model_tiers/*.tier.json` | `generated/model_tier_registry.json` |
| orchestrator classes | `agents/orchestrator_classes/*.class.json` | orchestrator generated readers |
| cohort patterns | `agents/cohort_patterns/*.pattern.json` | `generated/cohort_composition_registry.json` |
| runtime seam bindings | `agents/runtime_seam/*.binding.json` | `generated/runtime_seam_bindings.json` |

## Source Home Contract

`agents/source_home.manifest.json` is the machine-checkable atlas for this
home. It deliberately does not replace the source objects. It records:

- which families are allowed to live directly under `agents/`;
- which family card owns local editing posture;
- which schema or mechanic-local contract constrains each family;
- which generated readers each family publishes;
- which builders and validators prove the family stayed coherent;
- which stronger owner handles pressure that does not belong in `aoa-agents`.

The manifest should change when a source family is added, removed, renamed,
or given a new publication/validation route. It should not be used as a
shortcut for editing generated readers.

## Traversal

Start from the family that owns the source object, then follow its local
`AGENTS.md`.

Use `docs/` for public explanation, `schemas/` for shared contract shape,
`examples/` for schema-backed examples, `generated/` for derived readers, and
`mechanics/` for repeatable operation topology around these source families.

For adjuncts, read `agents/profiles/adjuncts/AGENTS.md` before editing any
companion object. Adjunct source stays in `agents/`; mechanic-local schemas,
docs, and validators stay with the owning mechanic part.

## Stop Lines

- `agents/` is not `.agents/`.
- `agents/` is not a runtime worker home.
- `agents/` is not a proof, memo, route, playbook, or skill owner.
- `agents/` does not make generated readers authoritative over source objects.
- `agents/source_home.manifest.json` is a route contract, not a generated
  reader and not a replacement for family source files.
