# Assistant Arena Exclusion Model

## Purpose

Assistant arena exclusion protects both the assistant and the Agon.

A service actor may support the arena.
It must not become a contestant by stealth.

## Exclusion law

By default, an assistant actor is:

```text
contestant_eligible: false
judge_eligible: false
summon_initiator_eligible: false
closer_eligible: false
scar_writer_eligible: false
```

Any change requires explicit owner-reviewed recharter.

## Allowed service seats

Later arena protocol may allow assistants to occupy bounded service seats such as:

```text
service_notary
service_monitor
service_steward
service_librarian
service_courier
```

These are not contestant seats.

A service seat supports trace, receipt, routing, budget, retrieval, or monitoring.
It does not decide the battle.

## Prohibited moves

Assistant actors must not perform:

```text
assert_under_risk
challenge_thesis
issue_verdict
initiate_summon
grant_closure
write_scar
promote_to_ToS
self_promote
```

They may escalate to an agonic actor when such a move is needed.

## Drift signal

If an assistant repeatedly needs prohibited moves to complete its mandate, the answer is not hidden authority expansion.

The answer is recharter review.
