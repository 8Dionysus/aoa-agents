# Subagent Projection Config

## Operating Card

| Field | Route |
| --- | --- |
| role | source wiring config for Codex custom-agent projection |
| input | reviewed role-to-Codex projection hints |
| output | generated Codex agent TOML files, config snippet, and projection manifest |
| owner | `mechanics/codex-projection/parts/subagent-projection/` |
| next route | subagent projection docs, refresh law, generated Codex projection |
| tools | `scripts/build_codex_subagents_v2.py`, `scripts/validate_codex_subagents.py` |
| validation | Codex subagent projection validator with this wiring path |

## Active Config

- [wiring.v2.json](wiring.v2.json)

## Boundaries

This config owns projection-time hints only. It does not install agents into a
host editor, grant runtime autonomy, or override workspace tool policy.
