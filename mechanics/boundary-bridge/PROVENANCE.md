# Boundary Bridge Provenance Bridge

This is the only active bridge from current mechanic docs into source and
archive accounting. Use it when auditing how former root paths or raw receipts
feed active parts, not when you need the current operating contract.

## Current Route First

Start with active surfaces:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

If those surfaces answer the task, stop there. Do not pull old-path
inventories into active route cards.

## Archive Route

- [legacy index](legacy/INDEX.md): old-path lookup mapped to active part routes.
- [distillation log](legacy/DISTILLATION_LOG.md): dated accounting for
  raw-to-active movement.
- [raw receipts](legacy/raw/README.md): preserved raw inputs when a migration
  has real source payloads.

The dated sections below preserve audit and accounting facts. Former root file
names stay historical here; active parts use current route names.

## 2026-05-26 Root Docs Move

7 mechanics-facing docs moved from `docs/` into `boundary-bridge/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/CROSS_REPO_ADOPTION_READINESS.md` | [parts/consumer-handoff/docs/cross-repo-adoption-readiness.md](parts/consumer-handoff/docs/cross-repo-adoption-readiness.md) | `consumer-handoff` |
| `docs/FEDERATION_CONSUMER_SEAMS.md` | [parts/federation-consumer-seams/docs/federation-consumer-seams.md](parts/federation-consumer-seams/docs/federation-consumer-seams.md) | `federation-consumer-seams` |
| `docs/FEDERATION_PROJECTION_BOUNDARIES.md` | [parts/federation-consumer-seams/docs/federation-projection-boundaries.md](parts/federation-consumer-seams/docs/federation-projection-boundaries.md) | `federation-consumer-seams` |
| `docs/AGENT_INSTALL_COMPATIBILITY.md` | [parts/published-compatibility/docs/install-compatibility.md](parts/published-compatibility/docs/install-compatibility.md) | `published-compatibility` |
| `docs/PUBLISHED_CONTRACT_COMPATIBILITY.md` | [parts/published-compatibility/docs/published-contract-compatibility.md](parts/published-compatibility/docs/published-contract-compatibility.md) | `published-compatibility` |
| `docs/REGISTRY_SOURCE_SURFACES.md` | [parts/source-surface-registry/docs/registry-source-surfaces.md](parts/source-surface-registry/docs/registry-source-surfaces.md) | `source-surface-registry` |
| `docs/WORKSPACE_SURFACE_TRIGGER_POSTURE.md` | [parts/workspace-trigger/docs/workspace-surface-trigger-posture.md](parts/workspace-trigger/docs/workspace-surface-trigger-posture.md) | `workspace-trigger` |

## 2026-05-26 Root Boundary Adoption Contract Move

2 boundary adoption schemas plus 2 examples moved from root `schemas/` and
`examples/` into active Boundary Bridge part-local contract routes.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/cross_repo_adoption_readiness_v1.json` | [parts/consumer-handoff/schemas/cross-repo-adoption-readiness.schema.json](parts/consumer-handoff/schemas/cross-repo-adoption-readiness.schema.json) | `consumer-handoff` |
| `examples/cross_repo_adoption_readiness.example.json` | [parts/consumer-handoff/examples/cross-repo-adoption-readiness.example.json](parts/consumer-handoff/examples/cross-repo-adoption-readiness.example.json) | `consumer-handoff` |
| `schemas/federation_projection_boundary_v1.json` | [parts/federation-consumer-seams/schemas/federation-projection-boundary.schema.json](parts/federation-consumer-seams/schemas/federation-projection-boundary.schema.json) | `federation-consumer-seams` |
| `examples/federation_projection_boundary.example.json` | [parts/federation-consumer-seams/examples/federation-projection-boundary.example.json](parts/federation-consumer-seams/examples/federation-projection-boundary.example.json) | `federation-consumer-seams` |

## Distillation Rule

When archived or former-path material changes current behavior, update the
relevant active part first. Then update this bridge and the package archive
index/log if route accounting changed. Active part docs must not grow
per-source inventories.
