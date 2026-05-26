# Runtime Seam Legacy Distillation Log

## 2026-05-26 Root Docs To Active Parts

Moved 4 mechanics-facing docs out of root `docs/` and into active part-local `docs/` directories. Git history preserves the verbatim file bodies; `PROVENANCE.md` and `legacy/INDEX.md` preserve old-path lookup.

| Part | Moved docs |
| --- | --- |
| `artifact-contracts` | 1 |
| `role-tier-bindings` | 1 |
| `transition-discipline` | 2 |

## 2026-05-26 Runtime Artifact Contracts To Active Part

Moved the runtime artifact contract payloads out of root `schemas/` and
`examples/` into active `artifact-contracts` part-local routes.

| Part | Moved schemas | Moved example route, examples, and fixtures |
| --- | ---: | ---: |
| `artifact-contracts` | 7 | 13 |

The former example `AGENTS.md` became an active part-local examples README.
Git history preserves the file bodies; `PROVENANCE.md` and `legacy/INDEX.md`
preserve old-path lookup. Stable schema `$id` values remain unchanged for
consumer compatibility.

## 2026-05-26 Runtime Artifact Checks To Active Part

Moved the dedicated runtime artifact validator and focused tests out of root
support districts and into the owning `artifact-contracts` part.
`scripts/validate_agents.py` now loads the part-local validator, while
`scripts/release_check.py` runs the part-local tests explicitly.

| Part | Moved scripts | Moved tests |
| --- | ---: | ---: |
| `artifact-contracts` | 1 | 1 |

## 2026-05-26 Agent Authority Claim Contract To Active Part

Moved the runtime-readable authority claim schema and example out of root
`schemas/` and `examples/` into active `artifact-contracts` part-local routes.
Git history preserves the file bodies; `PROVENANCE.md` and `legacy/INDEX.md`
preserve old-path lookup.

| Part | Moved schemas | Moved examples |
| --- | ---: | ---: |
| `artifact-contracts` | 1 | 1 |
