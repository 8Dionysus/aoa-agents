# AGENTS.md

## Applies To

This card applies to `mechanics/questbook/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/questbook/` owns the agent-layer Questbook operation route:
public index posture, root source quest store route law, generated quest
reader contracts, execution passport posture, and Alpha reference routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | quest-facing agent posture package |
| input | quest, passport, catalog, dispatch, Alpha route, role eligibility, and quest-surface pressure |
| output | bounded quest posture, generated quest reader, passport route, or playbook handoff |
| owner | this package for operation law; root `QUESTBOOK.md` owns human index and root `quests/` owns source records |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, root `QUESTBOOK.md`, root `quests/`, root generated quest readers, `PROVENANCE.md` |
| tools | dispatch-reader builder, Alpha reference builder, reference-route validator, repo validators |
| validation | quest/read-model checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. root `QUESTBOOK.md` and `quests/AGENTS.md` when source quest records change
8. `PROVENANCE.md` for provenance accounting

## Boundaries

- Root `QUESTBOOK.md` owns human open-obligation visibility.
- Root `quests/` owns lane-first source quest record placement.
- Root quest generated readers are read models built from `quests/`.
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

## Closeout

Report the changed Questbook part, quest lane or generated reader affected,
whether source records changed, checks run, checks skipped, and any playbook,
proof, or routing handoff.
