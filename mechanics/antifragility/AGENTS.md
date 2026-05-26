# AGENTS.md

## Applies To

This card applies to `mechanics/antifragility/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/antifragility/` routes failure-pressure learning for agents:
stress posture, via negativa checks, scar/adaptation surfaces, and bounded
survival language.

## Operating Card

| Field | Route |
| --- | --- |
| role | failure-pressure and negative-check package for the agent layer |
| input | stress, via negativa, scar, retention, adaptation, and degradation pressure |
| output | bounded stress posture, negative checklist, adaptation route, or proof/memory handoff |
| owner | this package for antifragility routing |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, `mechanics/checkpoint/`, `mechanics/agon/` |
| tools | stress-posture validator, repo validators |
| validation | targeted stress checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` before using `legacy/`
8. `mechanics/ARTIFACT_TOPOLOGY.md` before moving artifacts

## Boundaries

- Proof of resilience belongs to `aoa-evals`.
- Durable memory of scars belongs to `aoa-memo`.
- Runtime fault handling belongs to runtime owners.
- Negative constraints should route to positive operational alternatives.

## Validation

```bash
python scripts/validate_antifragility_stress.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed antifragility part, stress or via negativa surface, checks
run, checks skipped, and any proof or memory handoff.
