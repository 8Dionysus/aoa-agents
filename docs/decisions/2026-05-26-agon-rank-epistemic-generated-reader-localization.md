# 2026-05-26: Agon Rank And Epistemic Generated Reader Localization

## Status

Accepted.

## Context

Agon rank/jurisdiction, school/campaign, and epistemic actor generated
registries were still in root `generated/` after their configs, schemas, and
examples had moved into active Agon part-local routes.

Those registries are candidate-only readers over Agon part-local config. They
are not repo-level registries like `agent_registry.min.json`, and keeping them
at root blurred the distinction between repo-wide publication and
part-local mechanic companions.

## Decision

Move the generated readers into the owning Agon parts:

```text
mechanics/agon/parts/arena-rank-school/generated/rank-jurisdiction-registry.min.json
mechanics/agon/parts/arena-rank-school/generated/school-campaign-posture-registry.min.json
mechanics/agon/parts/epistemic-actor/generated/epistemic-actor-posture-registry.min.json
```

Teach the dedicated builders, validators, tests, and recurrence component
manifests the part-local routes. Guard former root generated paths through
`scripts/validate_agon_rank_epistemic_contracts.py`.

## Consequences

Root `generated/` continues to own repo-level registries and the broader
formation readers that still have root-level publication posture. Agon
rank/school/epistemic readers now live beside the config surfaces they
summarize.

Agon `PROVENANCE.md`, `legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`
preserve old-path lookup. Active docs should reference the part-local paths.

## Validation

```bash
python scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python scripts/validate_agon_agent_rank_jurisdiction.py
python scripts/build_agon_agent_school_campaign_posture_registry.py --check
python scripts/validate_agon_agent_school_campaign_posture_registry.py
python scripts/build_agon_epistemic_actor_posture_registry.py --check
python scripts/validate_agon_epistemic_actor_posture.py
python scripts/validate_agon_rank_epistemic_contracts.py
python scripts/validate_recurrence_component_manifests.py
python scripts/validate_agents.py
```
