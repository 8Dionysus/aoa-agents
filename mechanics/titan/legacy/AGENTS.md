# AGENTS.md

## Applies To

This card applies to `mechanics/titan/legacy/`.

## Role

`legacy/` preserves Titan source lineage and old-route accounting.

## Boundaries

- Do not make legacy the first route for current Titan behavior.
- Do not create placeholder raw receipts.
- Keep runtime, proof, and durable memory authority outside this package.

## Validation
Use the repository [validation map](../../../VALIDATION.md) and the nearest owner check when this route is relevant.

Use the repository validation map plus parent mechanic validators when legacy
meaning changes.
