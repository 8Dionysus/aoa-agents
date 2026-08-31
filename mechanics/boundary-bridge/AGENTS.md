# AGENTS.md

## Applies To

This card applies to `mechanics/boundary-bridge/` and descendants until a
nearer `AGENTS.md` narrows the route.

## Role

`mechanics/boundary-bridge/` routes consumer handoff and cross-repo boundary
pressure for `aoa-agents`: federation seams, published compatibility,
workspace triggers, install compatibility, and source-surface registries.

## Operating Card

| Field | Route |
| --- | --- |
| role | cross-boundary consumer handoff package for the agent layer |
| input | federation, compatibility, workspace trigger, source registry, install, and published-contract pressure |
| output | bounded consumer route, compatibility note, stronger-owner handoff, or validator route |
| owner | this package for agent-layer boundary bridge routing |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, owning repository route, `mechanics/release-support/` |
| tools | adoption/boundary validator, repo validators |
| validation | compatibility or surface-registry checks plus repo validators |

## Boundaries

- General routing policy belongs to the `aoa-sdk` routing control plane;
  `aoa-routing` remains its stable compatibility layer.
- Runtime boundaries belong to runtime owners.
- Public entry orientation belongs to `8Dionysus`.
- Durable memory handoff belongs to `aoa-memo`.

## Validation
Use the repository [validation map](../../VALIDATION.md) and the nearest owner check when this route is relevant.

## Closeout

Report the changed boundary part, consumer route affected, checks run, checks
skipped, and the next owner if the change is only a handoff.
