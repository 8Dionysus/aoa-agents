# Epistemic Actor Config

## Operating Card

| Field | Route |
| --- | --- |
| role | source seed config for Agon epistemic actor posture candidates |
| input | reviewed epistemic obligation records for agent roles |
| output | generated epistemic actor posture registry |
| owner | `mechanics/agon/parts/epistemic-actor/` |
| next route | parent part docs, generated registry, Agon validator |
| tools | `mechanics/agon/parts/epistemic-actor/scripts/build_agon_epistemic_actor_posture_registry.py` |
| validation | builder with `--check` plus `mechanics/agon/parts/epistemic-actor/scripts/validate_agon_epistemic_actor_posture.py` |

## Active Seed

- [posture.seed.json](posture.seed.json)

## Boundaries

This seed describes candidate obligations only. It does not grant live verdict
authority, durable scar writes, rank mutation, trust mutation, or assistant
contestant status.
