# generated/AGENTS.md

## Purpose

`generated/` contains derived machine-readable surfaces published from the source-authored agent layer.

Use [README.md](README.md) as the reader-family index. This card owns edit law,
builder routes, and validation posture.

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
- `generated/quest_catalog.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_dispatch.min.example.json`
- `generated/cohort_composition_registry.json`
- `generated/runtime_seam_bindings.json`
- `generated/codex_agents/agents/*.toml`
- `generated/codex_agents/config.subagents.generated.toml`
- `generated/codex_agents/projection_manifest.json`

Mechanic-local generated companions are documented at their owning part.
The Alpha reference-route reader lives at
`mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json`
because it is derived only from that part's examples.
Agon rank/school/epistemic readers live under
`mechanics/agon/parts/*/generated/` because they are derived from Agon
part-local seed/config surfaces.
Recursor readiness, pair, projection, and boundary readers live under
`mechanics/recurrence/parts/*/generated/` because they are derived from
Recurrence part-local seed/config and contract surfaces.
Quest catalog and dispatch readers stay root-published because they summarize
root `quests/` source records for low-context consumers.
Formation readers stay root-published because they summarize `agents/` source
objects and feed repo-wide role readiness, while `mechanics/agon/` and
`mechanics/experience/` own the operation contracts and stop-lines around those
readers.

## Source layers

These files are derived from:

- `agents/profiles/`
- `agents/profiles/adjuncts/`
- `agents/model_tiers/`
- `agents/orchestrator_classes/`
- `agents/cohort_patterns/`
- `agents/runtime_seam/`
- `quests/`
- `mechanics/agon/parts/*/config/`
- `mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json`
- `mechanics/recurrence/parts/*/config/`
- `mechanics/titan/parts/*/config/`

## Editing posture

Do not hand edit anything under `generated/`.
Change the source-authored layer or the builder if regeneration is wrong.
Review diffs here as public contract deltas, not as arbitrary JSON churn.
For the Alpha reference-route generated reader, use
`scripts/generate_alpha_reference_routes.py`; the output is part-local under
`mechanics/questbook/parts/alpha-reference-routes/generated/`.
For Agon rank/school/epistemic generated readers, use their dedicated
`scripts/build_agon_*.py` builders; the outputs are part-local under the
owning Agon parts.
For recursor generated readers, use `scripts/build_recursor_role_readiness.py`,
`scripts/build_recursor_projection_candidates.py`, and
`scripts/validate_recursor_boundary.py`; the outputs are part-local under the
owning Recurrence parts.
For Questbook catalog and dispatch readers, use
`scripts/generate_questbook_readers.py`; the outputs are root-published under
`generated/`.
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
