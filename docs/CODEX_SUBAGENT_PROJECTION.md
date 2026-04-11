# CODEX_SUBAGENT_PROJECTION

## Purpose

This document explains how `aoa-agents` projects source-authored role profiles
into Codex custom-agent TOML files without turning the projection into a second
source of truth.

## Boundary rule

Keep this order:

1. `profiles/*.profile.json`
2. `config/codex_subagent_wiring.v2.json`
3. generated `generated/codex_agents/agents/*.toml`
4. workspace install under `.codex/agents/`

If the projection drifts, the source profile and wiring win.

## Decision

Use `aoa-agents` profiles as the only role-meaning source, project them into
generated Codex custom-agent files inside the repository, and install those
generated files into the workspace `.codex/agents/` surface.

Keep MCP server ownership in the workspace `.codex/config.toml` only.
The generated agent files may name MCP affinity in instructions, but they must
not duplicate project-level MCP server declarations.

## Main alternatives rejected

- hand-authoring `/srv/.codex/agents/*.toml` as if installed files were the
  role source of truth
- copying archive-pack fixtures straight into the workspace without regenerating
  from live `profiles/*.profile.json`
- duplicating MCP server definitions into every custom-agent TOML file

## Tradeoffs

This choice adds one explicit install step from repo-owned generated surfaces
into workspace `.codex/agents/`.

That extra step is worth keeping because it preserves one clear role-authoring
surface, one clear projection-wiring surface, and one clear workspace install
surface instead of mixing them together.

## What lives where

- `profiles/*.profile.json` owns role meaning.
- `config/codex_subagent_wiring.v2.json` owns projection-time Codex policy such
  as sandbox posture, nickname candidates, and MCP affinity guidance.
- `generated/codex_agents/agents/*.toml` is the generated Codex custom-agent
  surface.
- `generated/codex_agents/config.subagents.generated.toml` is the generated
  workspace registration snippet.
- workspace `.codex/config.toml` keeps the final project-scoped registration.

## Current mapping

The current projection keeps the AoA role seed narrow:

- `architect` -> read-only
- `coder` -> workspace-write
- `reviewer` -> read-only
- `evaluator` -> read-only
- `memory-keeper` -> read-only

The generated agents keep MCP affinity in their instructions instead of
duplicating project-level MCP server definitions in every agent file.

## Build and validate

Generate the projection:

```bash
python scripts/build_codex_subagents_v2.py
```

Validate the committed projection:

```bash
python scripts/validate_codex_subagents.py \
  --profiles-root profiles \
  --wiring config/codex_subagent_wiring.v2.json \
  --agents-dir generated/codex_agents/agents \
  --config-snippet generated/codex_agents/config.subagents.generated.toml \
  --manifest generated/codex_agents/projection_manifest.json
```

## Workspace install posture

Treat `generated/codex_agents/` as the repo-owned published seam and
`.codex/agents/` as the project install surface.

Install by copying the generated TOML files into the workspace root and merging
the generated config snippet into the workspace `.codex/config.toml`.

Keep role-bearing work explicit.
Custom agents are role actors, not hidden recursive autonomy.
