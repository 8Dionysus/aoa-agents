# DESIGN.AGENTS.md

## Purpose

Use this file as the agent-facing reading card for repository design work.

## Read Order

1. `AGENTS.md`
2. `DESIGN.md`
3. `agents/AGENTS.md` when source objects move
4. `mechanics/AGENTS.md` when operation topology moves
5. `docs/decisions/` when structural ownership changes
6. nearest nested `AGENTS.md`

## Design Law

- `agents/` owns source-authored agent objects.
- `mechanics/` owns repeatable operation topology.
- `docs/` explains public agent-layer doctrine and boundaries.
- `schemas/` keeps shared contract shape until a mechanic-local package has a
  stronger reason to own a narrower schema.
- `examples/` keeps schema-backed examples until a mechanic-local package owns
  a narrower example lane.
- `generated/` remains derived.

## Operational Map Shape

Prefer route cards that answer:

| Field | Meaning |
| --- | --- |
| role | what this surface does |
| input | what enters here |
| output | what leaves here |
| owner | which surface owns truth |
| next route | where to go next |
| tools | what to run or inspect |
| validation | how to prove the route held |

When a boundary is needed, state the positive route that handles the pressure.

## Verification

Design topology changes should run:

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

Add builder checks when source objects or generated readers move.
