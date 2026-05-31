# DESIGN.AGENTS.md

## Purpose

Use this file as the agent-facing reading card for repository design work.

## Read Order

1. `AGENTS.md`
2. `DESIGN.md`
3. `agents/AGENTS.md` when source objects move
4. `mechanics/AGENTS.md` when operation topology moves
5. `.agents/AGENTS.md` when agent-facing companion lanes move
6. `docs/decisions/` when structural ownership changes
7. nearest nested `AGENTS.md`

## Design Law

- `agents/` owns source-authored agent objects.
- `agents/source_home.manifest.json` owns the checked source-home family map.
- `.agents/` owns agent-facing companion lanes such as exported skills and the
  Codex Spark fast-loop lane.
- `mechanics/` owns repeatable operation topology.
- `docs/` explains public agent-layer doctrine and boundaries.
- `schemas/` keeps shared contract shape until a mechanic-local package has a
  stronger reason to own a narrower schema.
- `examples/` keeps schema-backed examples until a mechanic-local package owns
  a narrower example lane.
- `generated/` remains derived.
- mechanic-local seeds and wiring live under the owning `mechanics/*/parts/*/config/` route when the operation package has a validator.
- recurrence component manifests live under `mechanics/recurrence/parts/component-manifests/manifests/`.

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

Design topology changes use the command routes in root `AGENTS.md` and the
nearest nested `AGENTS.md`.

Add the source-home validation lane when the source-object home, family map, or
generated-reader routes move. Add builder checks when source objects or
generated readers move, taking the exact commands from the owning route card.
