# runtime_seam/AGENTS.md

## Purpose

`runtime_seam/` is the source-authored role x tier binding surface for the public agent runtime seam.
It keeps phase, tier, role, and artifact contracts explicit without moving runtime implementation into `aoa-agents`.

## Source of truth

Canonical authoring lives in:

- `runtime_seam/*.binding.json`
- `schemas/runtime-seam-binding.schema.json`

Published derived surface:

- `generated/runtime_seam_bindings.json`

Read with:

- `docs/AGENT_RUNTIME_SEAM.md`
- `docs/RUNTIME_ARTIFACT_TRANSITIONS.md`

## Contract to preserve

Keep the public loop explicit and small:

`route -> plan -> do -> verify -> deep? -> distill`

Each binding should keep these fields coherent:

- `phase`
- `tier_id`
- `role_names`
- `artifact_type`

Bindings must stay aligned with published artifact schemas and with `examples/runtime_artifacts/`.

## Does not own

Do not encode here:

- routing logic
- playbook meaning
- memory-object canon
- eval doctrine
- network protocol commitments
- runtime infrastructure implementation

## Editing posture

Treat changes to phase coverage, tier assignment, role binding, or artifact type as public contract changes for neighboring consumers.
Keep the seam small, inspectable, and contract-first.

## Validation

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```
