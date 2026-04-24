# AGENTS.md

## Guidance for `config/`

`config/` holds build, registry, publication, and policy inputs for the agent role layer.

Config may affect generation or validation, but it must not define agent identity by stealth. Identity belongs in profiles, model tiers, orchestrator classes, cohort patterns, runtime seam docs, and schemas.

Keep config explicit, public-safe, and reviewable. Avoid private prompts, hidden allowlists, local-only paths, or unversioned assumptions.

When config changes generated surfaces, rebuild and inspect the diff against source-authored role contracts.

Verify with:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```
