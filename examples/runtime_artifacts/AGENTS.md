# examples/runtime_artifacts/AGENTS.md

## Purpose

`examples/runtime_artifacts/` contains inspectable examples for the public runtime artifact contracts.
Each `*.example.json` should align with the corresponding `schemas/artifact.*.schema.json` surface and with `generated/runtime_seam_bindings.json`.

## Invalid fixtures

`invalid/` exists for negative coverage and must stay intentionally invalid.

## Editing posture

Keep examples phase-correct, minimal, and portable.
Do not add tool wiring, transport envelopes, runtime logs, or vendor-specific fields.
Keep coverage aligned with `mechanics/runtime-seam/parts/transition-discipline/docs/runtime-artifact-transitions.md` and `mechanics/runtime-seam/parts/role-tier-bindings/docs/agent-runtime-seam.md`.

## Validation

Run `python -m pip install -r requirements-dev.txt`, then `python scripts/validate_agents.py`.
