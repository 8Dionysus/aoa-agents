# Reference Route Examples

## Purpose

This directory contains manifest-driven reference routes for the published
agent-layer loop.

These files stay aligned with:

- `mechanics/checkpoint/parts/reference-routes/schemas/reference-route-manifest.schema.json`
- `mechanics/checkpoint/parts/reference-routes/docs/reference-route-examples.md`
- `generated/runtime_seam_bindings.json`

## Contract anchors

Each route pack must keep `manifest.json` and its referenced artifact JSON files coherent.

These examples are not playbooks.

## Editing posture

Keep route packs bounded, portable, and public-safe.
Do not add runtime logs, scenario canon, or hidden transport details.
Use only already-published artifact schemas.

## Validation

Run `python scripts/validate_reference_route_contracts.py` and then
`python scripts/validate_agents.py`.
