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

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` before using `legacy/`
8. `.github/AGENTS.md` only when GitHub-native files change

## Boundaries

- GitHub merge policy and CI execution are not owned here.
- Runtime release deployment belongs to runtime owners.
- Assistant service release watches cross-route through `mechanics/experience/`.
- Root `AGENTS.md` still owns branch, PR, CI, and merge route.

## Validation

```bash
python scripts/release_check.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed release-support part, publication surface affected, checks
run, checks skipped, and any GitHub, CI, or runtime handoff.
