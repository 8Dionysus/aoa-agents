# AGENTS.md

## Applies To

This card applies to `mechanics/runtime-seam/parts/`.

## Role

`parts/` is the lower active route for runtime seam part selection.

## Boundaries

- Do not turn role-to-runtime contracts into runtime implementation.
- Proof verdicts and live orchestration policy route away.
- Provenance accounting is not current behavior.

## Validation
Use the repository [validation map](../../../VALIDATION.md) and the nearest owner check when this route is relevant.

Use the package validation route in `../AGENTS.md`, plus root validators.
