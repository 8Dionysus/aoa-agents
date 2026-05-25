# Recurrence Parts

`mechanics/recurrence/parts/` is the lower index for active recursor and
recurrence operation parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `recursor-readiness/` | paired role and readiness posture | `recursor-readiness/README.md` |
| `codex-recursor-projection/` | projection of recursor posture into Codex-facing surfaces | `codex-recursor-projection/README.md` |
| `component-manifests/` | recurrence component declarations and refresh posture | `component-manifests/README.md` |
| `anchor-return/` | recurrence return and discipline route | `anchor-return/README.md` |
| `agon-recursor-boundary/` | Agon-facing recursor limits | `agon-recursor-boundary/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
