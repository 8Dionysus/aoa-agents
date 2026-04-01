# model_tiers/AGENTS.md

## Purpose

`model_tiers/` is the tier-oriented source-authored surface for orchestration-shaped duties in `aoa-agents`.
Model tiers are effort classes and handoff posture, not model brands and not human role archetypes.

## Source of truth

Canonical authoring lives in:

- `model_tiers/*.tier.json`
- `schemas/model-tier.schema.json`

Published derived surface:

- `generated/model_tier_registry.json`

Read with:

- `docs/MODEL_TIER_MODEL.md`
- `docs/REGISTRY_SOURCE_SURFACES.md`

## Contract to preserve

Keep the public loop explicit and small:

`route -> plan -> do -> verify -> deep? -> distill`

Each tier should stay compact and expose:

- one `primary_duty`
- one `output_contract`
- one `default_memory_scope`
- named `handoff_targets`
- one `artifact_requirement`
- clear `activation_conditions`

## Does not own

Do not encode here:

- vendor or model-family branding
- routing policy owned by `aoa-routing`
- scenario canon owned by `aoa-playbooks`
- runtime infrastructure owned outside this repository

## Editing posture

Treat changes to `id`, `artifact_requirement`, `handoff_targets`, memory scope, or activation conditions as public contract changes.
Keep tier meaning separate from human role meaning.
Avoid widening a tier into a hidden runtime or a brand alias.

## Validation

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```
