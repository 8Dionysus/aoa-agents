# Release Support Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

Open `legacy/` only for former path lookup, raw receipt intake, or distillation history. Former root file names stay historical here; active parts use their current route names.

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
