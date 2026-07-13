# 2026-05-26: Recurrence Component Manifest Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0005
- Original date: 2026-05-26
- Surface classes: mechanic part, generated/readout, config/source
- Agent facets: mechanics atlas, recurrence
- Mechanic parents: recurrence, agon
- Guard families: part-local artifact, generated/read-model, source topology
- Posture: accepted

## Context

The remaining root `manifests/` files were not generic repository manifests.
They were recurrence component and hook declarations for Agon, recursor, and
Codex projection surfaces. The recurrence package already had a
`component-manifests` part, but the active JSON payloads still lived under
the former root recurrence manifest district.

That shape left the component manifest operation split across a root district
and an empty part, and the manifest set had no dedicated validator. It also
preserved old filename shapes such as `component.*.json` as active paths.

## Decision

Move recurrence component and hook manifests into:

```text
mechanics/recurrence/parts/component-manifests/manifests/
```

Use active semantic file names under `components/` and `hooks/`. Keep former
root manifest paths only as lookup facts in recurrence `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.

Add a validator and wire it into `scripts/validate_agents.py` so the manifest
set has an explicit validation route. A later check-localization slice moved
that validator into
`mechanics/recurrence/parts/component-manifests/scripts/` and moved the
focused manifest tests beside the part.

## Consequences

- Root `manifests/` is no longer the active recurrence component manifest
  district.
- The `component-manifests` part now owns component and hook declaration
  routing.
- The validator checks the expected file set, hook-to-component pairing, stale
  root path references, proof command script references, and local path/glob
  reachability.
- The `component-manifests` part owns its manifest payloads, focused validator,
  and focused tests.
- Shared schemas, examples, scripts, tests, generated readers, quest files, and
  agent source objects remain in their current districts until their own move
  proof exists.

## Verification

Verification routes through the focused owner checks and the repository release gate.
