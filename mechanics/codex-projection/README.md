# Codex Projection Mechanic

Status: active package.

`mechanics/codex-projection/` routes projection from agent source profiles into
Codex-facing subagent surfaces. It owns projection posture, specialization
eligibility, refresh law, and wiring route; it does not own Codex runtime
behavior.

## Operating Card

| Field | Route |
| --- | --- |
| role | Codex-facing projection operation package |
| input | profile, specialization, wiring, generated subagent, refresh-law, manifest, and projection-boundary pressure |
| output | refreshed projection route, eligibility record, generated eligibility readiness reader, generated manifest, compatibility note, or runtime/config handoff |
| owner | this package for projection routing; `agents/roles/` and `parts/subagent-projection/config/` for source inputs |
| next route | `PARTS.md`, Codex projection builders, `mechanics/agon/` for Agon projection boundaries |
| validation | Codex projection validators plus repo validators |

## Agent Layer Owns

- role-profile projection posture
- specialization eligibility posture before future projection
- specialization eligibility records and readiness readers that stay non-installing
- wiring and generated Codex agent compatibility inside `aoa-agents`
- refresh law that keeps projections source-owned and repeatable
- generated projection manifests as evidence, not authority

## Stronger Owner Split

- Codex runtime, host config, and editor behavior do not live here.
- OpenAI product guidance does not live here.
- Runtime service ownership routes away from `aoa-agents`.
