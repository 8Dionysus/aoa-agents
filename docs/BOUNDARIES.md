# Agent Layer Boundaries

This document records the most important ownership boundaries for `aoa-agents`.

## Rule 1: agent owns role, not everything the role touches

`aoa-agents` should own agent-layer meaning such as:
- agent profiles
- role contracts
- handoff posture
- memory posture
- evaluation posture
- compact composition hints

It should not become the default dumping ground for everything an agent might use.

## Rule 2: agent is not skill

An agent may prefer or compose skills.
That does not make the agent profile itself a skill bundle.

Reusable execution still belongs to `aoa-skills`.

## Rule 3: agent is not proof

An agent may be judged by eval surfaces.
That does not make the agent profile itself a proof object.

Bounded proof still belongs to `aoa-evals`.

## Rule 4: agent is not memory

An agent may have memory posture.
That does not make the agent layer the owner of memory objects or recall truth.

Memory still belongs to `aoa-memo`.

## Rule 5: agent is not routing

An agent may rely on routing.
That does not make the agent layer the owner of cross-repo dispatch.

Navigation still belongs to `aoa-routing`.

## Rule 6: handoff matters

A role profile should make clear when the agent should stop, hand off, escalate, or require review.
That posture should not stay implicit.

## Rule 7: keep profiles reviewable

If profiles become giant biographies or hidden prompt systems, the layer will stop being trustworthy.
Compactness and explicit posture matter.

## Rule 8: self-agent posture must stay checkpointed

If a role can reshape important system surfaces, it should expose approval, rollback, and health-check posture explicitly.

The agent layer owns the role-facing contract for that checkpoint stack.
It does not own the runtime implementation underneath it.

## Compact rule

`aoa-agents` should help AoA name its actors without letting the actor layer blur every other layer.
