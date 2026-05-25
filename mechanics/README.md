# Mechanics Atlas

`mechanics/` is the operation atlas for repeatable agent-layer mechanics in
`aoa-agents`.

It does not replace source objects under `agents/`, public explanation under
`docs/`, shared schemas under `schemas/`, examples under `examples/`, or
generated readers under `generated/`. It names the operations that repeatedly
move pressure across those surfaces and keeps owner boundaries visible.

## Operating Card

| Field | Route |
| --- | --- |
| role | atlas for repeatable agent-layer operations |
| input | recurring pressure that crosses source, docs, schema, example, generated, config, script, or test surfaces |
| output | active route family, package-growth candidate, validator route, or stronger-owner handoff |
| owner | `mechanics/AGENTS.md`, this atlas, and future mechanic package cards |
| next route | `mechanics/ARTIFACT_TOPOLOGY.md`, active route family, source owner, decision record |
| tools | repo validators and owning builders |
| validation | `python scripts/validate_semantic_agents.py`, `python scripts/validate_nested_agents.py`, `python scripts/validate_agents.py` |

## Active Route Families

| Family | Current Source Surfaces | Operation |
| --- | --- | --- |
| formation | `agents/profiles/adjuncts/`, formation docs, formation indexes | keep agonic actor, assistant civil, and formation-trial surfaces additive and bounded |
| projection | `agents/profiles/`, `config/codex_subagent_wiring.v2.json`, `generated/codex_agents/` | keep Codex subagent projection source-owned and refreshable |
| runtime seam | `agents/runtime_seam/`, runtime artifact schemas/examples, seam docs | keep role x tier bindings contract-first without runtime ownership |
| checkpoint | self-agent, continuity, stress, and reviewed-closeout docs/examples | keep checkpoint posture reviewable and reversible |
| quest posture | `QUESTBOOK.md`, `quests/`, quest generated readers, passport docs | keep quest-facing role posture bounded without playbook ownership |
| Titan role bearing | Titan docs/config/schemas/examples/generated projections | keep Titan bearer, lineage, summon, and incarnation role law inside the agent layer |
| release support | `CHANGELOG.md`, `docs/RELEASING.md`, release checks | keep publication posture coherent without becoming CI authority |

## Current Shape

This first topology slice activates the mechanics atlas and moves agent source
objects into `agents/`. It deliberately keeps large public docs, shared schemas,
examples, scripts, tests, and generated readers in their existing districts
until each mechanic has a package-local contract and validator support.

That keeps the first move reviewable: `agents/` becomes the object district now;
`mechanics/` becomes the route owner for future operation packages.

## Traversal

When work starts from a source object, enter through `agents/`.
When work starts from recurring operation pressure, enter through
`mechanics/`.
When work starts from public explanation, enter through `docs/` and then route
to the owning source object or operation family.

## Stop Lines

- A mechanic is not a proof verdict.
- A mechanic is not a memory object.
- A mechanic is not a runtime worker.
- A mechanic is not a playbook scenario.
- A mechanic is not a generated reader.
