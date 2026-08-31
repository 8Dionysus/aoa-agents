# AGENTS.md

## Applies To

This card applies to `mechanics/codex-projection/` and descendants until a
nearer `AGENTS.md` narrows the route.

## Role

`mechanics/codex-projection/` routes projection from source agent profiles into
Codex-facing subagent surfaces. It owns projection posture, specialization
eligibility, refresh law, and wiring route inside `aoa-agents`; it does not own
Codex runtime behavior.

## Operating Card

| Field | Route |
| --- | --- |
| role | Codex-facing projection operation package |
| input | profile, specialization, wiring, generated subagent, refresh-law, manifest, and projection-boundary pressure |
| output | refreshed projection route, eligibility record, generated manifest, compatibility note, or runtime/config handoff |
| owner | this package for projection routing; `agents/roles/` and part-local wiring config own source inputs |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, Codex projection builders, `mechanics/agon/` |
| tools | Codex projection validator, refresh-law validator, repo validators |
| validation | Codex projection checks plus repo validators |

## Boundaries

- Codex runtime, host config, and editor behavior do not live here.
- OpenAI product guidance does not live here.
- Runtime service ownership routes away from `aoa-agents`.
- Generated projection manifests are evidence, not authority.

## Validation
Use the repository [validation map](../../VALIDATION.md) and the nearest owner check when this route is relevant.

## Closeout

Report the changed projection part, source profile or generated surface
affected, builders run, checks skipped, and any runtime or config handoff.
