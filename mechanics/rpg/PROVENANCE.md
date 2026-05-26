# RPG Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

Open `legacy/` only for former path lookup, raw receipt intake, or distillation history. Former root file names stay historical here; active parts use their current route names.

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
