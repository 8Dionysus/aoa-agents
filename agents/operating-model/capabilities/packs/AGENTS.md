# agents/operating-model/capabilities/packs/AGENTS.md

## Purpose

`packs/` contains source-authored capability pack records.

Each `*.capability.json` file is an operating bundle: permission posture,
tool refs, skill refs, technique refs, memory routes, proof routes, projection
hints, owner boundaries, and stop lines.

## Editing posture

The filename stem must match `id`.

Keep each pack reusable across specializations when possible. If a capability
only makes sense for one role specialization, it may still live here, but its
owner boundaries must say why the pack does not own implementation.

Do not turn a pack into a workflow body. Route workflow implementation to
`aoa-skills`, proof doctrine to `aoa-evals`, memory truth to `aoa-memo`,
routing policy to `aoa-routing`, and runtime behavior to `abyss-stack`.

## Validation

Run:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```
