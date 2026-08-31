# AGENTS.md

## Applies To

This card applies to `mechanics/boundary-bridge/legacy/`.

## Role

`legacy/` preserves Boundary Bridge source lineage and old-route accounting.

## Boundaries

- Do not make legacy the first route for current boundary behavior.
- Do not create placeholder raw receipts.
- Keep routing policy, runtime, public-entry, and memory authority outside this package.

## Validation
Use the repository [validation map](../../../VALIDATION.md) and the nearest owner check when this route is relevant.

Use the repository validation map plus parent mechanic validators when legacy
meaning changes.
