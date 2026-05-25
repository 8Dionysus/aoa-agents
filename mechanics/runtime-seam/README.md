# Runtime Seam Mechanic

Status: skeleton.

`mechanics/runtime-seam/` routes role-to-runtime contract pressure without
owning runtime implementation. It covers role x tier bindings, public loop
steps, runtime artifact examples, and transition discipline.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent-layer runtime seam operation package |
| input | runtime seam binding, artifact transition, tier, registry, and runtime-facing contract pressure |
| output | bounded role x tier binding, generated runtime seam registry, artifact contract route, or runtime-owner handoff |
| owner | this package for seam routing; `agents/runtime_seam/` for source bindings |
| next route | `PARTS.md`, `agents/runtime_seam/AGENTS.md`, runtime seam builders |
| validation | runtime seam registry checks plus repo validators |

## Agent Layer Owns

- route, plan, do, verify, deep, distill, and transition role bindings
- generated runtime seam registry as a derived reader
- runtime artifact contract examples and transition posture

## Stronger Owner Split

- Runtime implementation belongs to runtime owners, usually `abyss-stack`.
- Proof verdicts belong to `aoa-evals`.
- Live orchestration policy does not live in this package.

## Validation

```bash
python scripts/build_published_surfaces.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```
