# Require Evidence-Complete Summon V4 For New Execution

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0063
- Original date: 2026-08-10
- Surface classes: owner skill home, execution request, runtime consumer seam
- Agent facets: role contract, incarnation, responsibility return
- Mechanic parents: cross-mechanic, boundary-bridge
- Guard families: source identity, external incarnation, model fit
- Posture: admitted external execution contract

## Context

`summon-request-v3` can carry an external actor, but it does not bind the exact
role resolution, model-fit query, or selected fit projection that justified
the incarnation. A valid runtime profile and model name therefore cannot prove
that the actor embodies the chosen obligation and role.

## Decision

New decisions and executions use `summon-request-v4` and return
`summon-result-v4`. The external lane requires and preserves exact refs for:

- `aoa-agents` role resolution;
- the content-addressed `aoa-models` fit query and selected fit projection;
- `aoa-sdk` incarnation binding v2, which binds the obligation, mandate, role,
  model-fit evidence, and runtime profile.

The v4 schemas are generated deterministically from the frozen v3 contracts so
shared request, lane, runtime, and closeout rules cannot drift through manual
copying. V3 remains byte-stable for reading historical receipts, but cannot
authorize a fresh launch or be emitted as a new result.

### 2026-08-11 - Keep returned runtime refs aligned with v4 execution

The first real v4 landing return exposed a generator defect: the result schema
correctly required incarnation-binding-v2 but inherited both
`abyss_stack_external_codex_runtime_profile_v1` and
`abyss_stack_external_codex_result_v1` from the frozen v3 result. That made a
truthful receipt for the signed runtime-profile-v2 incarnation and its actual
runtime-result-v2 invalid. The v4 result generator now overrides only these
owner-qualified refs to their v2 contracts. The historical v3 schema remains
byte-stable and continues to accept only the corresponding v1 refs; no role,
model, runtime, or effect authority is broadened by this correction.

## Consequences

- The execution leaf receives evidence selected by upstream owners without
  becoming a role, model, or runtime selector.
- Runtime and return adapters can verify one evidence chain instead of trusting
  model labels or prose.
- Historical v3 receipts remain inspectable without weakening new execution.
- Domain procedure ownership and A2A authority remain outside `aoa-summon`.

## Source Surfaces

- `skills/aoa-summon/scripts/build_summon_v4_schemas.py`
- `skills/aoa-summon/references/summon-request-v4.schema.json`
- `skills/aoa-summon/references/summon-result-v4.schema.json`
- `skills/aoa-summon/references/contract.yaml`
- `tests/test_aoa_agents_skill_tree.py`

## Follow-Up Route

Teach the external runtime admission boundary to resolve the v4 evidence refs
and the SDK incarnation-binding-v2 bytes before launch. Do not mutate the
already frozen and independently audited transport snapshot while doing so.

## Verification

Verification routes through schema regeneration checks, v3 byte-compatibility
tests, positive and negative v4 validation, semantic agent validators,
capability projections, and the repository release gate.
