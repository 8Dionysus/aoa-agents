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

## Active Package Map

These packages are active route homes for mechanics. The 2026-05-26 docs
landing moved mechanics-facing public docs out of root `docs/` and into
part-local `mechanics/*/parts/*/docs/` routes. The config localization moved
mechanic-specific seeds and wiring out of root `config/` and into part-local
`mechanics/*/parts/*/config/` routes. The manifest localization moved
recurrence component and hook manifests into
`mechanics/recurrence/parts/component-manifests/manifests/`. Other source,
support, generated, validation, schema, and agent-source
payloads stay in their owning districts until a later slice gives them a
package-local contract and validator route.
The Titan example localization moved schema-backed Titan examples into
part-local `mechanics/titan/parts/*/examples/` routes after adding a dedicated
example validator.
The Titan schema localization moved Titan-specific schemas into
part-local `mechanics/titan/parts/*/schemas/` routes while preserving stable
schema `$id` values.
The adoption/boundary localization moved adoption, retention, office, and
boundary bridge schemas/examples into their owning Experience, Agon, and
Boundary Bridge part-local contract routes.
The agent service contract localization moved the remaining assistant
service, office, release, watch, rollback, governance, authority-claim, and
release-hold schemas/examples into Experience, Runtime Seam, and Release
Support part-local contract routes.
The reference-route contract localization moved reference-route and Alpha
reference-route schemas/examples into Checkpoint and Questbook part-local
contract routes.
The Alpha reference-route generated reader localization moved the derived
Alpha reader into the Questbook `alpha-reference-routes` part because its only
source truth is that part's examples.
The Agon rank/school/epistemic generated reader localization moved
candidate-only rank, school/campaign, and epistemic registries into their
owning Agon parts because their source truth is already part-local config.
The recursor generated reader localization moved readiness, pair, projection,
and boundary readers into their owning Recurrence parts because their source
truth is already part-local config/schema/example material.
The Questbook topology repair keeps quest source truth in root `quests/` and
quest catalog/dispatch readers in root `generated/` while `mechanics/questbook/`
owns the operation law, source-store route, index route, and reader contract.
The mechanics package route-card pass adds `mechanics/<package>/AGENTS.md`
for every active package so agents can enter a mechanic through a nearest
package card before dropping into part-local cards.

| Mechanic | Current Source Surfaces | Operation |
| --- | --- | --- |
| `agon/` | Agon docs, part-local config seeds, adjuncts, part-local rank/school/epistemic generated readers, formation indexes, Wave I/II/II.5 builders and tests | route contest, formation, arena, rank, school, epistemic actor, and adoption pressure; `formation` is a part of `agon`, not the parent mechanic |
| `experience/` | assistant civil/service/office/adoption/release docs, adjuncts, schemas, examples | route assistant service, office, adoption, watch, and arena-exclusion pressure without becoming runtime service authority |
| `titan/` | Titan docs, part-local config, schemas, examples, generated projections, and builders | route Titan role-bearing, lineage, summon, roster, and service-cohort posture inside the agent layer |
| `recurrence/` | recursor docs, part-local config, part-local component manifests, schemas, examples, and part-local generated readers | route recursor readiness, paired recurrence, projection refresh, and component-return pressure |
| `runtime-seam/` | `agents/runtime_seam/`, runtime artifact schemas/examples, seam docs/generated readers | keep role x tier bindings and artifact transitions contract-first without owning runtime implementation |
| `codex-projection/` | `agents/profiles/`, part-local Codex wiring config, generated Codex agents, projection docs/tests | keep Codex subagent projection source-owned, refreshable, and bounded to role contracts |
| `checkpoint/` | self-agent, continuity, checkpoint, reviewed-closeout, and reference-route docs/schemas/examples | keep checkpoint posture reviewable, reversible, and separate from durable memory truth |
| `questbook/` | root `QUESTBOOK.md`, root `quests/`, root quest generated readers, Alpha reference-route schemas/examples/generated reader, passport/reference-route docs | keep quest-facing role posture bounded without taking playbook scenario ownership |
| `rpg/` | progression docs, part-local progression schema/example, mastery, cohort, and quest-readable role posture docs | route progression and unlock pressure without becoming game runtime or quest choreography |
| `antifragility/` | stress posture docs, part-local schemas/examples, via negativa, scar/adaptation docs, tests | route failure-pressure learning and negative checks without becoming proof authority |
| `boundary-bridge/` | federation seams, published contract compatibility, workspace trigger, source registries | route consumer handoff and cross-repo boundary pressure without becoming routing policy |
| `release-support/` | `CHANGELOG.md`, `mechanics/release-support/parts/repo-release-gate/docs/releasing.md`, release checks and release-readiness docs | keep publication posture coherent without becoming CI or GitHub authority |

## Current Shape

The first topology slice activated the mechanics atlas and moved agent source
objects into `agents/`. The docs and config localization slices turn the
mechanics packages from empty route skeletons into active route homes:

- part-local docs live under `mechanics/*/parts/*/docs/`;
- mechanic-specific seeds and wiring live under
  `mechanics/*/parts/*/config/`;
- recurrence component and hook manifests live under
  `mechanics/recurrence/parts/component-manifests/manifests/`;
- Titan schema-backed examples live under
  `mechanics/titan/parts/*/examples/`;
- Titan-specific schemas live under
  `mechanics/titan/parts/*/schemas/`;
- adoption, retention, office, and boundary bridge contracts live under their
  owning Experience, Agon, and Boundary Bridge part-local `schemas/` and
  `examples/` routes;
- assistant service, office, release, watch, rollback, governance,
  runtime-readable authority-claim, and release-hold contracts live under
  their owning Experience, Runtime Seam, and Release Support part-local
  `schemas/` and `examples/` routes;
- reference-route and Alpha reference-route contracts live under their owning
  Checkpoint and Questbook part-local `schemas/` and `examples/` routes;
- the Alpha reference-route generated reader lives under its owning Questbook
  part-local `generated/` route;
- Agon rank/school/epistemic generated readers live under their owning
  Agon part-local `generated/` routes;
- recursor generated readers live under their owning Recurrence part-local
  `generated/` routes;
- quest catalog and dispatch readers stay root-published under `generated/`
  because they summarize root quest records;
- quest catalog records and Agon quest notes live under root `quests/`;
- package `PARTS.md` files are the active part maps;
- package `AGENTS.md` files are the nearest package route cards;
- package `PROVENANCE.md` files are the only active bridge into old-path
  accounting;
- package `legacy/INDEX.md` and `legacy/DISTILLATION_LOG.md` preserve the
  former `docs/*`, `config/*`, `manifests/*`, prior flat quest-source,
  reference-route schema, reference-route example, and localized generated reader
  lookup maps without
  duplicating active authority.

Shared schemas/examples that have not received a package-local contract,
scripts, tests, agent source objects, and remaining generated readers remain
in their current owner districts until they receive their own package-local
contract and validation coverage.

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
