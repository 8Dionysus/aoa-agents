# 2026-05-26: Active Legacy Name Cleanup

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0050
- Original date: 2026-05-26
- Surface classes: legacy/provenance, mechanic package
- Agent facets: mechanics atlas
- Mechanic parents: agon
- Guard families: legacy/provenance
- Posture: accepted

## Context

The mechanics localization left several active route files named after older
root-stage slices such as `wave*`, `current_direction`, `roadmap_parity`,
`downstream_feed`, and validator-test mirrors. Those names made active
surfaces read like migration batches instead of the operation map now owned by
`mechanics/` and `agents/`.

## Decision

Rename active tests and landing docs to operation names:

- agonic actor rechartering
- assistant civil rechartering
- formation trial
- rank jurisdiction
- epistemic actor posture
- school campaign posture
- A2A summon return role posture hold
- root entrypoint routes, published consumer feeds, roadmap surface alignment,
  repo validator, and semantic route validator

Add `tests/test_active_legacy_name_noise.py` so future route work catches
legacy-name regressions in active paths. The guard intentionally excludes
`legacy/`, local memo candidates, captured quest history, and provenance or
decision records where old names are evidence rather than active route names.

## Consequences

Active route names now follow the mechanics topology instead of old landing
batch names. Former-root names remain searchable in legacy/provenance/history
surfaces, but they no longer define the active path layout.
