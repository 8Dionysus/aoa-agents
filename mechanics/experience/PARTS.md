# Experience Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `assistant-civil-service` | service identity, contract, governance, certification, civil rechartering | `agents/profiles/adjuncts/assistant_service_identity/`; `assistant_service_contract/`; `assistant_service_governance/`; `assistant_service_certification/`; `docs/ASSISTANT_CIVIL_RECHARTERING.md`; `docs/ASSISTANT_SERVICE_IDENTITY.md`; `docs/ASSISTANT_SERVICE_CONTRACT.md`; `docs/ASSISTANT_SERVICE_GOVERNANCE.md`; `docs/ASSISTANT_SERVICE_CERTIFICATION.md` |
| `office-operations` | office overlays, service registry, train/release posture, live office expectations | `agents/profiles/adjuncts/office_overlay/`; `docs/AGENT_OFFICE_OVERLAY.md`; `docs/ASSISTANT_OFFICE_REGISTRY.md`; `docs/ASSISTANT_OFFICE_TRAIN_RELEASE.md`; office examples and schemas |
| `adoption-and-regression` | adoption models, shared patterns, regression matrix, canary probes | `docs/ASSISTANT_ADOPTION_MODEL.md`; `docs/ASSISTANT_PATTERN_ADOPTION.md`; `docs/ASSISTANT_REGRESSION_MATRIX.md`; `docs/ASSISTANT_CANARY_PROBES.md`; matching examples and schemas |
| `watch-and-rollback` | deployment watch, post-release watch, rollback and incident posture | `docs/ASSISTANT_DEPLOYMENT_WATCH.md`; `docs/ASSISTANT_POST_RELEASE_WATCHES.md`; `docs/ASSISTANT_ROLLBACK_PROTOCOL.md`; assistant incident/watch examples and schemas |
| `arena-exclusion` | keep assistant posture civil and outside Agon contest lanes unless routed through `agon/formation` | `agents/profiles/adjuncts/assistant_arena_exclusion/`; `docs/ASSISTANT_ARENA_EXCLUSION.md`; `docs/ASSISTANT_ESCALATION_BOUNDARY.md` |
| `runtime-release-holds` | service holds that affect runtime-facing assistant posture | `docs/ASSISTANT_RUNTIME_RELEASE_HOLDS.md`; `docs/ASSISTANT_LIVE_SERVICE.md`; cross-route to `mechanics/runtime-seam/` and `mechanics/release-support/` |

## Move Posture

Assistant service payloads are dense enough for this package, but shared
schemas/examples should move only with matching validators and compatibility
aliases.
