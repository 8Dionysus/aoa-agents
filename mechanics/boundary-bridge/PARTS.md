# Boundary Bridge Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `federation-consumer-seams` | consumer seams and federation projection boundaries | `docs/FEDERATION_CONSUMER_SEAMS.md`; `docs/FEDERATION_PROJECTION_BOUNDARIES.md`; related schemas/examples |
| `published-compatibility` | published contract and install compatibility from the agent side | `docs/PUBLISHED_CONTRACT_COMPATIBILITY.md`; `docs/INSTALL_COMPATIBILITY.md`; compatibility tests |
| `workspace-trigger` | workspace surface trigger posture | `docs/WORKSPACE_SURFACE_TRIGGER_POSTURE.md`; generated surface readers if present |
| `source-surface-registry` | explain which source surfaces own agent truth | `docs/REGISTRY_SOURCE_SURFACES.md`; generated registries |
| `consumer-handoff` | route consumers without taking stronger-owner authority | `README.md`; `AGENTS.md`; `mechanics/ARTIFACT_TOPOLOGY.md` |

## Move Posture

This package should mostly stay as a map. Boundary payloads often point out of
`aoa-agents`; moving them inward can hide the stronger owner.
