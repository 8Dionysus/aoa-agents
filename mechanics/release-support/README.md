# Release Support Mechanic

Status: skeleton.

`mechanics/release-support/` routes repo publication posture: release checks,
changelog and releasing docs, release-readiness holds, and compatibility
verification. It supports release work without becoming CI, GitHub, or runtime
authority.

## Operating Card

| Field | Route |
| --- | --- |
| role | release and publication support package for `aoa-agents` |
| input | release, changelog, publishing, validation, compatibility, and release-hold pressure |
| output | release-readiness route, validation checklist, compatibility handoff, or GitHub/CI handoff |
| owner | this package for release-support routing |
| next route | `PARTS.md`, `mechanics/release-support/parts/repo-release-gate/docs/releasing.md`, `CHANGELOG.md`, release checks |
| validation | release check plus repo validators |

## Agent Layer Owns

- release-readiness posture for agent-layer contract surfaces
- validation route for published generated/read-model companions
- changelog and release notes as repository publication surfaces

## Stronger Owner Split

- GitHub merge policy and CI execution are not owned here.
- Runtime release deployment belongs to runtime owners.
- Assistant service release watches cross-route through `mechanics/experience/`.

## Validation

```bash
python scripts/release_check.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```
