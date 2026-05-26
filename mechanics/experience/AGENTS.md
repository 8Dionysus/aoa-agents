# AGENTS.md

## Applies To

This card applies to `mechanics/experience/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/experience/` routes assistant service, office operation, adoption,
watch, rollback, release hold, and arena-exclusion pressure for the
agent-layer experience.

## Operating Card

| Field | Route |
| --- | --- |
| role | assistant service and experience operation package |
| input | assistant civil, service, office, adoption, release, watch, rollback, arena-exclusion, and regression pressure |
| output | bounded assistant role posture, service contract route, watch or rollback route, or stronger-owner handoff |
| owner | this package for experience routing |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, `mechanics/agon/`, `mechanics/release-support/` |
| tools | assistant civil validator, service contract validator, adoption/boundary validator, repo validators |
| validation | experience contract checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` for provenance accounting
8. stronger owner routes for runtime, proof, memo, or playbook pressure

## Boundaries

- Runtime assistant services do not live here.
- `aoa-playbooks` owns scenario choreography.
- `aoa-evals` owns proof verdicts.
- `aoa-memo` owns durable memory truth.
- Agon formation pressure cross-routes to `mechanics/agon/`.

## Validation

```bash
python mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python -m unittest discover -s mechanics/experience/tests -p 'test_*.py'
python -m unittest discover -s mechanics/experience/parts/assistant-civil-service/tests -p 'test_*.py'
python scripts/validate_agent_service_contracts.py
python mechanics/experience/scripts/validate_adoption_boundary_contracts.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed experience part, assistant service or release surface
affected, checks run, checks skipped, and any stronger-owner handoff.
