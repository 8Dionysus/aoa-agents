# Agent Progression Model

## Purpose

This note defines the adjunct progression contract for agent roles in `aoa-agents`.

It exists so that long-horizon quest work can accumulate reviewable mastery and unlock posture without mutating the source-authored agent profile surface.

## Core rule

Progression attaches to `agent_id`. It does not live inside `profiles/*.profile.json`.

Profiles remain the source of role contract, memory posture, evaluation posture, preferred cohort patterns, preferred tier hints, and preferred skill families.

Progression remains an evidence-backed overlay that says:

- how mastery is accumulating
- what unlock posture has been earned
- which quest shapes are now safer fits
- which authority rights are available

## Mastery axes

Use multiple axes rather than a single score.

### `boundary_integrity`
Respects repo ownership, contract seams, and anti-collapse rules.

### `execution_reliability`
Produces bounded changes that survive named verification.

### `change_legibility`
Leaves readable diffs, summaries, handoffs, and state deltas.

### `review_sharpness`
Finds drift, contradictions, regressions, or missing checks.

### `proof_discipline`
Connects claims to evidence, eval surfaces, and named verdict posture.

### `provenance_hygiene`
Preserves source-of-truth, lineage, and redaction-aware traceability.

### `deep_readiness`
Handles ambiguity, arbitration, and escalation only when the route really needs depth.

## Rank posture

Rank is a reflection label, not a substitute for evidence.

Recommended first-wave labels:

- `initiate`
- `adept`
- `specialist`
- `veteran`
- `master`

A rank label should summarize a pattern of reviewed evidence. It should not overrule the underlying mastery axes or route-specific risk posture.

## Unlock posture

Unlocks should stay reviewable and small.

Good unlock classes in the first wave:

- difficulty ceiling
- risk ceiling
- tier IDs
- cohort patterns
- skill families
- authority rights

Do not use unlocks to hide new doctrine. If an unlock requires new public rules, that rule belongs in a stronger source surface first.

## Role affinity hints

These hints are descriptive only.

- `architect` usually leans toward `boundary_integrity` and `deep_readiness`
- `coder` usually leans toward `execution_reliability` and `change_legibility`
- `reviewer` usually leans toward `review_sharpness` and `boundary_integrity`
- `evaluator` usually leans toward `proof_discipline` and `review_sharpness`
- `memory-keeper` usually leans toward `provenance_hygiene` and `change_legibility`

## Evidence requirement

A progression object should cite reviewed evidence such as:

- quest IDs
- eval evidence IDs
- memo chronicle IDs
- bounded verification artifacts

One good run is useful evidence. Repeated reviewed evidence is stronger evidence.

## Anti-patterns

- putting XP fields in source profiles
- replacing mastery axes with one universal score
- granting authority rights without cited evidence
- treating progression as live routing policy
- hiding doctrine changes inside an example progression file
