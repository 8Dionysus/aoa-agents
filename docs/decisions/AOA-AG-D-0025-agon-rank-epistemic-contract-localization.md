# 2026-05-26: Agon Rank And Epistemic Contract Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0025
- Original date: 2026-05-26
- Surface classes: mechanic part, schema/contract, generated/readout
- Agent facets: mechanics atlas, agon formation
- Mechanic parents: agon
- Guard families: part-local artifact, schema validation, generated/read-model
- Posture: accepted

## Context

Agon rank/jurisdiction, school/campaign, and epistemic actor posture already
had part-local docs, configs, builders, and generated registries. Their
schema-backed contracts and examples still lived in root `schemas/` and
`examples/`, which made the active lookup path disagree with the owning
operation.

## Decision

Move these Agon contract payloads into their owning parts:

- rank/jurisdiction and school/campaign schemas/examples move into
  `mechanics/agon/parts/arena-rank-school/{schemas,examples}/`;
- epistemic actor schemas/example move into
  `mechanics/agon/parts/epistemic-actor/{schemas,examples}/`;
- `mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py` becomes the
  package-local contract validator and is called by `scripts/validate_agents.py`.

Generated Agon registries remained derived surfaces under `generated/` in this
contract-localization slice; the later generated-reader localization moved
them into part-local `generated/` routes once the generated move was small and
validator-backed. The later check-localization slice moved the dedicated
builders, validators, and focused tests into Agon package and part-local
routes.

## Consequences

Rank, school, and epistemic contract edits now start in the part that owns the
candidate-only operation. Former root paths are retained only as provenance and
legacy lookup facts.

Validation for this route is:

```bash
python mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_rank_jurisdiction.py
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_school_campaign_posture_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_school_campaign_posture_registry.py
python mechanics/agon/parts/epistemic-actor/scripts/build_agon_epistemic_actor_posture_registry.py --check
python mechanics/agon/parts/epistemic-actor/scripts/validate_agon_epistemic_actor_posture.py
python scripts/validate_agents.py
python -m unittest discover -s mechanics/agon/tests -p 'test_*.py'
python -m unittest discover -s mechanics/agon/parts/arena-rank-school/tests -p 'test_*.py'
python -m unittest discover -s mechanics/agon/parts/epistemic-actor/tests -p 'test_*.py'
```
