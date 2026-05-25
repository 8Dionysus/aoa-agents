# AGENTS.md

## Applies To

This card applies to `agents/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Role

`agents/` is the source-authored agent district for `aoa-agents`.
It holds the repo-owned role objects and compact role-facing contract inputs
that publish into generated registries and projection surfaces.

It is not the workspace `.agents/` install/export lane. `.agents/` carries
operator-facing skill exports and agent-facing installs; `agents/` carries
agent-layer source meaning.

## Operating Card

| Field | Route |
| --- | --- |
| role | source-authored agent object district |
| input | role, tier, class, cohort, adjunct, and runtime-seam source edits |
| output | updated source object, regenerated reader, validation result, or stronger-owner handoff |
| owner | nearest `agents/<family>/AGENTS.md` and source JSON family |
| next route | `agents/README.md`, target family `AGENTS.md`, owning docs, builder, validator |
| tools | `scripts/build_published_surfaces.py`, formation builders, projection builders |
| validation | this card's `Validation` section plus target family checks |

## Route Stack

- Above: root `AGENTS.md` owns repo identity, boundaries, and verification.
- Here: `agents/README.md` owns the source district map.
- Below: `agents/profiles/`, `agents/model_tiers/`,
  `agents/orchestrator_classes/`, `agents/cohort_patterns/`, and
  `agents/runtime_seam/` own local contracts and checks.

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `agents/README.md`
5. the nearest child `AGENTS.md`
6. the docs named by the child route card

## Owner Routes

| Need | Owner route |
| --- | --- |
| base role contracts | `agents/profiles/*.profile.json` |
| agonic and assistant adjuncts | `agents/profiles/adjuncts/` |
| tier-shaped execution posture | `agents/model_tiers/*.tier.json` |
| orchestrator class identity | `agents/orchestrator_classes/*.class.json` |
| bounded role cohort hints | `agents/cohort_patterns/*.pattern.json` |
| role x tier runtime seam bindings | `agents/runtime_seam/*.binding.json` |
| generated readers | `generated/` and the owning builder |
| operation topology | `mechanics/` |
| role doctrine and public explanation | `docs/` |

## Route Instead

| Pressure | Do this |
| --- | --- |
| schema shape changes | edit `schemas/` and run the owning validator |
| example fixture changes | edit `examples/` and run schema/example validation |
| generated reader drift | edit source input, run the builder, then validate |
| repeated operation pressure | route to `mechanics/` |
| skill, proof, memo, route, playbook, or runtime ownership | hand off to the owning repository |

## Compact Rules

- Keep source objects compact and reviewable.
- Keep schemas under `schemas/` until a later package-local artifact move has a
  mechanic owner and validator support.
- Keep examples under `examples/` until a later package-local artifact move has
  a mechanic owner and validator support.
- Do not turn role objects into skill workflows, proof verdicts, durable memory
  truth, routing policy, playbook scenarios, or runtime implementation.
- Do not hand-edit generated readers as if they were source truth.

## Validation

For source-object edits, run:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
```

If adjunct formation surfaces changed, also run the Wave I/II/II.5 builders and
validators named in `agents/profiles/AGENTS.md`.
