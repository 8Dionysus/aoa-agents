# AoA Agents Roadmap

This roadmap tracks the bootstrap and early shaping of the AoA agent layer.

## Current phase

`aoa-agents` is in bootstrap.
The current goal is not to build a giant orchestration engine immediately.
The goal is to define what the agent layer is for, what it owns, and what it must not silently absorb.

## Bootstrap substep: runtime seam hardening

Goals:
- add inspectable runtime artifact examples and bounded negative fixtures
- publish a machine-readable role × tier binding surface
- make transition and artifact coverage discipline explicit
- add optional published-contract smoke checks without requiring cross-repo CI checkout

Exit signals:
- every published runtime artifact schema has a valid example and bounded invalid fixture coverage
- the public role × tier mapping is machine-readable without changing existing registry wire shape
- the validator can confirm public contract reachability in neighboring repos when local roots are supplied

## Phase 1: agent layer definition

Goals:
- define `aoa-agents` as the canonical role and persona layer within AoA
- make the distinction between agent, skill, proof, memory, and routing explicit
- establish a compact agent registry and a minimal validator

Exit signals:
- the repository role is clear
- agent-layer boundaries are documented
- a compact machine-readable registry exists

## Phase 2: first agent profile discipline

Goals:
- define the first public shape for agent profiles
- distinguish basic role contracts such as architect, coder, reviewer, evaluator, and memory-keeper
- keep profile forms compact enough to review

## Phase 3: handoff and posture surfaces

Goals:
- make handoff rules explicit
- make memory posture explicit
- make evaluation posture explicit
- keep agent boundaries readable to humans and smaller models

## Phase 4: cohort composition

Goals:
- define bounded multi-agent composition hints
- clarify when agents operate solo, in pairs, or under orchestration
- avoid turning the agent layer into a hidden runtime monolith too early

Exit signals:
- the first official cohort pattern set is documented
- a machine-readable cohort composition registry exists
- the validator checks cohort pattern alignment against role and tier registries
- the self-agent checkpoint route maps to a canonical cohort pattern without absorbing playbook logic

## Phase 5: federation integration

Goals:
- connect `aoa-agents` cleanly to `aoa-skills`
- connect agent postures to `aoa-evals`
- connect agent memory posture to `aoa-memo`
- preserve clear boundaries relative to `aoa-routing`

## Standing discipline

Across all phases:
- keep roles explicit
- keep profiles compact
- keep handoff rules reviewable
- do not confuse the actor layer with execution, proof, memory, or routing
