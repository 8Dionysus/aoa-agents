# AGENTS.md

## Applies To

This card applies to `mechanics/release-support/` and descendants until a
nearer `AGENTS.md` narrows the route.

## Role

`mechanics/release-support/` routes repo publication posture: release checks,
changelog and releasing docs, release-readiness holds, compatibility
verification, and assistant release-watch posture.

## Operating Card

| Field | Route |
| --- | --- |
| role | release and publication support package for `aoa-agents` |
| input | release, changelog, publishing, validation, compatibility, and release-hold pressure |
| output | release-readiness route, validation checklist, compatibility handoff, or GitHub/CI handoff |
| owner | this package for release-support routing |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, `CHANGELOG.md`, root release workflow |
| tools | release check, semantic/nested/root validators |
| validation | release check plus repo validators |

## Boundaries

- GitHub merge policy and CI execution are not owned here.
- Runtime release deployment belongs to runtime owners.
- Assistant service release watches cross-route through `mechanics/experience/`.
- Root `AGENTS.md` still owns branch, PR, CI, and merge route.

## Validation
Use the repository [validation map](../../VALIDATION.md) and the nearest owner check when this route is relevant.

## Closeout

Report the changed release-support part, publication surface affected, checks
run, checks skipped, and any GitHub, CI, or runtime handoff.
