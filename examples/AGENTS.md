# examples/AGENTS.md

## Purpose

`examples/` contains public-safe, schema-backed examples for inspectable agent-layer contracts.
These files illustrate published contracts. They are not the source-authored canon layer.

## Subtrees

- `agent_agonic_formation.example.json` for the additive Wave I reader path
  across base role contract plus agonic companion surfaces
- `assistant_civil_formation.example.json` for the additive Wave II reader path
  across base role contract plus assistant civil companion surfaces
- `runtime_artifacts/` for public-loop artifact examples and negative fixtures
- `self_agent_checkpoint/` for governed self-agent checkpoint examples and negative fixtures
- `reference_routes/` for manifest-driven reference route packs over the published public loop
- `alpha_reference_routes/` for curated Alpha cohort reference-route surfaces used by the readiness proof lane

## Editing posture

Keep examples minimal, portable, and public-safe.
Do not invent new contract keys ahead of schema or runtime-seam changes.
Do not store real run history, secrets, or hidden transport assumptions.
Do not turn examples into live authority for arena seats, protocol packets, or
runtime state.

## Validation

Run `python -m pip install -r requirements-dev.txt` first. Then `python scripts/validate_agents.py` validates example alignment and negative fixtures.
For the Wave I reader path example, also run `python scripts/validate_agent_agonic_formation.py`.
For the Wave II reader path example, also run `python scripts/validate_assistant_civil_formation.py`.
