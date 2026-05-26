# Arena Rank School Config

## Operating Card

| Field | Route |
| --- | --- |
| role | source seed configs for Agon rank, jurisdiction, school, lineage, and campaign posture candidates |
| input | reviewed candidate posture records for agent roles and assistant anti-drift boundaries |
| output | generated Agon registry surfaces for rank/jurisdiction and school/campaign posture |
| owner | `mechanics/agon/parts/arena-rank-school/` |
| next route | parent part docs, generated registries, Agon validators |
| tools | `scripts/build_agon_agent_rank_jurisdiction_registry.py`, `scripts/build_agon_agent_school_campaign_posture_registry.py` |
| validation | Agon registry builders with `--check` plus matching validators |

## Active Seeds

- [rank-jurisdiction.seed.json](rank-jurisdiction.seed.json)
- [school-campaign-posture.seed.json](school-campaign-posture.seed.json)

## Boundaries

These seeds prepare candidate surfaces only. They do not mutate rank, trust,
school authority, live campaign state, durable scars, or verdict ownership.
