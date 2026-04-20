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
- subject-prep boundary plus unreleased companion turns and the first formation
  trial in `docs/AGENT_SUBJECT_PREP.md`, `docs/AGONIC_ACTOR_RECHARTERING.md`,
  `docs/ASSISTANT_CIVIL_RECHARTERING.md`, `docs/AGENT_FORMATION_TRIAL.md`, and
  `generated/agent_formation_trial.min.json`, keeping the agonic/assistant kind split
  additive without changing profile schemas yet

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

## Unreleased next turn: Agonic Actor Rechartering

The next unreleased agent-layer turn after `v0.2.2` is Wave I Agonic Actor
Rechartering. Its checked surface is:

- Wave I doctrine and landing docs:
  `docs/AGONIC_ACTOR_RECHARTERING.md`,
  `docs/AGON_WAVE1_LANDING.md`,
  `docs/AGENT_KIND_MODEL.md`,
  `docs/AGENT_SUBJECTIVITY_MODEL.md`,
  `docs/AGENT_OFFICE_MODEL.md`,
  `docs/AGENT_ARENA_ELIGIBILITY_MODEL.md`, and
  `docs/AGENT_RESISTANCE_REVISION_POSTURE.md`
- additive companion source surfaces:
  `profiles/adjuncts/kind/*.kind.json`,
  `profiles/adjuncts/subjectivity/*.subjectivity.json`,
  `profiles/adjuncts/office_overlay/*.office.json`,
  `profiles/adjuncts/arena_eligibility/*.arena_eligibility.json`, and
  `profiles/adjuncts/resistance_revision/*.resistance_revision.json`
- Wave I companion contracts and publication:
  `schemas/agent_kind_v1.json`,
  `schemas/agent_subjectivity_v1.json`,
  `schemas/agent_office_overlay_v1.json`,
  `schemas/agent_arena_eligibility_v1.json`,
  `schemas/agent_resistance_revision_v1.json`,
  `generated/agent_agonic_formation_index.min.json`, and
  `examples/agent_agonic_formation.example.json`
- explicit Wave I validation lane:
  `scripts/build_agent_agonic_formation_index.py`,
  `scripts/validate_agent_agonic_formation.py`, and
  `tests/test_agent_agonic_formation.py`

This turn keeps the base `profiles/*.profile.json` files as legacy role
contracts while Wave I lands reviewed companion surfaces for agonic actor
readiness. It does not widen `schemas/agent-profile.schema.json`, does not
rewrite generated role registries, and does not start arena protocol, scars,
retention, runtime packets, or ToS promotion.

## Unreleased follow-on turn: Assistant Civil Rechartering

The next unreleased follow-on turn after Wave I is Wave II Assistant Civil
Rechartering. Its checked surface is:

- Wave II doctrine and landing docs:
  `docs/ASSISTANT_CIVIL_RECHARTERING.md`,
  `docs/AGON_WAVE2_LANDING.md`,
  `docs/ASSISTANT_KIND_MODEL.md`,
  `docs/ASSISTANT_SERVICE_IDENTITY_MODEL.md`,
  `docs/ASSISTANT_SERVICE_CONTRACT_MODEL.md`,
  `docs/ASSISTANT_SERVICE_GOVERNANCE_MODEL.md`,
  `docs/ASSISTANT_SERVICE_CERTIFICATION_MODEL.md`,
  `docs/ASSISTANT_ARENA_EXCLUSION_MODEL.md`, and
  `docs/ASSISTANT_ESCALATION_TO_AGON.md`
- additive assistant companion source surfaces:
  `profiles/adjuncts/assistant_variant/*.assistant.variant.json`,
  `profiles/adjuncts/assistant_service_identity/*.assistant.identity.json`,
  `profiles/adjuncts/assistant_service_contract/*.assistant.contract.json`,
  `profiles/adjuncts/assistant_service_governance/*.assistant.governance.json`,
  `profiles/adjuncts/assistant_service_certification/*.assistant.certification.json`, and
  `profiles/adjuncts/assistant_arena_exclusion/*.assistant.arena_exclusion.json`
- Wave II companion contracts and publication:
  `schemas/assistant_variant_v1.json`,
  `schemas/assistant_service_identity_v1.json`,
  `schemas/assistant_service_contract_v1.json`,
  `schemas/assistant_service_governance_v1.json`,
  `schemas/assistant_service_certification_v1.json`,
  `schemas/assistant_arena_exclusion_v1.json`,
  `generated/assistant_civil_formation_index.min.json`, and
  `examples/assistant_civil_formation.example.json`
- explicit Wave II validation lane:
  `scripts/build_assistant_civil_formation_index.py`,
  `scripts/validate_assistant_civil_formation.py`, and
  `tests/test_assistant_civil_formation.py`

This turn keeps assistant variants as civil/service forms anchored to the same
five role houses without widening the public role catalog, without granting
contestant or judge authority, and without pulling runtime packets, scars,
verdicts, durable incident logs, or ToS promotion into `aoa-agents`.

## Unreleased follow-on turn: Formation Trial

The next unreleased follow-on turn after Wave II is Wave II.5 Formation Trial.
Its checked surface is:

- Wave II.5 doctrine and landing docs:
  `docs/AGENT_FORMATION_TRIAL.md`,
  `docs/AGON_PRE_PROTOCOL_AGENT_BOUNDARY.md`,
  `docs/FORMATION_TRIAL_READINESS.md`,
  `docs/CODEX_PROJECTION_AGON_BOUNDARY.md`, and
  `docs/AGON_WAVE2_5_LANDING.md`
- Wave II.5 companion contract and publication:
  `schemas/agent_formation_trial_v1.json`,
  `generated/agent_formation_trial.min.json`, and
  `examples/agent_formation_trial.example.json`
- explicit Wave II.5 validation lane:
  `scripts/build_agent_formation_trial.py`,
  `scripts/validate_agent_formation_trial.py`, and
  `tests/test_agent_formation_trial.py`

This turn judges whether the current five role houses survive as readable split
forms after Waves I and II. It opens Wave III design only as pre-protocol
readability, and it does not open arena sessions, lawful moves, sealed commits,
verdict logic, scars, retention checks, runtime packets, or ToS promotion
inside `aoa-agents`.

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
