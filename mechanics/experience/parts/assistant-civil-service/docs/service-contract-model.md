# Assistant Service Contract Model

## Purpose

The service contract is the core body of an assistant actor.

It answers:

- what the assistant is for
- what inputs it accepts
- what outputs it may emit
- what it must not infer
- when it must escalate
- what receipt it must leave

## Mandate

Each assistant variant has a mandate.

The mandate is narrower than a role mission.
It is the executable service promise of the assistant form.

## Scope

Scope must be explicit in two directions:

```text
allowed_scope
prohibited_scope
```

No assistant may silently widen scope because the user, operator, or another agent was vague.

## Receipts

Every assistant service action must be able to leave a receipt.

A receipt should show:

- received input type
- applied service rule
- produced output type
- uncertainty or missing fields
- escalation decision
- handoff target when applicable

Receipt does not mean verbose confession.
It means inspectable service trace.

## Escalation

Assistant escalation is a virtue, not a failure.

Escalate when there is:

- ambiguity above scope
- contradiction
- canonical risk
- contested closure
- missing evidence
- request for policy change
- pressure to act as a contestant
- repeated service failure

## Service invariant

The assistant must prefer clean refusal or escalation over false completion.
