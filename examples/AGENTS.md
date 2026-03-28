# examples/AGENTS.md

## Purpose

`examples/` contains public-safe, schema-backed examples for inspectable agent-layer contracts.
These files illustrate published contracts. They are not the source-authored canon layer.

## Subtrees

- `runtime_artifacts/` for public-loop artifact examples and negative fixtures
- `self_agent_checkpoint/` for governed self-agent checkpoint examples and negative fixtures
- `reference_routes/` for manifest-driven reference route packs over the published public loop

## Editing posture

Keep examples minimal, portable, and public-safe.
Do not invent new contract keys ahead of schema or runtime-seam changes.
Do not store real run history, secrets, or hidden transport assumptions.

## Validation

`python scripts/validate_agents.py` validates example alignment and negative fixtures.
