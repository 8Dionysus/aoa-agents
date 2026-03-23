# Self-Agent Checkpoint Stack

This document records the first-wave contract for self-agent surfaces in AoA.

It exists to keep self-agent work bounded, reviewable, and portable instead of turning it into mythology about autonomy.

## Core rule

A self-agent is not a free myth of self-modification.

If an agent can reshape important system surfaces, it should pass through a checkpoint stack.

## Required checkpoints

At the current baseline, the stack should name at least:

1. constitution or policy check
2. approval gate
3. rollback marker
4. post-change health check
5. bounded iteration limit
6. explicit improvement log

These checkpoints can be implemented differently by neighboring repos, but they should not remain implicit.

## Required profile posture

A self-agent surface should be able to state:

- `agent_id`
- `role`
- `alignment_profile`
- `sandbox`
- `memory_scope`
- `audit_policy`
- `approval_mode`
- `rollback_marker`
- `health_check`
- `max_iterations`

This repository owns the role-facing contract for those fields.
It does not own the runtime implementation beneath them.

## Current public schema

The current public schema at `schemas/self-agent-checkpoint.schema.json` is a
single-actor checkpoint contract.

It records checkpoint posture for one governed actor, typically the initiating
or currently governed role on the route.

Route-level coordination still lives in the canonical `checkpoint_cohort`
composition surface.
This schema does not replace `checkpoint_cohort` or define runtime
orchestration.

## Thinkers and operators

AoA should preserve a meaningful gap between thinking and acting roles.

Thinking roles may plan, critique, compare, and shape.
Operator-facing roles may execute bounded changes.

The checkpoint stack matters most when an actor crosses from reasoning posture into system-changing posture.

## Checkpoint cohort pattern

The portable self-agent cohort pattern is the canonical `checkpoint_cohort` pattern.

The current portable cohort pattern for a self-agent checkpoint route is:

- `architect` initiates the checkpoint and names the constitution or source-of-truth fit
- `coder` performs the bounded change only after approval is explicit
- `reviewer` checks the post-change health result and final boundedness
- `memory-keeper` keeps the provenance thread and improvement log legible

AoA does not need a new role family for this route.
It needs the existing roles to stay explicit and coordinated.

## Anti-goals

Avoid treating self-agent as:

- an excuse for unclear authority
- a bypass around approval and rollback posture
- a hidden playbook
- a hidden runtime implementation
- a mythic identity with no reviewable contract
