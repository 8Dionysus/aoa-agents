# Mechanics Payload Recon

This recon records why the current mechanic skeleton exists. It is a route
map over payload pressure, not permission to move every matching file.

## Pre-Move Root Folder Sweep

The initial root payload inventory found mechanic-bearing files in every large
root district before the 2026-05-26 docs landing:

| Root folder | File count | Mechanic pressure |
| --- | ---: | --- |
| `docs/` | 139 | public route cards, posture contracts, release notes, boundary law |
| `examples/` | 127 | contract examples for assistant, Agon, Titan, runtime, recurrence, checkpoints |
| `schemas/` | 120 | shared payload contracts for the same operation families |
| `agents/` | 89 | source-authored profiles, adjuncts, tiers, classes, cohorts, runtime seam bindings |
| `tests/` | 76 | builder, validator, projection, and route-surface guards |
| `scripts/` | 53 | builders and validators for formation, projection, Titan, recurrence, runtime, release |
| `generated/` | 36 | derived registries, indexes, Codex projections, quest/read-model companions |
| `quests/` | 20 | quest-facing role posture and Agon quest surfaces; localized to the questbook package on 2026-05-26 |
| `manifests/` | 11 | recurrence and projection component manifests; localized to the recurrence `component-manifests` part on 2026-05-26 |
| `config/` | 11 | Agon, recursor, Codex, and Titan source seeds; localized to part-level config routes on 2026-05-26 |
| `memo/` | 9 | local memory port; route only, not mechanic authority |
| `mechanics/` | 3 | prior atlas-only skeleton |
| `Spark/` | 2 | local Spark-facing route support |

## Dense Term Clusters

Approximate root-payload term counts from the same sweep:

| Term | Count | Primary route |
| --- | ---: | --- |
| `assistant` | 167 | `experience/` |
| `agon` / `agonic` | 76 | `agon/` |
| `titan` | 49 | `titan/` |
| `runtime` | 39 | `runtime-seam/` |
| `release` | 37 | `release-support/`, with assistant service release pressure cross-routed to `experience/` |
| `recursor` / `recurrence` | 43 | `recurrence/`, with Agon boundary pressure cross-routed to `agon/` |
| `codex` | 26 | `codex-projection/` |
| `quest` | 25 | `questbook/` |
| `self` / `checkpoint` | 33 | `checkpoint/` |
| `adoption` / `office` | 82 | `experience/` |
| `stress` | 6 | `antifragility/` and `checkpoint/` |
| `federation` | 4 | `boundary-bridge/` |

`agent` is intentionally not counted as a mechanic parent: it describes the
repository layer and source-object district. Agent source objects live under
`agents/`.

## Current Mechanic Set

The current package skeleton is:

| Mechanic | Why it exists now |
| --- | --- |
| `agon/` | Agon pressure already spans formation adjuncts, Wave I/II/II.5 builders, schemas, examples, config seeds, generated indexes, and quest surfaces. |
| `experience/` | Assistant service, office, adoption, watch, rollback, and release-readiness payloads form a dense service-experience operation cluster. |
| `titan/` | Titan role-bearing surfaces have their own docs, config, schemas, examples, generated projections, builders, and tests. |
| `recurrence/` | Recursor and recurrence surfaces already cross docs, config, schemas, examples, generated outputs, scripts, tests, and manifests. |
| `runtime-seam/` | Runtime seam bindings and artifact transition contracts are stable enough to route as a mechanic while runtime implementation stays elsewhere. |
| `codex-projection/` | Codex subagent projection has source wiring, generated projections, refresh law, tests, and manifest support. |
| `checkpoint/` | Self-agent checkpoint, continuity, reviewed-closeout, and reference-route posture recur across docs, examples, schemas, cohorts, and generated readers. |
| `questbook/` | Quest-facing role posture spans the part-local quest catalog, part-local quest records, Agon quest notes, generated dispatch/readers, and execution-passport docs. |
| `rpg/` | Progression, mastery, cohort, and unlock-like role posture exists as a thin but distinct agent-layer operation. |
| `antifragility/` | Stress, via negativa, and scar/adaptation pressure already has public posture and contract examples. |
| `boundary-bridge/` | Federation seams, published compatibility, workspace trigger posture, and source-surface registries route cross-repo consumers. |
| `release-support/` | Repo publication and release-readiness checks need an operation route that does not become CI authority. |

## Move Rule

A payload can move from a root district into a mechanic only after the target
mechanic has:

- a package card and part map
- source/support/generated/example classification for the payload
- stop-lines against stronger owners
- package-local or repo-level validation that still covers the old public
  contract
- a decision or route note when the move changes lookup topology

The docs landing satisfies that rule for mechanics-facing public docs by moving
them into part-local `docs/` directories and preserving old-path accounting in
package `PROVENANCE.md` plus `legacy/`. Other payload classes still need their
own move proof before leaving their current owner districts.

The config localization satisfies that rule for mechanic-specific source seed
and wiring payloads by moving them into part-local `config/` directories with
active config README cards, updated builders/validators, and package
provenance maps.

The manifest localization satisfies that rule for recurrence component and
hook manifests by moving them into the `component-manifests` part with an
active manifest route card and `validate_recurrence_component_manifests.py`.

The questbook localization satisfies that rule for root quest payloads by
moving the catalog doc, YAML quest records, and Agon quest notes into
part-local questbook routes while keeping generated quest readers in
`generated/`.

The Titan example localization satisfies that rule for schema-backed Titan
examples by moving them into part-local `examples/` directories and adding
`scripts/validate_titan_examples.py`.

The Titan schema localization satisfies that rule for Titan-specific contract
schemas by moving them into part-local `schemas/` directories and adding
`scripts/validate_titan_schemas.py`.

Shared non-Titan schemas, non-Titan examples, scripts, tests, generated
readers, and source agent objects remain in their current districts until their
own move proof exists.
