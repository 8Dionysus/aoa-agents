# Questbook Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `execution-passport` | quest execution passport from the agent side | `docs/QUEST_EXECUTION_PASSPORT.md`; passport schemas/examples |
| `quest-catalog` | quest source inventory and generated reader | `QUESTBOOK.md`; `quests/`; `generated/quest_catalog.min.json` |
| `dispatch-reader` | generated quest dispatch posture | `generated/quest_dispatch.min.json`; quest dispatch schemas/examples |
| `agon-quest-surfaces` | Agon-specific quest docs and quest ids | `quests/AOA-AG-Q-AGON-*.md`; cross-route to `mechanics/agon/` |
| `alpha-reference-routes` | Alpha reference route examples that remain role-facing | `examples/alpha_reference_routes/`; related docs |

## Move Posture

Quest source files remain in `quests/` and `QUESTBOOK.md`. This package only
names the operation route until quest validators understand package-local
paths.
