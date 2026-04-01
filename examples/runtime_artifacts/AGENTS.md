# examples/runtime_artifacts/AGENTS.md

## Purpose

`examples/runtime_artifacts/` contains inspectable examples for the public runtime artifact contracts.
Each `*.example.json` should align with the corresponding `schemas/artifact.*.schema.json` surface and with `generated/runtime_seam_bindings.json`.

## Invalid fixtures

`invalid/` exists for negative coverage and must stay intentionally invalid.

## Editing posture

Keep examples phase-correct, minimal, and portable.
Do not add tool wiring, transport envelopes, runtime logs, or vendor-specific fields.
Keep coverage aligned with `docs/RUNTIME_ARTIFACT_TRANSITIONS.md` and `docs/AGENT_RUNTIME_SEAM.md`.

## Validation

Run `python -m pip install -r requirements-dev.txt`, then `python scripts/validate_agents.py`.
