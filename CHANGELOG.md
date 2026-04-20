# Changelog

All notable changes to `aoa-agents` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

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

- `python scripts/release_check.py`

### Notes

- detailed checkpoint role follow-through, Codex subagent projection, and continuity changes for this patch remain enumerated below under `Added` and `Changed`

## [0.2.0] - 2026-04-10

### Summary

- this release adds checkpoint-growth role posture, antifragility/via-negativa adjuncts, and closeout-oriented follow-through skill surfaces
- progression-feed contracts, quest-schema validation, and role-posture wording are hardened across source-authored agent surfaces
- `aoa-agents` stays bounded to role contracts and execution posture rather than absorbing memo, eval, skill, or playbook ownership

### Validation

- `python scripts/release_check.py`

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

- source-authored role surfaces across `profiles/`, `cohort_patterns/`,
  `orchestrator_classes/`, `docs/`, `schemas/`, `examples/`, and `generated/`,
  including Phase Alpha cohort additions, orchestrator capsules, and
  progression-feed updates
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
- source-authored role, memory, evaluation, cohort, and runtime-seam docs across `CHARTER.md`, `docs/`, `profiles/`, `model_tiers/`, `cohort_patterns/`, and `runtime_seam/`
- published registries and consumer seams under `generated/agent_registry.min.json`, `generated/model_tier_registry.json`, `generated/cohort_composition_registry.json`, and `generated/runtime_seam_bindings.json`
- schema-backed runtime artifact examples and local validation helpers under `schemas/`, `examples/`, and `scripts/`

### Validation

- `python scripts/build_published_surfaces.py`
- `python scripts/validate_agents.py`

### Notes

- this release establishes the role layer as source-owned agent contract space, not as a replacement for skills, playbooks, memo objects, or eval doctrine
