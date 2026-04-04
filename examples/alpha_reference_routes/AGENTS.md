# examples/alpha_reference_routes/AGENTS.md

## Purpose

`examples/alpha_reference_routes/` contains curated Alpha cohort
reference-route surfaces for the readiness proof lane.

These files are playbook-facing example contracts. They are not runtime canon,
not live logs, and not composition authority.

## Source surfaces

- `schemas/alpha-reference-route.schema.json`
- `generated/alpha_reference_routes.min.json`
- `docs/REFERENCE_ROUTE_EXAMPLES.md`

## Editing posture

Keep the set aligned to the curated Alpha cohort and the fixed five-playbook
readiness scope.
Each file should stay compact, public-safe, and reviewable.
Do not widen the lane into general routing policy or invent a new agent family.

## Boundary

These routes describe a curated Alpha cohort.
They remain a readiness proof lane owned jointly with `aoa-playbooks`.
They do not replace playbooks, memo doctrine, or eval doctrine.
