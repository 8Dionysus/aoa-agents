# orchestrator_classes/AGENTS.md

## Purpose

`orchestrator_classes/` is the source-authored class-identity surface for orchestrators in `aoa-agents`.
It defines what a class is, what it reads first, what it may touch, and what it must never absorb.

## Source of truth

Canonical authoring lives in:

- `orchestrator_classes/*.class.json`
- `schemas/orchestrator-class.schema.json`

Published derived surfaces:

- `generated/orchestrator_class_catalog.min.json`
- `generated/orchestrator_class_capsules.json`
- `generated/orchestrator_class_sections.full.json`

Read with:

- `docs/ORCHESTRATOR_CLASS_MODEL.md`
- `docs/QUEST_EXECUTION_PASSPORT.md`

## Anti-confusion rule

Orchestrator class identity lives here, not in quests.
Quests may point at an orchestrator class, but they must not define what that class is.

## Official class set

Keep the initial bounded set explicit:

- `router`
- `review`
- `bounded_execution`

## Does not own

Do not turn orchestrator classes into:

- quest workloads from repo-local `quests/*.yaml`
- playbooks from `aoa-playbooks`
- proof doctrine from `aoa-evals`
- memory-object canon from `aoa-memo`
- runtime implementation from `abyss-stack`

## Validation

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```
