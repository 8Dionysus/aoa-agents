# Changelog

All notable changes to `aoa-agents` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

### Fixed

- Experience assistant civil validation now enforces the exact arena-exclusion
  example file set alongside the arena schema file set.
- Current contour now routes Titan Codex projection outputs through the full
  generated agents wildcard instead of publishing only `Atlas.toml`.

## [0.4.0] - 2026-05-31

### Summary

- This release turns `aoa-agents` into a checked role-layer topology: source
  role objects live under `agents/`, repeatable operation pressure lives under
  `mechanics/`, generated readers stay derived, and root documents stay compact
  route cards instead of inventories.
- The release reconciles the full `v0.2.3..HEAD` span: 124 first-parent
  commits, 58 canonical decision records, 43 local memo candidates, 25 portable
  skill surfaces, 12 mechanics packages, and 63 mechanics parts.
- `aoa-agents` remains the role, bearer, handoff, formation, projection, and
  checkpoint-contract layer. It still does not own skills, proof verdicts,
  durable memory truth, routing policy, playbooks, stats, KAG, or runtime
  behavior.

### Added

- A source-authored `agents/` home with five base role houses, companion form
  branches, role specializations, capability packs, model tiers, orchestrator
  classes, cohort patterns, runtime seam bindings, local route cards, and
  `agents/source_home.manifest.json`.
- Five candidate-only role specializations and matching capability packs:
  topology steward, repo refactor, release readiness, route drift review, and
  writeback steward.
- A package-shaped `mechanics/` atlas for Agon, Antifragility,
  Boundary Bridge, Checkpoint, Codex Projection, Experience, Questbook,
  Recurrence, Release Support, RPG, Runtime Seam, and Titan role-layer
  operations.
- Localized mechanics parts for formation, arena/rank/school posture,
  epistemic actor posture, assistant civil service, adoption/regression,
  runtime release holds, stress posture, checkpoint posture, quest readers,
  recurrence readers, runtime artifacts, Titan role-bearing, and release
  support.
- Codex projection infrastructure for source-owned subagent projection,
  refresh-law validation, assistant projection, Titan projection, and
  specialization eligibility records.
- Generated readers and registries for agent profiles, agonic formation,
  assistant civil formation, formation trials, role specializations,
  capability packs, model tiers, orchestrators, cohorts, runtime seam bindings,
  quest catalogs, quest dispatch, Codex agents, Titan Codex agents, and
  specialization eligibility readiness.
- A local `memo/` port with candidate, receipt, export, local, and compact
  index surfaces so role-layer decisions can be handed toward reviewed memory
  without claiming durable memory authority.
- Canonical `AOA-AG-D-####` decision records and generated lookup indexes by
  number, date, surface, agent facet, mechanic parent, and guard family.
- A portable `.agents/` skill foundation and the maintained Spark lane under
  `.agents/spark`.

### Changed

- Root documents were refactored into a compact entry contour: `README.md`,
  `AGENTS.md`, `CHARTER.md`, `DESIGN.md`, `DESIGN.AGENTS.md`, `ROADMAP.md`,
  `docs/README.md`, `docs/BOUNDARIES.md`, and `docs/CURRENT_CONTOUR.md` now
  have separated jobs instead of duplicating ledgers.
- Validation command authority was moved back to `AGENTS.md` route cards; other
  root-facing documents route to the owner surface instead of carrying command
  blocks.
- The roadmap and current contour now route shipped inventories to source
  homes, package READMEs, generated readers, and decision records instead of
  expanding root prose.
- Role-level memory posture now routes reviewed recall through `aoa-memo`
  object ids/read models and local writeback through `memo/` candidates,
  receipts, and exports.
- The `aoa_memo` MCP access-plane boundary is named for agent roles: brief and
  search, validation, local candidate work, and landing-plan dry-runs can
  support reviewed handoff, but they do not grant durable memory authority.
- Source/generated separation is stricter: builders own generated readers,
  generated readers remain evidence, and source role objects remain the
  authority.
- Codex custom-agent projection stays `base_role_profiles_only`; role
  specializations are visible through source and generated catalogs but remain
  candidate-only until eligibility records authorize projection.
- Mechanics packages now carry their own `AGENTS.md`, `PARTS.md`, provenance,
  legacy, scripts, schemas, examples, tests, and generated read models where
  applicable.
- Release validation is broader: the repository release gate now includes
  decision-index parity, source-home validation, semantic AGENTS checks,
  localized mechanics checks, published-surface generation, and generated drift
  detection.
- Workspace paths and repo-local route cards now target the `/srv/AbyssOS`
  workspace posture.

### Moved Or Retired

- Maintained Spark route surfaces moved under `.agents/spark`.
- Active root and mechanics legacy names were cleaned so old compatibility
  names do not appear as live owner surfaces.
- Date-prefixed decision lookup files were retired in favor of canonical
  `AOA-AG-D-####` paths and generated indexes.
- Mechanics docs, configs, examples, schemas, scripts, and tests that were
  previously root-adjacent or loosely grouped were localized under the owning
  package and part.
- Historical mechanics payloads now route through package-local provenance and
  legacy surfaces instead of acting like current authority.

### Validation

- Release validation is owned by the root `AGENTS.md` route and the
  `scripts/release_check.py` release gate.
- This release note was manually reconciled from the `v0.2.3..HEAD`
  first-parent history, canonical decision records, current source trees,
  generated registries, memo candidates, and the root-document follow-up that
  keeps validation command blocks in `AGENTS.md` route cards.

### Notes

- `v0.4.0` intentionally bundles the source-home, mechanics-localization,
  projection, memo-port, and root-contour work into one release line instead of
  treating each route repair as a separate public milestone.
- Release command examples stay in `AGENTS.md` route cards. This changelog
  records what shipped and how the release was reconciled.
- The release does not promote specializations into installed Codex agents and
  does not promote local memo candidates into durable memory truth.

## [0.2.3] - 2026-04-23

### Summary

- this patch lands Agon actor, assistant, and formation-trial posture from
  agonic/civil recharter waves through formation trials, recurrence actor
  formation, rank jurisdiction, schools, lineages, campaigns, and Wave XV
  actor posture
- recursor readiness, Titan service-cohort lineage, Titan bearer reservations,
  Titan incarnation identity, and Experience assistant projection, release,
  certification, adoption, governance, and office posture are added or
  tightened
- `aoa-agents` remains the role, bearer, and handoff-contract layer rather
  than a skill, runtime, memo, proof, or routing owner

### Added

- Wave I Agonic Actor Rechartering doctrine, companion adjunct surfaces, and
  explicit formation-index builder / validator / test lane
- Wave II Assistant Civil Rechartering doctrine, companion adjunct surfaces,
  and explicit assistant-formation builder / validator / test lane
- Wave II.5 Formation Trial doctrine, pre-protocol boundary docs, and explicit
  formation-trial builder / validator / test lane
- Agon recurrence actor-formation manifests, recursor role readiness seeds,
  rank-jurisdiction and schools/lineages/campaign posture, Wave XV actor
  posture, and assistant/actor boundary docs for arena eligibility,
  escalation, retention readiness, campaign boundaries, and epistemic/rank
  separation
- Titan service-cohort lineage, Titan bearer reservations, Titan role classes,
  Titan lineage ledger, and Titan incarnation identity/session surfaces
- Experience assistant projection, assistant release, certification,
  deployment/watch, adoption, governance, rollback, office, service identity,
  service contract, incident reentry, and post-release behavior posture
  surfaces

### Changed

- README, docs map, roadmap, and local guidance now distinguish legacy role
  contracts from landed agonic companion surfaces without widening the base
  profile schema or the current release baseline
- role-facing guidance now also distinguishes assistant civil/service variants
  from agonic actors without widening the public role catalog or the base
  profile schema
- route and generated-surface guidance now also expose the first formation
  trial as a pre-protocol readability judgment rather than hidden future lore
- formation-trial guards, recursor readiness schemas, exact role-set checks,
  adoption contract guards, assistant-service boundary checks, and Titan
  incarnation session identifiers were tightened

### Validation

- Validated through the repository release gate plus the Agon formation,
  assistant civil formation, and formation-trial builder/validator/test lanes
  that are now routed from owner `AGENTS.md` cards.

### Notes

- this patch strengthens role-bearing surfaces and incarnation lineage without
  making agent profiles executable skills, runtime ledgers, or memory truth

## [0.2.2] - 2026-04-19

### Summary

- this patch adds recurrence-aware Codex subagent projection,
  reviewed-closeout role posture holds, and richer SDK planning metadata
- memory-rights transitions and pre-Agon boundary wording are tightened
  without widening agent-layer ownership
- `aoa-agents` remains the bounded role-contract and execution-posture layer

### Added

- a recurrence manifest for Codex subagent projection, Codex projection
  metadata for SDK planning, and reviewed closeout role posture hold notes

### Changed

- memory-rights validation, memo reviewed-candidate adoption seams,
  pre-Agon preparation boundaries, and CI/protection surfaces are tightened
  for the current role wave

### Validation

- Validated through the repository release gate for the `v0.2.2` line.

### Notes

- this patch strengthens role-bearing execution posture while keeping routing,
  runtime, and memo authority in sibling repositories

## [0.2.1] - 2026-04-12

### Summary

- this patch lands checkpoint role follow-through, Codex subagent projection,
  and self-agency continuity posture updates
- continuity-anchor validation is tightened without widening the role layer
  beyond agent posture and contracts
- `aoa-agents` stays bounded to role-bearing execution semantics

### Added

- checkpoint role follow-through quest capture, Codex subagent projection
  surfaces, and the self-agency continuity lane contract.

### Changed

- continuity-anchor validation and adjacent role-posture wording are tightened
  across the current continuity wave.

### Validation

- Validated through the repository release gate for the `v0.2.1` line.

### Notes

- detailed checkpoint role follow-through, Codex subagent projection, and continuity changes for this patch remain enumerated below under `Added` and `Changed`

## [0.2.0] - 2026-04-10

### Summary

- this release adds checkpoint-growth role posture, antifragility/via-negativa adjuncts, and closeout-oriented follow-through skill surfaces
- progression-feed contracts, quest-schema validation, and role-posture wording are hardened across source-authored agent surfaces
- `aoa-agents` stays bounded to role contracts and execution posture rather than absorbing memo, eval, skill, or playbook ownership

### Validation

- Validated through the repository release gate for the `v0.2.0` line.

### Notes

- detailed profile, cohort, orchestrator, and generated-surface coverage for this release remains enumerated below under `Added`, `Changed`, and `Included in this release`

### Added

- workspace checkpoint growth role posture, progression feed surfaces, and
  role-focused follow-through quest capture
- third-wave antifragility stress adjuncts, workspace surface-trigger posture,
  and a via negativa checklist for the agent layer
- checkpoint closeout bridge install plus repo-local project-foundation and
  session-harvest skill surfaces for agent-owned closeout follow-through

### Changed

- tightened progression-feed contracts, quest schema validation, and d3
  contract role-posture wording across source-authored agent surfaces
- clarified verify paths and adjunct routing around generated registries,
  runtime seams, and checkpoint posture

### Included in this release

- source-authored role surfaces across legacy root family directories, `docs/`,
  `schemas/`, `examples/`, and `generated/`, including Phase Alpha cohort
  additions, orchestrator capsules, and progression-feed updates
- repo-local quest, follow-through, and validation surfaces under `.agents/`,
  `.github/`, `QUESTBOOK.md`, `quests/`, `AGENTS.md`, `README.md`, `scripts/`,
  and `tests/`, including quest harvest, project-foundation installs, and
  stricter external quest-schema handling

## [0.1.0] - 2026-04-01

First public baseline release of `aoa-agents` as the role and persona layer in the AoA public surface.

This changelog entry uses the release-prep merge date.

### Summary

- first public baseline release of `aoa-agents` as the repository that owns role contracts, handoff posture, memory posture, evaluation posture, and model-tier guidance at the agent layer
- the current public surface now ships `5` source-authored agent profiles, `7` model tiers, `4` cohort patterns, and `7` runtime seam bindings together with generated registries and consumer seams
- this release keeps the agent layer bounded: an agent remains a role-bearing actor that uses adjacent skill, memo, eval, and playbook layers without absorbing their meaning

### Added

- community-docs baseline established for this repository
- `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`
- source-authored role, memory, evaluation, cohort, and runtime-seam docs across `CHARTER.md`, `docs/`, and legacy root family directories
- published registries and consumer seams under `generated/agent_registry.min.json`, `generated/model_tier_registry.json`, `generated/cohort_composition_registry.json`, and `generated/runtime_seam_bindings.json`
- schema-backed runtime artifact examples and local validation helpers under `schemas/`, `examples/`, and `scripts/`

### Validation

- Validated through the baseline generated-surface build and agent-validation
  routes now owned by `AGENTS.md` cards.

### Notes

- this release establishes the role layer as source-owned agent contract space, not as a replacement for skills, playbooks, memo objects, or eval doctrine
