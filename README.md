# aoa-agents

`aoa-agents` is the role and persona layer of the AoA ecosystem. It makes
agents explicit as role-bearing actors with reviewable contracts, rather than
leaving them as prompt folklore or hidden orchestration assumptions.

An agent is not a skill. A skill is a bounded workflow. An agent is the
role-bearing actor that may use skills, route to proof, carry memory posture,
or hand off to a stronger owner without absorbing those layers.

This README is the public front door. When work becomes operational,
source-authored, generated, mechanic-local, or direction-bearing, follow the
linked owner surface instead of expanding this page.

> Current release: `v0.5.0`. See [CHANGELOG](CHANGELOG.md) for release notes.

## What This Repository Does

| Function | Surface |
| --- | --- |
| Repository authority boundary | [CHARTER](CHARTER.md) |
| Role-layer system form | [DESIGN](DESIGN.md) |
| Agent-facing guidance form | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| Agent route law and local checks | [AGENTS](AGENTS.md), then the nearest nested `AGENTS.md` |
| Source-authored agent object home | [agents](agents/README.md) |
| Repeatable agent-layer mechanics | [mechanics](mechanics/README.md) |
| Admitted agent-owner callable procedures | [skills](skills/README.md) |
| Agent-local statistical questions and reference packets | [stats](stats/README.md) |
| Documentation and owner-route map | [docs](docs/README.md) |
| Current shipped surface contour | [CURRENT_CONTOUR](docs/CURRENT_CONTOUR.md) |
| Owner boundaries | [BOUNDARIES](docs/BOUNDARIES.md) |
| Current direction | [ROADMAP.md](ROADMAP.md) |
| Durable obligations | [QUESTBOOK](QUESTBOOK.md) and [quests](quests/README.md) |

This repository is strongest when it clarifies who acts, under which contract,
with which handoff and authority limits. It is weakest when it tries to become
skills, proof, memory, routing, playbooks, runtime, or a giant prompt archive.

## Start Here

Read only the surface that matches the job.

| Need | Route |
| --- | --- |
| Shortest honest overview | this README -> [CHARTER](CHARTER.md) -> [DESIGN](DESIGN.md) -> [agents](agents/README.md) |
| Decide whether something belongs here | [CHARTER](CHARTER.md) -> [BOUNDARIES](docs/BOUNDARIES.md) |
| Edit role source objects | [agents](agents/README.md), then the nearest `agents/**/AGENTS.md` |
| Work on a repeatable operation | [mechanics](mechanics/README.md), then the owning package `AGENTS.md` and `PARTS.md` |
| Inspect agent-local statistics | [stats](stats/README.md), then [stats route law](stats/AGENTS.md) |
| Inspect current shipped route families | [CURRENT_CONTOUR](docs/CURRENT_CONTOUR.md) |
| Inspect generated companions | [generated](generated/README.md) and the source surface named by the generated file |
| Update direction | [ROADMAP.md](ROADMAP.md) |
| Work as an agent | [AGENTS](AGENTS.md), then the nearest nested route card |

## Role-Layer Check

Before adding, trusting, or publishing an agent-layer claim, ask the narrowest
owner that can answer it.

| Question | Owner route |
| --- | --- |
| May `aoa-agents` claim this? | [CHARTER](CHARTER.md), then [BOUNDARIES](docs/BOUNDARIES.md) |
| What is the agent model? | [AGENT_MODEL](docs/AGENT_MODEL.md) |
| Where do role sources live? | [agents](agents/README.md) and `agents/source_home.manifest.json` |
| Is this a base role, companion form, specialization, tier, cohort, orchestrator, capability pack, or runtime seam binding? | [agents](agents/README.md), then the owning branch card |
| Is this recurring operation pressure? | [mechanics](mechanics/README.md), then the package route |
| Is this a Codex projection or refresh question? | [codex-projection](mechanics/codex-projection/README.md) |
| Is this an agent-local statistical question? | keep its meaning and owner evidence in [stats](stats/README.md); shared grammar and composition route to `aoa-stats` |
| Is this proof, memory, routing, skill, technique, playbook, KAG, cross-owner stats, or runtime truth? | route to the sibling owner named in [BOUNDARIES](docs/BOUNDARIES.md) |

## Current Contour

`aoa-agents` currently carries:

- source-authored role houses and operating-model inputs under `agents/`;
- generated registries, formation readers, quest readers, runtime-seam readers,
  and Codex projection companions under `generated/`;
- mechanics packages for formation, projection, Titan role-bearing, runtime
  seams, checkpoints, quest posture, stress posture, recurrence, RPG, boundary
  bridges, and release support;
- local route cards that keep each district's authority visible.

The detailed shipped surface list lives in [CURRENT_CONTOUR](docs/CURRENT_CONTOUR.md).
The root README should not become that inventory.

## Technical Districts

| District | Use for |
| --- | --- |
| [agents](agents/README.md) | source-authored agent objects and operating-model inputs |
| [mechanics](mechanics/README.md) | repeatable role-layer operations and package-local contracts |
| [docs](docs/README.md) | public explanation, maps, boundaries, and decision records |
| [schemas](schemas/README.md) | shared schemas that are not yet part-local |
| [examples](examples/AGENTS.md) | public-safe schema-backed examples |
| [generated](generated/README.md) | derived readers and machine companions |
| [config](config/AGENTS.md) | repo-level publication and projection configuration |
| [scripts](scripts/AGENTS.md) | deterministic builders and validators |
| [tests](tests/AGENTS.md) | regression and contract checks |
| [.agents](.agents/AGENTS.md) | agent-facing companion lanes |
| [memo](memo/README.md) | local memory candidates and writeback port |
| [stats](stats/README.md) | agent-local statistical questions and evidence-linked reference packets |

Generated files are companions, not authority. Source docs, source JSON,
mechanic packages, builders, validators, tests, and decision records keep the
meaning.

## Validate

Executable validation routes live in [AGENTS](AGENTS.md#verify) and the
nearest nested `AGENTS.md`.

For root documentation route changes, use the root route card. Run source
builders only when source-authored inputs or generated companions move, and
take those commands from the nearest owning `AGENTS.md`.

## Working Rule

Grow the role layer by making the next actor boundary clearer.

Add role sources, mechanics, generated companions, examples, tests, decisions,
and memory candidates only where they improve reviewability and preserve owner
boundaries. When detail belongs to a sibling repository, mechanic, generated
reader, roadmap, changelog, quest, decision record, or route card, route it
there instead of making this README carry it.

## License

Apache-2.0
