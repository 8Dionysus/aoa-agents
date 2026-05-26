# Arena Rank School Part

This part routes `arena-rank-school` pressure inside `mechanics/agon/`.

## Active Docs

- [Agent Arena Eligibility Model](docs/arena-eligibility-model.md)
- [Assistant Campaign Boundary](docs/assistant-campaign-boundary.md)
- [Assistant Rank Boundary](docs/assistant-rank-boundary.md)
- [Agent Kind Conflict Resolution](docs/kind-conflict-resolution.md)
- [Agon Agent Rank Jurisdiction Surfaces](docs/rank-jurisdiction-surfaces.md)
- [School Affiliation Boundary](docs/school-affiliation-boundary.md)
- [Agent School / Campaign Posture](docs/school-campaign-posture.md)
- [Rank Jurisdiction Landing](docs/rank-jurisdiction-landing.md)
- [School Campaign Posture Landing](docs/school-campaign-posture-landing.md)

## Active Config

- [Rank/Jurisdiction Seed](config/rank-jurisdiction.seed.json)
- [School/Campaign Posture Seed](config/school-campaign-posture.seed.json)
- [Config Route](config/README.md)

## Active Schemas

- [Arena Eligibility Schema](schemas/arena-eligibility.schema.json)
- [Rank/Jurisdiction Schema](schemas/rank-jurisdiction.schema.json)
- [Rank/Jurisdiction Registry Schema](schemas/rank-jurisdiction-registry.schema.json)
- [School/Campaign Posture Schema](schemas/school-campaign-posture.schema.json)
- [School/Campaign Posture Registry Schema](schemas/school-campaign-posture-registry.schema.json)
- [Schema Route](schemas/README.md)

## Active Examples

- [Rank Surface Example](examples/rank-surface.example.json)
- [School/Campaign Posture Example](examples/school-campaign-posture.example.json)
- [Example Route](examples/README.md)

## Active Generated

- [Rank/Jurisdiction Registry](generated/rank-jurisdiction-registry.min.json)
- [School/Campaign Posture Registry](generated/school-campaign-posture-registry.min.json)

Generated readers are derived from this part's config and remain candidate-only
support surfaces, not live rank, school, or campaign authority.

## Active Checks

- [Rank/Jurisdiction Builder](scripts/build_agon_agent_rank_jurisdiction_registry.py)
- [Rank/Jurisdiction Validator](scripts/validate_agon_agent_rank_jurisdiction.py)
- [School/Campaign Builder](scripts/build_agon_agent_school_campaign_posture_registry.py)
- [School/Campaign Validator](scripts/validate_agon_agent_school_campaign_posture_registry.py)
- [Arena Rank School Tests](tests/)

## Validation

```bash
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_rank_jurisdiction.py
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_school_campaign_posture_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_school_campaign_posture_registry.py
python -m unittest discover -s mechanics/agon/parts/arena-rank-school/tests -p 'test_*.py'
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
