# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/checkpoint/` routes reviewable agent continuity: self-agent
checkpoint posture, continuity lanes, reviewed closeout role holds, reference
routes, and growth-facing checkpoint boundaries.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent-layer checkpoint and continuity package |
| input | self-agent, checkpoint, continuity, stress handoff, reviewed-closeout, reference-route, and growth posture pressure |
| output | bounded checkpoint posture, continuity route, review hold, or memory/proof/playbook handoff |
| owner | this package for checkpoint routing |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, `mechanics/antifragility/`, `mechanics/questbook/` |
| tools | checkpoint contract validator, reference-route validator, repo validators |
| validation | checkpoint and reference-route checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` for provenance accounting
8. `mechanics/ARTIFACT_TOPOLOGY.md` before moving artifacts

## Boundaries

- Durable memory truth belongs to `aoa-memo`.
- Proof verdicts belong to `aoa-evals`.
- Scenario closeout choreography belongs to `aoa-playbooks`.
- Runtime checkpoint execution belongs to runtime owners.

## Validation

```bash
python mechanics/checkpoint/scripts/validate_checkpoint_contracts.py
python scripts/validate_reference_route_contracts.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed checkpoint part, continuity or reference route affected,
checks run, checks skipped, and any memory/proof/playbook handoff.
