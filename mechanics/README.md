# Mechanics Atlas

`mechanics/` is the operation atlas for repeatable agent-layer mechanics in
`aoa-agents`.

It does not replace source objects under `agents/`, public explanation under
`docs/`, shared schemas under `schemas/`, examples under `examples/`, or
generated readers under `generated/`. It names the operations that repeatedly
move pressure across those surfaces and keeps owner boundaries visible.

## Operating Card

| Field | Route |
| --- | --- |
| role | atlas for repeatable agent-layer operations |
| input | recurring pressure that crosses source, docs, schema, example, generated, config, script, or test surfaces |
| output | active route family, package-growth candidate, validator route, or stronger-owner handoff |
| owner | `mechanics/AGENTS.md`, this atlas, and future mechanic package cards |
| next route | `mechanics/ARTIFACT_TOPOLOGY.md`, active route family, source owner, decision record |
| tools | repo validators and owning builders |
| validation | `python scripts/validate_semantic_agents.py`, `python scripts/validate_nested_agents.py`, `python scripts/validate_agents.py` |

## Active Package Skeleton

These packages are active route skeletons, not payload migrations. The root
payloads stay under `docs/`, `schemas/`, `examples/`, `config/`, `generated/`,
`scripts/`, `tests/`, `manifests/`, `quests/`, and `agents/` until a later
slice gives a package-local contract and validator enough authority to move
them.

| Mechanic | Current Source Surfaces | Operation |
| --- | --- | --- |
| `agon/` | Agon docs, adjuncts, config seeds, formation indexes, Wave I/II/II.5 builders and tests | route contest, formation, arena, rank, school, epistemic actor, and adoption pressure; `formation` is a part of `agon`, not the parent mechanic |
| `experience/` | assistant civil/service/office/adoption/release docs, adjuncts, schemas, examples | route assistant service, office, adoption, watch, and arena-exclusion pressure without becoming runtime service authority |
| `titan/` | Titan docs/config/schemas/examples/generated projections and builders | route Titan role-bearing, lineage, summon, roster, and service-cohort posture inside the agent layer |
| `recurrence/` | recursor docs/config/schemas/examples/generated readers and recurrence manifests | route recursor readiness, paired recurrence, projection refresh, and component-return pressure |
| `runtime-seam/` | `agents/runtime_seam/`, runtime artifact schemas/examples, seam docs/generated readers | keep role x tier bindings and artifact transitions contract-first without owning runtime implementation |
| `codex-projection/` | `agents/profiles/`, Codex wiring config, generated Codex agents, projection docs/tests | keep Codex subagent projection source-owned, refreshable, and bounded to role contracts |
| `checkpoint/` | self-agent, continuity, checkpoint, reviewed-closeout, and reference-route docs/examples | keep checkpoint posture reviewable, reversible, and separate from durable memory truth |
| `questbook/` | `QUESTBOOK.md`, `quests/`, quest generated readers, passport/reference-route docs | keep quest-facing role posture bounded without taking playbook scenario ownership |
| `rpg/` | progression, mastery, cohort, and quest-readable role posture docs | route progression and unlock pressure without becoming game runtime or quest choreography |
| `antifragility/` | stress posture, via negativa, scar/adaptation docs, schemas, examples, tests | route failure-pressure learning and negative checks without becoming proof authority |
| `boundary-bridge/` | federation seams, published contract compatibility, workspace trigger, source registries | route consumer handoff and cross-repo boundary pressure without becoming routing policy |
| `release-support/` | `CHANGELOG.md`, `docs/RELEASING.md`, release checks and release-readiness docs | keep publication posture coherent without becoming CI or GitHub authority |

## Current Shape

The first topology slice activated the mechanics atlas and moved agent source
objects into `agents/`. This slice adds package skeletons for the mechanics that
are already visible in root payload directories.

It deliberately still keeps large public docs, shared schemas, examples,
scripts, tests, manifests, config seeds, quest files, and generated readers in
their existing districts until each mechanic has a package-local contract and
validator support. That keeps this move reviewable: `mechanics/` names the
operation topology now; payload localization can happen later in smaller
verified slices.

## Traversal

When work starts from a source object, enter through `agents/`.
When work starts from recurring operation pressure, enter through
`mechanics/`.
When work starts from public explanation, enter through `docs/` and then route
to the owning source object or operation family.
When work starts from a file-name cluster, use `PAYLOAD_RECON.md` and the
target package `PARTS.md` before deciding whether it is a mechanic, a source
object, or a stronger-owner handoff.
When work starts from old-path, former-route, or provenance pressure, use
`LEGACY_TOPOLOGY.md` and the target package `PROVENANCE.md` before opening
`legacy/`.

## Stop Lines

- A mechanic is not a proof verdict.
- A mechanic is not a memory object.
- A mechanic is not a runtime worker.
- A mechanic is not a playbook scenario.
- A mechanic is not a generated reader.
- Legacy is not the active route for current behavior.
