# AGENT STRESS POSTURE

## Goal

Teach agent profiles to become narrower, clearer, and easier to hand off under stress.

An agent is a role-bearing actor that uses skills.
When stress rises, the role contract should become more explicit, not more improvisational.

## Why `aoa-agents` owns this

`aoa-agents` already owns profile meaning, role contracts, handoff posture, memory posture, and evaluation posture.

Stress posture belongs here because it changes:

- mutation appetite
- escalation timing
- proof expectations
- memory writeback strictness
- handoff discipline

It does not replace routing, playbooks, evals, or source-owned receipts.

## Additive shape

Prefer one additive adjunct surface such as:

- `schemas/agent_stress_posture_v1.json`
- `examples/agent_stress_posture.example.json`

If the live repo prefers fields inside `profiles/*.profile.json`, preserve that local convention.
Wave 3 does not require a profile rewrite.

## Stress-band contract

A useful agent stress posture should answer, by band:

- how much mutation appetite remains
- when to reground to source evidence
- when escalation is mandatory
- what proof threshold is required before continuing
- whether memory writeback stays normal, becomes reviewed-only, or stops
- which skill families remain preferred
- which action families become blocked

Recommended bands for wave 3:

- `low`
- `medium`
- `high`

This keeps posture legible without pretending to predict every edge case.

## Interaction rules

### Routing
Routing may suggest a next-hop posture, but routing does not author the role contract.

### Playbooks
Playbooks may consume agent stress posture to shape recurring degraded lanes, but a playbook is still scenario composition, not role identity.

### Memo
Memo may recall relevant lessons, but recall is context, not permission.

### Evals
Evals may later verify whether the chosen posture was appropriate.
The posture contract itself still belongs here.

## Guardrails

- do not let a stress profile silently widen authority
- do not turn stress posture into an excuse for hidden auto-repair
- do not widen memory writeback under stress
- do not force every profile to expose the exact same fields if the repo already has a better local fit
- do not replace owner-local receipts with role lore

## Acceptance shape

A healthy wave-3 landing would make it possible to point to:

- one additive stress-posture object family
- one example role that narrows under stress
- one documented rule for earlier escalation before mutation
- one documented rule for stricter memory writeback under stress
