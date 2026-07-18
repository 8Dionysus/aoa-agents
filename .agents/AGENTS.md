# AGENTS.md

## Applies To

This card applies to `.agents/` and all descendants unless a nearer
`AGENTS.md` narrows the path.

## Role

`.agents/` holds bounded agent-facing companion surfaces for operating inside
this repository. The active local surface is the Spark lane; globally exposed
owner skills remain canonical under `skills/`.

It is not the source-authored `agents/` district. Source role meaning remains
under `agents/`, with docs, schemas, mechanics, builders, and validators as
stronger owner surfaces where applicable.

## Read Before Editing

Read root `AGENTS.md`, then inspect the nearest local skill README, lane
README, route card, or manifest before changing prompt-like material.

For Codex Spark work, read `.agents/spark/AGENTS.md` and use
`.agents/spark/SWARM.md` only when a Spark swarm is explicitly requested.

## Boundaries

- Do not encode private memory, hidden authority, or unreviewable autonomy here.
- Do not make this lane the source of role truth, mechanic law, proof meaning,
  durable memory, routing policy, or runtime state.
- Do not add prompt material that bypasses source-family validation, route
  cards, or owner boundaries.
- Keep `.agents/spark/` as a fast-loop lane. Do not recreate globally installed
  owner or shared skill copies under `.agents/skills/`.

## Validation

Use the narrowest relevant checks first:

```bash
python scripts/validate_nested_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_agents.py
```

## Closeout

Report changed agent-facing files, source surfaces consulted, validation run,
validation skipped, remaining risk, and the next owner route when `.agents/`
was only a waypoint.
