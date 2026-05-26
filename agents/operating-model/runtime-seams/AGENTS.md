# agents/operating-model/runtime-seams/AGENTS.md

## Purpose

`agents/operating-model/runtime-seams/` is the source-authored role x tier binding surface for the public agent runtime seam.
It keeps phase, tier, role, and artifact contracts explicit without moving runtime implementation into `aoa-agents`.

## Source of truth

Canonical authoring lives in:

- `agents/operating-model/runtime-seams/*.binding.json`
- `schemas/runtime-seam-binding.schema.json`

Published derived surface:

- `generated/runtime_seam_bindings.json`

Read with:

- `mechanics/runtime-seam/parts/role-tier-bindings/docs/agent-runtime-seam.md`
- `mechanics/runtime-seam/parts/transition-discipline/docs/runtime-artifact-transitions.md`

## Contract to preserve

Keep the public loop explicit and small:

`route -> plan -> do -> verify -> deep? -> distill`

Each binding should keep these fields coherent:

- `phase`
- `tier_id`
- `role_names`
- `artifact_type`

Bindings must stay aligned with published artifact schemas and with
`mechanics/runtime-seam/parts/artifact-contracts/examples/`.

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
