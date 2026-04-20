# AOA-AG-Q-AGON-0003 — Formation Index Integration

## Purpose

Make Wave I formation surfaces visible to downstream consumers without mutating the base profile registry.

## Scope

- Keep `generated/agent_registry.min.json` stable.
- Publish `generated/agent_agonic_formation_index.min.json`.
- Decide owner-reviewed integration into `scripts/validate_agents.py` and `scripts/release_check.py`.
- Add docs route from README or docs index after landing.

## Non-goals

- Do not project full subjectivity into Codex TOML by default.
- Do not create runtime packets.
- Do not grant summon or closer authority.

## Exit

Formation index is deterministic and release checks can opt into Wave I validation.
