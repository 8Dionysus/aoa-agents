# QUEST execution passport

## Purpose

This document maps quest difficulty and risk to execution posture.

It does not replace the model-tier model.
It specializes it for quest routing and delegation.

## Core rule

A quest does not merely need a priority.
It needs an execution passport:

- `difficulty`
- `risk`
- `control_mode`
- `delegate_tier`
- optional `fallback_tier`
- optional `wrapper_class`

## Difficulty ladder

### `d0_probe`

Read-only triage, inventory, classification, or extraction.
Good fit:
- `router`
- `executor` for trivial extraction
- small local wrappers under supervision

### `d1_patch`

One small bounded change in one surface.
Good fit:
- `planner` if shape is unclear
- `executor` if shape is already bounded
- `verifier` afterward

### `d2_slice`

A bounded slice across several files in one owner surface.
Good fit:
- `planner -> executor -> verifier`
- local wrappers may assist only when the route is already bounded and `risk` is low

### `d3_seam`

A seam or contract route.
Examples:
- schema plus docs plus generated projection
- role contract plus runtime seam
- app intent surface plus catalog rendering
Default posture:
- split first
- do not delegate raw to small local wrappers

### `d4_architecture`

Broad architecture or policy route.
Default posture:
- human plus Codex
- `conductor` or `deep` involvement is allowed
- child quests should be split out before execution

### `d5_doctrine`

Rule-birth, boundary, or public-canon work.
Default posture:
- human-gated
- Codex may co-author
- local wrappers stay leaf-only helpers, never the doctrine author

## Risk ladder

### `r0_readonly`

No repo writes or only inert example output.

### `r1_repo_local`

Repo-local writes with no contract or side-effect change.

### `r2_contract`

Touches published schema, runtime contract, security posture, or operator-visible meaning.

### `r3_side_effect`

Real-world or runtime side effects.
Examples:
- input events
- infra mutation
- irreversible host change
- unsafe automation expansion

## Control modes

### `codex_supervised`

Default for low-risk bounded work.

### `human_gate`

Mandatory approval or direct handling required before execution or merge.

### `human_codex_copilot`

Used for architectural and doctrinal routes where human intent and Codex synthesis should stay in the loop.

### `blocked`

Not executable yet.

## Initial wrapper classes

- `local_reader`
- `local_builder`
- `local_patcher`
- `local_validator`
- `codex_primary`
- `human_only`
- `hybrid`

Wrapper classes are implementation-facing hints, not public doctrine about model brands.

## Delegation matrix

### Safe initial allowance

Local wrappers may take leaf quests when all of the following are true:
- difficulty is `d0_probe`, `d1_patch`, or bounded `d2_slice`
- risk is `r0_readonly` or `r1_repo_local`
- a parent or anchor already exists
- expected artifacts are named
- Codex or a human verifier remains in the loop

### Split requirement

Do not delegate `d3+` quests directly.
First split them into child leaves that can honestly be executed and verified.

### Escalation triggers

Escalate toward `conductor` or `deep` when:
- ambiguity stays high
- options conflict
- route drift repeats
- contract risk is high
- the route is birthing new rules rather than applying old ones
