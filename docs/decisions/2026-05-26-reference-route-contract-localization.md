# 2026-05-26: Reference Route Contract Localization

## Status

Accepted.

## Context

After the agent-service contract localization, the remaining root example
payloads were the public-loop reference route packs and Alpha curated
reference-route examples. Both already had mechanic homes:
`mechanics/checkpoint/parts/reference-routes/` for public-loop route packs and
`mechanics/questbook/parts/alpha-reference-routes/` for Alpha readiness
posture.

Keeping the schemas and examples in root made `examples/` and `schemas/` look
like active mechanic homes even though the package docs already named the
Checkpoint and Questbook parts as the operational routes.

## Decision

Move reference-route contracts into their owning parts:

- reference route manifest schema and route-pack examples into
  `mechanics/checkpoint/parts/reference-routes/{schemas,examples}/`
- Alpha curated reference-route schema and examples into
  `mechanics/questbook/parts/alpha-reference-routes/{schemas,examples}/`

Add `scripts/validate_reference_route_contracts.py` and route
`scripts/validate_agents.py` through the part-local paths so former root
paths stay absent, generated Alpha readers stay aligned, and reference route
packs continue to validate against cohort, tier, and runtime-seam contracts.

## Consequences

Root `examples/` no longer owns active reference-route examples. Root
`schemas/` no longer owns reference-route schemas; it remains the shared
registry/profile/cohort/model-tier/runtime-seam-binding schema district.

Stable schema `$id` values and manifest `route_id` values remain public
contract identifiers, not active repo paths. Active route-pack directories use
kebab-case package names.

Validation for this route is:

```bash
python scripts/validate_reference_route_contracts.py
python scripts/generate_alpha_reference_routes.py --check
python scripts/validate_agents.py
```
