# 2026-05-26: Titan Codex Projection Builder Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0012
- Original date: 2026-05-26
- Surface classes: mechanic part
- Agent facets: mechanics atlas, titan role-bearing
- Mechanic parents: titan, codex-projection
- Guard families: part-local artifact
- Posture: accepted

## Context

Titan role classes, bearers, lineage, schemas, examples, and package checks now
live under `mechanics/titan/parts/` or `mechanics/titan/`. The remaining root
Titan-specific script rendered Codex custom-agent companions from Titan
part-local role-bearing config into `generated/titan_codex_agents/`.

The output is root-published because it is a consumer/install seam. The
operation itself is Titan-specific: it reads named bearer records, role-class
records, and the Titan identity law that Codex-visible custom agents should be
Atlas, Sentinel, Mneme, Forge, and Delta rather than generic role class names.

External agent-building guidance also points toward an explicit operation map:
role, input, output, owner, tools, and validation. That favors a part-local
builder with a check mode over a root script whose owner must be inferred from
its file name.

Reference inputs:

- Anthropic, "Building effective agents": prefer simple composable patterns
  whose control flow is legible.
- OpenAI, "A practical guide to building AI agents": agent behavior is shaped
  by model, tools, instructions, and guardrails.
- MCP server concepts: separate data/resources, action/tools, prompts, and
  access roots instead of blending them into one surface.

## Decision

Move the Titan Codex projection builder into:

- `mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py`

Add `--check` mode so release and part tests can prove the root-published
generated TOML and manifest are current without rewriting them.

Keep generated companions in:

- `generated/titan_codex_agents/agents/*.toml`
- `generated/titan_codex_agents/projection_manifest.json`

because those are published consumer surfaces, not source truth.

## Consequences

- `mechanics/titan/parts/codex-projection/` becomes the active owner for Titan
  Codex projection behavior.
- `generated/` remains the edit-law owner for derived published outputs.
- `scripts/validate_agents.py` rejects the former root builder path.
- `scripts/release_check.py` checks Titan Codex projection freshness and runs
  the part-local tests.
- The projection test fixes the named-bearer contract so generic class TOML
  names such as `architect.toml`, `reviewer.toml`, or `memory-keeper.toml` do
  not return through this route.

## Verification

Verification routes through the focused owner checks and the repository release gate.
