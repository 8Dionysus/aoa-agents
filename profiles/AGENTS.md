# profiles/AGENTS.md

## Purpose

`profiles/` is the source-authored role-contract surface for reusable agent roles in `aoa-agents`.

## Source of truth

Canonical authoring lives in:

- `profiles/*.profile.json`
- `schemas/agent-profile.schema.json`

Published derived surface:

- `generated/agent_registry.min.json`

Read with:

- `docs/AGENT_PROFILE_SURFACE.md`
- `docs/AGENT_MEMORY_POSTURE.md`
- `docs/BOUNDARIES.md`

## Owns here

Keep this directory focused on role-bearing agent identity and posture:

- stable agent ids, names, and roles
- `mission`, `owns`, and `does_not_own`
- `handoff_rule` and `handoff_triggers`
- `memory_posture` and `memory_rights`
- `evaluation_posture` and `evaluation_focus`
- references to preferred skill families, cohort patterns, and tier ids

## Does not own

Do not turn a profile into:

- a skill bundle from `aoa-skills`
- proof doctrine from `aoa-evals`
- memory-object canon from `aoa-memo`
- routing logic from `aoa-routing`
- scenario composition from `aoa-playbooks`

## Editing posture

Treat changes to `id`, `name`, `role`, handoff posture, memory rights, evaluation posture, or boundary wording as semantic contract changes.
Keep profiles compact and reviewable.
Do not add giant persona prose, hidden orchestration logic, or secret operational assumptions.

## Validation

Run:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```
