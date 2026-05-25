# AGENTS.md

## Applies To

This card applies to `mechanics/boundary-bridge/legacy/`.

## Role

`legacy/` preserves Boundary Bridge source lineage and old-route accounting.

## Read Before Editing

Read `../PROVENANCE.md`, then `README.md`, `INDEX.md`, and
`DISTILLATION_LOG.md`.

## Boundaries

- Do not make legacy the first route for current boundary behavior.
- Do not create placeholder raw receipts.
- Keep routing policy, runtime, public-entry, and memory authority outside this package.

## Validation

Run `git diff --check` plus parent mechanic validators when legacy meaning
changes.
