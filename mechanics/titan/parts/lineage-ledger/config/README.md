# Lineage Ledger Config

## Operating Card

| Field | Route |
| --- | --- |
| role | source ledger for Titan bearer lineage events |
| input | reviewed first-appearance, succession, and lineage event records |
| output | Titan lineage validation input and lineage-facing docs/examples |
| owner | `mechanics/titan/parts/lineage-ledger/` |
| next route | lineage ledger docs, role-bearing config, Titan validator |
| tools | `scripts/validate_titan_lineage.py` |
| validation | Titan lineage validator with this ledger path |

## Active Config

- [ledger.v0.json](ledger.v0.json)

## Boundaries

This ledger records lineage events for role-bearing posture. It does not erase
bearer memory, declare durable memory truth, or become runtime roster authority.
