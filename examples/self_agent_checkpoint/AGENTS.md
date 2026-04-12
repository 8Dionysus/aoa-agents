# examples/self_agent_checkpoint/AGENTS.md

## Purpose

`examples/self_agent_checkpoint/` contains inspectable examples for the governed self-agent checkpoint contract and the adjacent self-agency continuity window contract.

## Contract anchors

Keep this subtree aligned with:

- `schemas/self-agent-checkpoint.schema.json`
- `schemas/self-agency-continuity-window.schema.json`
- `docs/SELF_AGENT_CHECKPOINT_STACK.md`
- `docs/SELF_AGENCY_CONTINUITY_LANE.md`
- `checkpoint_cohort`

## Invalid fixtures

`invalid/` exists for negative coverage and must stay intentionally invalid.

## Editing posture

Keep approval, rollback, audit, health, and bounded-iteration posture explicit.
Do not turn this subtree into runtime implementation, execution logs, or scenario canon.

## Validation

Run `python -m pip install -r requirements-dev.txt`, then `python scripts/validate_agents.py`.
