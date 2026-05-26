# Questbook Mechanic

Status: active package.

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
| next route | `PARTS.md`, root `QUESTBOOK.md`, root `quests/`, root generated quest readers |
| validation | dispatch-reader checks plus repo validators |

## Agent Layer Owns

- role posture and eligibility for quest-facing agent work
- execution passport contracts from the agent side
- quest catalog and dispatch reader contract/builder posture while the
  generated outputs stay root-published
- Alpha reference route readers as part-local derived companions
- Alpha reference route posture where it describes agent roles

## Stronger Owner Split

- `QUESTBOOK.md` owns human open-obligation visibility.
- `quests/` owns lane-first source quest record placement.
- `generated/quest_catalog*.json` and `generated/quest_dispatch*.json` are
  root-published read models built from `quests/`.
- `aoa-playbooks` owns scenario composition and choreography.
- `aoa-evals` owns quest proof or verdict surfaces.
- `aoa-routing` owns general routing policy.

## Validation

```bash
python mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py --check
python mechanics/questbook/parts/alpha-reference-routes/scripts/generate_alpha_reference_routes.py --check
python mechanics/questbook/scripts/validate_alpha_reference_routes.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

If a named quest builder is affected, run that builder before validators.
