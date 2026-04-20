# generated/AGENTS.md

## Purpose

`generated/` contains derived machine-readable surfaces published from the source-authored agent layer.

## Derived outputs

Current published outputs include:

- `generated/agent_registry.min.json`
- `generated/agent_agonic_formation_index.min.json`
- `generated/assistant_civil_formation_index.min.json`
- `generated/agent_formation_trial.min.json`
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
- `profiles/adjuncts/`
- `model_tiers/`
- `orchestrator_classes/`
- `cohort_patterns/`
- `runtime_seam/`
- `config/codex_subagent_wiring.v2.json`

## Editing posture

Do not hand edit anything under `generated/`.
Change the source-authored layer or the builder if regeneration is wrong.
Review diffs here as public contract deltas, not as arbitrary JSON churn.
For `generated/agent_agonic_formation_index.min.json`, use
`scripts/build_agent_agonic_formation_index.py` as the canonical builder and
`scripts/validate_agent_agonic_formation.py` as the explicit Wave I validator.
For `generated/assistant_civil_formation_index.min.json`, use
`scripts/build_assistant_civil_formation_index.py` as the canonical builder and
`scripts/validate_assistant_civil_formation.py` as the explicit Wave II
validator.
For `generated/agent_formation_trial.min.json`, use
`scripts/build_agent_formation_trial.py` as the canonical builder and
`scripts/validate_agent_formation_trial.py` as the explicit Wave II.5
validator.

## Regenerate and validate

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

If the Agon Wave I generated index changed, also run:

```bash
python scripts/build_agent_agonic_formation_index.py --check
python scripts/validate_agent_agonic_formation.py
python -m pytest -q tests/test_agent_agonic_formation.py
```

If the Agon Wave II generated index changed, also run:

```bash
python scripts/build_assistant_civil_formation_index.py --check
python scripts/validate_assistant_civil_formation.py
python -m pytest -q tests/test_assistant_civil_formation.py
```

If the Agon Wave II.5 formation-trial output changed, also run:

```bash
python scripts/build_agent_formation_trial.py --check
python scripts/validate_agent_formation_trial.py
python -m pytest -q tests/test_agent_formation_trial.py
```
