# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-agents`.

## Purpose

`aoa-agents` is the role and persona layer of AoA. It stores explicit agent profiles, role contracts, handoff posture, memory posture, evaluation posture, model-tier surfaces, and bounded cohort composition hints.

This repository is for role-bearing agent identity and posture, not for skills, proofs, routing, or scenario composition.

## Owns

This repository is the source of truth for:

- agent profile structure and wording
- role contracts
- handoff posture
- memory posture at the agent layer
- evaluation posture at the agent layer
- model-tier and bounded cohort composition surfaces
- generated registries and published agent-layer consumer seams

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering practice in `aoa-techniques`
- bounded execution workflows in `aoa-skills`
- proof doctrine or verdict logic in `aoa-evals`
- routing and dispatch logic in `aoa-routing`
- explicit memory-object meaning in `aoa-memo`
- higher-level scenario composition in `aoa-playbooks`
- derived knowledge substrate semantics in `aoa-kag`

An agent may point to these layers. It does not replace them.

## Core rule

An agent is not a skill.

A role contract may prefer certain skills, memory posture, and evaluation posture, but it should not absorb those adjacent layers into one blurry object.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `CHARTER.md`
3. `docs/BOUNDARIES.md`
4. the target source file you plan to edit
5. any generated registries or published surfaces affected by the task
6. neighboring repo docs if the task touches skills, memo, evals, playbooks, or routing

If a deeper directory defines its own `AGENTS.md`, follow the nearest one.

## Primary objects

The most important objects in this repository are:

- canonical profiles under `profiles/`
- model-tier, cohort-pattern, and runtime-seam source files
- schemas for published contracts and runtime-facing artifacts
- generated registries and seam outputs under `generated/`
- role, memory, progression, recurrence, and consumer-seam docs under `docs/`

## Hard NO

Do not:

- turn an agent profile into a skill bundle
- turn an agent profile into a playbook
- turn an agent profile into a memory-object schema
- turn an agent profile into proof doctrine
- store secrets, tokens, or private infrastructure details
- introduce vague persona prose with no operational contract

Do not let role identity become an excuse for unclear authority, unclear handoff, or mythic prose.

## Contribution doctrine

Use this flow: `PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- which profile, contract, schema, or published surface is changing
- whether role boundaries, handoff rules, memory posture, or evaluation posture are changing
- whether any published registries or consumer seams will change
- what cross-repo boundary risk exists

### DIFF

Keep the change focused. Preserve bounded role semantics and published contract clarity. Do not mix unrelated cleanup into a role change unless it is necessary for repository integrity.

### VERIFY

Minimum validation for source or generated-surface changes:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
```

Confirm that:

- role boundaries remain explicit
- handoff stays legible
- memory and evaluation posture remain named rather than implied
- no neighboring layer meaning was silently pulled into this repo

### REPORT

Summarize:

- what changed
- whether meaning changed or only docs, metadata, schemas, or generated surfaces changed
- whether role boundaries, handoff rules, or published consumer seams changed
- what validation you actually ran
- any remaining follow-up work

## Validation

Do not claim checks you did not run.

When federated reachability matters, use the documented `AOA_*_ROOT` variables to enable the optional consumer smoke checks against sibling repositories.
