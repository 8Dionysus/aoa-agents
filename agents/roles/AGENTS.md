# agents/roles/AGENTS.md

## Purpose

`agents/roles/` is the source-authored role-contract surface for reusable agent roles in `aoa-agents`.

## Source of truth

Canonical authoring lives in:

- `agents/roles/*/profile.json`
- `agents/roles/*/forms/*`
- `agents/roles/*/specializations/*/specialization.json`
- `schemas/agent-profile.schema.json`
- `schemas/role-specialization.schema.json`

Published derived surface:

- `generated/agent_registry.min.json`
- `generated/role_specialization_catalog.min.json`
- `generated/agent_agonic_formation_index.min.json`
- `generated/assistant_civil_formation_index.min.json`
- `generated/agent_formation_trial.min.json`

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
- additive agonic and assistant companion surfaces under `agents/roles/*/forms/`
  that keep `kind`, subjectivity, office overlay, arena eligibility,
  resistance/revision posture, service identity, service contract,
  service governance, certification, and arena exclusion separate from the
  base profile contract
- role-house survival inputs that the formation trial reads without
  widening the base profile contract or turning candidate seats into live
  authority
- role-owned specializations that narrow a base role into a named operating
  posture while referencing reusable capability packs from
  `agents/operating-model/capabilities/packs/`

## Does not own

Do not turn a profile into:

- a skill bundle from `aoa-skills`
- proof doctrine from `aoa-evals`
- memory-object canon from `aoa-memo`
- routing logic from `aoa-routing`
- scenario composition from `aoa-playbooks`
- tool implementation, technique bodies, or permission policy outside the
  referenced capability pack
- protocol law, verdicts, scars, retention history, runtime packets, or ToS
  promotion authority

## Editing posture

Treat changes to `id`, `name`, `role`, handoff posture, memory rights, evaluation posture, or boundary wording as semantic contract changes.
Keep profiles compact and reviewable.
Do not add giant persona prose, hidden orchestration logic, or secret operational assumptions.
Keep each base `profile.json` file stable. When Agon-facing actor form is the
real change, prefer the adjunct families under `agents/roles/*/forms/` instead of
widening `schemas/agent-profile.schema.json` casually.
When a role needs a narrower operating lane, add a specialization under
`agents/roles/<role>/specializations/<slug>/specialization.json` and point it at
a capability pack. Do not create top-level `coder-*`, `reviewer-*`, or
`architect-*` role houses unless the base role taxonomy itself changes.

## Validation

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

If `agents/roles/*/forms/` changed, also run:

```bash
python mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_agonic_formation.py
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python -m pytest -q mechanics/experience/parts/assistant-civil-service/tests/test_assistant_civil_formation.py
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_formation_trial.py
```
