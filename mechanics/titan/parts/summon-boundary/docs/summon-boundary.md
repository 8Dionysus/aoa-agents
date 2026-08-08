# Titan Summon Boundary

## Purpose

Define what counts as a lawful Titan summon and what must remain outside the first wave.

## Lawful summon

A lawful summon is explicit. For compatibility Titan lanes, it names the
service cohort or the Titan names and asks Codex to spawn subagents for bounded
work. For the external actor lane, an admitted responsibility transfer may
explicitly authorize one execution leaf through a complete task-local DAG.

The lawful default is:

```text
Atlas + Sentinel + Mneme
```

## Conditional summons

Forge requires mutation intent:

```text
I authorize Forge to implement this bounded change.
Targets: ...
Validation: ...
Rollback or stop condition: ...
```

Delta requires judgment intent:

```text
I authorize Delta to compare, evaluate, or issue a bounded verdict on this surface.
Question: ...
Evidence: ...
Success criterion: ...
```

## DAG-authorized external execution

`aoa-agents-skills` may authorize `aoa-summon` without a second literal user
summon only when the current goal authority has already admitted one complete
task-local actor DAG. The selected leaf must carry the exact obligation,
mandate, incarnation, responsibility holders, domain procedures, named
outputs, return owner, continuation, runtime launch, and stop refs. It must
launch a separately addressable CLI process/session and must not use the
built-in Codex subagent lane as external-incarnation proof.

This is explicit delegated authority inside an admitted responsibility
relation, not keyword autospawn or silent accompaniment. Any missing,
inferred, stale, or widened field blocks the leaf and returns responsibility
to the current holder.

## Forbidden summons

```text
summon everyone and let them decide
keep agents running silently in the background
let Forge edit whatever is needed
let Delta declare final truth
let Mneme write canonical memory
let Sentinel close the task secretly
let Atlas rewrite project governance
```

## Hook boundary

SessionStart and UserPromptSubmit hooks may add developer context. They must
not silently spawn the Titans or create a task-local responsibility transfer.
First-wave Titan accompaniment begins with an explicit user summon. External
execution begins only with the complete DAG authorization above.
