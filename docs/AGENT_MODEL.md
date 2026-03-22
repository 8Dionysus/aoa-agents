# Agent Model

This document defines the conceptual model of the AoA agent layer.

## Why an agent layer exists

AoA needs more than reusable practice, bounded execution, bounded proof, memory, and routing.
It also needs explicit actors.

The agent layer exists to make roles, posture, and handoff visible rather than leaving them implicit in prompts or orchestration code.

## What counts as an agent here

Within `aoa-agents`, an agent should mean a reusable role-bearing actor described through surfaces such as:
- role contract
- preferred skill families
- handoff posture
- memory posture
- evaluation posture
- compact composition hints

## Agent classes

The first useful distinction is between role archetypes such as:

### Architect

An agent focused on structure, boundaries, and system-shaping decisions.

### Coder

An agent focused on implementing bounded changes through explicit workflows.

### Reviewer

An agent focused on inspection, critique, drift detection, and bounded approval posture.

### Evaluator

An agent focused on bounded proof, comparison, and judgment surfaces.

### Memory-keeper

An agent focused on preserving provenance, recall, and memory hygiene.

## What an agent must not do

An agent profile should not silently become:
- a skill bundle
- a proof surface
- a routing layer
- a memory store

An agent may use all of those layers, but does not replace them.

## Agent posture

A good agent profile should make it easier to answer:
- what role is being played?
- what work is this role suited for?
- when should this role hand off?
- how much memory should this role rely on?
- how strict should its evaluation posture be?

## Self-agent as governed checkpoint

AoA may include self-agent surfaces, but they should stay governed rather than mythologized.

When an agent can reshape important system surfaces, its role contract should make checkpoint posture visible:

- constitution or policy check
- approval gate
- rollback marker
- health check
- bounded iteration limit
- improvement log requirement

See [SELF_AGENT_CHECKPOINT_STACK](SELF_AGENT_CHECKPOINT_STACK.md) for the compact contract.

## Self-agent checkpoint cohort

When a self-agent route becomes a real scenario-level method, AoA should prefer a small visible cohort over one magical actor.

Current bounded cohort pattern:

- `architect` initiates the route, checks constitutional fit, and keeps scope bounded
- `coder` executes the bounded change path after the gate is clear
- `reviewer` checks approval posture, health posture, and final boundedness
- `memory-keeper` preserves provenance and the improvement log as reviewable history

This keeps one role from silently becoming planner, operator, reviewer, and historian at the same time.

## Thinkers and operators

AoA benefits from preserving a gap between thinking roles and acting roles.

Thinking roles may plan, critique, compare, and shape.
Operator-facing roles may execute bounded changes.

This gap creates review surfaces and makes self-agent posture legible.

## Relationship to neighboring layers

- `aoa-techniques` stores reusable practice
- `aoa-skills` stores bounded execution
- `aoa-evals` stores bounded proof
- `aoa-routing` stores navigation and dispatch
- `aoa-memo` stores memory and recall surfaces
- `aoa-agents` stores reusable role-bearing actors

## Compact principle

The agent layer should make actors explicit without turning the system into theater.
