# 2026-05-26: Agon Rank And Epistemic Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0026
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard, generated/readout
- Agent facets: mechanics atlas, agon formation
- Mechanic parents: agon
- Guard families: part-local artifact, validation guard, generated/read-model
- Posture: accepted

## Context

Agon rank, school/campaign, and epistemic actor configs, schemas, examples,
and generated readers already live under their owning Agon parts. Their
builders, validators, and focused tests still lived in root `scripts/` and
`tests/`.

The checks do not coordinate the whole repository. They protect candidate-only
Agon part-local readers and contract surfaces.

## Decision

Move part-specific checks beside their owning parts:

- rank/jurisdiction and school/campaign builders, validators, and focused
  tests move into `mechanics/agon/parts/arena-rank-school/{scripts,tests}/`;
- epistemic actor builder, validator, and focused tests move into
  `mechanics/agon/parts/epistemic-actor/{scripts,tests}/`;
- the cross-part contract validator and focused test move into
  `mechanics/agon/{scripts,tests}/`.

`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
package-local validator directly. `scripts/release_check.py` runs the
package/part-local Agon tests explicitly.

## Consequences

Rank, school, and epistemic check edits now start at the owning Agon package or
part. Root `scripts/` keeps repository-level coordination and shared support;
root `tests/` keeps repository-level route checks.

Old root script and test paths are provenance facts only and are checked for
absence by the package-local contract validator.

## Validation

```bash
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_rank_jurisdiction.py
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_school_campaign_posture_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_school_campaign_posture_registry.py
python mechanics/agon/parts/epistemic-actor/scripts/build_agon_epistemic_actor_posture_registry.py --check
python mechanics/agon/parts/epistemic-actor/scripts/validate_agon_epistemic_actor_posture.py
python mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py
python -m unittest discover -s mechanics/agon/tests -p 'test_*.py'
python -m unittest discover -s mechanics/agon/parts/arena-rank-school/tests -p 'test_*.py'
python -m unittest discover -s mechanics/agon/parts/epistemic-actor/tests -p 'test_*.py'
python scripts/validate_agents.py
```
