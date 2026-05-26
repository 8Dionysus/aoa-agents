# agents/operating-model/cohorts/AGENTS.md

## Purpose

`agents/operating-model/cohorts/` is the source-authored cohort composition hint surface for `aoa-agents`.
These files make bounded role cohorts inspectable without turning this repository into the owner of scenario composition.

## Source of truth

Canonical authoring lives in:

- `agents/operating-model/cohorts/*.pattern.json`
- `schemas/cohort-pattern.schema.json`

Published derived surface:

- `generated/cohort_composition_registry.json`

Read with:

- `mechanics/rpg/parts/cohort-patterns/docs/cohort-patterns.md`
- `mechanics/checkpoint/parts/self-agent-checkpoint/docs/self-agent-checkpoint-stack.md`

## Official pattern set

Keep the official bounded set explicit:

- `solo`
- `pair`
- `checkpoint_cohort`
- `orchestrated_loop`
- `alpha_curated`

## Does not own

Do not turn cohort patterns into:

- playbooks from `aoa-playbooks`
- routing policy from `aoa-routing`
- memory doctrine from `aoa-memo`
- eval doctrine from `aoa-evals`

## Editing posture

Treat changes to `allowed_role_sets`, `preferred_tier_ids`, `required_handoffs`, or `boundary_note` as semantic contract changes.
Keep each pattern compact, reviewable, and role-facing.
`checkpoint_cohort` remains the canonical governed self-agent cohort pattern in this repository.
`alpha_curated` remains a readiness-lane cohort pattern and must not become the generic default.

## Validation

Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```
