# AGENT STRESS HANDOFFS

## Goal

Make stressed agent-to-agent handoffs explicit, bounded, and reusable.

A handoff under stress should not say only "something failed".
It should carry:

- what surface is stressed
- what posture is requested next
- what actions are blocked
- what evidence already exists
- what conditions permit re-entry later

## Why `aoa-agents` owns this

`aoa-agents` owns handoff posture and role boundaries.

A stress handoff envelope is not a playbook and not a receipt.
It is the role-layer wrapper that lets one actor pass bounded context to another without widening authority.

## Recommended envelope contents

A useful stress handoff envelope should include:

- sender role
- receiver role
- stressed repo and surface
- stress family and severity
- requested next posture
- blocked action families
- evidence refs
- unresolved questions
- required artifacts for the next actor
- re-entry conditions for returning control

## Relationship to neighboring layers

### Source receipts
Source owner repos still publish the primary evidence of what happened.

### Playbooks
A playbook may name the recurring lane that consumes the handoff.

### Routing
Routing may point toward a role or scenario, but it should not invent the envelope contents.

### KAG
KAG may consume a handoff envelope as a consumer signal, but it must still publish its own derived-layer health objects.

## Guardrails

- do not use a handoff envelope as proof
- do not let a handoff envelope authorize mutation that the sender could not authorize
- do not omit blocked actions under stress
- do not hand off without evidence refs when evidence already exists
- do not keep envelopes alive forever without review or expiry

## Acceptance shape

A healthy wave-3 landing would make it possible to point to:

- one machine-readable stress handoff envelope family
- one example envelope that routes from a narrower actor to a steward or reviewer
- one explicit re-entry condition set
- one explicit blocked-action list
