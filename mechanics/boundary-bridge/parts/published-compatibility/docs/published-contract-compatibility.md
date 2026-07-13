# Published Contract Compatibility

## Purpose

This document defines compatibility discipline for published `aoa-agents` contract surfaces.

It exists to keep source-authored role surfaces reviewable while protecting the published JSON and schema surfaces that neighboring consumers may treat as public contracts.

## Surfaces in scope

This compatibility discipline applies to:

- `schemas/*.json`
- `mechanics/runtime-seam/parts/artifact-contracts/schemas/*.json`
- `agents/roles/*/profile.json`
- `agents/operating-model/tiers/*.tier.json`
- `agents/operating-model/cohorts/*.pattern.json`
- `agents/operating-model/runtime-seams/*.binding.json`
- `generated/*.json`

The current published contract set includes:

- `generated/agent_registry.min.json`
- `generated/model_tier_registry.json`
- `generated/cohort_composition_registry.json`
- `generated/runtime_seam_bindings.json`
- `mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.*.schema.json`

Historical repo refs to the former root artifact-schema route are treated as
compatibility identifiers during optional consumer smoke checks and resolve to
the active `artifact-contracts` schemas. They do not recreate root schema
authority.

The example-only surface in this cycle is:

- `mechanics/checkpoint/parts/reference-routes/schemas/reference-route-manifest.schema.json`

## Core rule

Source-authored files may evolve, but published surfaces must remain legible, deterministic, and intentionally changed.

`version` and `layer` remain required top-level fields on every published generated registry.

## Registry v2 migration surface

The current committed generated registry contract is `version: 2` for:

- `generated/agent_registry.min.json`
- `generated/model_tier_registry.json`
- `generated/cohort_composition_registry.json`
- `generated/runtime_seam_bindings.json`

This is an intentional versioning move, not silent top-level metadata drift.

Migration/deprecation contract:

- Consumers must inspect `version` and `layer` before interpreting a published registry.
- Current v2 field names and stable publication order remain present during the documented overlap period.
- v1-only consumers must pin to a pre-v2 release or add an explicit compatibility adapter; this repository does not publish a hidden v1 shadow registry from the v2 generated files.
- A future v3 or another top-level metadata change needs a new migration section here before generated registries switch.

## Compatibility classes

### Additive

An additive change keeps current consumers valid without changing the existing wire shape they already read.

Compatible additive work includes:

- new docs
- new tests
- stricter drift checks
- new public-safe examples
- new example-only surfaces such as `mechanics/checkpoint/parts/reference-routes/schemas/reference-route-manifest.schema.json`

### Deprecated

Deprecation may be documented before a later breaking change, but the current published field name and meaning must remain present during the documented overlap period.

### Breaking

A breaking change includes:

- renaming or removing a published field
- changing the meaning of an existing published field without explicit migration
- changing published top-level metadata shape
- changing stable publication order in a way that creates hidden drift for consumers
- changing existing `mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.*.schema.json` wire shape without an intentional versioning move

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
- Do not silently switch published registry `version`; the current registry contract is v2 and future version changes require a documented migration surface before generated registries switch.
- Historical v1 stabilization guard retained for traceability: Do not introduce `v2` or new required env vars in this stabilization cycle.
- Do not treat example-only surfaces as runtime-facing canon.

## Validation

The owner validator covers top-level metadata, stable publication order,
published field sets, source-to-generated registry alignment, and the committed
adjunct projections. Generated registries refresh only from source-authored
registry inputs; exact executable routes live in the nearest `AGENTS.md`.
