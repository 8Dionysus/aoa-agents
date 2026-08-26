# 2026-08-23: Typed Goal participant publication stays fail-closed at intake

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0072
- Original date: 2026-08-23
- Surface classes: agent contract, mechanic, boundary, generated reader
- Agent facets: role contract, owner split, evidence posture
- Mechanic parents: boundary-bridge
- Guard families: exact identity, relation admission, currentness, privacy
- Posture: accepted

## Context

The exact Goal participant relation contract had a deterministic empty reader,
but no reusable input boundary separated an upstream owner publication from
source publication. A current exact Goal read was not enough to supply a
Goal-instance, assignment, model realization, runtime incarnation, or an
aoa-agents actor/obligation relation. Without an intake receipt, a shaped
fixture or a holder label could be mistaken for current source evidence.

## Options Considered

- Populate the checked-in source from the selected Goal and nearby live
  observations.
- Let consumers compose identity, role, task, model, and runtime from labels,
  paths, versions, or one Goal instance.
- Add an explicit typed owner publication, fail-closed admission receipt, and
  optional source publisher while retaining the checked-in empty state.

## Decision

Add `aoa_agents_goal_participant_relation_publication_v1` as the only generic
upstream input shape for this part. It requires one exact Goal/Goal-instance/
master-thread scope, producer and publication provenance, currentness without
an unadmitted continuation, the privacy omission set, a canonical payload
digest, and independent relation records with verifiable publisher-key
digests. `admit_goal_participant_publication.py` emits a structural
`aoa_agents_goal_participant_relation_admission_v1` receipt only after those
checks pass. An explicit source output may then replace `empty_deferred`; no
source write is inferred from a Goal, session, title, path, terminal, model
label, or runtime observation.

## Rationale

The intake boundary is implementable in `aoa-agents` without claiming any
stronger owner's facts. It gives future producers a precise dependency and
keeps identity, obligation, task assignment, model realization, and runtime
incarnation independent. Currentness, privacy, provenance, and claim limits
remain visible at both receipt and source boundaries.

## Consequences

- A current relation can be admitted with independently non-present dimensions;
  absent, stale, deferred, unknown, and invalid states are not upgraded.
- Incomplete pages, synthetic records, heuristic keys, missing digests, scope
  mismatches, and missing receipts fail closed.
- The checked-in source and generated graph remain empty/deferred until a
  producer supplies the exact owner records; no private current-session data
  is copied into the repository.
- Admission is structural and does not establish liveness, runtime health,
  wake, acceptance, completion, or human identity.

## Source Surfaces

- `mechanics/boundary-bridge/parts/participant-relations/contract.json`
- `mechanics/boundary-bridge/parts/participant-relations/schemas/goal-participant-publication.schema.json`
- `mechanics/boundary-bridge/parts/participant-relations/schemas/goal-participant-admission.schema.json`
- `mechanics/boundary-bridge/parts/participant-relations/scripts/admit_goal_participant_publication.py`
- `mechanics/boundary-bridge/parts/participant-relations/scripts/build_goal_participant_graph.py`
- `mechanics/boundary-bridge/parts/participant-relations/scripts/validate_goal_participant_graph.py`

## Follow-Up Route

The exact Goal/thread producer, aoa-session-memory Goal-instance source,
aoa-sdk assignment source, aoa-models realization source, abyss-stack runtime
source, and aoa-agents actor/obligation source must each publish their own
typed refs before a current Goal-scoped relation can be admitted. Dashboard
composition remains a downstream read-only consumer.

## Verification

Verification routes through the participant-relation builder/reader/validator,
negative publication fixtures, focused tests, decision-index parity,
`scripts/validate_agents.py`, and the repository release gate.
