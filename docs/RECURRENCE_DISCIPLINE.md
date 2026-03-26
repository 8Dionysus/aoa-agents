# RECURRENCE DISCIPLINE

## Purpose

This document defines recurrence discipline at the agent layer.
It is the bounded agent-layer landing of the federation recurrence law named in `Agents-of-Abyss`.

It does not turn `aoa-agents` into a runtime implementation repository.
It makes the agent-layer contract explicit when a route loses shape and must return to a prior valid anchor before bounded re-entry.

## Core Rule

Recurrence at the agent layer is carried through an explicit return decision.

It should be used when the route loses boundedness, source fit, artifact fit, verification posture, or checkpoint posture.

Return is not:

- a blind retry
- a new sovereign stage outside the public loop
- permission to widen context until something works
- ownership transfer of memory or runtime policy into this repository

## Public Loop Stays Small

The external public loop remains:

```text
route -> plan -> do -> verify -> deep? -> distill
```

`return` is carried by `transition_decision`.

It is a governed re-entry between phases, not a new stage.

## Canonical Decision Vocabulary

At the current baseline, `transition_decision` should continue to govern route movement with a small explicit vocabulary.

The practical public vocabulary is:

- `continue`
- `pause`
- `escalate`
- `return`
- `distill`

This note only hardens the meaning of `return`.

## When Return Is Legitimate

Use `return` when at least one of the following is true:

- the current actor can no longer state the active route goal and bounded artifact contract
- source-of-truth fit is unclear or has drifted
- verification posture was lost before the route was actually verified
- the route widened scope without a new bounded plan
- repeated stall or contradiction indicates that forward motion would be theater
- a checkpoint-governed route crossed an approval, rollback, or health boundary without preserving the last valid anchor

## Anchor Rule

A return decision should point back to a last valid anchor rather than vague prior context.

At the agent layer, the preferred anchor is an inspectable public artifact such as:

- `route_decision`
- `bounded_plan`
- `verification_result`
- `distillation_pack` in rare distill-led recovery cases

When relevant, a bounded checkpoint marker may also be named beside the artifact anchor, but checkpoint implementation still belongs outside this repository.

## Minimal Return Contract

At the current bootstrap baseline, a `transition_decision` with `decision = "return"` should be able to name:

- why the return is necessary
- which role or tier should receive the re-entry through `next_hop`
- which prior artifact is the anchor through `anchor_artifact`
- how re-entry should stay bounded through `reentry_note`

These fields keep return inspectable without turning the agent layer into a runtime engine.

## Re-entry Discipline

A valid return should preserve all of the following:

- the route remains within the published public loop
- the re-entry target is explicit rather than implied
- the anchor points to a prior valid artifact rather than loose chat continuity
- the route does not silently widen scope during recovery
- escalation remains a separate decision rather than a disguised return

## Relationship to Self-Agent Posture

A checkpointed self-agent route should prefer return over unbounded forward improvisation.

If a governed actor loses the change boundary, it should return to the last approved anchor before more change work occurs.

This keeps rollback posture real rather than ceremonial.

## Boundaries To Preserve

- `aoa-playbooks` still owns scenario composition and named route method
- `aoa-memo` still owns memory objects, checkpoint export, and writeback meaning
- `aoa-routing` still owns navigation and dispatch surfaces
- `aoa-evals` still owns proof doctrine and verdict logic
- `abyss-stack` still owns runtime context rebuild, retries, wrapper policy, and infrastructure implementation

## Anti-Goals

Avoid treating return as:

- a synonym for retry
- a hidden escalation to bigger models
- a pretext for loading the whole past context again
- a new runtime stage
- a license to bury drift under fluent prose
