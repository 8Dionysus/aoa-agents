# Route-Derived External Runtime Session Identity

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0068
- Original date: 2026-08-15
- Surface classes: external actor preparation, SDK request, runtime launch binding
- Agent facets: incarnation, session identity, responsibility return
- Mechanic parents: boundary-bridge, external actor preparation
- Guard families: owner boundary, task identity, runtime admission
- Posture: deterministic child-session binding

## Context

The external actor preparer accepted an execution `session_ref` and separately
derived the physical runtime `session_id` from `route_id`. A fresh role-first
route exposed that these could name the current holder's Codex session and the
child runtime session respectively. abyss-stack correctly rejected the packet
before process creation because the canonical SDK summon request and launch
manifest named different sessions.

## Decision

The passive preparer derives one actor runtime session identity from
`route_id`, including the full digest of the original route to distinguish
routes whose human-readable slugs would otherwise collide. It uses that exact
value for both the SDK summon request's `session_ref` and the abyss-stack
launch manifest's `session_id`. The current holder remains represented by the
obligation, return-owner, and responsibility transfer refs; it is not reused as
the physical child session identity.

This is an owner compiler invariant. Callers do not supply a redundant
`execution.session_ref`, reconcile low-level session strings, or patch
generated request/launch JSON by hand.

## Consequences

- Runtime admission sees one exact actor session identity across SDK and
  abyss-stack.
- Distinct valid route IDs cannot alias through delimiter normalization.
- Route identities remain model- and launcher-neutral.
- Existing parent/return-holder refs retain their responsibility meaning.
- The route packet still requires explicit apply and runtime admission; this
  decision does not start a process or accept a return.

## Source Surfaces

- `skills/aoa-summon/scripts/prepare_external_actor.py`
- `tests/test_external_actor_preparer.py`

## Verification

Verify the focused preparer test, repository test suite, generated decision
indexes, semantic/nested-agent validators, and the real fresh-session runtime
admission path.
