# generated/AGENTS.md

## Purpose

`generated/` contains derived machine-readable surfaces published from the source-authored agent layer.

## Derived outputs

Current published outputs include:

- `generated/agent_registry.min.json`
- `generated/model_tier_registry.json`
- `generated/orchestrator_class_catalog.min.json`
- `generated/orchestrator_class_capsules.json`
- `generated/orchestrator_class_sections.full.json`
- `generated/cohort_composition_registry.json`
- `generated/runtime_seam_bindings.json`
- `generated/codex_agents/agents/*.toml`
- `generated/codex_agents/config.subagents.generated.toml`
- `generated/codex_agents/projection_manifest.json`

## Source layers

These files are derived from:

- `profiles/`
- `model_tiers/`
- `orchestrator_classes/`
- `cohort_patterns/`
- `runtime_seam/`
- `config/codex_subagent_wiring.v2.json`

## Editing posture

Do not hand edit anything under `generated/`.
Change the source-authored layer or the builder if regeneration is wrong.
Review diffs here as public contract deltas, not as arbitrary JSON churn.

## Regenerate and validate

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```
