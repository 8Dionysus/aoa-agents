# aoa-agents

`aoa-agents` is the role and persona layer of the AoA ecosystem.

It exists to make agents explicit as role-bearing actors rather than leaving them as vague prompt folklore or hidden orchestration assumptions.

This repository is not the main home of reusable techniques, skill bundles, proof bundles, or memory objects.
Its role is different: it should define who acts, under what contract, with what boundaries, preferred skills, memory posture, evaluation posture, and handoff rules.

## Start here

If you are new to this repository, use this path:

1. Read [CHARTER](CHARTER.md) for the role and boundaries of the agent layer.
2. Read [docs/AGENT_MODEL](docs/AGENT_MODEL.md) for the conceptual model.
3. Read [docs/SELF_AGENT_CHECKPOINT_STACK](docs/SELF_AGENT_CHECKPOINT_STACK.md) for the bounded self-agent contract.
4. Read [docs/BOUNDARIES](docs/BOUNDARIES.md) for ownership rules.
5. Read [ROADMAP](ROADMAP.md) for the current direction.

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
- self-agent posture should be checkpointed rather than mythologized
- handoff should be a contract, not an accident
- memory posture should be named, not implied
- evaluation posture should be named, not retrofitted later
- the agent layer should not swallow neighboring AoA layers

## License

Apache-2.0
