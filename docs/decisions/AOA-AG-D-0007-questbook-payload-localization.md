# 2026-05-26: Questbook Payload Localization

## Status

Accepted, then superseded in part by
[`2026-05-26: Questbook source store topology repair`](AOA-AG-D-0008-questbook-source-store-topology-repair.md).

## Index Metadata

- Decision ID: AOA-AG-D-0007
- Original date: 2026-05-26
- Surface classes: mechanic part, example/source
- Agent facets: mechanics atlas, quest/alpha
- Mechanic parents: questbook, agon
- Guard families: part-local artifact, example validation, quest dispatch
- Posture: accepted

## Context

The questbook mechanic already owned quest-facing role posture, but the active
quest catalog doc and quest source records still lived at the repository root.
This decision initially treated those root surfaces as mechanics payloads. The
later topology repair restored the stronger source split used by sibling repos.

The YAML quest records feed generated quest catalog and dispatch readers. The
Agon quest notes are quest-facing posture records, not playbook choreography or
proof verdicts.

## Decision

The original decision moved the active quest catalog doc and YAML quest records
into the `quest-catalog` part and moved Agon quest notes into the
`agon-quest-surfaces` part.

The current active decision restores the root `QUESTBOOK.md` and root
`quests/` district while keeping `mechanics/questbook/` as the operation
package and validation route.

## Consequences

- `QUESTBOOK.md` owns the active human quest index.
- `quests/` owns active source quest records.
- `mechanics/questbook/parts/public-index/` and
  `mechanics/questbook/parts/quest-item-store/` route to those root surfaces.
- `scripts/validate_agents.py` validates the new source paths and generated
  quest readers.
- Playbook scenario choreography, proof verdicts, and durable memory truth
  remain outside this repository.

## Verification

Verification routes through the focused owner checks and the repository release gate.
