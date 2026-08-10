# Compile Obligation And Mandate Without Selecting Compute

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0064
- Original date: 2026-08-10
- Surface classes: owner skill home, obligation contract, role mandate
- Agent facets: role contract, responsibility posture, incarnation
- Mechanic parents: cross-mechanic, boundary-bridge
- Guard families: owner boundary, source identity, model fit, task-local DAG
- Posture: admitted passive contract compiler

## Context

The lifecycle skill described `agent-obligation-v1` and `actor-mandate-v1`, but
fresh sessions had no exact schemas or deterministic way to preserve their
semantic decisions. The selected role could be resolved exactly, yet a duty
such as `landing preparation` still had no explicit relation to the broader
`landing` family queried from `aoa-models`. String matching would be hidden
routing authority; leaving the relation in prose would make downstream fit
evidence unverifiable.

## Decision

Add strict owner schemas and `scripts/compile_actor_contract.py` for obligation
and mandate packets. Semantic judgment remains upstream:

- `detect-obligation` decides whether pressure creates an independent duty;
- `form-actor` selects the role and explicitly names the broader model-fit task
  family, its relation to the duty, and the current-holder authority for that
  relation;
- passive helpers verify the exact role chain, bind exact input digests, and
  produce deterministic obligation and mandate digests.

The compiler cannot accept model selection, runtime activation, or token-budget
fields. It also preserves the obligation lifecycle posture and stop line,
requires unique property and output identities, and makes no semantic choice.

## Consequences

- A duty and its broader fit family can differ without an implicit heuristic.
- `aoa-models` receives a stable task family and behavioral requirements while
  retaining fit-evidence ownership and no activation authority.
- `aoa-sdk` incarnation binding v2 can bind exact obligation, mandate, role,
  and fit evidence.
- The role and domain procedure remain independent of the current model body.

## Source Surfaces

- `skills/aoa-agents-skills/scripts/compile_actor_contract.py`
- `skills/aoa-agents-skills/references/agent-obligation-v1.schema.json`
- `skills/aoa-agents-skills/references/actor-mandate-v1.schema.json`
- `skills/aoa-agents-skills/references/detect-obligation.md`
- `skills/aoa-agents-skills/references/form-actor.md`
- `tests/test_aoa_agents_actor_contract_compiler.py`

## Follow-Up Route

Integrate the compiled mandate's explicit task family with the
content-addressed `aoa-models` query and bind the selected projection through
`aoa-sdk` incarnation v2 into `summon-request-v4` runtime admission.

## Verification

Verification routes through focused compiler and resolver tests, semantic
agent validation, decision indexes, capability projections, and the repository
release gate.
