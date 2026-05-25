# AoA Agents Design

`aoa-agents` is the role-bearing agent layer of AoA.

The repository is organized around a split between source objects, operation
mechanics, public explanation, shared contracts, examples, generated readers,
and configuration.

## Districts

| District | Role |
| --- | --- |
| `agents/` | source-authored agent objects and compact role-facing inputs |
| `mechanics/` | repeatable operation topology around agent-layer movement |
| `docs/` | public explanation, doctrine, boundaries, and maps |
| `schemas/` | shared JSON Schema contracts |
| `examples/` | schema-backed public examples and negative fixtures |
| `generated/` | derived registries, compact readers, and projections |
| `config/` | publication and projection configuration |
| `scripts/` | deterministic builders and validators |
| `tests/` | behavior and contract checks |

## Operational Route Card Rule

Agent-facing route cards should prefer positive operational maps over long
negative preambles.

Every durable card should answer the same compact questions:

| Field | Question |
| --- | --- |
| role | what this surface does |
| input | what pressure enters here |
| output | what this surface produces |
| owner | which local file or package owns truth |
| next route | where an agent should go next |
| tools | which builders, validators, MCP/resources, or scripts help |
| validation | what proves the change stayed bounded |

Stop-lines remain useful, but they should point to a route instead of ending
as a bare prohibition.

## Source Object Flow

Source-authored agent objects live under `agents/`.

`agents/` inputs publish through deterministic builders into `generated/`.
Generated readers are consumer surfaces, not source truth.

```text
agents/* source -> scripts/* builder -> generated/* reader -> docs/consumer route
```

## Mechanics Flow

Mechanics name repeatable operations that cross several surfaces.

Examples include formation, Codex projection, runtime-seam binding,
checkpoint posture, quest-facing role posture, Titan role-bearing surfaces, and
release support. A mechanic routes operation pressure; it does not absorb the
stronger owner of each payload.

## Boundary Rule

This repository owns role and persona meaning.

It does not own reusable techniques, skill workflows, proof verdicts, memory
truth, routing policy, playbook choreography, KAG substrate semantics, stats
summaries, runtime workers, or infrastructure implementation.

## Growth Rule

Prefer small topology moves with validators.

Moving a file into a new district should also update:

- the nearest `AGENTS.md`
- docs or design maps that name the old path
- builders and validators that read the path
- generated readers when source paths are published
- a decision record when future agents need the reason

For AGENTS cards, add or preserve an `Operating Card` table before expanding
local prose.
