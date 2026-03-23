# Documentation Map

This file is the human-first entrypoint for the `docs/` surface of `aoa-agents`.

Use it when you want to understand the AoA agent layer rather than the broader federation as a whole.

## Start here

- Read [CHARTER](../CHARTER.md) for the role and boundaries of the agent layer.
- Read [AGENT_MODEL](AGENT_MODEL.md) for the conceptual model.
- Read [AGENT_MEMORY_POSTURE](AGENT_MEMORY_POSTURE.md) for role-level memory rights and posture.
- Read [MODEL_TIER_MODEL](MODEL_TIER_MODEL.md) for the separate tier-oriented orchestration model.
- Read [AGENT_COHORT_PATTERNS](AGENT_COHORT_PATTERNS.md) for the bounded cohort composition surface.
- Read [AGENT_RUNTIME_SEAM](AGENT_RUNTIME_SEAM.md) for the contract-first runtime seam.
- Read [RUNTIME_ARTIFACT_TRANSITIONS](RUNTIME_ARTIFACT_TRANSITIONS.md) for public loop coverage and transition discipline.
- Read [SELF_AGENT_CHECKPOINT_STACK](SELF_AGENT_CHECKPOINT_STACK.md) for the bounded self-agent contract.
- Read [BOUNDARIES](BOUNDARIES.md) for ownership discipline relative to neighboring AoA layers.
- Read [ROADMAP](../ROADMAP.md) for the current direction.

## Docs in this repository

- [AGENT_MODEL](AGENT_MODEL.md) — what the agent layer is for
- [AGENT_MEMORY_POSTURE](AGENT_MEMORY_POSTURE.md) — how role-level memory rights stay explicit without becoming memory canon
- [MODEL_TIER_MODEL](MODEL_TIER_MODEL.md) — how the tier-oriented orchestration side stays explicit and bounded
- [AGENT_COHORT_PATTERNS](AGENT_COHORT_PATTERNS.md) — how official cohort patterns stay compact and distinct from playbooks
- [AGENT_RUNTIME_SEAM](AGENT_RUNTIME_SEAM.md) — how role-and-tier binding stays explicit without turning into runtime implementation
- [RUNTIME_ARTIFACT_TRANSITIONS](RUNTIME_ARTIFACT_TRANSITIONS.md) — how artifact coverage and transition governance stay bounded inside the public loop
- [SELF_AGENT_CHECKPOINT_STACK](SELF_AGENT_CHECKPOINT_STACK.md) — how self-agent surfaces stay bounded, reviewable, and rollback-aware
- [BOUNDARIES](BOUNDARIES.md) — what the agent layer owns and must not absorb

## Notes

This repository should stay bounded.
If a document starts trying to become a technique corpus, workflow corpus, proof corpus, or memory store, it probably belongs in a neighboring AoA repository instead.

Inspectable runtime seam examples live in `examples/runtime_artifacts/`.
Optional validator smoke checks may read neighboring published surfaces when `AOA_PLAYBOOKS_ROOT`, `AOA_EVALS_ROOT`, or `AOA_MEMO_ROOT` are set, but they only test contract reachability and do not import neighboring meaning into this repo.
