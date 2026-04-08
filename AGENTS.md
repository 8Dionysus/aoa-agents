# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-agents`.

## Purpose

`aoa-agents` is the role and persona layer of AoA.
It stores explicit agent profiles, role contracts, handoff posture, memory
posture, evaluation posture, model-tier surfaces, bounded cohort composition
hints, and the current agent-layer adjuncts for progression, recurrence, and
self-agent checkpoint posture.

This repository is for role-bearing agent identity and posture.
It is not the main home for skills, proofs, routing, scenario composition, or
runtime autonomy implementation.

## Owns

This repository is the source of truth for:

- agent profile structure and wording
- role contracts
- orchestrator class identity and related role-facing contract surfaces
- handoff posture
- memory posture at the agent layer
- evaluation posture at the agent layer
- model-tier and bounded cohort composition surfaces
- progression overlays, mastery-axis guidance, and unlock posture at the agent layer
- recurrence discipline and return posture at the agent layer
- self-agent checkpoint posture and role-facing checkpoint contract fields
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
- live runtime checkpoint execution, live quest state, or live routing policy

An agent may point to these layers.
It does not replace them.

## Core rules

An agent is not a skill.

A self-agent is not a free myth of self-modification.
Progression, recurrence, and self-agent surfaces must stay evidence-backed,
reviewable, and explicit about approval, rollback, and handoff posture.

## Growth posture

Bounded agency is the start discipline at this layer, not the endpoint.

`aoa-agents` may name continuity, mastery, unlock posture, governed return,
and checkpointed self-agent work.
It does so as role-facing contract and overlay doctrine.
It does not own the runtime implementation beneath those contracts.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. `CHARTER.md`
3. `docs/BOUNDARIES.md`
4. the target source file you plan to edit
5. any generated registries or published surfaces affected by the task
6. neighboring repo docs if the task touches skills, memo, evals, playbooks, or routing

Then branch by task:

- progression, mastery axes, or unlock posture: `docs/AGENT_PROGRESSION_MODEL.md`
- recurrence, return, or transition vocabulary: `docs/RECURRENCE_DISCIPLINE.md`
- self-agent checkpoint posture: `docs/SELF_AGENT_CHECKPOINT_STACK.md`
- orchestrator class or runtime seam work: `docs/ORCHESTRATOR_CLASS_MODEL.md` and `docs/AGENT_RUNTIME_SEAM.md`

If a deeper directory defines its own `AGENTS.md`, follow the nearest one.

## Primary objects

The most important objects in this repository are:

- canonical profiles under `profiles/`
- model-tier, orchestrator-class, cohort-pattern, progression, and runtime-seam source files
- schemas for published contracts and runtime-facing artifacts
- generated registries and seam outputs under `generated/`
- role, memory, progression, recurrence, self-agent, and consumer-seam docs under `docs/`

## Hard NO

Do not:

- turn an agent profile into a skill bundle
- turn an agent profile into a playbook
- turn an agent profile into a memory-object schema
- turn an agent profile into proof doctrine
- store secrets, tokens, or private infrastructure details
- introduce vague persona prose with no operational contract
- put XP-style progression fields inside source profiles
- replace mastery axes with one universal score
- grant authority rights without cited evidence
- treat progression as live routing policy
- bypass approval, rollback, or checkpoint posture under the label `self-agent`
- let self-agent language become mythic identity with no reviewable contract

Do not let role identity become an excuse for unclear authority, unclear
handoff, or hidden runtime ownership.

## Contribution doctrine

Use this flow: `PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- which profile, progression surface, checkpoint surface, contract, schema, or published surface is changing
- whether role boundaries, handoff rules, memory posture, evaluation posture, progression posture, or checkpoint posture are changing
- whether any published registries or consumer seams will change
- what cross-repo boundary or authority risk exists

### DIFF

Keep the change focused.
Preserve bounded role semantics, progression evidence posture, and published
contract clarity.
Do not mix unrelated cleanup into a role change unless it is necessary for
repository integrity.

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
- progression remains an evidence-backed overlay rather than profile mutation
- mastery axes, unlock posture, and authority rights stay reviewable
- self-agent checkpoint posture remains explicit about approval, rollback, and bounded iteration
- no neighboring layer meaning was silently pulled into this repo

### REPORT

Summarize:

- what changed
- whether meaning changed or only docs, metadata, schemas, or generated surfaces changed
- whether role boundaries, handoff rules, progression posture, checkpoint posture, or published consumer seams changed
- what validation you actually ran
- any remaining follow-up work

## Validation

Do not claim checks you did not run.

When federated reachability matters, use the documented `AOA_*_ROOT` variables
to enable the optional consumer smoke checks against sibling repositories.
