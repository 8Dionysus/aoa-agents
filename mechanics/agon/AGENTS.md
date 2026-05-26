# AGENTS.md

## Applies To

This card applies to `mechanics/agon/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/agon/` is the agent-layer Agon operation package. It routes
formation, contest posture, arena boundaries, rank and school posture,
epistemic actor discipline, recursor boundaries, and adoption or retention
after trial pressure.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent-layer Agon operation package |
| input | Agon, formation, arena, rank, school, trial, scar, adoption, retention, and epistemic actor pressure |
| output | bounded role posture, formation contract route, generated-reader posture, or stronger-owner handoff |
| owner | this package for operation routing; `agents/profiles/adjuncts/` and part-local config/schema/example surfaces own source payloads |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, Agon builders, decision records |
| tools | Agon contract validators, formation builders, generated-reader builders, repo validators |
| validation | this card's `Validation` section plus touched part-local checks |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` for provenance accounting
8. `mechanics/ARTIFACT_TOPOLOGY.md` before moving source, support, generated, schema, example, script, or test payloads

## Boundaries

- AoA center owns Agon doctrine.
- `aoa-playbooks` owns scenario choreography.
- `aoa-evals` owns proof verdicts about trials.
- Runtime owners own live execution.
- Formation is a part of Agon here, not the parent mechanic.

## Validation

Run the narrow builder or validator for the affected part, then the smallest
repo-safe subset from:

```bash
python mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py
python scripts/validate_assistant_civil_formation.py
python scripts/validate_experience_assistant_civil_contracts.py
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
python mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py
python scripts/validate_agon_rank_epistemic_contracts.py
python scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python scripts/validate_agon_agent_rank_jurisdiction.py
python scripts/build_agon_agent_school_campaign_posture_registry.py --check
python scripts/validate_agon_agent_school_campaign_posture_registry.py
python scripts/build_agon_epistemic_actor_posture_registry.py --check
python scripts/validate_agon_epistemic_actor_posture.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed Agon part, payload class, source or generated owner, checks
run, checks skipped, and any stronger-owner handoff.
