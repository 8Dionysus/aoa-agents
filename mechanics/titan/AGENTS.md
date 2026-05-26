# AGENTS.md

## Applies To

This card applies to `mechanics/titan/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

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
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, Titan builders, `mechanics/runtime-seam/`, `mechanics/codex-projection/` |
| tools | Titan lineage validator, Titan schema/example validators, Titan projection renderer, repo validators |
| validation | Titan builders/tests plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` before using `legacy/`
8. stronger owner routes for center doctrine, runtime, memo, or proof pressure

## Boundaries

- AoA center owns larger Titan doctrine.
- Runtime owners own live Titan service processes.
- `aoa-memo` owns memory truth; this package only routes role-facing recall posture.
- `aoa-evals` owns proof of Titan outputs.

## Validation

```bash
python scripts/validate_titan_lineage.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --ledger mechanics/titan/parts/lineage-ledger/config/ledger.v0.json
python scripts/validate_titan_schemas.py
python scripts/validate_titan_examples.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

If Titan Codex projection outputs change, also run:

```bash
python scripts/render_titan_codex_agents.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --out-dir generated/titan_codex_agents/agents --manifest generated/titan_codex_agents/projection_manifest.json --prune
```

## Closeout

Report the changed Titan part, source config/schema/example/generated surface
affected, checks run, checks skipped, and any center, runtime, memo, or proof
handoff.
