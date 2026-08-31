# AGENTS.md

## Applies To

This card applies to `mechanics/runtime-seam/legacy/`.

## Role

`legacy/` preserves Runtime Seam source lineage and old-route accounting.

## Boundaries

- Do not make legacy the first route for current runtime seam behavior.
- Do not create placeholder raw receipts.
- Keep runtime implementation outside this package.

## Validation
Use the repository [validation map](../../../VALIDATION.md) and the nearest owner check when this route is relevant.

Use the repository validation map plus parent mechanic validators when legacy
meaning changes.
