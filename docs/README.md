# Documentation Map

This file is the human-first entrypoint for the `docs/` surface of `aoa-agents`.

Use it when you want to understand the AoA agent layer rather than the broader federation as a whole.

## Start here

- Read [CHARTER](../CHARTER.md) for the role and boundaries of the agent layer.
- Read [AGENT_MODEL](AGENT_MODEL.md) for the conceptual model.
- Read [AGENT_RUNTIME_SEAM](AGENT_RUNTIME_SEAM.md) for the contract-first runtime seam.
- Read [SELF_AGENT_CHECKPOINT_STACK](SELF_AGENT_CHECKPOINT_STACK.md) for the bounded self-agent contract.
- Read [BOUNDARIES](BOUNDARIES.md) for ownership discipline relative to neighboring AoA layers.
- Read [ROADMAP](../ROADMAP.md) for the current direction.

## Docs in this repository

- [AGENT_MODEL](AGENT_MODEL.md) — what the agent layer is for
- [AGENT_RUNTIME_SEAM](AGENT_RUNTIME_SEAM.md) — how role-and-tier binding stays explicit without turning into runtime implementation
- [SELF_AGENT_CHECKPOINT_STACK](SELF_AGENT_CHECKPOINT_STACK.md) — how self-agent surfaces stay bounded, reviewable, and rollback-aware
- [BOUNDARIES](BOUNDARIES.md) — what the agent layer owns and must not absorb

## Notes

This repository should stay bounded.
If a document starts trying to become a technique corpus, workflow corpus, proof corpus, or memory store, it probably belongs in a neighboring AoA repository instead.
