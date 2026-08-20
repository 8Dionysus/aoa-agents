# 2026-07-29: Agent-local memory is an isolated role leaf

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0070
- Original date: 2026-07-29
- Surface classes: agent contract, memory posture, authority boundary
- Agent facets: role contract, agent-local memory
- Mechanic parents: cross-mechanic
- Guard families: tenant isolation, sibling-owner boundary, reviewed promotion
- Posture: accepted

## Context

The shared `aoa-memo` organ can preserve reviewed cross-session truth, but one
shared memory surface cannot safely absorb every role-local episode,
procedure, failure, and adaptation. Agent-local memory can reduce repeated
re-grounding and contain faults, yet it also creates risks: cross-agent
contamination, tenant leakage, access-count reinforcement, duplicate storage,
silent private-to-shared publication, and local policy becoming hidden role
authority.

The agent layer owns exact role identity and role-level memory posture. It does
not own shared memory semantics, promotion, routing, runtime execution,
projection truth, or evaluation verdicts.

## Decision

Represent optional agent-local memory as one isolated leaf bound to an exact
`agent_id`, `tenant_id`, role profile, namespace identifier, and generation.

The leaf may:

- retain bounded episodic and procedural cases;
- adapt local ranking from outcome-qualified evidence within an explicit
  delta bound;
- expire, isolate, and roll back its own generation;
- nominate a content-minimized candidate for reviewed `aoa-memo` promotion.

It may not:

- read another agent or tenant namespace;
- use access count or role authority as a utility signal;
- publish directly to shared memory or a KAG projection;
- change role, permission, routing, effect, evaluation, or training authority;
- let local rollback mutate reviewed shared state.

Disabling the leaf must preserve shared reviewed recall. Every local-to-shared
handoff is nomination-only and remains subject to duplicate reconciliation,
conflict handling, and sole-operator review in the owning `aoa-memo` lane.

## Consequences

- Agent-local storage and ranking can evolve per consumer without fragmenting
  shared truth.
- A local fault has an explicit namespace boundary and degradation posture.
- Role profiles remain identity authority; the namespace cannot silently
  rewrite them.
- `aoa-memo`, `aoa-sdk`, `abyss-stack`, `aoa-kag`, `aoa-stats`, and
  `aoa-evals` retain their separate owner responsibilities.
- Real utility, review burden, model portability, resource pressure, and
  long-horizon behavior require comparative and soak evidence before live
  admission.

## Validation

Verification covers the namespace schema and semantic validator, decision
indexes, semantic and nested-agent validators, repository validation, and the
full test suite.
