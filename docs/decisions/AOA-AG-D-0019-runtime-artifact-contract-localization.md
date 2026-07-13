# 2026-05-26: Runtime Artifact Contract Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0019
- Original date: 2026-05-26
- Surface classes: mechanic part, schema/contract
- Agent facets: mechanics atlas, runtime seam
- Mechanic parents: runtime-seam
- Guard families: part-local artifact, schema validation, runtime seam
- Posture: accepted

## Context

The Runtime Seam mechanic already had an `artifact-contracts` part, but the
runtime artifact schemas and their public example fixtures still lived under
root `schemas/` and `examples/`.

Those payloads are not general shared schemas. They describe the agent-layer
runtime artifact loop and transition governance that `runtime-seam` keeps
explicit without owning runtime implementation.

## Decision

Move the runtime artifact schemas, examples, and invalid fixtures into
`mechanics/runtime-seam/parts/artifact-contracts/{schemas,examples}/`.
Keep stable schema `$id` values unchanged because they are public contract
identifiers, not active repository path authority.

Protect the contract set with a dedicated validator loaded by
`scripts/validate_agents.py` so the active part-local file set, schema
validity, examples, invalid fixtures, and former root-route absence are checked
explicitly. The validator now lives under the owning part-local script route.

Keep optional consumer smoke checks compatible with historical artifact-schema
repo refs by resolving those refs to the new part-local schemas.

Preserve former root lookup only through Runtime Seam `PROVENANCE.md` and
`legacy/`.

## Consequences

- The `artifact-contracts` part now owns the runtime artifact schemas,
  examples, and invalid fixtures.
- Root `schemas/` and `examples/` remain active for shared or not-yet-localized
  contracts.
- Existing schema `$id` values remain stable for consumers.
- Existing external repo refs to the former artifact-schema route can still
  resolve during smoke checks.
- Old root runtime artifact routes remain historical lookup facts only.

## Verification

Verification routes through the focused owner checks and the repository release gate.
