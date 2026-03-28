# examples/reference_routes/AGENTS.md

## Purpose

`examples/reference_routes/` contains manifest-driven reference routes for the published agent-layer loop.

These files stay aligned with:

- `schemas/reference-route.example.schema.json`
- `docs/REFERENCE_ROUTE_EXAMPLES.md`
- `generated/runtime_seam_bindings.json`

## Contract anchors

Each route pack must keep `manifest.json` and its referenced artifact JSON files coherent.

These examples are not playbooks.

## Editing posture

Keep route packs bounded, portable, and public-safe.
Do not add runtime logs, scenario canon, or hidden transport details.
Use only already-published artifact schemas.

## Validation

`python scripts/validate_agents.py`
