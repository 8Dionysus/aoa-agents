# Alpha Reference Route Examples

## Purpose

This directory contains curated Alpha cohort reference-route surfaces for the
readiness proof lane.

These files are playbook-facing example contracts. They are not runtime canon,
not live logs, and not composition authority.

## Source surfaces

- `mechanics/questbook/parts/alpha-reference-routes/schemas/alpha-reference-route.schema.json`
- `mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json`
- `mechanics/checkpoint/parts/reference-routes/docs/reference-route-examples.md`

## Editing posture

Keep the set aligned to the curated Alpha cohort and the fixed five-playbook
readiness scope.
Each file should stay compact, public-safe, and reviewable.
Do not widen the lane into general routing policy or invent a new agent family.

## Boundary

These routes describe a curated Alpha cohort.
They remain a readiness proof lane owned jointly with `aoa-playbooks`.
They do not replace playbooks, memo doctrine, or eval doctrine.

## Validation

Run `python scripts/generate_alpha_reference_routes.py --check`,
`python scripts/validate_reference_route_contracts.py`, and
`python scripts/validate_agents.py`.
