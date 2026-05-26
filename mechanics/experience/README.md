# Experience Mechanic

Status: skeleton.

`mechanics/experience/` routes assistant-facing experience pressure: civil
service posture, office overlays, adoption, watch, rollback, release holds,
and arena-exclusion boundaries.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent-layer assistant and office experience package |
| input | assistant service, office, adoption, canary, watch, rollback, release, escalation, and arena-exclusion pressure |
| output | bounded service posture, office operation route, adoption/watch route, release-hold handoff, or stronger-owner handoff |
| owner | this package for experience routing; `agents/roles/*/forms/assistant/` for source assistant forms |
| next route | `PARTS.md`, `mechanics/agon/` for formation pressure, `mechanics/release-support/` for repo release pressure |
| validation | assistant formation builders, experience assistant civil contract validator, adoption/boundary validator, assistant route tests, semantic/nested/repo validators |

## Agent Layer Owns

- assistant identity, service contract, governance, and certification posture
- office overlays and service watch expectations for role-bearing agents
- adoption and regression posture for assistant-facing patterns
- escalation and arena-exclusion rules inside the agent layer

## Stronger Owner Split

- Live service implementation belongs to runtime owners.
- User support policy and business process do not live here.
- Proof of assistant quality belongs to `aoa-evals`.
- Durable memory truth belongs to `aoa-memo`.

## Validation

Run affected assistant builders/tests, then:

```bash
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py
python mechanics/experience/scripts/validate_adoption_boundary_contracts.py
python -m unittest discover -s mechanics/experience/tests -p 'test_*.py'
python -m unittest discover -s mechanics/experience/parts/assistant-civil-service/tests -p 'test_*.py'
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```
