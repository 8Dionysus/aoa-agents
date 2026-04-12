# CODEX_SUBAGENT_REFRESH_LAW

## Purpose

This document is the owner refresh law for
`component:codex-subagents:projection`.

Use it when source-authored profiles and projection wiring stay intact but the
generated Codex custom-agent files, projection manifest, or workspace install
seam drift, repeat the same repair, or block adjacent routes.

## Boundary

Keep this order:

1. `profiles/*.profile.json`
2. `config/codex_subagent_wiring.v2.json`
3. generated projection surfaces under `generated/codex_agents/`
4. workspace install under `.codex/agents/` and workspace registration in
   `.codex/config.toml`

If the component drifts, source profiles and projection wiring win.

This law complements `CODEX_SUBAGENT_PROJECTION.md`. It does not make
`aoa-agents` the owner of workspace MCP declarations, a hidden auto-mutator,
or a second runtime authority.

## Component scope

- `component_ref`: `component:codex-subagents:projection`
- `owner_repo`: `aoa-agents`
- source-authored inputs:
  - `profiles/*.profile.json`
  - `config/codex_subagent_wiring.v2.json`
- generated surfaces:
  - `generated/codex_agents/agents/*.toml`
  - `generated/codex_agents/config.subagents.generated.toml`
  - `generated/codex_agents/projection_manifest.json`
- projected or installed surfaces:
  - `.codex/agents/`
- followthrough home:
  - `aoa-playbooks:component-refresh-cycle`

## Drift signals

- `profile_changed_without_projection_refresh`
  - drift class: `projection_drift`
  - meaning: source profiles changed while generated Codex agents stayed stale
  - recommended route class: `regenerate`
- `wiring_drift_detected`
  - drift class: `wiring_drift`
  - meaning: projection wiring and generated agent surfaces no longer agree
  - recommended route class: `regenerate`
- `workspace_install_projection_stale`
  - drift class: `install_drift`
  - meaning: generated repo-side projection and installed workspace agents no
    longer match
  - recommended route class: `reproject`
- `codex_subagent_validation_failed`
  - drift class: `validation_drift`
  - meaning: repo validation found projection or manifest mismatch
  - recommended route class: `repair`
- `boundary_mismatch_repeated`
  - drift class: `manual_repeat`
  - meaning: the same nickname, boundary, or install mismatch was repaired by
    hand more than once
  - recommended route class: `regenerate`

## Refresh routes

- check:
  - `python scripts/validate_agents.py`
  - `python scripts/validate_codex_subagents.py --profiles-root profiles --wiring config/codex_subagent_wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json`
- execute:
  - `python scripts/build_published_surfaces.py`
  - `python scripts/build_codex_subagents_v2.py`
- validate:
  - `python scripts/validate_agents.py`
  - `python scripts/validate_codex_subagents.py --profiles-root profiles --wiring config/codex_subagent_wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json`
  - `python -m pytest -q tests`

Use `repair` only for a bounded owner fix that keeps source authorship in
`profiles/` or wiring config. Use `regenerate` or `reproject` when generated or
installed surfaces drift.

## Proof and rollback

Proof commands:

- `python scripts/validate_agents.py`
- `python scripts/validate_codex_subagents.py --profiles-root profiles --wiring config/codex_subagent_wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json`
- `python -m pytest -q tests`

Rollback anchors:

- `docs/CODEX_SUBAGENT_PROJECTION.md`
- `config/codex_subagent_wiring.v2.json`
- `generated/codex_agents/config.subagents.generated.toml`
- `generated/codex_agents/projection_manifest.json`

Refresh window:

- `stale_after_days`: `7`
- `repeat_trigger_threshold`: `2`
- `open_window_days`: `5`

## Negative rules

- Do not hand-author workspace `.codex/agents/*.toml` as role truth.
- Do not treat installed workspace agents as a second authoring layer.
- Do not duplicate project-level MCP server declarations into every generated
  agent TOML.
- Do not rewrite role meaning just to preserve a stale projection.
- Do not turn repeated projection refresh into hidden recursive autonomy.
