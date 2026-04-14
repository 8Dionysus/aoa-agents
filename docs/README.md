# Documentation Map

This file is the human-first entrypoint for the `docs/` surface of `aoa-agents`.

Use it when you want to understand the AoA agent layer rather than the broader federation as a whole.

## Start here

- Read [CHARTER](../CHARTER.md) for the role and boundaries of the agent layer.
- Read [AGENT_MODEL](AGENT_MODEL.md) for the conceptual model.
- Read [AGENT_SUBJECT_PREP](AGENT_SUBJECT_PREP.md) for the bounded future-prep note on subject-bearing agent surfaces, the agonic/assistant kind split, and the civil/service assistant path.
- Read [AGENT_PROFILE_SURFACE](AGENT_PROFILE_SURFACE.md) for the source-authored role-contract surface.
- Read [ORCHESTRATOR_CLASS_MODEL](ORCHESTRATOR_CLASS_MODEL.md) for the source-authored orchestrator-class surface.
- Read [REGISTRY_SOURCE_SURFACES](REGISTRY_SOURCE_SURFACES.md) for the source-authored machine-readable registry layer.
- Read [CODEX_SUBAGENT_PROJECTION](CODEX_SUBAGENT_PROJECTION.md) for the projected Codex custom-agent install surface.
- Read [CODEX_SUBAGENT_REFRESH_LAW](CODEX_SUBAGENT_REFRESH_LAW.md) for the owner refresh route when source profiles, projection wiring, generated agent TOML, or workspace install seams drift.
- Read [AGENT_MEMORY_POSTURE](AGENT_MEMORY_POSTURE.md) for role-level memory rights and posture.
- Read [AGENT_STRESS_POSTURE](AGENT_STRESS_POSTURE.md) for additive role narrowing under stress.
- Read [AGENT_STRESS_HANDOFFS](AGENT_STRESS_HANDOFFS.md) for bounded stress handoff envelopes between actors.
- Read [MODEL_TIER_MODEL](MODEL_TIER_MODEL.md) for the separate tier-oriented orchestration model.
- Read [AGENT_COHORT_PATTERNS](AGENT_COHORT_PATTERNS.md) for the bounded cohort composition surface.
- Read [AGENT_RUNTIME_SEAM](AGENT_RUNTIME_SEAM.md) for the contract-first runtime seam.
- Read [FEDERATION_CONSUMER_SEAMS](FEDERATION_CONSUMER_SEAMS.md) for the bounded cross-repo consumer seams.
- Read [WORKSPACE_SURFACE_TRIGGER_POSTURE](WORKSPACE_SURFACE_TRIGGER_POSTURE.md) for the additive workspace-trigger law around `aoa surfaces detect`.
- Read [RUNTIME_ARTIFACT_TRANSITIONS](RUNTIME_ARTIFACT_TRANSITIONS.md) for public loop coverage and transition discipline.
- Read [RECURRENCE_DISCIPLINE](RECURRENCE_DISCIPLINE.md) for explicit recurrence discipline and bounded return governance.
- Read [SELF_AGENT_CHECKPOINT_STACK](SELF_AGENT_CHECKPOINT_STACK.md) for the bounded self-agent contract.
- Read [SELF_AGENCY_CONTINUITY_LANE](SELF_AGENCY_CONTINUITY_LANE.md) for the bounded continuity window and anchor-return contract.
- Read [REFERENCE_ROUTE_EXAMPLES](REFERENCE_ROUTE_EXAMPLES.md) for example-only and Alpha route packs.
- Read [QUEST_EXECUTION_PASSPORT](QUEST_EXECUTION_PASSPORT.md) for quest-facing execution posture.
- Read [BOUNDARIES](BOUNDARIES.md) for ownership discipline relative to neighboring AoA layers.
- Read [ROADMAP](../ROADMAP.md) for the current direction.

## Docs in this repository

- [AGENT_MODEL](AGENT_MODEL.md) — what the agent layer is for
- [AGENT_SUBJECT_PREP](AGENT_SUBJECT_PREP.md) — what future subject-bearing agent preparation, agonic/assistant kind separation, and civil/service assistant formation may and may not move into the agent layer
- [AGENT_PROFILE_SURFACE](AGENT_PROFILE_SURFACE.md) — how source-authored role contracts stay distinct from the compact generated registry
- [ORCHESTRATOR_CLASS_MODEL](ORCHESTRATOR_CLASS_MODEL.md) — how orchestrator classes stay source-authored, capsule-friendly, and distinct from quest workloads
- [REGISTRY_SOURCE_SURFACES](REGISTRY_SOURCE_SURFACES.md) — how source-authored machine-readable tier, cohort, and seam surfaces publish compact registries
- [CODEX_SUBAGENT_PROJECTION](CODEX_SUBAGENT_PROJECTION.md) — how active role profiles project into generated Codex custom-agent TOML and workspace config snippets without moving authorship out of `profiles/`
- [CODEX_SUBAGENT_REFRESH_LAW](CODEX_SUBAGENT_REFRESH_LAW.md) — how repeated projection drift turns into owner-owned refresh work without making generated or installed agent files canonical
- [AGENT_MEMORY_POSTURE](AGENT_MEMORY_POSTURE.md) — how role-level memory rights stay explicit without becoming memory canon
- [AGENT_STRESS_POSTURE](AGENT_STRESS_POSTURE.md) — how role-bearing actors narrow mutation appetite, proof posture, and memory writeback under stress without widening authority
- [AGENT_STRESS_HANDOFFS](AGENT_STRESS_HANDOFFS.md) — how stressed actors pass bounded evidence, blocked actions, and re-entry conditions without turning handoff envelopes into proof
- [MODEL_TIER_MODEL](MODEL_TIER_MODEL.md) — how the tier-oriented orchestration side stays explicit and bounded
- [AGENT_COHORT_PATTERNS](AGENT_COHORT_PATTERNS.md) — how official cohort patterns stay compact and distinct from playbooks
- [AGENT_RUNTIME_SEAM](AGENT_RUNTIME_SEAM.md) — how role-and-tier binding stays explicit without turning into runtime implementation
- [WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE](WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md) — how the April 9 workspace checkpoint-growth closeout leaves one bounded agent-layer role-posture adjunct without widening profiles
- [WAVE5_A2A_SUMMON_RETURN_ROLE_POSTURE_HOLD](WAVE5_A2A_SUMMON_RETURN_ROLE_POSTURE_HOLD.md) — how the Wave5 A2A summon return closeout leaves one bounded agent-layer hold without widening profiles
- [FEDERATION_CONSUMER_SEAMS](FEDERATION_CONSUMER_SEAMS.md) — how neighboring repositories consume bounded agent-layer contracts without moving canon here
- [WORKSPACE_SURFACE_TRIGGER_POSTURE](WORKSPACE_SURFACE_TRIGGER_POSTURE.md) — how workspace sessions open additive `aoa surfaces detect` without turning the agent layer into routing or skill canon
- [RUNTIME_ARTIFACT_TRANSITIONS](RUNTIME_ARTIFACT_TRANSITIONS.md) — how artifact coverage and transition governance stay bounded inside the public loop
- [RECURRENCE_DISCIPLINE](RECURRENCE_DISCIPLINE.md) — how recurrence stays explicit, anchor-based, and bounded without becoming runtime implementation
- [SELF_AGENT_CHECKPOINT_STACK](SELF_AGENT_CHECKPOINT_STACK.md) — how self-agent surfaces stay bounded, reviewable, and rollback-aware
- [SELF_AGENCY_CONTINUITY_LANE](SELF_AGENCY_CONTINUITY_LANE.md) — how continuity windows, bounded revision, and anchor-return posture stay explicit at the agent layer
- [REFERENCE_ROUTE_EXAMPLES](REFERENCE_ROUTE_EXAMPLES.md) — how reference route packs and Alpha companions stay example-only and playbook-facing
- [QUEST_EXECUTION_PASSPORT](QUEST_EXECUTION_PASSPORT.md) — how quest difficulty, risk, control, and delegate-tier posture stay inspectable
- [BOUNDARIES](BOUNDARIES.md) — what the agent layer owns and must not absorb

## Verify current published surfaces

- Run `python scripts/validate_agents.py` for the local non-mutating contract and example checks.
- Run `python -m pytest -q tests` for the local test suite.
- Add `AOA_PLAYBOOKS_ROOT`, `AOA_EVALS_ROOT`, `AOA_MEMO_ROOT`, and `AOA_ROUTING_ROOT` only when you want bounded consumer-smoke checks against sibling repositories.
- Use `python scripts/build_published_surfaces.py` only after editing source-authored registry inputs.

## Notes

This repository should stay bounded.
If a document starts trying to become a technique corpus, workflow corpus, proof corpus, or memory store, it probably belongs in a neighboring AoA repository instead.

Inspectable runtime seam examples live in `examples/runtime_artifacts/`.
Inspectable self-agent checkpoint examples live in `examples/self_agent_checkpoint/`.
Adjunct published outputs currently include `generated/alpha_reference_routes.min.json`, `generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`, and `generated/codex_agents/`.
`generated/codex_agents/` is the repo-side install surface for workspace `.codex/agents/`.
Optional validator smoke checks may read neighboring published surfaces when `AOA_PLAYBOOKS_ROOT`, `AOA_EVALS_ROOT`, `AOA_MEMO_ROOT`, or `AOA_ROUTING_ROOT` are set, but they only test bounded contract reachability and do not import neighboring meaning into this repo.
