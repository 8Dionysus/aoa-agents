# AoA Agents Roadmap

This roadmap tracks the bootstrap baseline and the current `v0.2.x`
contract-hardening waves for the AoA agent layer.

## Current phase

The bootstrap baseline is landed.

The current goal is not to widen the catalog too early.
The current goal is to make the existing public agent-layer surfaces stable,
scenario-backed, projection-aware, and consumer-provable without moving
runtime, playbook, routing, memo, or eval canon into this repository.

The current `v0.2.x` release line already carries:
- checkpoint role follow-through, Codex subagent projection, and self-agency continuity posture as live repo-owned surfaces rather than future ideas
- Codex custom-agent projection and owner refresh-law surfaces in `docs/CODEX_SUBAGENT_PROJECTION.md`, `docs/CODEX_SUBAGENT_REFRESH_LAW.md`, `config/codex_subagent_wiring.v2.json`, and `generated/codex_agents/`
- runtime seam, stress posture, and stress handoff adjuncts in `generated/runtime_seam_bindings.json`, `docs/AGENT_STRESS_POSTURE.md`, and `docs/AGENT_STRESS_HANDOFFS.md`
- adjunct quest and Alpha readiness surfaces in `docs/QUEST_EXECUTION_PASSPORT.md`, `generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`, and `generated/alpha_reference_routes.min.json`
- pre-Agon subject-prep boundaries in `docs/AGENT_SUBJECT_PREP.md`, including
  the future agonic/assistant kind split without changing profile schemas yet

The near-term roadmap should therefore read as projection and contract
hardening, not as a pre-projection bootstrap placeholder.

## Current cycle

### Wave 1: public contract stabilization

Goals:
- publish explicit compatibility discipline for source-authored and generated contract surfaces
- harden validator checks around top-level metadata, stable publication order, and silent field drift
- keep existing generated wire shapes and artifact schemas unchanged

Exit signals:
- published compatibility rules are documented
- validator fails on accidental generated-surface drift
- generated registry order remains deterministic and inspectable

### Wave 2: scenario-backed reference routes

Goals:
- add example-only route packs over the current public loop
- validate cohort fit, tier fit, seam fit, and artifact fit for each route pack
- keep these surfaces educational and inspectable rather than normative

Exit signals:
- four reference route packs validate end-to-end
- manifests remain schema-backed and example-only
- no runtime logic or playbook canon is introduced

### Wave 3: federation consumer proof

Goals:
- make bounded consumer promises explicit for `aoa-playbooks`, `aoa-evals`, `aoa-memo`, and `aoa-routing`
- expand optional smoke checks around those seams without requiring cross-repo checkout by default
- preserve self-contained local validation when consumer roots are not supplied

Exit signals:
- federated smoke checks cover all four current consumer seams
- the consumer check matrix is documented
- local validation remains autonomous when roots are absent

## Current published contour

The currently published agent-layer contour already includes:
- source-authored role, tier, orchestrator, cohort, and runtime-seam inputs under `profiles/`, `model_tiers/`, `orchestrator_classes/`, `cohort_patterns/`, and `runtime_seam/`
- published registries and consumer seams under `generated/agent_registry.min.json`, `generated/model_tier_registry.json`, `generated/cohort_composition_registry.json`, and `generated/runtime_seam_bindings.json`
- Codex subagent projection outputs under `generated/codex_agents/agents/*.toml` and `generated/codex_agents/config.subagents.generated.toml`
- role-posture adjuncts for stress, checkpoint-growth, quest, and Alpha reference routes under `docs/AGENT_STRESS_POSTURE.md`, `docs/AGENT_STRESS_HANDOFFS.md`, `docs/WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md`, `docs/QUEST_EXECUTION_PASSPORT.md`, `generated/quest_catalog.min.json`, `generated/quest_dispatch.min.json`, and `generated/alpha_reference_routes.min.json`

The main near-term risk is roadmap drift: Codex subagent projection, stress
adjuncts, quest capture, and Alpha readiness are already shipped surfaces and
should stay visible in current-direction docs instead of hiding only in
README or release notes.

## Bootstrap substep: runtime seam hardening

Status: landed as baseline.

Goals:
- add inspectable runtime artifact examples and bounded negative fixtures
- publish a machine-readable role × tier binding surface
- make transition and artifact coverage discipline explicit
- make recurrence discipline explicit without turning return into a new runtime stage
- add optional published-contract smoke checks without requiring cross-repo CI checkout

Exit signals:
- every published runtime artifact schema has a valid example and bounded invalid fixture coverage
- the public role × tier mapping is machine-readable without changing existing registry wire shape
- `transition_decision` can express anchor-based return in a compact inspectable way
- the validator can confirm public contract reachability in neighboring repos when local roots are supplied

## Phase 1: agent layer definition

Goals:
- define `aoa-agents` as the canonical role and persona layer within AoA
- make the distinction between agent, skill, proof, memory, and routing explicit
- establish a compact agent registry and a minimal validator

Exit signals:
- the repository role is clear
- agent-layer boundaries are documented
- a compact machine-readable registry exists

## Phase 2: first agent profile discipline

Goals:
- define the first public shape for agent profiles
- distinguish basic role contracts such as architect, coder, reviewer, evaluator, and memory-keeper
- keep profile forms compact enough to review

## Phase 3: handoff and posture surfaces

Goals:
- make handoff rules explicit
- make memory posture explicit
- make evaluation posture explicit
- keep agent boundaries readable to humans and smaller models

## Phase 4: cohort composition

Goals:
- define bounded multi-agent composition hints
- clarify when agents operate solo, in pairs, or under orchestration
- avoid turning the agent layer into a hidden runtime monolith too early

Exit signals:
- the first official cohort pattern set is documented
- a machine-readable cohort composition registry exists
- the validator checks cohort pattern alignment against role and tier registries
- the self-agent checkpoint route maps to a canonical cohort pattern without absorbing playbook logic

## Phase 5: federation integration

Goals:
- connect `aoa-agents` cleanly to `aoa-skills`
- connect agent postures to `aoa-evals`
- connect agent memory posture to `aoa-memo`
- preserve clear boundaries relative to `aoa-routing`
- harden bounded consumer seams against routing-published memo recall entrypoints
  without moving tiny-model family-selection policy into `aoa-agents`

Near-term interpretation:
- prove the current published seams first
- stabilize the contract before any larger catalog growth
- postpone new role families until after the current cycle lands

## Standing discipline

Across all phases:
- keep roles explicit
- keep profiles compact
- keep handoff rules reviewable
- do not confuse the actor layer with execution, proof, memory, or routing
