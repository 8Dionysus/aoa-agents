# Codex Projection Provenance Bridge

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

## 2026-05-26 Assistant Projection Check Move

The assistant projection resolver validator moved from root `scripts/` into
the active `assistant-projection` part after the resolver payloads themselves
had already moved there. The focused resolver test moved beside the part and
was converted to the repo's release-check `unittest` route. Root
`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
part-local validator explicitly.

| Former root path | Active route | Part |
| --- | --- | --- |
| `scripts/validate_assistant_projection_resolver.py` | [parts/assistant-projection/scripts/validate_assistant_projection_resolver.py](parts/assistant-projection/scripts/validate_assistant_projection_resolver.py) | `assistant-projection` |
| `tests/test_wave1_assistant_projection.py` | [parts/assistant-projection/tests/test_assistant_projection_resolver.py](parts/assistant-projection/tests/test_assistant_projection_resolver.py) | `assistant-projection` |

## 2026-05-26 Refresh Law Example Move

1 refresh-law route example moved from root `examples/` into
`codex-projection/parts/refresh-law/examples/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `examples/subagent_projection_refresh_law.example.json` | [parts/refresh-law/examples/subagent-refresh-law.example.json](parts/refresh-law/examples/subagent-refresh-law.example.json) | `refresh-law` |

## 2026-05-26 Refresh Law Check Move

The Codex refresh-law validator moved from root `scripts/` into the active
`refresh-law` part after the example itself had already moved there. Root
`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
part-local validator explicitly.

| Former root path | Active route | Part |
| --- | --- | --- |
| `scripts/validate_codex_refresh_law_contracts.py` | [parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py](parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py) | `refresh-law` |

## 2026-05-26 Codex Subagent Projection Builder Move

The root-published generated Codex agent companions stayed under
`generated/codex_agents/`, but the dedicated builder, projection module,
validator, and focused tests moved into the active `subagent-projection` part.

| Former root path | Active route | Part |
| --- | --- | --- |
| `scripts/build_codex_subagents_v2.py` | [parts/subagent-projection/scripts/build_codex_subagents_v2.py](parts/subagent-projection/scripts/build_codex_subagents_v2.py) | `subagent-projection` |
| `scripts/codex_subagent_projection.py` | [parts/subagent-projection/scripts/codex_subagent_projection.py](parts/subagent-projection/scripts/codex_subagent_projection.py) | `subagent-projection` |
| `scripts/validate_codex_subagents.py` | [parts/subagent-projection/scripts/validate_codex_subagents.py](parts/subagent-projection/scripts/validate_codex_subagents.py) | `subagent-projection` |
| `tests/test_codex_subagent_projection.py` | [parts/subagent-projection/tests/test_codex_subagent_projection.py](parts/subagent-projection/tests/test_codex_subagent_projection.py) | `subagent-projection` |

## Distillation Rule

When archived or former-path material changes current behavior, update the
relevant active part first. Then update this bridge and the package archive
index/log if route accounting changed. Active part docs must not grow
per-source inventories.
