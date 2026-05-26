# RPG Provenance Bridge

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

2 mechanics-facing docs moved from `docs/` into `rpg/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/AGENT_COHORT_PATTERNS.md` | [parts/cohort-patterns/docs/cohort-patterns.md](parts/cohort-patterns/docs/cohort-patterns.md) | `cohort-patterns` |
| `docs/AGENT_PROGRESSION_MODEL.md` | [parts/progression-model/docs/agent-progression-model.md](parts/progression-model/docs/agent-progression-model.md) | `progression-model` |

## 2026-05-26 Progression Payload Move

1 progression schema and 1 example moved from root support districts into
`parts/progression-model/`. Stable schema `$id` values remain public contract
identifiers, not active repo paths.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/agent_progression.schema.json` | [parts/progression-model/schemas/agent-progression.schema.json](parts/progression-model/schemas/agent-progression.schema.json) | `progression-model` |
| `examples/agent_progression.example.json` | [parts/progression-model/examples/agent-progression.example.json](parts/progression-model/examples/agent-progression.example.json) | `progression-model` |

## 2026-05-26 Progression Check Move

The RPG progression validator moved from root `scripts/` into the
`progression-model` part after the payload itself had already moved there. Root
`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
part-local validator explicitly.

| Former root path | Active route | Part |
| --- | --- | --- |
| `scripts/validate_rpg_progression.py` | [parts/progression-model/scripts/validate_rpg_progression.py](parts/progression-model/scripts/validate_rpg_progression.py) | `progression-model` |

## Distillation Rule

When archived or former-path material changes current behavior, update the
relevant active part first. Then update this bridge and the package archive
index/log if route accounting changed. Active part docs must not grow
per-source inventories.
