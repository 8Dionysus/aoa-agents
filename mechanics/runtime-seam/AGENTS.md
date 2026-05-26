# AGENTS.md

## Applies To

This card applies to `mechanics/runtime-seam/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/runtime-seam/` routes role-to-runtime contract pressure without
owning runtime implementation. It covers role x tier bindings, public loop
steps, runtime artifact contracts, and transition discipline.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent-layer runtime seam operation package |
| input | runtime seam binding, artifact transition, tier, registry, and runtime-facing contract pressure |
| output | bounded role x tier binding, generated runtime seam registry, artifact contract route, or runtime-owner handoff |
| owner | this package for seam routing; `agents/runtime_seam/` owns source bindings |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, `agents/runtime_seam/AGENTS.md`, runtime seam builders |
| tools | published surface builder, runtime artifact validator, repo validators |
| validation | runtime seam registry checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `agents/runtime_seam/AGENTS.md` when source bindings change
8. `PROVENANCE.md` before using `legacy/`

## Boundaries

- Runtime implementation belongs to runtime owners, usually `abyss-stack`.
- Proof verdicts belong to `aoa-evals`.
- Live orchestration policy does not live in this package.
- Generated runtime seam registries are derived readers.

## Validation

```bash
python scripts/validate_runtime_artifact_contracts.py
python scripts/build_published_surfaces.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed runtime-seam part, source binding or artifact contract
affected, generated readers rebuilt or untouched, checks run, and any runtime
owner handoff.
