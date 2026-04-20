# AOA-AG-Q-AGON-0006: Assistant Projection Boundary

## Repository

`aoa-agents`

## Goal

Prevent assistant civil surfaces from leaking into Codex projection as live prompt behavior without explicit projection review.

## Work

- review `docs/CODEX_SUBAGENT_PROJECTION.md`
- decide whether assistant variants should be excluded, summarized, or projected into a separate civil/service plane
- keep workspace-write and arena authority separate
- ensure `coder.assistant` does not inherit autonomous workspace authority

## Exit

- Codex projection boundary is documented
- assistant variants remain source surfaces until an owner-reviewed projection path exists
