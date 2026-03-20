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

## Relationship to neighboring layers

- `aoa-techniques` stores reusable practice
- `aoa-skills` stores bounded execution
- `aoa-evals` stores bounded proof
- `aoa-routing` stores navigation and dispatch
- `aoa-memo` stores memory and recall surfaces
- `aoa-agents` stores reusable role-bearing actors

## Compact principle

The agent layer should make actors explicit without turning the system into theater.
