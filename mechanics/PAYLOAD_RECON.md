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

The antifragility stress localization satisfies that rule for stress-posture
contract schemas and examples by moving them into the `stress-posture` part and
adding `scripts/validate_antifragility_stress.py`.

The RPG progression localization satisfies that rule for the adjunct
progression schema and example by moving them into the `progression-model` part
and adding `scripts/validate_rpg_progression.py`.

The assistant projection resolver localization satisfies that rule for
Codex-facing assistant projection resolver schemas and example by moving them
into the `assistant-projection` part and adding
`scripts/validate_assistant_projection_resolver.py`.

The runtime artifact contract localization satisfies that rule for runtime
artifact schemas, examples, and invalid fixtures by moving them into the
`runtime-seam/artifact-contracts` part and adding
`scripts/validate_runtime_artifact_contracts.py`.

The checkpoint contract localization satisfies that rule for self-agent
checkpoint and continuity-window schemas/examples by splitting them into the
`checkpoint/self-agent-checkpoint` and `checkpoint/continuity-lane` parts and
adding `scripts/validate_checkpoint_contracts.py`.

The recursor contract localization satisfies that rule for recurrence recursor
schemas/examples by splitting them into `recursor-readiness`,
`codex-recursor-projection`, and `agon-recursor-boundary` parts and adding
`scripts/validate_recursor_contracts.py`.

The Agon rank/epistemic contract localization satisfies that rule for
candidate-only rank, school/campaign, and epistemic actor schemas/examples by
splitting them into `arena-rank-school` and `epistemic-actor` parts and adding
`scripts/validate_agon_rank_epistemic_contracts.py`.

The Agon formation contract localization satisfies that rule for Wave I
agonic formation and Wave II.5 formation-trial schemas/examples by placing
formation contracts under `mechanics/agon/parts/formation/`, arena eligibility
under `mechanics/agon/parts/arena-rank-school/schemas/`, and adding
`scripts/validate_agon_formation_contracts.py`.

The Experience assistant civil contract localization satisfies that rule for
Wave II assistant civil schemas/examples by placing service contracts under
`mechanics/experience/parts/assistant-civil-service/`, arena exclusion under
`mechanics/experience/parts/arena-exclusion/schemas/`, and adding
`scripts/validate_experience_assistant_civil_contracts.py`.

Shared remaining non-Titan, non-runtime-artifact, non-checkpoint,
non-recursor, non-Agon-rank/epistemic, non-Agon-formation, and
non-Experience-assistant-civil schemas,
remaining non-Titan, non-runtime-artifact, non-checkpoint, non-recursor,
non-Agon-rank/epistemic, non-Agon-formation, and
non-Experience-assistant-civil examples,
scripts, tests, generated readers, and source agent objects remain in their
current districts until their own move proof exists.
