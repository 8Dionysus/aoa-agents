# 2026-05-26: Checkpoint Contract Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0021
- Original date: 2026-05-26
- Surface classes: mechanic part, schema/contract, validation guard
- Agent facets: mechanics atlas, checkpoint/self-agent
- Mechanic parents: checkpoint
- Guard families: part-local artifact, schema validation, validation guard
- Posture: accepted

## Context

The Checkpoint mechanic already had separate `self-agent-checkpoint` and
`continuity-lane` parts, but their public schemas and examples still shared
root `schemas/` and `examples/` routes.

The payloads are not general shared schemas. They define bounded self-agent
checkpoint posture and adjacent self-agency continuity-window posture at the
agent layer.

## Decision

Move the self-agent checkpoint schema, example, and invalid fixtures into
`mechanics/checkpoint/parts/self-agent-checkpoint/{schemas,examples}/`.

Move the self-agency continuity-window schema and example into
`mechanics/checkpoint/parts/continuity-lane/{schemas,examples}/`.

Use part-local slug-style example and fixture names while keeping stable schema
`$id` values unchanged because they are public contract identifiers, not active
repository path authority.

Protect the contract set with a dedicated validator loaded by
`scripts/validate_agents.py` so the active file set, schema validity,
examples, invalid fixtures, and former root-route absence are checked
explicitly. The validator now lives under the owning checkpoint package script
route because it spans both `self-agent-checkpoint` and `continuity-lane`.

Preserve former root lookup only through Checkpoint `PROVENANCE.md` and
`legacy/`.

## Consequences

- The `self-agent-checkpoint` part now owns the governed checkpoint contract
  schema, example, and invalid fixtures.
- The `continuity-lane` part now owns the continuity-window schema and example.
- Root `schemas/` and `examples/` remain active for shared or not-yet-localized
  contracts.
- Existing schema `$id` values remain stable for consumers.
- Old root checkpoint routes remain historical lookup facts only.

## Verification

Verification routes through the focused owner checks and the repository release gate.
