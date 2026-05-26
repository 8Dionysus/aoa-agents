# Agon Mechanic

Status: skeleton.

`mechanics/agon/` routes agent-layer participation in Agon: formation,
contest posture, arena boundaries, rank and school posture, epistemic actor
discipline, and adoption or retention after trial pressure.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent-layer Agon operation package |
| input | Agon, agonic, formation, arena, rank, school, trial, scar, adoption, and epistemic actor pressure |
| output | bounded role posture, formation index route, arena/rank/school posture, or stronger-owner handoff |
| owner | this package for operation routing; `agents/profiles/adjuncts/` for source adjuncts |
| next route | `PARTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`, formation builders, decision record |
| validation | Wave I/II/II.5 formation builders and repo validators named below |

## Agent Layer Owns

- agent role posture inside Agon-facing pressure
- formation as a part of Agon, not as the parent mechanic
- assistant civil rechartering only where it is an Agon formation operation
- arena eligibility, rank jurisdiction, school campaign, and epistemic actor posture for agents
- generated formation indexes as derived readers, not source truth

## Stronger Owner Split

- AoA center owns Agon doctrine.
- `aoa-playbooks` owns scenario choreography.
- `aoa-evals` owns proof verdicts about trials.
- Runtime owners own live execution.

## Validation

Run the narrow builder or validator for the affected part, then:

```bash
python scripts/validate_agent_agonic_formation.py
python scripts/validate_assistant_civil_formation.py
python scripts/build_agent_formation_trial.py --check
python scripts/validate_agent_formation_trial.py
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

Use a smaller subset only when the touched part is clearly narrower.
