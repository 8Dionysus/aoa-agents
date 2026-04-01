# REFERENCE ROUTE EXAMPLES

## Purpose

`examples/reference_routes/` contains example-only, non-normative route packs.

These route packs make the public loop inspectable through small manifest-driven examples that stay inside existing artifact schemas and runtime seam bindings.

## Core rule

They are not playbooks.
They are not routing policy.
They are not runtime canon.

They exist as teaching and validation surfaces only.

## Manifest surface

Each route pack is anchored by `manifest.json`.

The manifest exposes:

- `route_id`
- `cohort_pattern`
- `role_set`
- `steps`

Each step must name:

- `phase`
- `tier_id`
- `role_name`
- `artifact_path`

The artifact files referenced by `artifact_path` must use only the already-published `schemas/artifact.*.schema.json` contracts.

## Current route packs

The current bounded set is:

- `solo_bounded_route`
- `pair_change_route`
- `checkpoint_self_change_route`
- `orchestrated_loop_route`

Together they show bounded role posture, review edges, governed self-change posture, and the full orchestrated loop without adding runtime logic.

## Boundaries to preserve

- do not turn these examples into scenario canon
- do not add hidden transport, tool wiring, or runtime logs
- do not let manifests replace `aoa-playbooks` or `aoa-routing`
- keep the surface public-safe and portable

## Validation

Run `python -m pip install -r requirements-dev.txt` first. Then `python scripts/validate_agents.py` validates the manifest schema, route pack coverage, cohort fit, tier path fit, runtime seam fit, and every referenced artifact instance.
