# 2026-05-26: Alpha Reference-Route Generated Reader Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0039
- Original date: 2026-05-26
- Surface classes: mechanic part, generated/readout
- Agent facets: mechanics atlas, quest/alpha
- Mechanic parents: questbook
- Guard families: part-local artifact, generated/read-model, quest dispatch
- Posture: accepted

## Context

The reference-route contract localization moved the Alpha curated
reference-route schema and examples into
`mechanics/questbook/parts/alpha-reference-routes/`.

One derived reader still remained in root `generated/` even though it was built
only from those part-local Alpha examples. Keeping that reader at the root made
the repository imply that it was a repo-wide generated registry rather than a
Questbook companion view.

## Decision

Move the Alpha reference-route generated reader to:

```text
mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json
```

Teach
`mechanics/questbook/parts/alpha-reference-routes/scripts/generate_alpha_reference_routes.py`,
`mechanics/questbook/scripts/validate_alpha_reference_routes.py`, and
`scripts/validate_agents.py` the part-local route, and keep the former root path
absent through validation.

## Consequences

Root `generated/` continues to own repo-level registries, formation indexes,
quest catalog/dispatch readers, and Codex projections. The Alpha reader is
part-local because its only source truth is the Questbook Alpha example set.

Questbook `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md` now preserve the old-path lookup. Active docs
should reference the part-local path.

## Validation

Verification routes through the focused owner checks and the repository release gate.
