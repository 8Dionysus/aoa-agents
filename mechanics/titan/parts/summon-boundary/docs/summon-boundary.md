# Titan Summon Boundary

## Purpose

Define what counts as a lawful Titan summon and what must remain outside the first wave.

## Lawful summon

A lawful summon is explicit. It names the service cohort or the Titan names and asks Codex to spawn subagents for bounded work.

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

SessionStart and UserPromptSubmit hooks may add developer context. They must not silently spawn the Titans. First-wave Titan accompaniment begins with explicit summon.
