# Delegation classes

This owner surface preserves the semantic boundary for the two provider-neutral
classes defined by `aoa-sdk`. It does not replace the SDK contract or the
`abyss-stack` runtime contract.

## `ephemeral_read_worker_v1`

This class is a cheap, stateless read-only operation over a bounded immutable
input set. The parent holder keeps responsibility. The result is
content-addressed and carries economy observation, but the operation does not
form an actor role, create a mandate, transfer responsibility, or create a
durable return obligation.

`aoa-agents` must therefore keep the current holder in the responsibility
field, pass only the bounded result onward, and use typed escalation to
`external_incarnation_v1` if the work becomes an independently owned duty.
The read worker is not a smaller actor and must not inherit role, model-fit, or
runtime authority merely because a provider executes it.

## `external_incarnation_v1`

This class is the full responsibility-bearing route. `aoa-agents` supplies the
exact role contract and actor mandate, records the responsibility transfer,
and filters the reviewed return. `aoa-models` supplies the exact model
realization; `aoa-sdk` supplies the incarnation binding and continuation;
`abyss-stack` supplies process, session, and event evidence; and `aoa-evals`
owns eval meaning.

The class keeps eval, closeout, and acceptance as separate lifecycle refs. A
runtime process completing, a transport receipt, or a reviewed return does not
by itself establish any of those claims. The first concrete adapter is the
Codex CLI; a local/provider adapter consumes the same ABI and remains a
replaceable runtime implementation. Built-in Codex child-agent lanes are not
an external incarnation.

Both classes are source contracts only while `d0-baseline:baseline-ready` is
absent. Activation, pilot, promotion, and economy claims require the paired
Codex and local/provider baseline and fresh owner admission.

## Owner stop line

Do not select a model, launch a process, interpret transport as A2A meaning,
issue an eval verdict, close the Goal, or grant acceptance from this document.
Return the exact stronger-owner refs and the current responsibility holder when
one is missing or contradictory.
