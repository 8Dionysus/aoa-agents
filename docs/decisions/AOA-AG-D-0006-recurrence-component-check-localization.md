# 2026-05-26: Recurrence Component Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0006
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, recurrence
- Mechanic parents: recurrence
- Guard families: part-local artifact, validation guard
- Posture: accepted

## Context

The recurrence component and hook manifests already lived in
`mechanics/recurrence/parts/component-manifests/manifests/`, but their focused
validator still lived in root `scripts/` and the focused tests still lived in
root `tests/` as pytest-style functions.

That kept the component manifest payloads part-local while the check surface
remained root-level and outside the explicit `release_check.py` part-local test
route.

## Decision

Move the validator to
`mechanics/recurrence/parts/component-manifests/scripts/` and move the focused
tests to `mechanics/recurrence/parts/component-manifests/tests/`.

Keep `scripts/validate_agents.py` as the repo-wide coordinator by loading the
part-local validator explicitly. Add the part-local manifest tests to
`scripts/release_check.py`.

## Consequences

- The `component-manifests` part owns the manifests, focused validator, and
  focused tests.
- Root `scripts/` keeps only repo-level coordination for this contract.
- Root `tests/` keeps broader repo tests; manifest-specific tests now run in
  the part-local release route.
- Former root paths remain discoverable only through `PROVENANCE.md` and
  `legacy/`.

## Verification

Verification routes through the focused owner checks and the repository release gate.
