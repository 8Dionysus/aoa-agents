# Codex Projection Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

Open `legacy/` only for former path lookup, raw receipt intake, or distillation history. Former root file names stay historical here; active parts use their current route names.

## 2026-05-26 Root Docs Move

3 mechanics-facing docs moved from `docs/` into `codex-projection/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/CODEX_PROJECTION_AGON_BOUNDARY.md` | [parts/agon-boundary/docs/projection-agon-boundary.md](parts/agon-boundary/docs/projection-agon-boundary.md) | `agon-boundary` |
| `docs/CODEX_SUBAGENT_REFRESH_LAW.md` | [parts/refresh-law/docs/subagent-refresh-law.md](parts/refresh-law/docs/subagent-refresh-law.md) | `refresh-law` |
| `docs/CODEX_SUBAGENT_PROJECTION.md` | [parts/subagent-projection/docs/subagent-projection.md](parts/subagent-projection/docs/subagent-projection.md) | `subagent-projection` |

## 2026-05-26 Root Config Move

1 mechanic-specific wiring config moved from root `config/` into
`codex-projection/parts/subagent-projection/config/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `config/codex_subagent_wiring.v2.json` | [parts/subagent-projection/config/wiring.v2.json](parts/subagent-projection/config/wiring.v2.json) | `subagent-projection` |

## 2026-05-26 Assistant Projection Payload Move

2 assistant projection resolver schemas and 1 example moved from root support
districts into `parts/assistant-projection/`. Stable schema `$id` values remain
public contract identifiers, not active repo paths.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/assistant-projection-resolver.schema.json` | [parts/assistant-projection/schemas/assistant-projection-resolver.schema.json](parts/assistant-projection/schemas/assistant-projection-resolver.schema.json) | `assistant-projection` |
| `schemas/assistant_projection_resolver_v1.json` | [parts/assistant-projection/schemas/assistant-projection-resolver-v1.schema.json](parts/assistant-projection/schemas/assistant-projection-resolver-v1.schema.json) | `assistant-projection` |
| `examples/assistant_projection_resolver.example.json` | [parts/assistant-projection/examples/assistant-projection-resolver.example.json](parts/assistant-projection/examples/assistant-projection-resolver.example.json) | `assistant-projection` |

## 2026-05-26 Refresh Law Example Move

1 refresh-law route example moved from root `examples/` into
`codex-projection/parts/refresh-law/examples/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `examples/subagent_projection_refresh_law.example.json` | [parts/refresh-law/examples/subagent-refresh-law.example.json](parts/refresh-law/examples/subagent-refresh-law.example.json) | `refresh-law` |
