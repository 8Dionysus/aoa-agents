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

## Current First Slice

The first topology refactor moves the source-authored agent object districts
under `agents/` and activates `mechanics/` as an operation atlas.

It does not yet move the flat public docs and shared contract artifacts into
mechanic-local packages. Those moves should be smaller later slices, because
many tests, validators, generated references, and public docs currently use
the existing paths as contract anchors.

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

