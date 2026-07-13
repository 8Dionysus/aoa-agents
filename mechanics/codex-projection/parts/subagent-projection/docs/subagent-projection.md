# Codex Subagent Projection

## Purpose

This document explains how `aoa-agents` projects source-authored role profiles
into Codex custom-agent TOML files without turning the projection into a second
source of truth.

When repeated drift or stale generated/install surfaces show up around this
projection, use `mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md` as the owner refresh route.
That law stays subordinate to the same source profiles and wiring described
here.

## Boundary rule

Keep this order:

1. `agents/roles/*/profile.json`
2. `mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json`
3. generated `generated/codex_agents/agents/*.toml`
4. workspace install under `.codex/agents/`

If the projection drifts, the source profile and wiring win.

The active projection scope is `base_role_profiles_only`.
Role-local specializations under
`agents/roles/*/specializations/*/specialization.json` are source-layer actors
and catalog entries, not Codex custom-agent install entries. Promotion of a
specialization into `.codex/agents/` needs a new projection eligibility surface
that names the install identity, permission posture, refresh law, and owner
consent.
That surface now starts at
`mechanics/codex-projection/parts/specialization-eligibility/`, but it remains a
gate and does not widen this builder's projection scope.

## Decision

Use `aoa-agents` profiles as the only role-meaning source, project them into
generated Codex custom-agent files inside the repository, and install those
generated files into the workspace `.codex/agents/` surface.

Keep MCP server ownership in the workspace `.codex/config.toml` only.
The generated agent files may name MCP affinity in instructions, but they must
not duplicate project-level MCP server declarations.

## Wave 1 assistant projection resolver

Wave 1 adds one compact contract surface for the assistant projection
resolver and its no-self-rewrite posture:

- `mechanics/codex-projection/parts/assistant-projection/schemas/assistant-projection-resolver.schema.json`
- `mechanics/codex-projection/parts/assistant-projection/examples/assistant-projection-resolver.example.json`

The resolver keeps the following order explicit:

1. source profile
2. projection wiring
3. generated Codex agent files
4. workspace install surface

The no-self-rewrite posture stays separate from projection. Generated agents
may be refreshed by the owner repo, but they do not rewrite their own role
meaning, their source profile, or the projection law that produced them.

## Main alternatives rejected

- hand-authoring `/srv/AbyssOS/.codex/agents/*.toml` as if installed files were the
  role source of truth
- copying archive-pack fixtures straight into the workspace without regenerating
  from live `agents/roles/*/profile.json`
- duplicating MCP server definitions into every custom-agent TOML file

## Tradeoffs

This choice adds one explicit install step from repo-owned generated surfaces
into workspace `.codex/agents/`.

That extra step is worth keeping because it preserves one clear role-authoring
surface, one clear projection-wiring surface, and one clear workspace install
surface instead of mixing them together.

## What lives where

- `agents/roles/*/profile.json` owns role meaning.
- `agents/roles/*/specializations/*/specialization.json` owns narrower
  source-layer actor posture and publishes through the specialization catalog;
  it is not consumed by this projection.
- `mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json` owns projection-time Codex policy such
  as sandbox posture, nickname candidates, and MCP affinity guidance.
- `generated/codex_agents/agents/*.toml` is the generated Codex custom-agent
  surface.
- `generated/codex_agents/config.subagents.generated.toml` is the generated
  workspace registration snippet.
- `generated/codex_agents/projection_manifest.json` is the bounded downstream
  contract for consumers that need role projection metadata without taking over
  role meaning or workspace MCP ownership.
- workspace `.codex/config.toml` keeps the final project-scoped registration.

## Current mapping

The current base-role projection keeps the AoA role seed narrow:

- `architect` -> read-only
- `coder` -> workspace-write
- `reviewer` -> read-only
- `evaluator` -> read-only
- `memory-keeper` -> read-only

The generated agents keep MCP affinity in their instructions instead of
duplicating project-level MCP server definitions in every agent file.

The projection manifest may repeat bounded planning fields such as
`sandbox_mode`, `nickname_candidates`, `mcp_affinity`, and config-relative
`config_path` so neighboring control-plane consumers can plan against the same
projection wiring without treating installed `.codex/agents/` files as source
truth.

## Build and validate

Generate the projection:

Validate the committed projection:

## Workspace install posture

Treat `generated/codex_agents/` as the repo-owned published seam and
`.codex/agents/` as the project install surface.

Install by copying the generated TOML files into the workspace root and merging
the generated config snippet into the workspace `.codex/config.toml`.

Keep role-bearing work explicit.
Custom agents are role actors, not hidden recursive autonomy.
