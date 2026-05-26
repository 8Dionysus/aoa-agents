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

| Mechanic | Current Source Surfaces | Operation |
| --- | --- | --- |
| `agon/` | Agon docs, part-local config seeds, adjuncts, formation indexes, Wave I/II/II.5 builders and tests | route contest, formation, arena, rank, school, epistemic actor, and adoption pressure; `formation` is a part of `agon`, not the parent mechanic |
| `experience/` | assistant civil/service/office/adoption/release docs, adjuncts, schemas, examples | route assistant service, office, adoption, watch, and arena-exclusion pressure without becoming runtime service authority |
| `titan/` | Titan docs, part-local config, schemas, examples, generated projections, and builders | route Titan role-bearing, lineage, summon, roster, and service-cohort posture inside the agent layer |
| `recurrence/` | recursor docs, part-local config, part-local component manifests, schemas, examples, and generated readers | route recursor readiness, paired recurrence, projection refresh, and component-return pressure |
| `runtime-seam/` | `agents/runtime_seam/`, runtime artifact schemas/examples, seam docs/generated readers | keep role x tier bindings and artifact transitions contract-first without owning runtime implementation |
| `codex-projection/` | `agents/profiles/`, part-local Codex wiring config, generated Codex agents, projection docs/tests | keep Codex subagent projection source-owned, refreshable, and bounded to role contracts |
| `checkpoint/` | self-agent, continuity, checkpoint, reviewed-closeout, and reference-route docs/examples | keep checkpoint posture reviewable, reversible, and separate from durable memory truth |
| `questbook/` | part-local quest catalog, part-local quest records, Agon quest notes, quest generated readers, passport/reference-route docs | keep quest-facing role posture bounded without taking playbook scenario ownership |
| `rpg/` | progression, mastery, cohort, and quest-readable role posture docs | route progression and unlock pressure without becoming game runtime or quest choreography |
| `antifragility/` | stress posture, via negativa, scar/adaptation docs, schemas, examples, tests | route failure-pressure learning and negative checks without becoming proof authority |
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
- quest catalog records and Agon quest notes live under
  `mechanics/questbook/parts/*/quests/`;
- package `PARTS.md` files are the active part maps;
- package `PROVENANCE.md` files are the only active bridge into old-path
  accounting;
- package `legacy/INDEX.md` and `legacy/DISTILLATION_LOG.md` preserve the
  former `docs/*`, `config/*`, `manifests/*`, root quest catalog, and
  root quest-source lookup maps without
  duplicating active authority.

Shared schemas, non-Titan examples, scripts, tests, agent source objects, and
generated readers remain in their current owner districts until they receive
their own package-local contract and validation coverage.

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
