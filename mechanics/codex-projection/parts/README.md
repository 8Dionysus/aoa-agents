# Codex Projection Parts

`mechanics/codex-projection/parts/` is the lower index for active Codex
projection operation parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `subagent-projection/` | source profile to generated Codex subagent projection | `subagent-projection/README.md` |
| `refresh-law/` | keep generated projections refreshable and source-owned | `refresh-law/README.md` |
| `specialization-eligibility/` | gate role specializations before any future Codex custom-agent projection | `specialization-eligibility/README.md` |
| `agon-boundary/` | prevent Agon formation pressure from leaking into Codex projection authority | `agon-boundary/README.md` |
| `assistant-projection/` | assistant projection resolver and compatibility posture | `assistant-projection/README.md` |
| `titan-projection/` | Titan projection into Codex-facing generated agents | `titan-projection/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
