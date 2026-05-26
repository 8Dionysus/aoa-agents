# Mechanics Artifact Topology

This note governs when existing root-level technical artifacts may move into
`mechanics/`.

## Operating Card

| Field | Route |
| --- | --- |
| role | artifact movement rule for mechanic-localization |
| input | proposal to move docs, schemas, examples, scripts, tests, generated readers, or config into a mechanic |
| output | move permission, defer route, package-local contract requirement, or stronger-owner handoff |
| owner | `mechanics/AGENTS.md` and the target mechanic package once it exists |
| next route | target mechanic card, current artifact owner, builder/validator, decision record |
| tools | `rg`, repo validators, owning builder checks |
| validation | `validate_semantic_agents.py`, `validate_nested_agents.py`, `validate_agents.py`, plus moved-surface checks |

## Current Rule

Do not move `docs/`, `schemas/`, `examples/`, `scripts/`, `tests/`, or
`generated/` payloads into a mechanic only because the file name matches a
topic.

Move a payload only when the target mechanic has:

- a named repeatable operation
- an owner split
- local stop-lines
- validation commands
- a route card that explains whether the payload is source, support,
  generated, example, or legacy

## Current Slices

The first topology refactor moves the source-authored agent object districts
under `agents/` and activates `mechanics/` as an operation atlas.

The next slice added package skeletons under `mechanics/` after a root payload
sweep.

The 2026-05-26 docs landing moves mechanics-facing public docs into
part-local `mechanics/*/parts/*/docs/` routes and updates legacy accounting for
former `docs/*` paths. It does not move shared schemas, examples, scripts,
tests, generated readers, manifests, quest files, config seeds, or agent source
objects. Those payload classes remain current support/source/generated
districts until a dedicated package-local contract and validator route make
the move smaller and reviewable.

The 2026-05-26 config localization moves mechanic-specific seed and wiring
payloads from root `config/` into the owning part-local
`mechanics/*/parts/*/config/` route after each target part has an active config
card and validator route. Root `config/` remains reserved for future
repository-level config; it is not the active home for Agon, recurrence, Codex
projection, or Titan mechanic seeds.

The 2026-05-26 manifest localization moves recurrence component and hook
manifests from root `manifests/` into
`mechanics/recurrence/parts/component-manifests/manifests/` after adding a
manifest validator. Root `manifests/` is not the active owner for recurrence
component declarations.

The 2026-05-26 Questbook source-store repair keeps `QUESTBOOK.md`, `quests/`,
and root quest generated readers in their root districts while
`mechanics/questbook/parts/*` owns public-index, quest-item-store, and
dispatch-reader route law.

The 2026-05-26 Titan example localization moves schema-backed Titan examples
from root `examples/` into active `mechanics/titan/parts/*/examples/` routes
after adding a package-local example validator. Root `examples/` remains active
for shared examples whose mechanic-local contract is not explicit yet.

The 2026-05-26 Titan schema localization moves Titan-specific schemas from
root `schemas/` into active `mechanics/titan/parts/*/schemas/` routes after
adding a package-local schema validator. Root `schemas/` remains active for
shared non-Titan contracts.

The 2026-05-26 antifragility stress localization moves stress-posture schemas
and examples from root `schemas/` and `examples/` into active
`mechanics/antifragility/parts/stress-posture/{schemas,examples}/` routes after
adding a part-local validator. Stable schema `$id` values remain public
contract identifiers, not active repo paths.

The 2026-05-26 RPG progression localization moves the adjunct progression
schema and example from root `schemas/` and `examples/` into active
`mechanics/rpg/parts/progression-model/{schemas,examples}/` routes after adding
a part-local validator. Stable schema `$id` values remain public contract
identifiers, not active repo paths.

The 2026-05-26 assistant projection resolver localization moves Codex-facing
assistant projection resolver schemas and example from root `schemas/` and
`examples/` into active
`mechanics/codex-projection/parts/assistant-projection/{schemas,examples}/`
routes after adding a part-local validator. Stable schema `$id` values remain
public contract identifiers, not active repo paths.

The 2026-05-26 runtime artifact contract localization moves runtime artifact
schemas, examples, and invalid fixtures from root `schemas/` and `examples/`
into active
`mechanics/runtime-seam/parts/artifact-contracts/{schemas,examples}/` routes
after adding a part-local validator. Stable schema `$id` values remain public
contract identifiers, not active repo paths.

The 2026-05-26 checkpoint contract localization moves self-agent checkpoint
and continuity-window schemas/examples from root `schemas/` and `examples/`
into active `mechanics/checkpoint/parts/*/{schemas,examples}/` routes after
adding a part-local validator. Stable schema `$id` values remain public
contract identifiers, not active repo paths.

The 2026-05-26 recursor contract localization moves recursor readiness,
projection-candidate, and Agon-boundary schemas/examples from root `schemas/`
and `examples/` into active `mechanics/recurrence/parts/*/{schemas,examples}/`
routes after adding a part-local validator. Stable schema `$id` values remain
public contract identifiers, not active repo paths.

The 2026-05-26 Agon rank/epistemic contract localization moves rank,
jurisdiction, school/campaign, and epistemic actor schemas/examples from root
`schemas/` and `examples/` into active
`mechanics/agon/parts/*/{schemas,examples}/` routes after adding a part-local
validator. Stable schema `$id` values, where present, remain public contract
identifiers, not active repo paths.

The 2026-05-26 Agon formation contract localization moves Wave I agonic
formation and Wave II.5 formation-trial schemas/examples from root `schemas/`
and `examples/` into active `mechanics/agon/parts/formation/` and
`mechanics/agon/parts/arena-rank-school/` contract routes after adding a
part-local validator. Stable schema `$id` values remain public contract
identifiers, not active repo paths.

The 2026-05-26 Experience assistant civil contract localization moves Wave II
assistant civil schemas/examples from root `schemas/` and `examples/` into
active `mechanics/experience/parts/assistant-civil-service/` and
`mechanics/experience/parts/arena-exclusion/` contract routes after adding a
part-local validator. Stable schema `$id` values remain public contract
identifiers, not active repo paths.

The 2026-05-26 Codex refresh-law example localization moves the Codex
subagent projection refresh-law example from root `examples/` into active
`mechanics/codex-projection/parts/refresh-law/examples/` after adding a
part-local validator.

The 2026-05-26 adoption/boundary contract localization moves adoption,
retention, office, and boundary bridge schemas/examples from root `schemas/`
and `examples/` into active Experience, Agon, and Boundary Bridge part-local
contract routes after adding a validator that protects the active file sets,
schema/example alignment, guardrail booleans, numeric ranges, enum closure,
and former root path absence. Stable schema `$id`, `kind`, and
`schema_id`/`schema_version` values remain public contract identifiers, not
active repo paths.

The 2026-05-26 agent service contract localization moves the remaining
assistant service, office, release, watch, rollback, governance,
runtime-readable authority-claim, and release-hold schemas/examples from root
`schemas/` and `examples/` into active Experience, Runtime Seam, and Release
Support part-local contract routes after adding
`scripts/validate_agent_service_contracts.py`. The route split follows the
current mechanic docs: authority claims belong to Runtime Seam, release holds
belong to Release Support, and assistant service/office/watch pressure belongs
to Experience. Stable schema `$id`, `kind`, and identifier values remain
public contract identifiers, not active repo paths.

The 2026-05-26 reference-route contract localization moves reference-route and
Alpha reference-route schemas/examples from root `schemas/` and `examples/`
into active Checkpoint and Questbook part-local contract routes after adding
`scripts/validate_reference_route_contracts.py`. The route split follows the
current mechanic docs: public-loop route packs belong to Checkpoint
`reference-routes`; Alpha playbook-facing readiness examples belong to
Questbook `alpha-reference-routes`. Stable schema `$id` values and manifest
`route_id` values remain public contract identifiers, not active repo paths.

The 2026-05-26 Alpha reference-route generated reader localization moves the
derived Alpha reader from root `generated/` into
`mechanics/questbook/parts/alpha-reference-routes/generated/` after the Alpha
schema and examples already had a part-local route and validator. Root
`generated/` continues to own repo-level registries and readers; this reader
is part-local because its only source truth is the Questbook Alpha example set.

The 2026-05-26 Agon rank/school/epistemic generated reader localization moves
candidate-only rank jurisdiction, school/campaign posture, and epistemic actor
registry readers from root `generated/` into their owning Agon parts after the
schemas, examples, and config seeds already had part-local routes and
validators. Root `generated/` continues to own repo-level registries and
formation readers; these readers are part-local because they summarize Agon
part-local config.

The 2026-05-26 recursor generated reader localization moves readiness, pair,
projection-candidate, and Agon boundary readers from root `generated/` into
their owning Recurrence parts after the recursor configs, schemas, examples,
and component manifests already had part-local routes and validators. Root
`generated/` continues to own repo-level registries and formation readers;
these readers are part-local because they summarize Recurrence part-local
config and contract surfaces.

The 2026-05-26 Questbook source-store repair keeps quest catalog and dispatch
readers root-published under `generated/` because they summarize root
`quests/` source records. `mechanics/questbook/parts/dispatch-reader/` owns the
projection contract and validation route, not the generated files themselves.

The 2026-05-26 formation generated-reader posture keeps
`generated/agent_agonic_formation_index.min.json`,
`generated/assistant_civil_formation_index.min.json`, and
`generated/agent_formation_trial.min.json` root-published because their source
truth is under `agents/` and their consumer posture is repo-wide. The Agon and
Experience parts own formation contracts, examples, docs, and stop-lines around
those readers, not the generated files as part-local companions.

Use `mechanics/PAYLOAD_RECON.md`, `mechanics/LEGACY_TOPOLOGY.md`, and the
target package `PARTS.md` as evidence before proposing a move.

## Stronger Owners

If a payload starts to become any of the following, route it away instead of
mechanic-localizing it here:

| Payload pressure | Route instead |
| --- | --- |
| runtime implementation | runtime owner, usually `abyss-stack` |
| proof verdict or eval bundle | `aoa-evals` |
| durable memory object or recall truth | `aoa-memo` |
| routing policy | `aoa-routing` |
| playbook scenario choreography | `aoa-playbooks` |
| reusable skill or technique | `aoa-skills` or `aoa-techniques` |

## Package Skeleton Rule

Package skeletons may be added before payload movement when they make current
root pressure legible. A skeleton should name:

- the repeatable operation
- current payload classes
- package parts
- stronger-owner stop-lines
- validation route

Skeletons must not claim that payloads already moved or that a mechanic owns a
root district wholesale.

## Legacy Rule

Do not call a current root payload legacy merely because it is waiting for a
future package-local move. In this repository, `legacy/` means provenance and
old-route accounting.

Add raw legacy receipts only when there is real historical material to
preserve. Empty raw inventories should say they are empty.
