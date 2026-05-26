# Alpha Reference Routes Part

This part routes `alpha-reference-routes` pressure inside `mechanics/questbook/`.

## Active Contracts

- [schemas/alpha-reference-route.schema.json](schemas/alpha-reference-route.schema.json)
- [examples/](examples/)
- [generated/alpha-reference-routes.min.json](generated/alpha-reference-routes.min.json)

The compact generated companion is part-local because it is derived only from
this part's Alpha route examples.

Validate with `python scripts/validate_reference_route_contracts.py` and
`python scripts/generate_alpha_reference_routes.py --check`.

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
