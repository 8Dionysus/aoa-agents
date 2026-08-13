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

### 2026-08-13 - Compile reviewed returns without crossing owner boundaries

The first v4 runtime returns also need a deterministic owner-local closeout
adapter. `skills/aoa-summon/scripts/compile_external_execution_result.py`
consumes the exact v4 request, SDK request and decision, terminal runtime
result-v2, runtime-profile-v2 ref, and reviewed A2A return-v1. It verifies the
request digest, SDK identity, terminality, review disposition, output-key set,
usage locator, external handles, and authority ceiling before emitting one
`summon-result-v4` receipt.

The compiler preserves the stronger owner artifacts as exact refs and treats an
embedded usage observation as a content-addressed JSON-pointer locator into the
terminal result. It may accept outputs only when the supplied reviewed
disposition is `proceed`; owner acceptance, publication, runtime/A2A/usage
meaning, stats admission, proof, role selection, and model fit remain outside
the receipt compiler. V3 remains frozen and is not read as a source for new
results.

### 2026-08-13 - Close the reviewed-return validation gaps

The passive compiler now validates the supplied owner request against the
generated `summon-request-v4` schema before applying its external-lane
checks. A reviewed A2A return must carry the runtime-owned
`abyss_stack_external_codex_a2a_return_v1` provenance, bind its
`evidence_digests.writer_result` to the exact terminal runtime-result digest,
name an artifact path present in the reviewed remote task, and bind
`remote_task.task_id` and `remote_task.agent_id` exactly to the terminal
runtime `task_id` and `incarnation_id`. A proceed closeout is admitted only
for a completed runtime whose canonical
`wake_evaluation` is `result.validated` under `validated-completion`; a
`result.review_required` repair return cannot be widened into acceptance.

Embedded usage evidence is limited to the canonical
`/usage_observation` locator and the runtime-owned observation shape. Returned
artifacts are checked as a duplicate-free exact set of requested symbolic
output identities; unknown paths and basename aliases are not inferred or
silently ignored. These checks strengthen fail-closed evidence admission only;
they do not mint or reinterpret SDK, runtime, A2A, stats, proof, model-fit, or
owner-acceptance authority, and the original authority-blocked writer return
remains preserved evidence.

### 2026-08-13 - Admit only path-loaded owner artifacts

Path-loaded runtime profiles are admitted as
`abyss_stack_external_codex_runtime_profile_v2` only when the loaded payload
itself declares that exact schema version before a content ref is emitted. A
standalone usage artifact is admitted only through one explicit
`abyss_stack_external_codex_usage_observation_v1` envelope with a
`usage_observation_id`, `status`, and `gap_reasons`; the latter two fields use
the same canonical shape and gap law as embedded `/usage_observation` evidence.
Missing, relabeled, malformed, or extra-field payloads fail closed. Ref-only
usage and runtime-profile branches, and the embedded canonical locator branch,
retain their existing exact semantics. This narrows artifact admission only;
it does not mint runtime, usage, stats, proof, or owner-acceptance authority.

### 2026-08-13 - Bind the complete SDK request and derivative identity

Closeout now compares the complete owner summon body and passport with the SDK
request using the request compiler's single documented translation:
`a2a_remote` or `either` becomes `external_cli`, and the duplicate nested
output list is removed. Both admitted preparation effects, `read_only` and
`repo_mutation`, remain available; no other effect is accepted.

An actor-safe immutable-input envelope cannot by itself authenticate its
embedded `source_artifact_digest`, so the closeout receipt addresses the exact
envelope bytes instead of promoting that claim to stronger-owner identity.
The CLI separates content-ref input (`--usage-observation-ref`) from standalone
usage artifacts (`--usage-observation`) and refuses to replace an existing
receipt. These changes close evidence substitution and destructive-rerun gaps
without adding launch, selection, proof, or owner-acceptance authority.

Independent external review then exposed three remaining substitutions. The
SDK input must still say `a2a_remote` or `either`; accepting an already
translated `external_cli` value would bypass the single request-compiler
translation. An actor envelope's declared source schema must agree with the
unwrapped A2A payload's own schema version. Finally, the reviewed return must
bind the complete original SDK summon-request ref rather than a matching digest
alone. Closeout now fails closed on all three relations.

Exact-head GitHub review exposed two additional cross-attempt substitutions.
The terminal runtime result must bind its runtime-owned owner-admission ref to
the exact supplied owner-request identity and bytes; because that request
contains the runtime-launch and continuity refs plus the task/effect posture, an earlier
launch result cannot close a later request that merely reuses the same child
identity. Closeout also resolves the exact incarnation-binding-v2 artifact
named by the request and requires its incarnation, continuation, effect
posture, and runtime-profile provenance to match the request, terminal runtime,
and supplied profile ref. These checks add no new selection authority: they
only prevent an unrelated launch or syntactically valid profile from being
reported as the execution that actually returned.

A subsequent exact-head external Luna review and GitHub review exposed three
remaining contradictions. The logical continuation obligation is not a Codex
thread UUID, so the compiler does not equate them. Instead, the exact admitted
request and incarnation artifact bind the logical continuation, while every
runtime invocation must name the terminal runtime's physical `thread_id`.
Owner admission must match `request_ref` as well as the request-byte digest.
Finally, usage status is now semantic rather than decorative: `complete`
requires an empty gap list and `partial` requires at least one fully canonical
gap. These are evidence-link checks only; they grant no runtime or continuation
authority.

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
- `skills/aoa-summon/scripts/compile_external_execution_result.py`
- `tests/test_compile_external_execution_result.py`

## Follow-Up Route

Teach the external runtime admission boundary to resolve the v4 evidence refs
and the SDK incarnation-binding-v2 bytes before launch. Do not mutate the
already frozen and independently audited transport snapshot while doing so.

## Verification

Verification routes through schema regeneration checks, v3 byte-compatibility
tests, positive and negative v4 validation, semantic agent validators,
capability projections, and the repository release gate.
