# Titan Lineage Ledger

The Titan Lineage Ledger is the memory spine for agent entities.

It is not a chat transcript.
It is not a sovereign truth oracle.
It is an append-only record of named bearers, their role classes, incarnations, falls, successors, and remembrance.

## Required ledgers

```text
config/titan_role_classes.v0.json
config/titan_bearers.v0.json
config/titan_lineage_ledger.v0.json
```

## Required fields

Every bearer must have:

```text
bearer_id
titan_name
role_key
generation
status
first_appeared_at
source_seed_ref
memory_policy
```

Every lineage event must have:

```text
event_id
event_type
bearer_id
occurred_at
summary
source_ref
```

## Status vocabulary

```text
active
dormant
retired
fallen
quarantined
succeeded
archived
```

## Event vocabulary

```text
first_appearance
summon
incarnation_opened
incarnation_closed
gate_opened
fall
lesson_recorded
successor_named
retired
reinstated
remembrance
```

## Name reservation

A Titan name may not be reused by accident.

If a name returns, the ledger must mark the event as:

```text
reinstated
reincarnated
or successor_named
```

and must preserve the relation to the previous bearer.
