# 2026-05-26: Agon Rank And Epistemic Contract Localization

## Status

Accepted.

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
- `scripts/validate_agon_rank_epistemic_contracts.py` becomes the
  package-local contract validator and is called by `scripts/validate_agents.py`.

Generated Agon registries remained derived surfaces under `generated/` in this
contract-localization slice; the later generated-reader localization moved
them into part-local `generated/` routes once the generated move was small and
validator-backed. Builder scripts remain support surfaces under `scripts/`.

## Consequences

Rank, school, and epistemic contract edits now start in the part that owns the
candidate-only operation. Former root paths are retained only as provenance and
legacy lookup facts.

Validation for this route is:

```bash
python scripts/validate_agon_rank_epistemic_contracts.py
python scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python scripts/validate_agon_agent_rank_jurisdiction.py
python scripts/build_agon_agent_school_campaign_posture_registry.py --check
python scripts/validate_agon_agent_school_campaign_posture_registry.py
python scripts/build_agon_epistemic_actor_posture_registry.py --check
python scripts/validate_agon_epistemic_actor_posture.py
python scripts/validate_agents.py
python -m pytest -q tests/test_agon_rank_epistemic_contracts.py tests/test_agon_agent_rank_jurisdiction.py tests/test_agon_agent_school_campaign_posture_registry.py tests/test_agon_epistemic_actor_posture.py
```
