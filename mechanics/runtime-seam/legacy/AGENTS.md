# AGENTS.md

## Applies To

This card applies to `mechanics/runtime-seam/legacy/`.

## Role

`legacy/` preserves Runtime Seam source lineage and old-route accounting.

## Read Before Editing

Read `../PROVENANCE.md`, then `README.md`, `INDEX.md`, and
`DISTILLATION_LOG.md`.

## Boundaries

- Do not make legacy the first route for current runtime seam behavior.
- Do not create placeholder raw receipts.
- Keep runtime implementation outside this package.

## Validation

Run `git diff --check` plus parent mechanic validators when legacy meaning
changes.
