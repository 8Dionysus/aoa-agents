# 2026-05-26: Experience Agent Service Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0037
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, assistant civil
- Mechanic parents: experience
- Guard families: part-local artifact, validation guard
- Posture: accepted

## Context

Agent service schemas and examples already live under Experience part-local
routes, with two cross-routed contract homes in Runtime Seam and Release
Support. The dedicated validator and focused test still lived in root
`scripts/` and `tests/`.

The validator is broader than one Experience part, but the operation pressure
is still Experience-owned: assistant service, office operations, release holds,
watch, rollback, governance, and arena-exclusion contract behavior.

## Decision

Move the agent service validator and focused test into the Experience package:

- `mechanics/experience/scripts/validate_agent_service_contracts.py`
- `mechanics/experience/tests/test_agent_service_contracts.py`

Keep the check package-level rather than part-local because it validates
several Experience parts and reads Runtime Seam plus Release Support
contract routes.

`scripts/validate_agents.py` remains the repo-wide coordinator and loads the
package-local validator directly. `scripts/release_check.py` already runs
Experience package tests explicitly.

## Consequences

Agent service check edits now start in the Experience package. Runtime Seam
and Release Support route cards may point to this validator as a consumer of
their part-local contracts, but they do not become the active owner of the
assistant service check.

Old root script and test paths are provenance facts only and are checked for
absence by the package-local validator.

## Validation

Verification routes through the focused owner checks and the repository release gate.
