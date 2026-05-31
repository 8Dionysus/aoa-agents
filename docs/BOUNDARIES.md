# Agent Layer Boundaries

This document records the ownership boundaries that keep `aoa-agents` from
absorbing every layer an agent touches.

## Operating Card

| Field | Route |
| --- | --- |
| role | owner-boundary map for the agent layer |
| input | role, persona, handoff, projection, memory-posture, proof-posture, routing, playbook, or runtime authority pressure |
| output | local role-layer allowance, stop-line, or stronger-owner route |
| owner | this boundary map plus [CHARTER](../CHARTER.md) for repository authority |
| next route | [agents](../agents/README.md), [mechanics](../mechanics/README.md), or the sibling owner named below |
| validation | [AGENTS.md#verify](../AGENTS.md#verify) when boundary wording changes |

## Core Rule

`aoa-agents` owns role-bearing actor meaning. It does not own everything that a
role can use.

Healthy role-layer surfaces answer:

- who acts;
- what contract governs the actor;
- what posture, handoff, and capability references are visible;
- which generated companions summarize the source;
- where the actor must route when the pressure belongs to a stronger owner.

## Local Allowance

`aoa-agents` may own:

- base role houses and role contracts;
- role-local specializations and capability-pack references;
- handoff, memory, evaluation, stress, projection, and checkpoint posture at the
  actor layer;
- model tiers, orchestrator classes, cohort hints, and runtime-seam bindings as
  agent-layer contract surfaces;
- Codex projection eligibility and refresh posture when it is bounded to source
  role objects and owner consent;
- generated registries and readers derived from source-owned role-layer inputs.

## Stronger Owners

| Pressure | Stronger owner |
| --- | --- |
| reusable practice | `aoa-techniques` |
| bounded execution workflows | `aoa-skills` |
| proof doctrine, verdicts, scoring, and regression claims | `aoa-evals` |
| memory objects, recall truth, retention, and reviewed memory corpus | `aoa-memo` |
| navigation, dispatch, and route policy | `aoa-routing` |
| recurring scenario choreography, questline method, and campaigns | `aoa-playbooks` |
| derived graph or retrieval substrate semantics | `aoa-kag` |
| movement summaries and observability views | `aoa-stats` |
| runtime workers, services, storage, lifecycle, and infrastructure | `abyss-stack` |
| AoA center doctrine and federation rules | `Agents-of-Abyss` |
| ToS-authored knowledge meaning | `Tree-of-Sophia` |

## Boundary Rules

### Agent Is Not Skill

An agent may prefer or compose skills. That does not make the profile a skill
bundle. Reusable execution stays in `aoa-skills`.

### Capability Pack Is Not Implementation

A capability pack may collect permission posture, tool refs, skill refs,
technique refs, memory routes, proof routes, and projection hints. It does not
implement or own those layers.

### Specialization Is Not Automatic Projection

A role specialization such as `coder.repo-refactor` is a narrower source-layer
actor contract inside a base role house.

It does not automatically become a Codex custom agent, workspace install entry,
or runtime worker. Codex projection remains base-role-only until an explicit
eligibility record names install identity, permission posture, refresh law, and
owner consent.

The eligibility gate lives under
`mechanics/codex-projection/parts/specialization-eligibility/` and does not
install agents by itself.

### Agent Is Not Proof

An agent may be evaluated by proof surfaces. That does not make the profile an
eval bundle or verdict. Bounded proof stays in `aoa-evals`.

### Agent Is Not Memory

An agent may have memory posture and memory rights. That does not make the role
layer the owner of memory objects or recall truth. Memory stays in `aoa-memo`.

### Agent Is Not Routing

An agent may rely on routing. That does not make the role layer the owner of
cross-repo dispatch. Navigation and route policy stay in `aoa-routing`.

### Agent Is Not Runtime

An agent may define runtime-facing contracts, role-tier bindings, or artifact
transition posture. It does not own live workers, services, storage, daemons, or
runtime state.

## Handoff Rule

A role profile or mechanic should say when the agent should stop, hand off,
escalate, or require review. Handoff posture should not stay implicit.

## Compactness Rule

Profiles, root docs, and route cards should stay inspectable. If a surface
starts becoming a biography, prompt archive, proof doctrine, memory corpus,
scenario book, or runtime manual, route it away.

## Self-Agent And Formation Rule

Self-agent, recurrence, progression, checkpoint, Titan, quest, and formation
language must stay bounded, reviewable, evidence-linked, and reversible.

If a role can reshape important system surfaces, expose approval, rollback,
health-check, bounded-iteration, and handoff posture explicitly. Runtime
implementation and durable memory remain with stronger owners.

## Compact Principle

`aoa-agents` should help AoA name its actors without letting the actor layer
blur every other layer.
