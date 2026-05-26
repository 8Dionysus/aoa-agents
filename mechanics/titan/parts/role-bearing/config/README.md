# Role Bearing Config

## Operating Card

| Field | Route |
| --- | --- |
| role | source configs for Titan role classes and active bearers |
| input | reviewed role-class definitions and named bearer records |
| output | Titan lineage validation input and generated Titan Codex agent projection |
| owner | `mechanics/titan/parts/role-bearing/` |
| next route | role-bearer ontology, lineage ledger config, Titan projection builder |
| tools | `mechanics/titan/scripts/validate_titan_lineage.py`, `scripts/render_titan_codex_agents.py` |
| validation | Titan lineage validator and Titan Codex projection renderer |

## Active Configs

- [role-classes.v0.json](role-classes.v0.json)
- [bearers.v0.json](bearers.v0.json)

## Boundaries

These configs define role-bearing posture. They do not own runtime service
deployment, durable memory truth, proof verdicts, or AoA center doctrine.
