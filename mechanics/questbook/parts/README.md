# Questbook Parts

`mechanics/questbook/parts/` is the lower index for active quest-facing role
posture parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `execution-passport/` | quest execution passport from the agent side | `execution-passport/README.md` |
| `public-index/` | route to the root human quest index | `public-index/README.md`, `../../../QUESTBOOK.md` |
| `quest-item-store/` | route to lane-first source quest records | `quest-item-store/README.md`, `../../../quests/` |
| `dispatch-reader/` | generated quest catalog and dispatch posture | `dispatch-reader/README.md`, `../../../generated/quest_*.json` |
| `alpha-reference-routes/` | Alpha reference route schema, examples, and generated companion that remain role-facing | `alpha-reference-routes/README.md`, `alpha-reference-routes/schemas/`, `alpha-reference-routes/examples/`, `alpha-reference-routes/generated/` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
