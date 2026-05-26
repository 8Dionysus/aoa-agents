# 2026-05-26: Spark Agent Lane Home

## Status

Accepted.

## Context

`aoa-agents` still had a root `Spark/` directory with a local route card and
swarm recipe. Sibling source comparison shows the maintained pattern:
`Agents-of-Abyss`, `aoa-evals`, `aoa-memo`, `aoa-skills`, and
`aoa-techniques` keep Spark under `.agents/spark/`.

Spark is agent-facing operating guidance. It is not a mechanic package, source
role object, generated reader, schema contract, proof bundle, durable memory
object, or runtime implementation.

## Decision

Move the Spark lane from:

```text
Spark/
```

to:

```text
.agents/spark/
```

Add `.agents/AGENTS.md` as the agent-facing companion district card and teach
`scripts/validate_agents.py` plus `scripts/validate_nested_agents.py` to guard
the new path and former-root absence.

## Consequences

The repository root no longer carries a standalone Spark lane. Agent-facing
companion surfaces route through `.agents/`, while source-authored role meaning
remains under `agents/` and repeatable operation topology remains under
`mechanics/`.

Future Spark work starts at `.agents/spark/AGENTS.md` and
`.agents/spark/SWARM.md`. If a Spark lane starts carrying durable process law,
move that law to the owning source, mechanic, proof, memo, playbook, or runtime
surface instead of widening Spark.

## Validation

```bash
python scripts/validate_nested_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_agents.py
python scripts/release_check.py
```
