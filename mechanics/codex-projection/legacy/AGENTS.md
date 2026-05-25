# AGENTS.md

## Applies To

This card applies to `mechanics/codex-projection/legacy/`.

## Role

`legacy/` preserves Codex Projection source lineage and old-route accounting.

## Read Before Editing

Read `../PROVENANCE.md`, then `README.md`, `INDEX.md`, and
`DISTILLATION_LOG.md`.

## Boundaries

- Do not make legacy the first route for current projection behavior.
- Do not create placeholder raw receipts.
- Keep Codex runtime and host configuration outside this package.

## Validation

Run `git diff --check` plus parent mechanic validators when legacy meaning
changes.
