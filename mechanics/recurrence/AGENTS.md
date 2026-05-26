# AGENTS.md

## Applies To

This card applies to `mechanics/recurrence/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/recurrence/` routes recursor and recurrence pressure for agents:
recursor readiness, paired recurrence, Codex recursor projection,
component manifests, anchor return, and Agon recursor boundaries.

## Operating Card

| Field | Route |
| --- | --- |
| role | recursor and recurrence operation package |
| input | recursor pair, role, readiness, projection, component manifest, return, and recurrence pressure |
| output | bounded recurrence route, generated recursor reader, projection handoff, or stronger-owner handoff |
| owner | this package for agent-layer recurrence routing |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, recursor builders, `mechanics/codex-projection/`, `mechanics/agon/` |
| tools | recursor builders, recursor validators, component manifest validator, repo validators |
| validation | recursor contract checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` for provenance accounting
8. stronger owner routes for runtime, memo, or playbook recurrence pressure

## Boundaries

- AoA center owns recurrence doctrine.
- Runtime owners own live recurrence execution.
- `aoa-memo` owns durable memory continuity.
- `aoa-playbooks` owns recurring scenario choreography.

## Validation

```bash
python mechanics/recurrence/scripts/build_recursor_role_readiness.py --check
python mechanics/recurrence/scripts/build_recursor_projection_candidates.py --check
python mechanics/recurrence/scripts/validate_recursor_contracts.py
python mechanics/recurrence/scripts/validate_recursor_role_readiness.py
python mechanics/recurrence/scripts/validate_recursor_boundary.py
python scripts/validate_recurrence_component_manifests.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed recurrence part, generated reader or component manifest
affected, checks run, checks skipped, and any runtime, memo, or playbook
handoff.
