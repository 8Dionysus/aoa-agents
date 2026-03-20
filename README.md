# aoa-agents

`aoa-agents` is the role and persona layer of the AoA ecosystem.

It exists to make agents explicit as role-bearing actors rather than leaving them as vague prompt folklore or hidden orchestration assumptions.

This repository is not the main home of reusable techniques, skill bundles, proof bundles, or memory objects.
Its role is different: it should define who acts, under what contract, with what boundaries, preferred skills, memory posture, evaluation posture, and handoff rules.

## Start here

If you are new to this repository, use this path:

1. Read [CHARTER](CHARTER.md) for the role and boundaries of the agent layer.
2. Read [docs/AGENT_MODEL](docs/AGENT_MODEL.md) for the conceptual model.
3. Read [docs/BOUNDARIES](docs/BOUNDARIES.md) for ownership rules.
4. Read [ROADMAP](ROADMAP.md) for the current direction.

For the shortest next route by intent:
- if you need the ecosystem center and layer map, go to [`Agents-of-Abyss`](https://github.com/8Dionysus/Agents-of-Abyss)
- if you need authored execution workflows rather than actor contracts, go to [`aoa-skills`](https://github.com/8Dionysus/aoa-skills)
- if you need portable proof surfaces rather than role posture, go to [`aoa-evals`](https://github.com/8Dionysus/aoa-evals)
- if you need memory and recall meaning, go to [`aoa-memo`](https://github.com/8Dionysus/aoa-memo)
- if you need scenario compositions across multiple surfaces, go to [`aoa-playbooks`](https://github.com/8Dionysus/aoa-playbooks)

## Quick route table

| repository | owns | go here when |
|---|---|---|
| `aoa-agents` | agent profiles, role contracts, handoff posture, memory posture, evaluation posture | you need to define who acts under what role contract |
| `Agents-of-Abyss` | ecosystem identity, layer map, federation rules, program-level direction | you need the center and the constitutional view of AoA |
| `aoa-skills` | bounded agent-facing execution workflows | you need execution interfaces rather than actor contracts |
| `aoa-evals` | portable proof surfaces for bounded claims | you need quality and boundary checks rather than role definitions |
| `aoa-memo` | memory objects, recall surfaces, provenance threads | you need memory-layer meaning rather than agent-layer contracts |
| `aoa-playbooks` | recurring operational scenarios and multi-surface compositions | you need scenario recipes rather than role-bearing actors |

## What this repository is for

`aoa-agents` should own agent-layer meaning about:
- agent profiles
- role contracts
- handoff postures
- preferred skill families
- memory access posture
- evaluation posture
- agent composition hints
- compact agent registries and validation

## What this repository is not for

This repository should not become the main home for:
- reusable techniques
- skill bundles
- eval bundles
- routing surfaces
- memory objects
- infrastructure implementation details
- giant prompt archives pretending to be role design

An agent is not a skill.
A skill is a bounded workflow.
An agent is a role-bearing actor that uses skills.

## Relationship to the AoA federation

Within AoA:
- `aoa-techniques` owns practice meaning
- `aoa-skills` owns execution meaning
- `aoa-evals` owns bounded proof meaning
- `aoa-routing` should own dispatch and navigation surfaces
- `aoa-memo` should own memory and recall meaning
- `aoa-agents` should own role and persona meaning

## Local validation

This repository includes a compact machine-readable agent-layer registry at:
- `generated/agent_registry.min.json`

To validate the current agent-layer surface locally, run:

```bash
python scripts/validate_agents.py
```

## Current status

`aoa-agents` is in bootstrap.
The goal of this first public baseline is to define the role, boundaries, and first machine-readable agent-layer surface without overbuilding orchestration too early.

## Principles

- agents should be explicit rather than magical
- roles should stay bounded and reviewable
- handoff should be a contract, not an accident
- memory posture should be named, not implied
- evaluation posture should be named, not retrofitted later
- the agent layer should not swallow neighboring AoA layers

## License

Apache-2.0
