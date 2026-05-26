# Questbook Legacy Distillation Log

## 2026-05-26 Root Docs To Active Parts

Moved 1 mechanics-facing docs out of root `docs/` and into active part-local `docs/` directories. Git history preserves the verbatim file bodies; `PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.

| Part | Moved docs |
| --- | --- |
| `execution-passport` | 1 |

## 2026-05-26 Questbook Source Store Topology Repair

Restored the human quest index to root `QUESTBOOK.md` and moved former flat
quest source paths into root lane/state directories under `quests/`.
`mechanics/questbook/` now routes the source-store, public-index, and
dispatch-reader contracts without owning the source record files.

| Route | Moved payloads |
| --- | ---: |
| `quests/agents/<state>/` | 9 |
| `quests/agon/captured/` | 11 |

## 2026-05-26 Alpha Reference Routes To Active Parts

Moved Alpha reference-route schema and example payloads out of root
`schemas/` and `examples/` into the active questbook `alpha-reference-routes`
part.

| Part | Moved schemas | Moved route README and examples |
| --- | ---: | ---: |
| `alpha-reference-routes` | 1 | 6 |

Git history preserves the file bodies; `PROVENANCE.md` and
`legacy/INDEX.md` preserve old-path lookup.

## 2026-05-26 Alpha Reference Route Generated Reader To Active Part

Moved the Alpha reference-route generated reader out of root `generated/` and
into the active Questbook `alpha-reference-routes` part.

| Part | Moved generated readers |
| --- | ---: |
| `alpha-reference-routes` | 1 |

Git history preserves the file body; `PROVENANCE.md` and `legacy/INDEX.md`
preserve old-path lookup.

## 2026-05-26 Alpha Reference Route Checks To Active Package

Moved the Alpha reference-route builder, validator, and focused tests out of
root support districts and into the owning Questbook package and part-local
routes.

| Package | Moved scripts | Moved tests |
| --- | ---: | ---: |
| `questbook` | 2 | 1 |

## Active Root Quest Generated Readers

Quest catalog and dispatch generated readers stay root-published under
`generated/` because they summarize root `quests/` source records.
`mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py`
rebuilds and checks them.

## 2026-05-26 Questbook Reader Builder To Active Part

Moved the dedicated Questbook catalog/dispatch builder out of root `scripts/`
and into the active `dispatch-reader` part. The generated reader files stayed
root-published.

| Part | Moved scripts | Root generated readers moved |
| --- | ---: | ---: |
| `dispatch-reader` | 1 | 0 |
