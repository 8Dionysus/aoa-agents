# 2026-05-26: Agent Service Contract Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0036
- Original date: 2026-05-26
- Surface classes: mechanic part, schema/contract
- Agent facets: mechanics atlas, assistant civil
- Mechanic parents: experience, agon, release-support, runtime-seam
- Guard families: part-local artifact, schema validation
- Posture: accepted

## Context

The remaining root `schemas/` and `examples/` contract payloads were mostly
assistant service, office, release, watch, rollback, and governance contracts.
They already had active mechanic docs under Experience parts, while two
agent-level contracts had clearer neighboring owners: authority claims under
Runtime Seam and release holds under Release Support.

Keeping all of these payloads in root made `schemas/` and `examples/` look like
active mechanic homes even after the mechanics atlas and part maps had become
the operational route.

## Decision

Move the contract pairs into their owning part-local routes:

- Experience service, office, release, watch, rollback, governance, and
  assistant-to-Agon boundary contracts under
  `mechanics/experience/parts/*/{schemas,examples}/`
- the runtime-readable authority claim contract under
  `mechanics/runtime-seam/parts/artifact-contracts/{schemas,examples}/`
- the release-hold policy contract under
  `mechanics/release-support/parts/runtime-release-hold/{schemas,examples}/`

Add an agent service validator and route `scripts/validate_agents.py` through
it so former root paths stay absent and schema/example invariants remain
explicit. Its active route is now
`mechanics/experience/scripts/validate_agent_service_contracts.py`; the check
was localized after the contract payload move.

## Consequences

Root `schemas/` now holds shared registry/profile/reference contracts rather
than assistant service mechanics. At this slice boundary, root `examples/`
held reference-route examples rather than assistant service mechanic examples;
the later reference-route localization gives those examples their own
part-local route.

The move keeps stable schema `$id`, `kind`, and identifier values unchanged as
public contract identifiers. Former root lookup is preserved through each
target package `PROVENANCE.md` and `legacy/` maps.

Validation for this route is:

Verification routes through the focused owner checks and the repository release gate.
