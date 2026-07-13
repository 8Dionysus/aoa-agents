# 2026-05-26: Experience Adoption Boundary Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0035
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, assistant civil
- Mechanic parents: experience, agon
- Guard families: part-local artifact, validation guard
- Posture: accepted

## Context

Wave III adoption, office, Agon retention, and Boundary Bridge contract
payloads already live under their owning mechanic parts. Their dedicated
validator and focused test still lived in root `scripts/` and `tests/`.

The validator spans several parts and cross-routes into Agon and Boundary
Bridge, but the operation pressure originated in the Experience adoption and
regression wave. Sibling mechanics layouts keep executable checks beside the
mechanic or part they protect instead of leaving mechanic-owned checks in root.

## Decision

Move the adoption/boundary validator and focused test into the Experience
package:

- `mechanics/experience/scripts/validate_adoption_boundary_contracts.py`
- `mechanics/experience/tests/test_adoption_boundary_seed_contracts.py`

Keep the check package-level rather than part-local because it validates
Experience adoption/office parts together with Agon adoption-retention and
Boundary Bridge consumer/federation parts.

`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
package-local validator directly. `scripts/release_check.py` already runs
Experience package tests explicitly.

## Consequences

Adoption/boundary check edits now start in the Experience package. Boundary
Bridge and Agon route cards may point to this validator as a consumer of their
part-local contracts, but they do not become the active owner of the Wave III
Experience check.

Old root script and test paths are provenance facts only and are checked for
absence by the package-local validator.

## Validation

Verification routes through the focused owner checks and the repository release gate.
