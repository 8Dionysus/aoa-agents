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
| `quests/` | 20 | quest-facing role posture and Agon quest surfaces; repaired to root lane/state source ownership on 2026-05-26 |
| `manifests/` | 11 | recurrence and projection component manifests; localized to the recurrence `component-manifests` part on 2026-05-26 |
| `config/` | 11 | Agon, recursor, Codex, and Titan source seeds; localized to part-level config routes on 2026-05-26 |
| `memo/` | 9 | local memory port; route only, not mechanic authority |
| `mechanics/` | 3 | prior atlas-only skeleton |
| `Spark/` | 2 | local Spark-facing route support; moved to `.agents/spark/` on 2026-05-26 |

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
| `questbook/` | Quest-facing role posture spans root `QUESTBOOK.md`, root `quests/`, generated dispatch/readers, public-index and source-store route law, and execution-passport docs. |
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
them into part-local `docs/` directories and preserving old-path accounting
through package `PROVENANCE.md`. Other payload classes still need their own
move proof before leaving their current owner districts.

The config localization satisfies that rule for mechanic-specific source seed
and wiring payloads by moving them into part-local `config/` directories with
active config README cards, updated builders/validators, and package
provenance maps.

The manifest localization satisfies that rule for recurrence component and
hook manifests by moving them into the `component-manifests` part with an
active manifest route card and part-local
`mechanics/recurrence/parts/component-manifests/scripts/validate_recurrence_component_manifests.py`.

The Questbook source-store repair satisfies that rule by refusing to move root
quest source truth into mechanics: root `QUESTBOOK.md` and root `quests/` stay
active, while `mechanics/questbook/parts/*` records the public-index,
quest-item-store, and dispatch-reader route law.

The Titan example localization satisfies that rule for schema-backed Titan
examples by moving them into part-local `examples/` directories and adding
a Titan package-local example validator.

The Titan schema localization satisfies that rule for Titan-specific contract
schemas by moving them into part-local `schemas/` directories and adding
a Titan package-local schema validator.

The Titan check localization satisfies that rule for Titan package-owned
validators and focused tests by moving them into
`mechanics/titan/{scripts,tests}/`; the root release gate still runs the
package-local tests explicitly.

The antifragility stress localization satisfies that rule for stress-posture
contract schemas and examples by moving them into the `stress-posture` part and
adding a part-local stress-posture validator.

The RPG progression localization satisfies that rule for the adjunct
progression schema and example by moving them into the `progression-model` part
and adding the part-local validator under
`mechanics/rpg/parts/progression-model/scripts/`.

The assistant projection resolver localization satisfies that rule for
Codex-facing assistant projection resolver schemas and example by moving them
into the `assistant-projection` part and keeping the focused validator under
`mechanics/codex-projection/parts/assistant-projection/scripts/`.

The runtime artifact contract localization satisfies that rule for runtime
artifact schemas, examples, and invalid fixtures by moving them into the
`runtime-seam/artifact-contracts` part and adding
`mechanics/runtime-seam/parts/artifact-contracts/scripts/validate_artifact_contracts.py`.

The checkpoint contract localization satisfies that rule for self-agent
checkpoint and continuity-window schemas/examples by splitting them into the
`checkpoint/self-agent-checkpoint` and `checkpoint/continuity-lane` parts and
adding `mechanics/checkpoint/scripts/validate_checkpoint_contracts.py`.

The recursor contract localization satisfies that rule for recurrence recursor
schemas/examples by splitting them into `recursor-readiness`,
`codex-recursor-projection`, and `agon-recursor-boundary` parts and adding
`mechanics/recurrence/scripts/validate_recursor_contracts.py`.

The Agon rank/epistemic contract localization satisfies that rule for
candidate-only rank, school/campaign, and epistemic actor schemas/examples by
splitting them into `arena-rank-school` and `epistemic-actor` parts and adding
`mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py`.

The Agon formation contract localization satisfies that rule for Wave I
agonic formation and Wave II.5 formation-trial schemas/examples by placing
formation contracts under `mechanics/agon/parts/formation/`, arena eligibility
under `mechanics/agon/parts/arena-rank-school/schemas/`, and adding
`mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py`.

The Experience assistant civil contract localization satisfies that rule for
Wave II assistant civil schemas/examples by placing service contracts under
`mechanics/experience/parts/assistant-civil-service/`, arena exclusion under
`mechanics/experience/parts/arena-exclusion/schemas/`, and adding
`mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py`.

The Experience assistant civil check localization satisfies that rule for Wave
II assistant civil builders, validators, and tests by moving formation-reader
support into `mechanics/experience/parts/assistant-civil-service/{scripts,tests}/`
and the cross-part contract check into `mechanics/experience/{scripts,tests}/`.
The generated reader stays root-published because it summarizes `agents/`
source adjunct records.

The Codex refresh-law example localization satisfies that rule for the Codex
projection refresh route example by placing it under
`mechanics/codex-projection/parts/refresh-law/examples/` and adding the
part-local validator under
`mechanics/codex-projection/parts/refresh-law/scripts/`.

The adoption/boundary contract localization satisfies that rule for adoption,
retention, office, and boundary bridge schemas/examples by placing them under
their owning Experience, Agon, and Boundary Bridge part-local
`schemas/`/`examples/` routes and adding
`mechanics/experience/scripts/validate_adoption_boundary_contracts.py`.

The Experience adoption/boundary check localization satisfies that rule for
the Wave III adoption/boundary validator and focused test by moving them into
`mechanics/experience/{scripts,tests}/`. The check stays package-local because
it spans Experience adoption/office parts and cross-routes into Agon
adoption-retention plus Boundary Bridge consumer/federation parts.

The agent service contract localization satisfies that rule for the remaining
assistant service, office, release, watch, rollback, governance,
runtime-readable authority-claim, and release-hold schemas/examples by routing
them into the active part-local contract homes named by the package docs and
adding `mechanics/experience/scripts/validate_agent_service_contracts.py`.

The Experience agent service check localization satisfies that rule for the
agent service validator and focused test by moving them into
`mechanics/experience/{scripts,tests}/`. The check stays package-local because
it spans multiple Experience parts and cross-routes Runtime Seam authority
claim plus Release Support release-hold contracts.

The reference-route contract localization satisfies that rule for
reference-route and Alpha reference-route schemas/examples by routing public
loop route packs into `mechanics/checkpoint/parts/reference-routes/`, routing
Alpha playbook-facing readiness examples into
`mechanics/questbook/parts/alpha-reference-routes/`, and adding
`scripts/validate_reference_route_contracts.py`.

The Alpha reference-route generated reader localization satisfies that rule for
the derived Alpha reader by placing it next to the Questbook
`alpha-reference-routes` examples it summarizes and teaching
`scripts/generate_alpha_reference_routes.py`,
`scripts/validate_reference_route_contracts.py`, and
`scripts/validate_agents.py` the part-local route plus former-root absence.

The Agon rank/school/epistemic generated reader localization satisfies that
rule for candidate-only generated registries by placing them next to the Agon
part-local config, schemas, and examples they summarize and teaching the
dedicated builders, validators, component manifests, and tests the part-local
routes plus former-root absence.

The recursor generated reader localization satisfies that rule for Recurrence
derived readers by placing readiness, pair, projection, and boundary readers
next to the part-local config/schema/example surfaces they summarize and
teaching the recursor builders, validators, component manifests, and tests the
part-local routes plus former-root absence.

The Questbook source-store repair follows the stronger sibling-repo pattern:
root `QUESTBOOK.md` owns human visibility, root `quests/` owns source records,
root `generated/quest_*` readers summarize those records, and
`mechanics/questbook/` owns the route law plus builder-backed validation.

The formation generated-reader posture follows the same source-first rule in
the opposite direction from the part-local generated moves: formation schemas
and examples live in Agon and Experience parts, but
`generated/agent_agonic_formation_index.min.json`,
`generated/assistant_civil_formation_index.min.json`, and
`generated/agent_formation_trial.min.json` remain root-published because they
summarize `agents/` source objects and feed repo-wide role readiness.

The root agent schema posture applies the same rule to remaining root schemas:
shared role/profile, registry, tier, orchestrator, cohort, and runtime-seam
schemas stay under `schemas/` because they constrain `agents/` source families
and repo-wide generated registries. They are not waiting for mechanics moves.

The Spark lane placement follows the established agent-lane source pattern:
root `Spark/` was moved to `.agents/spark/` because it is agent-facing
fast-loop guidance, not a mechanic package, generated reader, schema contract,
or source-authored role object.

The mechanics package route-card pass follows the established refactored-repo
mechanics pattern by adding `mechanics/<package>/AGENTS.md` to every active
package. The cards make nearest-owner entry legible between `mechanics/AGENTS.md`
and `parts/AGENTS.md`; no payload class moves in this slice.

The antifragility stress check localization follows the same part-owner rule
for executable checks by moving the stress-posture validator and focused test
into `mechanics/antifragility/parts/stress-posture/{scripts,tests}/`. Root
`scripts/validate_agents.py` remains the repo-wide validation coordinator, and
`scripts/release_check.py` runs the part-local test explicitly.

Shared remaining non-Titan, non-runtime-artifact, non-checkpoint,
non-recursor, non-Agon-rank/epistemic, non-Agon-formation, and
non-Experience-assistant-civil, non-adoption/boundary, non-agent-service,
non-reference-route schemas,
remaining non-Titan, non-runtime-artifact, non-checkpoint, non-recursor,
non-Agon-rank/epistemic, non-Agon-formation, and
non-Experience-assistant-civil, non-Codex-refresh-law,
non-adoption/boundary, non-agent-service, non-reference-route examples,
scripts, tests, remaining generated readers, and source agent objects remain
in their current districts until their own move proof exists.
