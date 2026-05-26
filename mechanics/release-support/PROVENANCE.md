# Release Support Provenance Bridge

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

2 mechanics-facing docs moved from `docs/` into `release-support/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/RELEASING.md` | [parts/repo-release-gate/docs/releasing.md](parts/repo-release-gate/docs/releasing.md) | `repo-release-gate` |
| `docs/AGENT_RELEASE_HOLD_POLICY.md` | [parts/runtime-release-hold/docs/agent-release-hold-policy.md](parts/runtime-release-hold/docs/agent-release-hold-policy.md) | `runtime-release-hold` |

## 2026-05-26 Agent Release Hold Contract Move

The release-hold schema/example moved from root `schemas/` and `examples/`
into the `runtime-release-hold` part. It is validated with
`scripts/validate_agent_service_contracts.py`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/agent_release_hold_v1.json` | [parts/runtime-release-hold/schemas/agent-release-hold.schema.json](parts/runtime-release-hold/schemas/agent-release-hold.schema.json) | `runtime-release-hold` |
| `examples/agent_release_hold.example.json` | [parts/runtime-release-hold/examples/agent-release-hold.example.json](parts/runtime-release-hold/examples/agent-release-hold.example.json) | `runtime-release-hold` |

## Distillation Rule

When archived or former-path material changes current behavior, update the
relevant active part first. Then update this bridge and the package archive
index/log if route accounting changed. Active part docs must not grow
per-source inventories.
