# AGENTS.md

## Applies To

This card applies to `agents/profiles/adjuncts/` and every adjunct family below it.

## Role

`agents/profiles/adjuncts/` holds additive role companions for base profiles.
These objects let agonic actor and assistant civil forms attach to the five
role houses without widening `agents/profiles/*.profile.json` or making a
companion surface stronger than its owning mechanic.

## Operating Card

| Field | Route |
| --- | --- |
| role | source home for profile companion objects |
| input | agonic actor, assistant civil, formation-trial, and role-house survival pressure |
| output | adjunct source object, formation index, validation result, or mechanic handoff |
| owner | this card plus the owning mechanic schema and validator |
| next route | `agents/source_home.manifest.json`, target adjunct family, owning mechanic docs, builder, validator |
| tools | formation and assistant civil builders under `mechanics/*/parts/*/scripts/` |
| validation | `python scripts/validate_agent_source_home.py` plus adjunct validators in `agents/profiles/AGENTS.md` |

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `DESIGN.AGENTS.md`
3. `agents/AGENTS.md`
4. `agents/README.md`
5. `agents/source_home.manifest.json`
6. `agents/profiles/AGENTS.md`
7. the owning mechanic docs and schema for the adjunct family

## Source Families

| Family | Meaning | Owner route |
| --- | --- | --- |
| `kind/` | agonic actor kind posture | `mechanics/agon/parts/formation/` |
| `subjectivity/` | subjectivity and speaking-position posture | `mechanics/agon/parts/formation/` |
| `office_overlay/` | office and capability overlay posture | `mechanics/experience/parts/office-operations/` |
| `arena_eligibility/` | pre-arena eligibility posture | `mechanics/agon/parts/arena-rank-school/` |
| `resistance_revision/` | resistance and revision posture | `mechanics/agon/parts/formation/` |
| `assistant_variant/` | assistant civil variant posture | `mechanics/experience/parts/assistant-civil-service/` |
| `assistant_service_identity/` | assistant service identity posture | `mechanics/experience/parts/assistant-civil-service/` |
| `assistant_service_contract/` | assistant service contract posture | `mechanics/experience/parts/assistant-civil-service/` |
| `assistant_service_governance/` | assistant service governance posture | `mechanics/experience/parts/assistant-civil-service/` |
| `assistant_service_certification/` | assistant service certification posture | `mechanics/experience/parts/assistant-civil-service/` |
| `assistant_arena_exclusion/` | assistant arena-exclusion posture | `mechanics/experience/parts/arena-exclusion/` |

## Boundaries

- Keep adjuncts additive to base profiles.
- Keep mechanic-specific schema meaning with the owning mechanic part.
- Do not turn companion forms into live arena authority, verdict logic, scars,
  retention history, runtime packets, or ToS promotion.
- Do not move these objects into generated readers or root schemas as a
  shortcut around mechanic-local validation.

## Validation

Run:

```bash
python scripts/validate_agent_source_home.py
python mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
```

## Closeout

Report which adjunct families changed, which formation readers stayed current,
which mechanic-owned validators ran, and whether the base profile contract was
left untouched.
