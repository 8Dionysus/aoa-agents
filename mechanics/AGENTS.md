# AGENTS.md

## Applies To

This card applies to `mechanics/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Role

`mechanics/` is the operation atlas for repeatable agent-layer mechanics.
It routes recurring pressure around Agon formation, assistant experience,
Titan role-bearing, recurrence, Codex projection, runtime-seam binding,
checkpoint posture, questbook posture, progression, antifragility,
boundary-bridge handoff, and release support without turning those operations
into runtime implementation, proof authority, memory truth, or playbook
choreography.

## Operating Card

| Field | Route |
| --- | --- |
| role | operation atlas for repeatable agent-layer mechanics |
| input | recurring operation pressure, artifact movement pressure, package-boundary changes, validation-route changes |
| output | operation route, package-growth decision, source-owner route, validator update, or stronger-owner handoff |
| owner | `mechanics/README.md` for atlas shape; package `README.md` and `PARTS.md` for child package route law |
| next route | `mechanics/PAYLOAD_RECON.md`, `mechanics/ARTIFACT_TOPOLOGY.md`, target package `PARTS.md`, target source family under `agents/`, owning docs, decision record |
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
5. `mechanics/PAYLOAD_RECON.md` before deciding which mechanic a root payload
   belongs to
6. `mechanics/LEGACY_TOPOLOGY.md` before creating, editing, or using package
   `legacy/` surfaces
7. `mechanics/ARTIFACT_TOPOLOGY.md` before moving docs, schemas, examples,
   scripts, tests, or generated companions into a mechanic
8. target package `README.md`, `PARTS.md`, and `parts/README.md` when a nearer
   package exists
9. target package `PROVENANCE.md` before opening package `legacy/`
10. `docs/decisions/` before changing active mechanics topology
11. the source family under `agents/` or `docs/` that the mechanic routes

## Route Instead

| Pressure | Do this |
| --- | --- |
| source role object change | route to `agents/` |
| public explanation change | route to `docs/` and link back to the mechanic |
| shared schema/example change | keep `schemas/` or `examples/` until package-local validation exists; move mechanic-specific schemas or examples only with an explicit validator |
| generated drift | update source and builder, then regenerate |
| file-name cluster pressure | use `mechanics/PAYLOAD_RECON.md` and target `PARTS.md`; do not promote a topic into a mechanic by filename alone |
| old-path or provenance pressure | use target package `PROVENANCE.md`; legacy is an accounting route, not current behavior |
| proof, memo, route, playbook, skill, runtime, or infra authority | hand off to the owning repository |

## Compact Rules

- Mechanics name repeatable operations; they are not topic buckets.
- Source role objects stay in `agents/`.
- Shared schemas stay in `schemas/` until a mechanic-specific contract and
  validator make a narrower package-local home real.
- Mechanics-facing public docs live in part-local `mechanics/*/parts/*/docs/`
  once moved; root `docs/` keeps only broader docs-surface entrypoints and
  non-mechanic conceptual models.
- Mechanic-specific seeds, wiring, and recurrence component manifests live in
  part-local routes once moved; root-level districts keep only payloads that
  still have stronger shared ownership.
- Mechanic-specific public examples live in part-local
  `mechanics/*/parts/*/examples/` once a dedicated validator protects the
  active file set and schema alignment.
- Mechanic-specific schemas live in part-local
  `mechanics/*/parts/*/schemas/` once a dedicated validator protects the
  active file set and public identifier posture.
- Quest source records live in root `quests/`; `mechanics/questbook/` owns the
  source-store route, index route, and generated-reader contract.
- Quest catalog and dispatch readers remain root-published generated
  companions because they summarize root `quests/`.
- Generated companions stay weaker than builders and source surfaces.
- `legacy/` preserves lineage and path accounting; it is not the default route
  for current edits.
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

The current child packages own route maps, part maps, and migrated
mechanics-facing docs, config seeds, recurrence component manifests, and
questbook operation law. Other root-district payload classes move only after
their package-local contract and validation route are explicit.

## Validation

For root mechanics route changes, run:

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

If the change also moves source objects or generated companions, add the owning
builder checks named by the affected `agents/**/AGENTS.md` card.
