# 2026-05-26: Adoption And Boundary Contract Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0034
- Original date: 2026-05-26
- Surface classes: mechanic part, schema/contract
- Agent facets: mechanics atlas, assistant civil
- Mechanic parents: experience, agon, boundary-bridge
- Guard families: part-local artifact, schema validation
- Posture: accepted

## Context

Adoption, retention, office, and boundary bridge contract families already had
active mechanic docs under Experience, Agon, and Boundary Bridge parts, but
their schemas and public examples still lived in root `schemas/` and
`examples/`.

Keeping these contracts in root made adoption look like one shared blob even
though the operation pressure splits across assistant service adoption, Agon
retention/scar handling, office compatibility, and cross-repo consumer seams.

## Decision

Move these schema/example pairs into their owning part-local contract routes:

- Experience adoption and regression contracts under
  `mechanics/experience/parts/adoption-and-regression/`
- Experience office adoption contracts under
  `mechanics/experience/parts/office-operations/`
- Agon adoption/retention contracts under
  `mechanics/agon/parts/adoption-retention/`
- Boundary Bridge consumer and federation contracts under
  `mechanics/boundary-bridge/parts/consumer-handoff/` and
  `mechanics/boundary-bridge/parts/federation-consumer-seams/`

Add an adoption/boundary validator to keep the active file sets,
schema/example alignment, guardrail invariants, and former root path absence
explicit. Its active route is now
`mechanics/experience/scripts/validate_adoption_boundary_contracts.py`; the
check was localized after the contract payload move.

## Consequences

Root `schemas/` and `examples/` no longer act as the active homes for this
adoption/boundary family. Former root path lookup is preserved through the
target package `PROVENANCE.md` and `legacy/` maps.

Stable schema `$id`, `kind`, and `schema_id`/`schema_version` values remain
public contract identifiers. They are not active repo paths and are not
rewritten in this localization pass.

Validation for this route is:

```bash
python mechanics/experience/scripts/validate_adoption_boundary_contracts.py
python scripts/validate_agents.py
```
