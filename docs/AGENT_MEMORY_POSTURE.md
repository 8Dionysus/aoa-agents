# AGENT MEMORY POSTURE

## Purpose

This document defines memory posture at the agent layer.

It does not redefine memory objects.
It defines how existing agent roles are expected to read, write, promote, freeze, or hand off memory-facing work.

## Core rule

`aoa-memo` owns memory-object canon, memory doctrine, and recall meaning.
`aoa-routing` selects the next memo path.
`aoa-agents` owns role-level memory rights and posture.
`aoa-agents` only states which roles may use published or routed object recall seams.
When consumed through `aoa-routing` tiny-model entrypoints, doctrine recall remains
the default memo path and `memory_objects` remains an explicit parallel family
selected through `recall_family`.

An agent posture should answer:

- what memory bands the role reads by default
- what it may write directly
- what it may nominate for promotion
- what it must hand off instead of deciding alone

## Shared recall scope classes

`aoa-agents` names recall scope classes, not memo object identifiers.
`aoa-memo` may still publish concrete object scopes such as `thread:contract-hardening` or `repo:aoa-memo`.

The current shared recall scope grammar is:

- `thread` for one bounded working thread or named active route
- `session` for restartable near-term continuity inside one active session band
- `repo` for one owning repository's local doctrine, examples, or checkpoints
- `project` for cross-session memory inside one named project lane
- `workspace` for sibling-repo coordination inside one checked-out workspace
- `ecosystem` for AoA-wide cross-repo recall

These are scope classes.
They are not memory posture labels and they are not direct grants to read every object carrying a similarly prefixed scope identifier.

## Public memory bands

Use the public memo temperature scale:

- `hot`
- `warm`
- `cool`
- `cold`
- `frozen`

Also respect the `core` overlay as a constitutional band.

## Role postures

### `architect`

- default read bands: `core`, selected `warm`, selected `cool`
- default write bands: `warm`
- default recall scope classes: `repo`, `project`, `workspace`, `ecosystem`
- promotion rights: may nominate `warm -> cool`
- freeze rights: no default freeze authority
- handoff posture: hand off durable object shaping to `memory-keeper` when memory design becomes first-class work

### `coder`

- default read bands: `core`, selected `hot`, narrow `warm`
- default write bands: `hot`
- default recall scope classes: `thread`, `session`, `repo`, `project`
- promotion rights: may nominate `hot -> warm`
- freeze rights: none
- handoff posture: hand off durable writeback and retention questions when the route becomes cross-session or policy-relevant

### `reviewer`

- default read bands: `core`, `warm`, selected `cool`
- default write bands: `warm`
- default recall scope classes: `thread`, `session`, `repo`, `project`
- promotion rights: may confirm or block promotion proposals
- freeze rights: may recommend freeze, but should not freeze alone by default
- handoff posture: hand off durable memory capture to `memory-keeper` after review posture is explicit

### `evaluator`

- default read bands: `core`, selected `warm`
- default write bands: `warm` for bounded evaluation traces only
- default recall scope classes: `session`, `repo`, `project`, `workspace`
- promotion rights: may nominate stable evaluation patterns
- freeze rights: none
- handoff posture: keep eval doctrine separate from memo truth and hand off durable memory capture when needed

### `memory-keeper`

- default read bands: `core`, `warm`, `cool`, selected `cold`
- default write bands: `warm`, `cool`, `cold`
- default recall scope classes: `thread`, `session`, `repo`, `project`, `workspace`, `ecosystem`
- promotion rights: may promote, demote, retire, and rescue within named policy
- freeze rights: may prepare freeze candidates, but human review remains preferred for `frozen`
- handoff posture: should hand off source-authored canon questions to neighboring source-of-truth layers instead of absorbing them

## Practical rights

### Read rights

Read rights should stay role-shaped and need-based.

- low-latency execution roles should not read the whole archive by default
- review and memory roles may read wider history when the route requires it
- `core` should stay broadly readable because it carries constitutional constraints

### Write rights

Write rights should stay narrower than read rights.

- `hot` write is common for active work
- `warm` write should require enough evidence to survive one session
- `cool` or `cold` write should imply consolidation or review intent

### Promotion and freeze

Default rule:

- most roles may nominate promotion
- few roles should finalize promotion
- `frozen` should remain rare and review-heavy

## Boundaries to preserve

- memory posture is not the same thing as memory ownership
- role posture must not replace memo schemas
- memory posture must not silently encode evaluation doctrine
- wide recall is not a sign of sophistication by itself

## Minimal contract

When a role contract or registry entry mentions memory posture, it should remain clear:

- which bands are read by default
- which bands are writable
- which recall scopes are allowed by default
- which promotions are allowed
- when human or `memory-keeper` review is required

Machine-readable agent surfaces should keep this split explicit:

- `memory_posture` for the coarse recall stance
- `memory_rights.default_read_bands` for public memo bands plus `core`
- `memory_rights.default_write_bands` for direct write authority
- `memory_rights.allowed_recall_scopes` for bounded recall scope classes
- `memory_rights.promotion_rights` for nomination, confirmation, and lifecycle actions
- `memory_rights.freeze_rights` for recommend, prepare, and finalize posture
