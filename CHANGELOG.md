# Changelog

All notable changes to `aoa-agents` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

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
