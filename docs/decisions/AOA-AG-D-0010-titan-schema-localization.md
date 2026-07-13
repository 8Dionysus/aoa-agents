# 2026-05-26: Titan Schema Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0010
- Original date: 2026-05-26
- Surface classes: mechanic part, schema/contract
- Agent facets: mechanics atlas, titan role-bearing
- Mechanic parents: titan, checkpoint
- Guard families: part-local artifact, schema validation
- Posture: accepted

## Context

Titan docs, config, and examples now live under `mechanics/titan/parts/`, but
Titan-specific schemas still lived in root `schemas/`. That left the active
contract surface split across root schema names and part-local examples.

These schemas are not shared agent-layer contracts like profiles, model tiers,
runtime artifacts, checkpoints, or reference routes. They describe Titan role
class, bearer identity, lineage, incarnation, roster, service-cohort, report,
and summon-boundary payloads.

## Decision

Move Titan-specific schemas into `mechanics/titan/parts/*/schemas/` using
part-local names. Keep stable `$id` values unchanged because they are public
contract identifiers, not active repository path authority.

Add a Titan schema validator and wire it into `scripts/validate_agents.py` so
the active file set, JSON Schema validity, and old active filename shape are
checked explicitly.

Preserve former root lookup only through Titan `PROVENANCE.md` and `legacy/`.

## Consequences

- Titan parts now co-locate docs, config where applicable, schemas, and
  examples.
- Root `schemas/` remains the home for shared non-Titan contracts.
- Existing schema `$id` values remain stable for consumers.
- Example validation now reads the part-local schemas.

## Verification

Verification routes through the focused owner checks and the repository release gate.
