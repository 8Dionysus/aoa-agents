# ORCHESTRATOR CLASS MODEL

## Purpose

This document defines the source-authored orchestrator class layer in `aoa-agents`.

It exists so that orchestrator identity can stay compact, class-shaped, and reviewable without getting mixed into quest payloads or runtime-only prompt state.

## Anti-confusion rule

Orchestrator class identity lives in `aoa-agents`, not in quests.

Quests may describe growth work, proof work, or route alignment for an orchestrator class.
They do not define what the class is.

## Why this layer exists

The federation already separates:

- role and persona meaning in `aoa-agents`
- route meaning in `aoa-playbooks`
- proof meaning in `aoa-evals`
- recurrence and writeback meaning in `aoa-memo`

Orchestrator classes sit inside the agent layer because they are class identity and boundary law.
They should not be reconstructed from workload metadata later.

## Reader posture

This layer publishes three reader surfaces:

- inspect/catalog: `generated/orchestrator_class_catalog.min.json`
- capsule: `generated/orchestrator_class_capsules.json`
- expand: `generated/orchestrator_class_sections.full.json`

These surfaces are source-owned now so they can be mirrored later without renaming or reshaping.

## Initial class set

### `router`

Chooses the repo, owner layer, source-of-truth surface, and next bounded read set.
It has no mutation authority.

### `review`

Decides closure, residual risk, re-entry posture, or stop conditions.
It does not own net-new execution planning.

### `bounded_execution`

Produces the smallest correct next bounded step under playbook law and boundary law.
It may not widen scope silently or override review.

## Contract fields

Every source-authored orchestrator class publishes:

- `id`
- `name`
- `status`
- `summary`
- `primary_goal`
- `allowed_owner_layers`
- `read_order`
- `required_surfaces`
- `forbidden_surfaces`
- `expected_outputs`
- `verify_refs`
- `boundary_note`

## Boundaries to preserve

Do not let this layer absorb:

- quest workload state
- playbook route canon
- proof bundles or scoring logic
- memo-object canon
- runtime implementation detail

The class layer answers "what kind of orchestrator is this?" and "what law governs it?"
It does not answer "what work is active right now?".
