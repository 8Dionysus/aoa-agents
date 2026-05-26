# AGENTS.md

## Applies To

This card applies to `agents/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Role

`agents/` is the source-authored agent home for `aoa-agents`.
It holds the repo-owned role objects and compact role-facing contract inputs
that publish into generated registries and projection surfaces.

It is not the workspace `.agents/` install/export lane. `.agents/` carries
operator-facing skill exports and agent-facing installs; `agents/` carries
agent-layer source meaning.

## Operating Card

| Field | Route |
| --- | --- |
| role | source-authored agent object home |
| input | role, tier, class, cohort, adjunct, and runtime-seam source edits |
| output | updated source object, source-home manifest route, regenerated reader, validation result, or stronger-owner handoff |
| owner | `agents/source_home.manifest.json`, nearest branch `AGENTS.md`, and source JSON family |
| next route | `agents/README.md`, `agents/source_home.manifest.json`, target branch `AGENTS.md`, owning docs, builder, validator |
| tools | `scripts/validate_agent_source_home.py`, `scripts/build_published_surfaces.py`, formation builders, projection builders |
| validation | this card's `Validation` section plus target family checks |

## Route Stack

- Above: root `AGENTS.md` owns repo identity, boundaries, and verification.
- Here: `agents/README.md` owns the source home map and
  `agents/source_home.manifest.json` owns the checked family topology.
- Below: `agents/roles/` owns role houses and their nested forms;
  `agents/operating-model/` owns cross-role tiers, orchestrators, cohorts, and
  runtime-seam bindings.

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `agents/README.md`
5. `agents/source_home.manifest.json`
6. the nearest child `AGENTS.md`
7. the docs named by the child route card

## Owner Routes

| Need | Owner route |
| --- | --- |
| base role contracts | `agents/roles/*/profile.json` |
| agonic and assistant adjuncts | `agents/roles/*/forms/` |
| tier-shaped execution posture | `agents/operating-model/tiers/*.tier.json` |
| orchestrator class identity | `agents/operating-model/orchestrators/*.class.json` |
| bounded role cohort hints | `agents/operating-model/cohorts/*.pattern.json` |
| role x tier runtime seam bindings | `agents/operating-model/runtime-seams/*.binding.json` |
| checked source-home topology | `agents/source_home.manifest.json` |
| generated readers | `generated/` and the owning builder |
| operation topology | `mechanics/` |
| role doctrine and public explanation | `docs/` |

## Route Instead

| Pressure | Do this |
| --- | --- |
| repo-wide schema shape changes | edit `schemas/` and run the owning validator |
| mechanic-specific schema shape changes | route to the owning `mechanics/*/parts/*/schemas/` directory |
| example fixture changes | edit `examples/` and run schema/example validation |
| generated reader drift | edit source input, run the builder, then validate |
| repeated operation pressure | route to `mechanics/` |
| skill, proof, memo, route, playbook, or runtime ownership | hand off to the owning repository |

## Compact Rules

- Keep source objects compact and reviewable.
- Keep the source home manifest aligned with every active family, owner card,
  schema or mechanic-local contract, publication target, builder, and validator.
- Keep repo-wide agent source and registry schemas under `schemas/`.
- Keep mechanic-specific schemas under the owning mechanic part once that part
  has a route card and validator support.
- Keep examples under `examples/` until a later package-local artifact move has
  a mechanic owner and validator support.
- Do not turn role objects into skill workflows, proof verdicts, durable memory
  truth, routing policy, playbook scenarios, or runtime implementation.
- Do not hand-edit generated readers as if they were source truth.

## Validation

For source-object edits, run:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agent_source_home.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
```

If adjunct formation surfaces changed, also run the agonic actor, assistant
civil, and formation-trial builders and validators named in
`agents/roles/AGENTS.md`.
