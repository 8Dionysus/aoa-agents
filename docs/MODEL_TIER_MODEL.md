# MODEL TIER MODEL

## Purpose

This document defines the tier-oriented side of the agent layer.

It does not replace human role archetypes such as `architect`, `coder`, `reviewer`, `evaluator`, or `memory-keeper`.
It adds a separate model-tier registry for orchestration-shaped duties.

## Core rule

Tier roles describe effort classes and handoff posture, not model brands.

They should answer:

- who routes
- who plans
- who executes
- who verifies
- who conducts escalation
- who handles rare deep synthesis
- who distills durable memory candidates

## State machine

The external state machine remains:

`route -> plan -> do -> verify -> deep? -> distill`

This is a public orchestration contract.
It should stay small and explicit.

## Pattern alignment

The official cohort patterns align to the tier model as bounded hints:

- `solo` usually stays close to `router`, `executor`, and `verifier`
- `pair` usually stays close to `planner`, `executor`, and `verifier`
- `checkpoint_cohort` usually adds `archivist` after governed change work
- `orchestrated_loop` may span the whole public loop, including `conductor`, `deep`, and `archivist`

These pattern names are composition hints, not routing policy or scenario canon.

## Tier roles

### `router`

- fastest bounded triage
- classifies task shape, risk, and next tier
- leaves a route decision rather than doing the whole job

### `planner`

- shapes a bounded plan
- names decision points, verification posture, and escalation boundaries

### `executor`

- performs the bounded task work
- should stay action-focused rather than absorbing planning and review by default

### `verifier`

- checks output, contradictions, and named limits
- should keep path and outcome review legible

### `conductor`

- governs the transition between tiers
- decides whether the loop should continue, escalate, pause, or distill
- should remain rare and explicit rather than hidden inside every tier

### `deep`

- reserved for high-cost synthesis, arbitration, framing, or recovery
- should not run by default on every route

### `archivist`

- distills summaries, entities, decisions, and memory candidates
- should not replace source-authored canon or philosophical judgment

## Memory posture

Tier memory posture should stay narrower than role memory posture.

Preferred default shape:

- `router`: `core` plus selected `hot`
- `planner`: `core`, selected `hot`, selected `warm`
- `executor`: `core`, selected `hot`
- `verifier`: `core`, selected `hot`, selected `warm`
- `conductor`: `core`, selected `hot`, selected `warm`
- `deep`: `core`, selected `warm`, selected `cool`
- `archivist`: `core`, selected `warm`, selected `cool`, selected `cold`

## Activation discipline

`deep` should be triggered only when the route has a real reason, such as:

- high uncertainty
- conflict between strong options
- repeated stall without progress
- high cost of error
- need for rule birth or contradiction arbitration

`archivist` should activate after a non-trivial route that needs durable distillation.

## Boundaries to preserve

- tier roles are not brand names
- tier roles are not the same as human role archetypes
- `aoa-routing` may point toward tiers, but it does not own tier doctrine
- `abyss-stack` may document model profiles, but it does not own agent-layer tier meaning

## Minimal contract

Each tier should have:

- one primary duty
- one output contract
- one default memory scope
- named handoff targets
- one expected artifact
