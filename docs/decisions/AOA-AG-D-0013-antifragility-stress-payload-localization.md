# 2026-05-26: Antifragility Stress Payload Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0013
- Original date: 2026-05-26
- Surface classes: mechanic part, example/source
- Agent facets: mechanics atlas, stress posture
- Mechanic parents: antifragility, checkpoint
- Guard families: part-local artifact, example validation
- Posture: accepted

## Context

Antifragility stress docs already live under
`mechanics/antifragility/parts/stress-posture/`, but their schema-backed public
adjuncts still lived in root `schemas/` and `examples/`. That kept a named
repeatable operation split between active part docs and root support payloads.

The two schemas and two examples are not shared profile, model-tier,
checkpoint, runtime-artifact, or reference-route contracts. They describe the
stress-posture part's own role narrowing bands and bounded handoff envelope.

## Decision

Move stress-posture schemas and examples into
`mechanics/antifragility/parts/stress-posture/{schemas,examples}/` using
part-local names. Keep stable schema `$id` values unchanged because they are
public contract identifiers, not active repository path authority.

Add a stress-posture validator and wire the same file-set, schema, example,
and old-route checks into `scripts/validate_agents.py`.

Preserve former root lookup only through antifragility `PROVENANCE.md` and
`legacy/`.

## Consequences

- The `stress-posture` part now co-locates docs, schemas, and examples.
- Root `schemas/` and `examples/` remain active for shared or not-yet-localized
  contracts.
- Existing schema `$id` values remain stable for consumers.
- Old root stress payload names remain historical lookup facts only.

## Verification

Verification routes through the focused owner checks and the repository release gate.
