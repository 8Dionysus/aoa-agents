# generated/AGENTS.md

## Purpose

`generated/` contains derived machine-readable surfaces published from the source-authored agent layer.

Use [README.md](README.md) as the reader-family index. This card owns edit law,
builder routes, and validation posture.

## Derived outputs

Current published outputs include:

- `generated/agent_registry.min.json`
- `generated/role_specialization_catalog.min.json`
- `generated/capability_pack_registry.min.json`
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
- `generated/titan_codex_agents/agents/*.toml`
- `generated/titan_codex_agents/projection_manifest.json`

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
Titan Codex projection readers stay root-published because they are Codex
custom-agent install companions, while `mechanics/titan/parts/codex-projection/`
owns their builder and freshness check.

## Source layers

These files are derived from:

- `agents/roles/`
- `agents/roles/*/specializations/`
- `agents/operating-model/capabilities/packs/`
- `agents/roles/*/forms/`
- `agents/operating-model/tiers/`
- `agents/operating-model/orchestrators/`
- `agents/operating-model/cohorts/`
- `agents/operating-model/runtime-seams/`
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
`mechanics/questbook/parts/alpha-reference-routes/scripts/generate_alpha_reference_routes.py`;
the output is part-local under
`mechanics/questbook/parts/alpha-reference-routes/generated/`.
For Agon rank/school/epistemic generated readers, use their dedicated
`scripts/build_agon_*.py` builders; the outputs are part-local under the
owning Agon parts.
For recursor generated readers, use `scripts/build_recursor_role_readiness.py`,
`scripts/build_recursor_projection_candidates.py`, and
`scripts/validate_recursor_boundary.py`; the outputs are part-local under the
owning Recurrence parts.
For Questbook catalog and dispatch readers, use
`mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py`;
the outputs are root-published under `generated/`.
For `generated/codex_agents/`, use
`mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py`
as the canonical builder and
`mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py`
as the freshness checker.
That projection is base-role-only: it derives from
`agents/roles/*/profile.json` plus projection wiring, while
`agents/roles/*/specializations/*/specialization.json` derives only into
`generated/role_specialization_catalog.min.json` in this slice.
For `generated/agent_agonic_formation_index.min.json`, use
`mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py`
as the canonical builder and
`mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py`
as the explicit agonic actor validator.
For `generated/assistant_civil_formation_index.min.json`, use
`mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py` as the canonical builder and
`mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py` as the explicit assistant civil
validator.
For `generated/agent_formation_trial.min.json`, use
`mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py` as
the canonical builder and
`mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py` as
the explicit formation-trial validator.
For `generated/role_specialization_catalog.min.json` and
`generated/capability_pack_registry.min.json`, use
`scripts/build_published_surfaces.py` as the canonical builder and
`scripts/validate_agents.py` as the explicit source/catalog validator.
For `generated/agent_registry.min.json`, `manifests/artifact_bundles/role_contract_registry.bundle.json`
adds the OS Abyss ABI/SLSA registry envelope. Validate that transport surface
with `python scripts/validate_abyss_machine_role_registry_bundle.py`; release
or export consumers must use the durable registry plus materialized subject
store trust-gate path. The generated registry remains subordinate to
`agents/roles/*/profile.json` and `agents/roles/AGENTS.md`.
For `generated/titan_codex_agents/`, use
`mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py`
as the canonical builder and freshness checker.

## Regenerate and validate

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

If the agonic actor generated index changed, also run:

```bash
python mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_agonic_formation.py
```

If the assistant civil generated index changed, also run:

```bash
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python -m pytest -q mechanics/experience/parts/assistant-civil-service/tests/test_assistant_civil_formation.py
```

If the formation-trial output changed, also run:

```bash
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_formation_trial.py
```

If Titan Codex projection output changed, also run:

```bash
python mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --out-dir generated/titan_codex_agents/agents --manifest generated/titan_codex_agents/projection_manifest.json --prune --check
python -m unittest discover -s mechanics/titan/parts/codex-projection/tests -p "test_*.py"
```

If Codex subagent projection output changed, also run:

```bash
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python -m unittest discover -s mechanics/codex-projection/parts/subagent-projection/tests -p "test_*.py"
```
