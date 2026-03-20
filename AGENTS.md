# AGENTS.md

Guidance for coding agents and humans contributing to `aoa-agents`.

## Purpose

`aoa-agents` is the role and persona layer of AoA.

It stores explicit agent profiles, role contracts, handoff posture, memory posture, evaluation posture, and other bounded definitions of who an agent is and how it should operate across neighboring AoA layers.

This repository is for role-bearing agent identity and posture, not for skills, proofs, routing, or scenario composition.

## Owns

This repository is the source of truth for:

- agent profile structure
- role-contract wording
- handoff posture
- memory posture at the agent layer
- evaluation posture at the agent layer
- registry or catalog surfaces that describe agent roles

## Does not own

Do not treat this repository as the source of truth for:

- reusable engineering practice in `aoa-techniques`
- bounded execution workflows in `aoa-skills`
- proof doctrine or verdict logic in `aoa-evals`
- routing and dispatch logic in `aoa-routing`
- explicit memory-object meaning in `aoa-memo`
- higher-level scenario composition in `aoa-playbooks`
- derived knowledge substrate semantics in `aoa-kag`

An agent may point to these layers.
It does not replace them.

## Core rule

An agent is not a skill.

A role contract may prefer certain skills, memory posture, and evaluation posture, but it should not absorb those adjacent layers into a single blurry object.

If the task requires workflow meaning, proof meaning, or memory-object meaning, route to the canonical neighboring repository instead of rewriting it here.

## Read this first

Before making changes, read in this order:

1. `README.md`
2. any role-contract or profile-schema docs referenced by the README
3. the target source file you plan to edit
4. any generated agent registry or capsule surfaces affected by the task
5. neighboring repo docs if the task touches skills, memo, evals, or playbooks

## Primary objects

The most important objects in this repository are:

- agent profiles
- role contracts
- handoff rules
- memory posture surfaces
- evaluation posture surfaces
- generated agent catalogs or registry outputs

## Allowed changes

Safe, normal contributions include:

- refining a role contract
- tightening handoff wording
- clarifying memory posture
- clarifying evaluation posture
- fixing metadata drift between source files and generated outputs
- adding a new bounded agent profile when it clearly belongs to the role/persona layer

## Changes requiring extra care

Use extra caution when:

- changing profile names or identifiers
- changing contract fields that other layers may reference
- changing generated registry shape
- changing role boundaries
- changing handoff rules in ways that affect neighboring repos
- adding role language that implies skills, playbooks, or proof doctrine are owned here

## Hard NO

Do not:

- turn an agent profile into a skill bundle
- turn an agent profile into a playbook
- turn an agent profile into a memory-object schema
- turn an agent profile into proof doctrine
- store secrets, tokens, or private infrastructure details
- introduce vague persona prose with no operational contract

Do not let role identity become an excuse for unclear authority or unclear handoff.

## Agent doctrine

A good agent-layer change should make it easier to answer:

- who this agent is
- what role boundaries it carries
- what it should hand off
- how it uses memory
- how it should be evaluated
- which neighboring layers define the concrete work it performs

A bad change usually makes the agent more mythic, more total, less bounded, or more entangled with adjacent layers than it should be.

## Public hygiene

Assume everything here is public, inspectable, and challengeable.

Write for portability:

- keep role scope explicit
- keep handoff boundaries explicit
- keep memory posture distinct from memory objects
- keep evaluation posture distinct from eval doctrine
- avoid secret operational assumptions
- sanitize examples

## Default editing posture

Prefer the smallest reviewable change.

Preserve canonical wording unless the task explicitly requires semantic change.
If semantic change is made, report it explicitly.

## Contribution doctrine

Use this flow:

`PLAN -> DIFF -> VERIFY -> REPORT`

### PLAN

State:

- what agent profile or role surface is changing
- what boundary or handoff risk exists
- what neighboring layers may be affected
- whether the change is semantic or metadata-only

### DIFF

Keep the change focused.

Do not mix unrelated cleanup into an agent-layer change unless it is necessary for repository integrity.

### VERIFY

Confirm that:

- the role remains bounded
- handoff posture remains coherent
- memory posture remains distinct from memory objects
- evaluation posture remains distinct from eval doctrine
- generated outputs remain aligned if metadata surfaces changed

### REPORT

Summarize:

- what profiles or contracts changed
- whether semantics changed or only metadata changed
- whether handoff, memory posture, or evaluation posture changed
- what validation was run
- any neighboring repo follow-up likely needed

## Validation

Run the validation commands documented in `README.md`.

If catalogs, capsules, or other generated agent surfaces changed, regenerate and validate them before finishing.

Do not claim checks you did not run.

## Cross-repo neighbors

Use these neighboring repositories when the task crosses boundaries:

- `aoa-skills` for bounded execution workflows
- `aoa-memo` for explicit memory objects
- `aoa-evals` for proof surfaces
- `aoa-playbooks` for higher-level scenario composition
- `aoa-routing` for smallest-next-object navigation
- `Agents-of-Abyss` for ecosystem-level map and boundary doctrine

## Output expectations

When reporting back after a change, include:

- which agent profiles or contracts changed
- whether semantics changed or only metadata changed
- whether handoff, memory posture, or evaluation posture changed
- whether generated outputs changed
- what validation was run
- any neighboring repo follow-up likely needed

## Default editing posture

Prefer the smallest reviewable change.
Preserve canonical wording unless the task explicitly requires semantic change.
If semantic change is made, report it explicitly.