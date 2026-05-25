# Codex Projection Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `subagent-projection` | source profile to generated Codex subagent projection | `agents/profiles/*.profile.json`; `config/codex_subagent_wiring.v2.json`; `generated/codex_agents/`; `scripts/build_codex_subagents_v2.py`; `scripts/codex_subagent_projection.py` |
| `refresh-law` | keep generated projections refreshable and source-owned | `docs/CODEX_SUBAGENT_REFRESH_LAW.md`; `examples/subagent_projection_refresh_law.example.json`; projection tests |
| `agon-boundary` | prevent Agon formation pressure from leaking into Codex projection authority | `docs/CODEX_PROJECTION_AGON_BOUNDARY.md`; cross-route to `mechanics/agon/` |
| `assistant-projection` | assistant projection resolver and compatibility posture | `examples/assistant_projection_resolver.example.json`; assistant projection schemas/examples |
| `titan-projection` | Titan projection into Codex-facing generated agents | `generated/titan_codex_agents/`; Titan projection builders/tests; cross-route to `mechanics/titan/` |

## Move Posture

Generated Codex outputs stay under `generated/`; source wiring stays under
`config/`. This package names the operation route before any path move.
