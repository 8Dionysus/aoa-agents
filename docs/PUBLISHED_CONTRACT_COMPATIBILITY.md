# PUBLISHED CONTRACT COMPATIBILITY

## Purpose

This document defines compatibility discipline for published `aoa-agents` contract surfaces.

It exists to keep source-authored role surfaces reviewable while protecting the published JSON and schema surfaces that neighboring consumers may treat as public contracts.

## Surfaces in scope

This compatibility discipline applies to:

- `schemas/*.json`
- `profiles/*.profile.json`
- `model_tiers/*.tier.json`
- `cohort_patterns/*.pattern.json`
- `runtime_seam/*.binding.json`
- `generated/*.json`

The current published contract set includes:

- `generated/agent_registry.min.json`
- `generated/model_tier_registry.json`
- `generated/cohort_composition_registry.json`
- `generated/runtime_seam_bindings.json`
- `schemas/artifact.*.schema.json`

The example-only surface in this cycle is:

- `schemas/reference-route.example.schema.json`

## Core rule

Source-authored files may evolve, but published surfaces must remain legible, deterministic, and intentionally changed.

`version` and `layer` remain required top-level fields on every published generated registry.

## Compatibility classes

### Additive

An additive change keeps current consumers valid without changing the existing wire shape they already read.

Compatible additive work includes:

- new docs
- new tests
- stricter drift checks
- new public-safe examples
- new example-only surfaces such as `schemas/reference-route.example.schema.json`

### Deprecated

Deprecation may be documented before a later breaking change, but the current published field name and meaning must remain present during the documented overlap period.

### Breaking

A breaking change includes:

- renaming or removing a published field
- changing the meaning of an existing published field without explicit migration
- changing published top-level metadata shape
- changing stable publication order in a way that creates hidden drift for consumers
- changing existing `schemas/artifact.*.schema.json` wire shape without an intentional versioning move

## Stable publication order

Published generated registries must keep stable publication order.

Current order discipline is:

- agents publish in stable `(id, name)` order
- model tiers publish in public loop order
- cohort patterns publish in their official bounded pattern order
- runtime seam bindings publish in runtime phase order

## Boundaries to preserve

- Do not silently rename published keys.
- Do not silently remove published keys.
- Do not introduce `v2` or new required env vars in this stabilization cycle.
- Do not treat example-only surfaces as runtime-facing canon.

## Validation

Verify the current committed contract set with:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_agents.py
```

Refresh the generated registries only after editing source-authored registry inputs:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

The validator should fail on accidental drift in top-level metadata, stable publication order, published field sets, source-to-generated registry alignment, and the current adjunct published projections that this repository commits.
