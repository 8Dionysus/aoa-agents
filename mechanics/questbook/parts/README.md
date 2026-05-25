# Questbook Parts

`mechanics/questbook/parts/` is the lower index for active quest-facing role
posture parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `execution-passport/` | quest execution passport from the agent side | `execution-passport/README.md` |
| `quest-catalog/` | quest source inventory and generated reader | `quest-catalog/README.md` |
| `dispatch-reader/` | generated quest dispatch posture | `dispatch-reader/README.md` |
| `agon-quest-surfaces/` | Agon-specific quest docs and quest ids | `agon-quest-surfaces/README.md` |
| `alpha-reference-routes/` | Alpha reference route examples that remain role-facing | `alpha-reference-routes/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
