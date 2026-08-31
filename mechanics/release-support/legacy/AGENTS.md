# AGENTS.md

## Applies To

This card applies to `mechanics/release-support/legacy/`.

## Role

`legacy/` preserves Release Support source lineage and old-route accounting.

## Boundaries

- Do not make legacy the first route for current release support.
- Do not create placeholder raw receipts.
- Keep CI, GitHub, and deployment authority outside this package.

## Validation
Use the repository [validation map](../../../VALIDATION.md) and the nearest owner check when this route is relevant.

Use the repository validation map plus parent mechanic validators when legacy
meaning changes.
