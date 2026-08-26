# 2026-08-23: Exact Goal participant relations stay a bounded agent-layer seam

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0071
- Original date: 2026-08-23
- Surface classes: agent contract, mechanic, boundary, generated reader
- Agent facets: role contract, owner split, evidence posture
- Mechanic parents: boundary-bridge
- Guard families: exact identity, relation admission, no fallback, privacy
- Posture: accepted

## Context

Goal/thread participant views need to relate actor obligation, assignment,
model realization, and runtime incarnation without turning a dashboard row,
holder suffix, role label, PID, path, or bare Goal id into identity. The
stronger owners publish those dimensions independently, and the prior owner
review found that collapsing absent or invalid evidence into generic participant
states creates false bindings.

## Options Considered

- Let a dashboard or consumer derive a participant graph from nearby labels and
  runtime observations.
- Put Goal, model, session, and runtime canon into `aoa-agents`.
- Publish a bounded agent-layer relation contract whose exact references and
  publisher-owned key preserve stronger-owner boundaries.

## Decision

Add `mechanics/boundary-bridge/parts/participant-relations/` as the
`aoa-agents` source surface for exact Goal/thread participant and assignment
relations. Require exact owner references with schema versions and content
digests for populated dimensions, preserve independent state values, and join
only through the publisher-owned `relation_key`. Build a deterministic reader
from the source feed; do not emit display, model, runtime, or evidence
fallbacks.

The checked-in source feed remains empty with deferred currentness until an
exact owner-published relation is admitted. Goal/thread, model, session, and
runtime owners retain their stronger truth.

## Rationale

The seam gives consumers a reviewable contract and a stable admission point
without pretending that a source-owned relation is a live process graph. It
also makes pagination, currentness, and privacy omissions explicit so that a
partial or stale owner response cannot become a generic participant label.

## Consequences

- Consumers receive a deterministic, schema-validated relation shape with no
  heuristic joins.
- Missing, unknown, stale, deferred, and invalid dimensions remain visible to
  the consumer rather than being upgraded to presence.
- An owner must publish an exact relation key and endpoint references before a
  relation can enter the source feed.
- Live presence, runtime health, wake/return, semantic acceptance, and Goal
  completion remain outside this part.

## Source Surfaces

- `mechanics/boundary-bridge/parts/participant-relations/contract.json`
- `mechanics/boundary-bridge/parts/participant-relations/records/goal-participant-relations.source.json`
- `mechanics/boundary-bridge/parts/participant-relations/scripts/build_goal_participant_graph.py`
- `mechanics/boundary-bridge/parts/participant-relations/scripts/validate_goal_participant_graph.py`

## Follow-Up Route

Future live binding work must arrive from the exact Goal/thread, model, session,
and runtime owners and remain subject to their owner contracts. Dashboard
composition belongs to the dashboard owner; it must consume this seam without
adding heuristic joins or claiming acceptance.

## Verification

Verification routes through the participant-relation builder/reader/validator,
its focused tests, `scripts/validate_agents.py`, the decision index generator,
and the repository release gate.
