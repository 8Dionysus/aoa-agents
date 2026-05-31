# AoA Agents Charter

## Purpose

`aoa-agents` is the role and persona layer of the AoA ecosystem.

Its purpose is to make agents explicit as reusable role-bearing actors with
clear contracts, rather than leaving them implicit inside prompts, workflow
code, or orchestration folklore.

## Authority Boundary

This charter answers what `aoa-agents` may claim about the agent layer.

Operational routes live in [AGENTS](AGENTS.md). System form lives in
[DESIGN](DESIGN.md). Source object topology lives in [agents](agents/README.md).
Repeatable operation topology lives in [mechanics](mechanics/README.md).
Owner boundaries are summarized in [BOUNDARIES](docs/BOUNDARIES.md).

This charter gives those surfaces their repository boundary; it does not
replace them.

## Mission

`aoa-agents` exists so AoA can name who acts, under what contract, with what
handoff, memory, evaluation, capability, projection, and review posture.

It should:

- define reusable role-bearing agent profiles;
- keep role contracts compact and reviewable;
- name handoff posture, memory posture, evaluation posture, and capability
  references without absorbing those neighboring layers;
- keep role specialization and projection gates explicit;
- publish generated companions only from source-owned role-layer inputs;
- make actor composition legible without becoming routing, playbook, or runtime
  authority.

## What This Repository Owns

| Agent-layer object | Meaning |
| --- | --- |
| Role houses | source-authored base role contracts under `agents/roles/*/profile.json` |
| Companion forms | role-owned agonic and assistant adjunct surfaces |
| Role specializations | narrower role-local actor contracts inside a base role house |
| Operating-model inputs | capability packs, tiers, orchestrator classes, cohorts, and runtime-seam bindings |
| Handoff posture | when an actor stops, escalates, requests review, or routes away |
| Memory and evaluation posture | role-level rights and expectations, not memory objects or proof verdicts |
| Projection posture | Codex and specialization eligibility boundaries when source-owned and refresh-law bounded |
| Generated companions | registries, readers, and projections derived from source-owned role-layer inputs |
| Agent-layer mechanics | repeatable operation routes around role formation, projection, checkpoint, stress, quest, Titan, recurrence, and release posture |

## Routed To Stronger Owners

| Object class | Stronger owner |
| --- | --- |
| reusable practice | `aoa-techniques` |
| bounded execution workflows | `aoa-skills` |
| proof doctrine, verdicts, scoring, and regression claims | `aoa-evals` |
| memory objects, recall truth, and retention | `aoa-memo` |
| navigation, dispatch, and route policy | `aoa-routing` |
| recurring scenario choreography | `aoa-playbooks` |
| derived graph or retrieval substrate semantics | `aoa-kag` |
| observability summaries and movement windows | `aoa-stats` |
| runtime workers, services, storage, and lifecycle | `abyss-stack` |
| AoA center doctrine and federation rules | `Agents-of-Abyss` |
| ToS-authored knowledge meaning | `Tree-of-Sophia` |

## Agent-Layer Discipline

An agent claim is healthy when a reader can identify:

- the role being played;
- the source contract that defines it;
- the handoff and review posture;
- the neighboring layers it references;
- the generated companion, if any;
- the stronger owner when the pressure leaves the role layer.

An agent profile should not become a skill bundle, proof surface, memory schema,
routing policy, scenario book, runtime worker, or hidden prompt archive.

## Review Rule

Before changing the repository's root posture, role-canon boundary,
source/generated relationship, projection posture, public route map, or owner
split, check:

1. this charter for repository authority;
2. [DESIGN](DESIGN.md) for the system form being preserved;
3. [AGENTS](AGENTS.md) for the active editing route;
4. [agents](agents/README.md) for source object topology;
5. [mechanics](mechanics/README.md) when repeatable operation pressure is in scope;
6. [BOUNDARIES](docs/BOUNDARIES.md) for sibling owner stop-lines;
7. generated surfaces, builders, validators, and tests before claiming parity.

If the change belongs to another AoA repository, `aoa-agents` should route to
that owner rather than absorbing the object.
