# Experience Parts

`mechanics/experience/parts/` is the lower index for active assistant
experience operation parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `assistant-civil-service/` | service identity, contract, governance, certification, civil rechartering | `assistant-civil-service/README.md` |
| `office-operations/` | office overlays, service registry, train/release posture, live office expectations | `office-operations/README.md` |
| `adoption-and-regression/` | adoption models, shared patterns, regression matrix, canary probes | `adoption-and-regression/README.md` |
| `watch-and-rollback/` | deployment watch, post-release watch, rollback and incident posture | `watch-and-rollback/README.md` |
| `arena-exclusion/` | civil assistant posture outside Agon contest lanes | `arena-exclusion/README.md` |
| `runtime-release-holds/` | service holds that affect runtime-facing assistant posture | `runtime-release-holds/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
