# AGENTS.md

## Guidance for `config/`

`config/` is reserved for repository-level build, registry, publication, and
policy inputs for the agent role layer.

Mechanic-specific seeds and wiring now live in part-local routes under
`mechanics/*/parts/*/config/`. Use those active part routes first when the
pressure belongs to Agon, recurrence, Codex projection, or Titan role-bearing.

Config may affect generation or validation, but it must not define agent identity by stealth. Identity belongs in profiles, model tiers, orchestrator classes, cohort patterns, runtime seam docs, and schemas.

Keep config explicit, public-safe, and reviewable. Avoid private prompts, hidden allowlists, local-only paths, or unversioned assumptions.

When repository-level config changes generated surfaces, rebuild and inspect
the diff against source-authored role contracts. When mechanic-local config
changes, use the owning mechanic package and part validator.

Verify with:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
