# Boundary Bridge Mechanic

Status: skeleton.

`mechanics/boundary-bridge/` routes consumer handoff and cross-repo boundary
pressure for `aoa-agents`: federation seams, published compatibility, workspace
surface triggers, install compatibility, and source-surface registries.

## Operating Card

| Field | Route |
| --- | --- |
| role | cross-boundary consumer handoff package for the agent layer |
| input | federation, compatibility, workspace trigger, source registry, install, and published-contract pressure |
| output | bounded consumer route, compatibility note, stronger-owner handoff, or validator route |
| owner | this package for agent-layer boundary bridge routing |
| next route | `PARTS.md`, owning repository card for the stronger owner, `mechanics/release-support/` |
| validation | compatibility tests plus repo validators |

## Agent Layer Owns

- agent-side contract compatibility and source-surface registry posture
- consumer handoff language for generated readers and published surfaces
- workspace trigger posture where it affects role contracts

## Stronger Owner Split

- General routing policy belongs to `aoa-routing`.
- Runtime boundaries belong to runtime owners.
- Public entry orientation belongs to `8Dionysus`.
- Durable memory handoff belongs to `aoa-memo`.

## Validation

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

Run any named compatibility or surface-registry check when the touched payload
has one.
