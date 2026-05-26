# Quest District

This directory holds durable `aoa-agents` obligations that should survive the
current diff.

It is not a private scratchpad and not a second roadmap. Program direction
belongs in [ROADMAP](../ROADMAP.md). The human open-obligation index is
[QUESTBOOK](../QUESTBOOK.md). Questbook operation law starts in
[mechanics/questbook](../mechanics/questbook/README.md).

Quest sources live in lane-first lifecycle directories:

```text
quests/<lane>/<state>/<quest-file>
```

## Lanes

| Lane | Use |
| --- | --- |
| [agents](agents/README.md) | schema-backed `AOA-AG-Q-*.yaml` agent-layer quest records |
| [agon](agon/README.md) | Agon agent-posture quest notes and follow-through records |

## Lifecycle States

| State | Use |
| --- | --- |
| `captured` | public-safe obligation exists, but route shaping is not complete |
| `triaged` | route-bearing obligation with enough shape to split, promote, or close |
| `ready` | next owner action is clear and bounded |
| `active` | currently being advanced by an owner lane |
| `blocked` | waiting on a named dependency or owner decision |
| `reanchor` | old route no longer matches; choose a new owner, band, or evidence path |
| `done` | landed with enough public evidence to leave the active index |
| `dropped` | intentionally closed without landing, with a visible reason |

## File Families

| Family | Meaning | Guardrail |
| --- | --- | --- |
| `agents/<state>/AOA-AG-Q-*.yaml` | schema-backed agent-layer obligations | YAML `state` must match the lifecycle directory |
| `agon/<state>/*.md` | Agon posture quest notes | keep authority with Agon mechanics and owner routes |
| `generated/quest_*.json` | root-published quest read models | rebuild with `mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py` |

## Boundaries

- `QUESTBOOK.md` owns human open-obligation visibility.
- `quests/` owns source quest record placement.
- `mechanics/questbook/` owns the operation package and validation route.
- Generated readers summarize source records; they do not author quest meaning.
