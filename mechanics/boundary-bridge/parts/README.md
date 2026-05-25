# Boundary Bridge Parts

`mechanics/boundary-bridge/parts/` is the lower index for active consumer
handoff and cross-boundary parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `federation-consumer-seams/` | consumer seams and federation projection boundaries | `federation-consumer-seams/README.md` |
| `published-compatibility/` | published contract and install compatibility from the agent side | `published-compatibility/README.md` |
| `workspace-trigger/` | workspace surface trigger posture | `workspace-trigger/README.md` |
| `source-surface-registry/` | explain which source surfaces own agent truth | `source-surface-registry/README.md` |
| `consumer-handoff/` | route consumers without taking stronger-owner authority | `consumer-handoff/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
