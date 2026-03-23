# REGISTRY SOURCE SURFACES

## Purpose

This document defines the source-authored machine-readable surfaces that publish
compact registries from `aoa-agents`.

It exists to keep published JSON registries deterministic and reviewable
without pretending that `generated/*` files are the authoring layer.

## Source-authored directories

The current source-authored registry surfaces live at:

- `model_tiers/*.tier.json`
- `cohort_patterns/*.pattern.json`
- `runtime_seam/*.binding.json`

These source files publish the current compact registries:

- `generated/model_tier_registry.json`
- `generated/cohort_composition_registry.json`
- `generated/runtime_seam_bindings.json`

## Build path

Regenerate the published machine-readable surfaces with:

```bash
python scripts/build_published_surfaces.py
```

This build keeps a stable public order for:

- model tiers
- cohort patterns
- runtime seam phases

That stability matters because neighboring repos may treat these registries as
published contracts, not as arbitrary JSON blobs.

## Boundaries to preserve

These source-authored files are still agent-layer surfaces.

They must not absorb:

- routing policy from `aoa-routing`
- scenario composition from `aoa-playbooks`
- memory-object canon from `aoa-memo`
- proof doctrine from `aoa-evals`

They may publish compact role-facing or tier-facing contracts that neighboring
layers consume.
They do not become the neighboring layers themselves.

## Validation

The item schemas for these source-authored surfaces are:

- `schemas/model-tier.schema.json`
- `schemas/cohort-pattern.schema.json`
- `schemas/runtime-seam-binding.schema.json`

Validation still runs through:

```bash
python scripts/validate_agents.py
```

Validation confirms:

- each source-authored item matches its item schema
- each generated registry matches the source-authored layer exactly
- tier, cohort, and seam references remain coherent with the public agent layer
