# 2026-05-26: Active Provenance Bridge Wording
## Index Metadata

- Decision ID: AOA-AG-D-0048
- Original date: 2026-05-26
- Surface classes: legacy/provenance, mechanic package
- Agent facets: mechanics atlas
- Mechanic parents: cross-mechanic
- Guard families: legacy/provenance
- Posture: accepted


## Context

The mechanics packages had gained package-level route cards, but several active
cards still repeated archive wording directly. That made the active path noisier
than the source pattern in `Agents-of-Abyss`: agents should enter active parts
first, and only use `PROVENANCE.md` when former-path or source-accounting
evidence is needed.

## Decision

Rename the central topology note to `mechanics/PROVENANCE_TOPOLOGY.md` and
reword active mechanics cards around provenance rather than archive internals.

Package `PARTS.md`, package `AGENTS.md`, and `parts/AGENTS.md` files now point
to `PROVENANCE.md` as the bridge without repeating archive names. Package
`PROVENANCE.md` files remain the active bridge for old-path lookup.

`scripts/validate_nested_agents.py` now rejects repeated archive bridge wording
in the active mechanics route-card layer.

## Consequences

This is a route-language cleanup. It does not move payloads, change source
contracts, or remove package archive indexes.

Future active cards should describe the working route and name `PROVENANCE.md`
when evidence lookup is needed. They should not duplicate archive inventories.
