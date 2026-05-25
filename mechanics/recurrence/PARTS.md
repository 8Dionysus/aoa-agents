# Recurrence Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `recursor-readiness` | paired role and readiness posture | `config/recursor_pair.seed.json`; `config/recursor_roles.seed.json`; `docs/RECURSOR_PAIR_READINESS.md`; `docs/RECURSOR_ROLES.md`; recursor schemas/examples |
| `codex-recursor-projection` | projection of recursor posture into Codex-facing surfaces | `config/codex_recursor_projection.candidate.json`; `docs/CODEX_RECURSOR_PROJECTION.md`; generated recursor projection outputs |
| `component-manifests` | recurrence component declarations and refresh posture | `manifests/recurrence/component.*.json`; recurrence manifest docs |
| `anchor-return` | recurrence return and discipline route | `docs/RECURRENCE_DISCIPLINE.md`; `docs/RECURSOR_ANCHOR_RETURN.md` |
| `agon-recursor-boundary` | Agon-facing recursor limits | `docs/AGON_RECURSOR_BOUNDARY.md`; `docs/AGON_RECURRENCE_ADAPTER.md`; cross-route to `mechanics/agon/` |

## Move Posture

Recurrence payloads are split across config, manifests, generated readers, and
docs. Do not package-localize them until manifest validators and generated
paths are updated together.
