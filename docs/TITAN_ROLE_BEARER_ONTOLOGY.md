# Titan Role-Bearer Ontology

## The mistake this fixes

A role is not a person.

`architect` is a role class.
`Atlas` is a bearer.

Many bearers may carry the same role class across time. They may differ in temperament, memory, style, scars, thresholds, tools, and lineage.

## Core objects

### Role class

A role class defines a stable capability surface:

```text
role_key
sandbox posture
allowed gates
tool affinity
default constraints
evaluation posture
```

Example:

```text
role_key: architect
class_name: structure
default_sandbox: read-only
```

### Bearer identity

A bearer identity is the remembered entity carrying a role class.

Example:

```text
bearer_id: titan:atlas:founder
titan_name: Atlas
role_key: architect
generation: 0
status: active
```

### Incarnation

An incarnation is a session/runtime appearance of a bearer.

Example:

```text
incarnation_id: inc:2026-04-22:atlas:001
bearer_id: titan:atlas:founder
session_id: session-001
thread_id: codex-thread-...
```

### Lineage event

Lineage events are append-only.

They record:
- first appearance
- summon
- gate opening
- failure
- fall
- remembrance
- succession
- retirement
- reincarnation

## Non-erasure law

A fallen bearer remains in the ledger.

The system may mark it:

```text
fallen
retired
quarantined
succeeded
archived
```

It must not silently delete it.

## Succession law

A successor may inherit:
- role class
- lessons
- scars
- constraints
- memory candidates
- unfinished duties

A successor does not erase the fallen.

## Codex naming law

When Codex is asked to spawn a remembered person, the Codex-visible `name` should be the bearer `titan_name`.

The internal `role_key` remains inside the generated instructions and projection manifest.

```text
Codex-visible name: Atlas
role_key: architect
bearer_id: titan:atlas:founder
```

## Nickname law

`nickname_candidates` may be used for ephemeral workers.

They are not sufficient for remembered Titan persons because they are presentation-level and do not define identity.
