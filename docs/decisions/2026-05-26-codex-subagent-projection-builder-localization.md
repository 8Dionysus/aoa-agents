# 2026-05-26: Codex Subagent Projection Builder Localization

## Status

Accepted.

## Context

Codex subagent projection docs and wiring config already live under
`mechanics/codex-projection/parts/subagent-projection/`, but the builder,
projection module, validator, and focused tests still lived in root execution
districts. Those files protect one mechanic part: projecting active
`agents/roles/*/profile.json` records plus part-local wiring into the
root-published `generated/codex_agents/` install seam.

The generated output remains repo-wide because it is a consumer-facing Codex
custom-agent surface. The operation itself belongs with the projection part
that owns the source wiring and refresh law.

External agent-building guidance favors explicit operating maps: role, input,
output, owner, tools, and validation. Keeping the builder and validator beside
the part-local config makes that map visible without hiding the published
generated output.

Reference inputs:

- Anthropic, "Building effective agents": keep agent systems legible through
  simple composable patterns.
- OpenAI, "A practical guide to building AI agents": agents combine model,
  tools, instructions, and guardrails.
- MCP server concepts: separate tools, resources, prompts, and access roots
  instead of blending source, action, and output into one surface.

## Decision

Move Codex subagent projection behavior into:

- `mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py`
- `mechanics/codex-projection/parts/subagent-projection/scripts/codex_subagent_projection.py`
- `mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py`
- `mechanics/codex-projection/parts/subagent-projection/tests/test_codex_subagent_projection.py`

Keep generated companions in:

- `generated/codex_agents/agents/*.toml`
- `generated/codex_agents/config.subagents.generated.toml`
- `generated/codex_agents/projection_manifest.json`

because those are published consumer surfaces, not source truth.

## Consequences

- `mechanics/codex-projection/parts/subagent-projection/` becomes the active
  owner for Codex subagent projection behavior.
- `generated/` remains the edit-law owner for derived published outputs.
- `scripts/build_published_surfaces.py` and `scripts/validate_agents.py` remain
  repo-wide coordinators and import the part-local projection module.
- `scripts/validate_agents.py` rejects the former root builder, module,
  validator, and focused test paths.
- `scripts/release_check.py` runs the part-local projection tests explicitly.

## Verification

```bash
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python -m unittest discover -s mechanics/codex-projection/parts/subagent-projection/tests -p "test_*.py"
python scripts/validate_agents.py
python scripts/release_check.py
```
