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
