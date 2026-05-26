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

The 2026-05-26 questbook localization moves the quest catalog doc, YAML quest
records, and Agon quest notes into `mechanics/questbook/parts/*` after updating
the questbook validator route and generated quest readers. Generated quest
catalog and dispatch readers remain derived surfaces under `generated/`.

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
