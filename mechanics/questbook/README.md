# Questbook Mechanic

Status: skeleton.

`mechanics/questbook/` routes quest-facing role posture for `aoa-agents`.
It keeps quest passports, quest catalog readers, dispatch posture, and Alpha
reference routes legible without taking playbook scenario authority.

## Operating Card

| Field | Route |
| --- | --- |
| role | quest-facing agent posture package |
| input | quest, passport, catalog, dispatch, Alpha route, role eligibility, and quest-surface pressure |
| output | bounded quest posture, generated quest reader, passport route, or playbook handoff |
| owner | this package for agent-layer quest posture |
| next route | `PARTS.md`, quest catalog docs, part-local quest sources, generated quest readers |
| validation | quest/read-model checks plus repo validators |

## Agent Layer Owns

- role posture and eligibility for quest-facing agent work
- execution passport contracts from the agent side
- generated quest catalog and dispatch readers as derived companions
- Alpha reference route posture where it describes agent roles

## Stronger Owner Split

- `aoa-playbooks` owns scenario composition and choreography.
- `aoa-evals` owns quest proof or verdict surfaces.
- `aoa-routing` owns general routing policy.

## Validation

```bash
python scripts/generate_alpha_reference_routes.py --check
python scripts/validate_reference_route_contracts.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

If a named quest builder is affected, run that builder before validators.
