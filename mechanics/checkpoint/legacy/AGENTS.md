# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/legacy/`.

## Role

`legacy/` preserves Checkpoint source lineage and old-route accounting.

## Boundaries

- Do not make legacy the first route for current checkpoint behavior.
- Do not create placeholder raw receipts.
- Keep durable memory and proof authority outside this package.

## Validation
Use the repository [validation map](../../../VALIDATION.md) and the nearest owner check when this route is relevant.

Use the repository validation map plus parent mechanic validators when legacy
meaning changes.
