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
- Codex custom-agent projection and owner refresh-law surfaces in `mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md`, `mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md`, `mechanics/codex-projection/parts/refresh-law/examples/subagent-refresh-law.example.json`, `mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json`, and `generated/codex_agents/`
- runtime seam, stress posture, and stress handoff adjuncts in `generated/runtime_seam_bindings.json`, `mechanics/antifragility/parts/stress-posture/docs/stress-posture.md`, and `mechanics/antifragility/parts/stress-posture/docs/stress-handoffs.md`
- adjunct quest and Alpha readiness surfaces in `QUESTBOOK.md`, `quests/`, `mechanics/questbook/parts/execution-passport/docs/quest-execution-passport.md`, `mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json`, `generated/quest_catalog.min.json`, and `generated/quest_dispatch.min.json`
- subject-prep boundary plus unreleased companion turns and the first formation
  trial in `mechanics/agon/parts/formation/docs/subject-prep.md`, `mechanics/agon/parts/formation/docs/actor-rechartering.md`,
  `mechanics/experience/parts/assistant-civil-service/docs/civil-rechartering.md`, `mechanics/agon/parts/formation/docs/formation-trial.md`, and
  `generated/agent_formation_trial.min.json`, keeping the agonic/assistant kind split
  additive without changing profile schemas yet

The near-term roadmap should therefore read as projection and contract
hardening, not as a pre-projection bootstrap placeholder.

The current topology line also now separates source-authored agent objects from
repeatable operation mechanics:

- `agents/` owns role, tier, orchestrator-class, cohort, and runtime-seam
  source inputs.
- `mechanics/` owns the operation atlas for formation, projection,
  runtime-seam binding, checkpoint posture, quest posture, Titan role-bearing
  movement, and release-support pressure.
- Large public docs, shared schemas, examples, scripts, tests, and generated
  readers stay in their current districts until a later mechanic package has a
  local contract and validator support.

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
- source-authored role, tier, orchestrator, cohort, and runtime-seam inputs under `agents/profiles/`, `agents/model_tiers/`, `agents/orchestrator_classes/`, `agents/cohort_patterns/`, and `agents/runtime_seam/`
- the mechanics atlas under `mechanics/`
- published registries and consumer seams under `generated/agent_registry.min.json`, `generated/model_tier_registry.json`, `generated/cohort_composition_registry.json`, and `generated/runtime_seam_bindings.json`
- Codex subagent projection outputs under `generated/codex_agents/agents/*.toml` and `generated/codex_agents/config.subagents.generated.toml`
- role-posture adjuncts for stress, checkpoint-growth, quest, and Alpha reference routes under `mechanics/antifragility/parts/stress-posture/docs/stress-posture.md`, `mechanics/antifragility/parts/stress-posture/docs/stress-handoffs.md`, `mechanics/checkpoint/parts/growth-checkpoint/docs/workspace-checkpoint-growth-role-posture.md`, `mechanics/questbook/parts/execution-passport/docs/quest-execution-passport.md`, `mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json`, `generated/quest_catalog.min.json`, and `generated/quest_dispatch.min.json`

The main near-term risk is roadmap drift: Codex subagent projection, stress
adjuncts, quest capture, and Alpha readiness are already shipped surfaces and
should stay visible in current-direction docs instead of hiding only in
README or release notes.

## Unreleased next turn: Agonic Actor Rechartering

The next unreleased agent-layer turn after `v0.2.3` is Wave I Agonic Actor
Rechartering. Its checked surface is:

- Wave I doctrine and landing docs:
  `mechanics/agon/parts/formation/docs/actor-rechartering.md`,
  `mechanics/agon/parts/formation/docs/wave1-landing.md`,
  `mechanics/agon/parts/formation/docs/kind-model.md`,
  `mechanics/agon/parts/formation/docs/subjectivity-model.md`,
  `mechanics/experience/parts/office-operations/docs/agent-office-model.md`,
  `mechanics/agon/parts/arena-rank-school/docs/arena-eligibility-model.md`, and
  `mechanics/agon/parts/formation/docs/resistance-revision-posture.md`
- additive companion source surfaces:
  `agents/profiles/adjuncts/kind/*.kind.json`,
  `agents/profiles/adjuncts/subjectivity/*.subjectivity.json`,
  `agents/profiles/adjuncts/office_overlay/*.office.json`,
  `agents/profiles/adjuncts/arena_eligibility/*.arena_eligibility.json`, and
  `agents/profiles/adjuncts/resistance_revision/*.resistance_revision.json`
- Wave I companion contracts and publication:
  `mechanics/agon/parts/formation/schemas/agent-kind.schema.json`,
  `mechanics/agon/parts/formation/schemas/subjectivity.schema.json`,
  `mechanics/agon/parts/formation/schemas/office-overlay.schema.json`,
  `mechanics/agon/parts/arena-rank-school/schemas/arena-eligibility.schema.json`,
  `mechanics/agon/parts/formation/schemas/resistance-revision.schema.json`,
  `generated/agent_agonic_formation_index.min.json`, and
  `mechanics/agon/parts/formation/examples/agent-agonic-formation.example.json`
- explicit Wave I validation lane:
  `mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py`,
  `mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py`, and
  `mechanics/agon/parts/formation/tests/test_agent_agonic_formation.py`

This turn keeps the base `agents/profiles/*.profile.json` files as legacy role
contracts while Wave I lands reviewed companion surfaces for agonic actor
readiness. It does not widen `schemas/agent-profile.schema.json`, does not
rewrite generated role registries, and does not start arena protocol, scars,
retention, runtime packets, or ToS promotion.

## Unreleased follow-on turn: Assistant Civil Rechartering

The next unreleased follow-on turn after Wave I is Wave II Assistant Civil
Rechartering. Its checked surface is:

- Wave II doctrine and landing docs:
  `mechanics/experience/parts/assistant-civil-service/docs/civil-rechartering.md`,
  `mechanics/agon/parts/formation/docs/wave2-landing.md`,
  `mechanics/experience/parts/assistant-civil-service/docs/assistant-kind-model.md`,
  `mechanics/experience/parts/assistant-civil-service/docs/service-identity-model.md`,
  `mechanics/experience/parts/assistant-civil-service/docs/service-contract-model.md`,
  `mechanics/experience/parts/assistant-civil-service/docs/service-governance-model.md`,
  `mechanics/experience/parts/assistant-civil-service/docs/service-certification-model.md`,
  `mechanics/experience/parts/arena-exclusion/docs/arena-exclusion-model.md`, and
  `mechanics/experience/parts/arena-exclusion/docs/escalation-to-agon.md`
- additive assistant companion source surfaces:
  `agents/profiles/adjuncts/assistant_variant/*.assistant.variant.json`,
  `agents/profiles/adjuncts/assistant_service_identity/*.assistant.identity.json`,
  `agents/profiles/adjuncts/assistant_service_contract/*.assistant.contract.json`,
  `agents/profiles/adjuncts/assistant_service_governance/*.assistant.governance.json`,
  `agents/profiles/adjuncts/assistant_service_certification/*.assistant.certification.json`, and
  `agents/profiles/adjuncts/assistant_arena_exclusion/*.assistant.arena_exclusion.json`
- Wave II companion contracts and publication:
  `mechanics/experience/parts/assistant-civil-service/schemas/assistant-variant.schema.json`,
  `mechanics/experience/parts/assistant-civil-service/schemas/service-identity.schema.json`,
  `mechanics/experience/parts/assistant-civil-service/schemas/service-contract.schema.json`,
  `mechanics/experience/parts/assistant-civil-service/schemas/service-governance.schema.json`,
  `mechanics/experience/parts/assistant-civil-service/schemas/service-certification.schema.json`,
  `mechanics/experience/parts/assistant-civil-service/schemas/civil-formation.schema.json`,
  `mechanics/experience/parts/arena-exclusion/schemas/arena-exclusion.schema.json`,
  `generated/assistant_civil_formation_index.min.json`, and
  `mechanics/experience/parts/assistant-civil-service/examples/civil-formation.example.json`
- explicit Wave II validation lane:
  `scripts/build_assistant_civil_formation_index.py`,
  `scripts/validate_assistant_civil_formation.py`,
  `scripts/validate_experience_assistant_civil_contracts.py`, and
  `tests/test_assistant_civil_formation.py` plus
  `tests/test_experience_assistant_civil_contracts.py`

This turn keeps assistant variants as civil/service forms anchored to the same
five role houses without widening the public role catalog, without granting
contestant or judge authority, and without pulling runtime packets, scars,
verdicts, durable incident logs, or ToS promotion into `aoa-agents`.

## Unreleased follow-on turn: Formation Trial

The next unreleased follow-on turn after Wave II is Wave II.5 Formation Trial.
Its checked surface is:

- Wave II.5 doctrine and landing docs:
  `mechanics/agon/parts/formation/docs/formation-trial.md`,
  `mechanics/agon/parts/pre-protocol-boundary/docs/pre-protocol-agent-boundary.md`,
  `mechanics/agon/parts/pre-protocol-boundary/docs/formation-trial-readiness.md`,
  `mechanics/codex-projection/parts/agon-boundary/docs/projection-agon-boundary.md`, and
  `mechanics/agon/parts/formation/docs/wave2-5-landing.md`
- Wave II.5 companion contract and publication:
  `mechanics/agon/parts/formation/schemas/formation-trial.schema.json`,
  `generated/agent_formation_trial.min.json`, and
  `mechanics/agon/parts/formation/examples/formation-trial.example.json`
- explicit Wave II.5 validation lane:
  `mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py`,
  `mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py`, and
  `mechanics/agon/parts/formation/tests/test_agent_formation_trial.py`

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
