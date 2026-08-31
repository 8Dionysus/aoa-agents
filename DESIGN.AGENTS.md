# DESIGN.AGENTS.md

## Purpose

Use this file as the agent-facing reading card for repository design work.

## Route

Start with `AGENTS.md` and `DESIGN.md`, then follow the nearest owner card:
`agents/AGENTS.md` for source objects, `mechanics/AGENTS.md` for operation
topology, `stats/AGENTS.md` for agent-local statistical packets, and
`.agents/AGENTS.md` for companion lanes. Consult `docs/decisions/` when
structural ownership changes.

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
- `stats/` owns agent-local statistical meaning and reference packets while
  shared grammar and cross-owner composition remain in `aoa-stats`.
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

Design topology changes use root [VALIDATION.md](VALIDATION.md); the root and
nearest nested `AGENTS.md` cards identify the applicable owner checks.

Add the source-home validation lane when the source-object home, family map, or
generated-reader routes move. Add builder checks when source objects or
generated readers move, taking the exact commands from the owning route card.
