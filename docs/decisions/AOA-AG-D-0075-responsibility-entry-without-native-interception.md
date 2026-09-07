# Responsibility Entry Without Native Interception

## Status

Accepted. Partially supersedes AOA-AG-D-0069 as stated below.

## Index Metadata

- Decision ID: AOA-AG-D-0075
- Original date: 2026-09-07
- Surface classes: owner skill home, capability route, external actor lifecycle
- Agent facets: obligation, responsibility transfer, incarnation
- Mechanic parents: boundary-bridge, summon-boundary
- Guard families: owner boundary, runtime binding, continuity
- Posture: independent responsibility entry; native helpers remain native

## Context

Mandatory classification and repeated cross-owner instructions made the AoA
skill a condition for ordinary Codex delegation. Resuming a session could
recreate a responsibility that already had a holder. Shortening the entrypoint
alone did not remove those semantic costs.

## Options Considered

- Retain universal classification and move its instructions into references.
- Keep one entry for independent AoA responsibility, using existing compilers
  and runtime interfaces only when that responsibility needs them.

## Decision

`aoa-agents-skills` forms, transfers, continues, or receives an independent AoA
responsibility. Ordinary work and native Codex helpers do not require an SDK
route, a negative classification receipt, or `aoa-summon`. Native delegation
still requires the user's applicable authorization.

For an independent duty, preserve the separately addressable external actor
route. The holder supplies meaningful choices: duty, role, authority, expected
return, and environment constraints. The existing passive external-actor
preparer compiles the cross-owner package and validates identity and authority;
it must not invent missing owner evidence or launch a runtime.

On continuation, inspect the existing responsibility and holder before forming
anything new. Session resume or compaction alone does not invalidate that
identity. Reclassification follows a changed responsibility boundary, not a
session event. Changed permissions and unavailable runtime bindings still
require their own checks.

`aoa-summon` remains an execution/return leaf for a prepared external actor or
an explicitly supplied legacy compatibility packet. Its legacy classification
and identity checks are retained; they are not a gate on native helpers.
Launch, waiting, and wake rely on supported runtime interfaces. Missing runtime
capabilities remain integration gaps, not instructions to create a second
scheduler or infer Goal state.

The same-request execute authority accepted in AOA-AG-D-0069 remains valid;
this decision supersedes its universal native admission and resume repetition
clauses only.

## Rationale

AoA adds domain meaning and accountable continuity. Codex owns its native
execution mechanisms. Semantic decisions belong with the holder; deterministic
packet assembly belongs with existing compilers. Neither should duplicate the
other's responsibilities.

## Consequences

- Detail loads only at the relevant responsibility or execution boundary.
- Existing typed legacy packets stay readable without becoming mandatory.
- A useful return states results, evidence, limits, and the next owner action;
  it does not automatically create stats, memory, or proof obligations.
- Source and contract checks cannot establish usefulness or live continuity;
  behavioral trials remain separate and require authorized delegation.

## Source Surfaces

- `skills/AGENTS.md`
- `skills/aoa-agents-skills/SKILL.md`
- `skills/aoa-agents-skills/references/role-first-entry.md`
- `skills/aoa-agents-skills/references/responsibility-classification.md`
- `skills/aoa-summon/scripts/prepare_external_actor.py`
- `skills/aoa-summon/SKILL.md`
- `skills/aoa-summon/references/lane-and-return.md`
- `capabilities/families/agent-lifecycle.yaml`
- `skills/port.manifest.json`

## Follow-Up Route

SDK owns its advisory routing contract and OS profile membership owns removal
of the universal routing skill. Runtime owners retain launch and wake support.
Compare real native, independent-duty, continuation, and return tasks when
those trials are authorized; do not infer their outcome from prompt parity.

## Verification

Rebuild decision and capability projections, validate the skill homes, and run
the focused actor-preparation and execution contract suites. Check installation
and fresh host visibility separately from source validity and behavior.
