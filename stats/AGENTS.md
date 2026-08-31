# AGENTS.md

## Applies To

This card applies to `stats/` in `aoa-agents`.

## Role

This directory owns agent-local statistical questions, their embedded
measurement contracts, and evidence-linked reference packets. Shared
statistical grammar and cross-owner composition remain owned by `aoa-stats`.

## Boundaries

- `port.manifest.json` owns the agent-local question and measurement meaning.
- Reference packets are derived snapshots and remain weaker than eligibility
  source records and their owner decision.
- The eligibility ratio reports explicit `eligible` decision labels only. It
  does not establish projection, installability, proof strength, workspace
  acceptance, runtime activation, or generated-agent availability.
- Keep packet refs repository-relative and raw role or evidence content out of
  packets.

## Validation
Use the repository [validation map](../VALIDATION.md) and the nearest owner check when this route is relevant.

Inspect the owner read model at
`mechanics/codex-projection/parts/specialization-eligibility/generated/` first.

Then validate the port and packet with the central contract owner through the
repository validation map.

## Closeout

Report the question or contract changed, owner evidence inspected, whether the
reference packet was refreshed, and which validation route ran.
