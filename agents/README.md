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
| owner | `agents/source_home.manifest.json` plus nearest branch `AGENTS.md` |
| next route | target family, builder, generated reader, validator |
| tools | `scripts/validate_agent_source_home.py`, `scripts/build_published_surfaces.py`, and family-specific builders |
| validation | `scripts/validate_agent_source_home.py`, `scripts/validate_agents.py`, plus family-specific checks |

## Active Source Families

`agents/` has two active branches:

- `agents/roles/` for role houses: each role owns its base profile and nested
  agonic/assistant forms plus role-owned specializations.
- `agents/operating-model/` for cross-role operating contracts: tiers,
  capability packs, orchestrators, cohorts, and runtime-seam bindings.

| Family | Path | Publishes To |
| --- | --- | --- |
| base role houses | `agents/roles/*/profile.json` | `generated/agent_registry.min.json` |
| agonic and assistant companions | `agents/roles/*/forms/` | formation indexes under `generated/` |
| role specializations | `agents/roles/*/specializations/*/specialization.json` | `generated/role_specialization_catalog.min.json` |
| capability packs | `agents/operating-model/capabilities/packs/*.capability.json` | `generated/capability_pack_registry.min.json` |
| model tiers | `agents/operating-model/tiers/*.tier.json` | `generated/model_tier_registry.json` |
| orchestrator classes | `agents/operating-model/orchestrators/*.class.json` | orchestrator generated readers |
| cohort patterns | `agents/operating-model/cohorts/*.pattern.json` | `generated/cohort_composition_registry.json` |
| runtime seam bindings | `agents/operating-model/runtime-seams/*.binding.json` | `generated/runtime_seam_bindings.json` |

## Source Home Contract

`agents/source_home.manifest.json` is the machine-checkable atlas for this
home. It deliberately does not replace the source objects. It records:

- which branches are allowed to live directly under `agents/`;
- which branch card owns local editing posture;
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

For agonic or assistant forms, read `agents/roles/AGENTS.md` before editing any
companion object. Form source stays in the owning role house; mechanic-local
schemas, docs, and validators stay with the owning mechanic part.

For specializations, keep the source inside the base role house and reference a
capability pack from `agents/operating-model/capabilities/packs/`. This keeps
`coder`, `reviewer`, `architect`, and other roles stable while allowing
`coder.repo-refactor` or `reviewer.route-drift-review` to carry narrower
permission, tool, skill, technique, memory, and proof posture.

Codex custom-agent projection currently installs the base role profiles only.
Specializations are published through
`generated/role_specialization_catalog.min.json`; they do not become
`.codex/agents/` entries until a separate projection eligibility surface says
which specialization is installable, with which permissions, and under whose
refresh law.
That eligibility queue lives under
`mechanics/codex-projection/parts/specialization-eligibility/records/`, with a
generated readiness reader at
`mechanics/codex-projection/parts/specialization-eligibility/generated/specialization-eligibility-readiness.min.json`.

## Stop Lines

- `agents/` is not `.agents/`.
- `agents/` is not a runtime worker home.
- `agents/` is not a proof, memo, route, playbook, or skill owner.
- `agents/` does not make generated readers authoritative over source objects.
- `agents/source_home.manifest.json` is a route contract, not a generated
  reader and not a replacement for family source files.
