# Titan Mechanic

Status: active package.

`mechanics/titan/` routes Titan role-bearing surfaces inside `aoa-agents`:
bearer ontology, role classes, lineage, summon boundaries, runtime roster
contracts, service cohorts, and Codex-facing projections.

## Operating Card

| Field | Route |
| --- | --- |
| role | Titan role-bearing package for the agent layer |
| input | Titan bearer, role class, lineage, summon, incarnation, roster, memory loom, service cohort, and projection pressure |
| output | bounded Titan role posture, generated projection route, or stronger-owner handoff |
| owner | this package for agent-layer Titan operation routing |
| next route | `PARTS.md`, Titan builders, `mechanics/runtime-seam/`, `mechanics/codex-projection/` |
| validation | Titan builders/tests plus repo validators |

## Agent Layer Owns

- role-bearing posture for Titan-facing agents
- source config seeds for Titan role classes, bearers, and lineage
- part-local schemas for Titan role, lineage, incarnation, roster,
  service-cohort, and summon-boundary contracts
- part-local public-safe examples for Titan role, lineage, incarnation, roster,
  service cohort, and summon-boundary contracts
- generated Titan projection companions as derived readers
- boundaries between role posture, summon protocol, and runtime roster contracts

## Stronger Owner Split

- AoA center owns larger Titan doctrine.
- Runtime owners own live Titan service processes.
- `aoa-memo` owns memory truth; this package only routes role-facing recall posture.
- `aoa-evals` owns proof of Titan outputs.

## Validation

```bash
python mechanics/titan/scripts/validate_titan_lineage.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --ledger mechanics/titan/parts/lineage-ledger/config/ledger.v0.json
python mechanics/titan/scripts/validate_titan_schemas.py
python mechanics/titan/scripts/validate_titan_examples.py
python -m unittest discover -s mechanics/titan/tests -p "test_*.py"
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

If Titan Codex projection outputs change, also run:

```bash
python scripts/render_titan_codex_agents.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --out-dir generated/titan_codex_agents/agents --manifest generated/titan_codex_agents/projection_manifest.json --prune
```
