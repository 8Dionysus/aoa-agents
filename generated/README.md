# Generated Reader Index

`generated/` stores repo-wide derived reader surfaces for `aoa-agents`.

These files help agents and tooling scan source-authored role objects, quest
records, tier registries, orchestrator classes, cohort hints, runtime seam
bindings, and Codex projection outputs while preserving authored source
ownership.

## Operating Card

| Field | Route |
| --- | --- |
| role | repo-wide generated reader index |
| input | agent source objects, quest records, mechanic part payloads, and builder outputs |
| output | reader family route, source owner route, builder route, or validation route |
| owner | source surfaces and builders own truth; `generated/AGENTS.md` owns edit law |
| next route | source family, quest record, mechanic part, builder, validator, or route card |
| tools | published-surface builder, formation builders, quest readers, projection builders |
| validation | [generated/AGENTS.md#regenerate-and-validate](AGENTS.md#regenerate-and-validate) and source-owner checks |

## Current Root Readers

| Reader | Source shape | Builder or guard |
| --- | --- | --- |
| `generated/agent_registry.min.json` | base role profiles under `agents/roles/*/profile.json` | `scripts/build_published_surfaces.py` |
| `generated/agent_agonic_formation_index.min.json` | agonic form source records under `agents/roles/*/forms/agonic/` | `mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py` |
| `generated/assistant_civil_formation_index.min.json` | assistant form source records under `agents/roles/*/forms/assistant/` | `mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py` |
| `generated/agent_formation_trial.min.json` | base profiles plus agonic and assistant formation readers | `mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py` |
| `generated/model_tier_registry.json` | model-tier source records under `agents/operating-model/tiers/` | `scripts/build_published_surfaces.py` |
| `generated/orchestrator_class_catalog.min.json` | orchestrator-class source records under `agents/operating-model/orchestrators/` | `scripts/build_published_surfaces.py` |
| `generated/orchestrator_class_capsules.json` | orchestrator-class source records under `agents/operating-model/orchestrators/` | `scripts/build_published_surfaces.py` |
| `generated/orchestrator_class_sections.full.json` | orchestrator-class source records under `agents/operating-model/orchestrators/` | `scripts/build_published_surfaces.py` |
| `generated/cohort_composition_registry.json` | cohort source records under `agents/operating-model/cohorts/` | `scripts/build_published_surfaces.py` |
| `generated/runtime_seam_bindings.json` | runtime seam source bindings under `agents/operating-model/runtime-seams/` | `scripts/build_published_surfaces.py` |
| `generated/quest_catalog.min.json` | source quest records under `quests/` | `mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py` |
| `generated/quest_dispatch.min.json` | source quest records under `quests/` | `mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py` |
| `generated/quest_catalog.min.example.json` | public-safe quest catalog shape | `mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py` |
| `generated/quest_dispatch.min.example.json` | public-safe quest dispatch shape | `mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py` |
| `generated/codex_agents/` | Codex subagent projection from profile source objects and projection wiring | `mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py` |
| `generated/titan_codex_agents/` | Titan Codex projection from Titan part-local source payloads | `mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py` |

## Part-Local Generated Companions

Some generated companions live below the mechanic part that owns the operation:

- Alpha reference-route reader:
  `mechanics/questbook/parts/alpha-reference-routes/generated/`;
- Agon rank, school, and epistemic readers:
  `mechanics/agon/parts/*/generated/`;
- Recursor readiness, projection, and boundary readers:
  `mechanics/recurrence/parts/*/generated/`.

Part-local generated output stays weaker than the part-local source surfaces,
schemas, examples, configs, and builders.

## Read Chain

Use generated readers in this order:

```text
question or tool route
-> generated reader
-> agent source object, quest record, or mechanic part
-> source owner surface
-> validator or builder check
```

Generated readers answer "where should I look next?" Source surfaces answer
"what is true?" after the reader returns the agent to the owner path.
