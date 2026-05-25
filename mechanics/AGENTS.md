# AGENTS.md

## Applies To

This card applies to `mechanics/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Role

`mechanics/` is the operation atlas for repeatable agent-layer mechanics.
It routes recurring pressure around formation, projection, runtime-seam
binding, checkpoint posture, Titan role-bearing surfaces, quest-facing posture,
release support, and consumer handoff without turning those operations into
runtime implementation or proof authority.

## Operating Card

| Field | Route |
| --- | --- |
| role | operation atlas for repeatable agent-layer mechanics |
| input | recurring operation pressure, artifact movement pressure, package-boundary changes, validation-route changes |
| output | operation route, package-growth decision, source-owner route, validator update, or stronger-owner handoff |
| owner | `mechanics/README.md` for atlas shape; future `mechanics/<slug>/AGENTS.md` for package law |
| next route | `mechanics/ARTIFACT_TOPOLOGY.md`, target source family under `agents/`, owning docs, decision record |
| tools | semantic AGENTS validator, nested AGENTS validator, source builders when payloads move |
| validation | this card's `Validation` section plus package-specific checks when packages exist |

## Route Stack

- Above: root `AGENTS.md` owns repo identity, boundaries, and verification.
- Here: `mechanics/README.md` owns the active mechanics atlas.
- Design: `DESIGN.md` owns the repository topology split between source
  objects, operation mechanics, docs, schemas, examples, generated surfaces,
  and config.
- Decisions: `docs/decisions/` owns why structural districts exist.

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `mechanics/README.md`
5. `mechanics/ARTIFACT_TOPOLOGY.md` before moving docs, schemas, examples,
   scripts, tests, or generated companions into a mechanic
6. `docs/decisions/` before changing active mechanics topology
7. the source family under `agents/` or `docs/` that the mechanic routes

## Route Instead

| Pressure | Do this |
| --- | --- |
| source role object change | route to `agents/` |
| public explanation change | route to `docs/` and link back to the mechanic |
| shared schema/example change | keep `schemas/` or `examples/` until package-local validation exists |
| generated drift | update source and builder, then regenerate |
| proof, memo, route, playbook, skill, runtime, or infra authority | hand off to the owning repository |

## Compact Rules

- Mechanics name repeatable operations; they are not topic buckets.
- Source role objects stay in `agents/`.
- Shared schemas stay in `schemas/` until a mechanic-specific contract and
  validator make a narrower package-local home real.
- Public explanation can stay in `docs/` while this atlas is still the active
  route owner for operation topology.
- Generated companions stay weaker than builders and source surfaces.
- Runtime autonomy, proof verdicts, durable memory truth, routing policy,
  playbook choreography, and infrastructure implementation route to their
  owning repositories.

## Package Growth Rule

A new child mechanic should appear only when it has:

- a repeatable operation, not only a theme
- source surfaces and payload classes
- owner split and stop-lines
- validation route
- a decision or explicit route note when it changes repository topology

## Validation

For root mechanics route changes, run:

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

If the change also moves source objects or generated companions, add the owning
builder checks named by the affected `agents/**/AGENTS.md` card.
