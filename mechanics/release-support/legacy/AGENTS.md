# AGENTS.md

## Applies To

This card applies to `mechanics/release-support/legacy/`.

## Role

`legacy/` preserves Release Support source lineage and old-route accounting.

## Read Before Editing

Read `../PROVENANCE.md`, then `README.md`, `INDEX.md`, and
`DISTILLATION_LOG.md`.

## Boundaries

- Do not make legacy the first route for current release support.
- Do not create placeholder raw receipts.
- Keep CI, GitHub, and deployment authority outside this package.

## Validation

Run `git diff --check` plus parent mechanic validators when legacy meaning
changes.
