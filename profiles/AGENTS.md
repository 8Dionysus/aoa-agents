# profiles/AGENTS.md

## Purpose

`profiles/` is the source-authored role-contract surface for reusable agent roles in `aoa-agents`.

## Source of truth

Canonical authoring lives in:

- `profiles/*.profile.json`
- `profiles/adjuncts/*`
- `schemas/agent-profile.schema.json`

Published derived surface:

- `generated/agent_registry.min.json`
- `generated/agent_agonic_formation_index.min.json`
- `generated/assistant_civil_formation_index.min.json`

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
- additive agonic and assistant companion surfaces under `profiles/adjuncts/`
  that keep `kind`, subjectivity, office overlay, arena eligibility,
  resistance/revision posture, service identity, service contract,
  service governance, certification, and arena exclusion separate from the
  base profile contract

## Does not own

Do not turn a profile into:

- a skill bundle from `aoa-skills`
- proof doctrine from `aoa-evals`
- memory-object canon from `aoa-memo`
- routing logic from `aoa-routing`
- scenario composition from `aoa-playbooks`
- protocol law, verdicts, scars, retention history, runtime packets, or ToS
  promotion authority

## Editing posture

Treat changes to `id`, `name`, `role`, handoff posture, memory rights, evaluation posture, or boundary wording as semantic contract changes.
Keep profiles compact and reviewable.
Do not add giant persona prose, hidden orchestration logic, or secret operational assumptions.
Keep the base `*.profile.json` files stable. When Agon-facing actor form is the
real change, prefer the adjunct families under `profiles/adjuncts/` instead of
widening `schemas/agent-profile.schema.json` casually.

## Validation

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

If `profiles/adjuncts/` changed, also run:

```bash
python scripts/build_agent_agonic_formation_index.py --check
python scripts/validate_agent_agonic_formation.py
python -m pytest -q tests/test_agent_agonic_formation.py
python scripts/build_assistant_civil_formation_index.py --check
python scripts/validate_assistant_civil_formation.py
python -m pytest -q tests/test_assistant_civil_formation.py
```
