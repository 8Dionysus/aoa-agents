# 2026-05-26: Agents Convex Source Tree

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0052
- Original date: 2026-05-26
- Surface classes: agent source, root/topology, generated/readout
- Agent facets: source-home, role contract
- Mechanic parents: agon, codex-projection, experience, runtime-seam
- Guard families: source topology, generated/read-model
- Posture: accepted

## Context

The first `agents/` source-home pass created a checked manifest and moved
agent-layer inputs away from the repository root. That solved the district
boundary, but the active tree still read as a flat family list: profiles,
adjuncts, tiers, orchestrator classes, cohorts, and runtime seams sat beside
each other even though they answer different questions.

The sibling refactors in `Agents-of-Abyss`, `aoa-memo`, `aoa-evals`,
`aoa-skills`, and `aoa-techniques` do not share one folder template. Their
common rule is stronger: each organ grows a tree around its real owner shape.
For `aoa-agents`, the owner shape is role-bearing agents plus the cross-role
operating model that lets those roles be read and projected.

## Decision

Make `agents/` convex and owner-shaped:

- `agents/roles/<role>/profile.json` is the base source record for one role.
- `agents/roles/<role>/forms/agonic/*.json` holds the role's agonic companion
  forms.
- `agents/roles/<role>/forms/assistant/*.json` holds the role's assistant civil
  forms.
- `agents/operating-model/tiers/` holds cross-role effort tier records.
- `agents/operating-model/orchestrators/` holds orchestrator class records.
- `agents/operating-model/cohorts/` holds cohort pattern records.
- `agents/operating-model/runtime-seams/` holds runtime-seam binding records.

The manifest, schemas, builders, validators, generated readers, and route cards
must use these paths as the active source topology. The former type-first
directories are not active source homes.

## Consequences

- A role can now be inspected as one house: base profile, agonic forms, and
  assistant forms are neighbors under the role that owns them.
- Cross-role operating contracts stay separate from role houses, so tiers,
  orchestrators, cohorts, and runtime-seam bindings do not masquerade as role
  identity.
- Builders and validators must traverse by owner shape instead of assuming
  one flat directory per object kind.
- Legacy source path names are noise in active docs, tests, validators, and
  generated route cards. If historical notes mention them, they should be
  clearly historical or superseded.
- Generated reader wire shapes may stay stable, but their source path metadata
  must point to the convex source tree.

## Validation

Topology-aware validation should include:

```bash
python scripts/validate_agent_source_home.py
python scripts/build_published_surfaces.py
python mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
python -m unittest discover -s tests -p 'test_*.py'
```
