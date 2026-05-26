# Experience Legacy Distillation Log

## 2026-05-26 Root Docs To Active Parts

Moved 44 mechanics-facing docs out of root `docs/` and into active part-local `docs/` directories. Git history preserves the verbatim file bodies; `PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.

| Part | Moved docs |
| --- | --- |
| `adoption-and-regression` | 6 |
| `arena-exclusion` | 3 |
| `assistant-civil-service` | 8 |
| `office-operations` | 12 |
| `runtime-release-holds` | 7 |
| `watch-and-rollback` | 8 |

## 2026-05-26 Assistant Civil Contracts To Active Parts

Moved 7 Wave II assistant civil schemas and 1 public reader example out of
root `schemas/`/`examples/` and into active Experience part-local contract
routes. Git history preserves the verbatim file bodies; `PROVENANCE.md` and
`legacy/INDEX.md` preserve old-path lookup.

| Part | Moved schemas | Moved examples |
| --- | ---: | ---: |
| `assistant-civil-service` | 6 | 1 |
| `arena-exclusion` | 1 | 0 |

## 2026-05-26 Assistant Civil Checks To Active Routes

Moved 3 Wave II assistant civil builders/validators and 2 focused tests out
of root `scripts/` and `tests`. Formation-reader support moved into the
`assistant-civil-service` part; the cross-part contract validator moved to
Experience package-level `scripts/` because it spans `assistant-civil-service`
and `arena-exclusion`. Git history preserves the file bodies; root paths are
lookup facts only.

| Route | Moved scripts | Moved tests |
| --- | ---: | ---: |
| `assistant-civil-service` | 2 | 1 |
| Experience package | 1 | 1 |

## 2026-05-26 Adoption Boundary Checks To Active Routes

Moved the Wave III adoption/boundary validator and focused test out of root
`scripts/` and `tests` into Experience package-level routes. The check stays
package-level because it spans Experience adoption/office parts and
cross-routes into Agon and Boundary Bridge contract parts. Git history
preserves the file bodies; root paths are lookup facts only.

| Route | Moved scripts | Moved tests |
| --- | ---: | ---: |
| Experience package | 1 | 1 |

## 2026-05-26 Agent Service Checks To Active Routes

Moved the agent service validator and focused test out of root `scripts/` and
`tests` into Experience package-level routes. The check stays package-level
because it spans multiple Experience parts and reads Runtime Seam and Release
Support part-local contracts. Git history preserves the file bodies; root
paths are lookup facts only.

| Route | Moved scripts | Moved tests |
| --- | ---: | ---: |
| Experience package | 1 | 1 |

## 2026-05-26 Root Adoption/Office Contracts To Active Parts

Moved 14 adoption and office-operation schemas plus 14 matching examples out
of root `schemas/` and `examples/` and into active part-local `schemas/` and
`examples/` directories. Git history preserves the verbatim file bodies; root
paths are lookup facts only.

| Part | Moved schemas | Moved examples |
| --- | ---: | ---: |
| `adoption-and-regression` | 11 | 11 |
| `office-operations` | 3 | 3 |

## 2026-05-26 Agent Service Contracts To Active Parts

Moved 34 assistant service, office, release, watch, rollback, and governance
schemas/examples out of root `schemas/` and `examples/` and into active
Experience part-local routes. Runtime-readable authority claim and release
hold contracts route through Runtime Seam and Release Support. Git history
preserves the verbatim file bodies; root paths are lookup facts only.

| Part | Moved schemas | Moved examples |
| --- | ---: | ---: |
| `adoption-and-regression` | 3 | 3 |
| `arena-exclusion` | 2 | 2 |
| `assistant-civil-service` | 1 | 1 |
| `office-operations` | 8 | 8 |
| `runtime-release-holds` | 8 | 8 |
| `watch-and-rollback` | 12 | 12 |
