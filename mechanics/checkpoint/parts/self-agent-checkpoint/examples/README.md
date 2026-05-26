# Self-Agent Checkpoint Examples

## Purpose

This directory contains inspectable examples for the governed self-agent
checkpoint contract owned by the `self-agent-checkpoint` part.

## Contract anchors

Keep this subtree aligned with:

- [../schemas/self-agent-checkpoint.schema.json](../schemas/self-agent-checkpoint.schema.json)
- `mechanics/checkpoint/parts/self-agent-checkpoint/docs/self-agent-checkpoint-stack.md`
- `checkpoint_cohort`

## Active Example

- [self-agent-checkpoint.example.json](self-agent-checkpoint.example.json)

## Invalid fixtures

`invalid/` exists for negative coverage and must stay intentionally invalid.
Do not turn an invalid fixture into a second example.

## Editing posture

Keep approval, rollback, audit, health, and bounded-iteration posture explicit.
Do not turn this subtree into runtime implementation, execution logs, or scenario canon.

## Validation

Run `python -m pip install -r requirements-dev.txt`, then:

```bash
python mechanics/checkpoint/scripts/validate_checkpoint_contracts.py
python scripts/validate_agents.py
```
