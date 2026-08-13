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

### 2026-08-13 - Reject invalid incarnation authority before launch

Independent external Luna review found that closeout enforced the SDK
permission-posture cross-field invariants while request compilation did not.
The request compiler now rejects an external-effects flag that disagrees with
the effect classes, a read-only sandbox carrying non-read-only effects, and
secret access paired with `approval_policy=never`. It also requires the
incarnation effect ceiling to equal the exact runtime task and actor mandate.
This is an earlier fail-closed check on already owner-defined authority; it
does not narrow valid `read_only` or `repo_mutation` work and does not create
selection, launch, or acceptance authority.

### 2026-08-13 - Admit only owner-defined path-loaded artifacts

Path-loaded runtime profiles are admitted as
`abyss_stack_external_codex_runtime_profile_v2` only when the loaded payload
itself declares that exact schema version before a content ref is emitted.
Usage remains an owner-defined subtree of the exact terminal runtime result;
there is no separate path-loaded usage artifact contract to mint here. An
optional usage content ref may only assert the canonical JSON-pointer identity
and subtree digest. Missing, relabeled, malformed, or unrelated assertions
fail closed. This narrows artifact admission only; it does not mint runtime,
usage, stats, proof, or owner-acceptance authority.

### 2026-08-13 - Bind the complete SDK request and derivative identity

Closeout now compares the complete owner summon body and passport with the SDK
request using the request compiler's single documented translation:
`a2a_remote` or `either` becomes `external_cli`, and the duplicate nested
output list is removed. Both admitted preparation effects, `read_only` and
`repo_mutation`, remain available; no other effect is accepted.

An actor-safe immutable-input envelope cannot by itself authenticate its
embedded `source_artifact_digest`, so the closeout receipt addresses the exact
envelope bytes instead of promoting that claim to stronger-owner identity.
The CLI accepts an optional exact usage assertion through
`--usage-observation-ref` and refuses to replace an existing receipt. These
changes close evidence substitution and destructive-rerun gaps
without adding launch, selection, proof, or owner-acceptance authority.

The exact independent-review request is also one authority chain rather than
three parallel output declarations. Its top-level expected outputs, nested
summon outputs, and quest-passport expected artifacts must be the same exact,
nonempty, duplicate-free closure before closeout can accept the review.
Likewise, the continuation return owner is the exact concrete holder from the
obligation and mandate, including identity and digest; retaining only its
repository would permit responsibility to return to another holder.
The exact mandate also remains inside the obligation that formed it: its goal
and the request passport route anchor equal the obligation goal, while its
identity and continuity postures preserve the obligation lifecycle rather
than upgrading a task-instance duty into a persistent office.

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

The next exact-head GitHub review found two remaining owner-chain gaps. The
incarnation binding is now compared with the request across the exact
obligation, mandate, role resolution, model-fit query and projection, SDK task
request, role-contract identity, child identity, parent DAG, SDK decision,
responsibility transfer, and domain-procedure inputs. A receipt therefore
cannot report the request's actor chain while its exact binding names another
one. Usage remains the canonical observation subtree of the exact terminal
runtime result; `--usage-observation-ref` may only assert that same locator and
digest and can no longer replace it with evidence from another attempt. No
standalone usage artifact is minted because `abyss-stack` defines no such
owner artifact on this surface.

A fresh exact-head external Luna review found four final substitution and
contract-drift paths. Closeout now loads the exact actor-mandate-v1 artifact,
verifies its owner schema and semantic self-digest, and requires the request to
select that semantic identity while the incarnation binding names its exact
artifact bytes. Continuation lists reject any stale same-identity ref even when
the current exact ref is also present. Every actor-safe input envelope must
bind its provenance schema version to the payload schema version or, for an
intentionally schema-less owner payload, to the explicit expected owner
schema. The owner contract also removes the retired standalone usage-artifact
route and matches the compiler's canonical embedded observation plus optional
exact-ref assertion. These repairs narrow evidence admission; they do not add
role, model, runtime, review, or owner-acceptance authority.

Exact-head GitHub review then found that a derivative could retain a matching
schema version while omitting `source_schema_ref`. The shared envelope loader
now requires every actor-safe input envelope to retain both a nonempty source
schema ref and source schema version before any payload-specific validation.
The reviewed A2A path still narrows that ref to its canonical runtime schema.
This authenticates the derivative's schema identity without promoting its
unattested source-artifact digest.

The following exact-head GitHub review exposed two deeper owner-chain gaps
that an independent Luna pass did not report. The result compiler now admits
only the complete strict incarnation-binding-v2 shape, verifies its semantic
binding digest, requires its run-plan and model-realization refs, and preserves
one aoa-models source across the realization and fit projection. Both exact
content refs are now mandatory in the owner request and compiled receipt and
must match the binding, rather than trusting a recomputable binding digest. It also
compares the exact mandate's obligation, role resolution, selected role, and
ordered domain procedures with the request and binding. Recomputing surrounding
untrusted digests can therefore no longer substitute a truncated binding or a
different mandate chain. These are relationship checks over selected evidence,
not new model-selection or runtime authority.

The next exact-head GitHub review found two further contradictions in the
positive closeout fixture. The request could widen `child_scope.allowed_tools`
beyond both the mandate environment and the incarnation tool profile, and its
return owner could differ from the exact mandate, transfer prior holder, or
continuation owner. Closeout now requires one tool, MCP, effect, sandbox, and
return chain across those objects. Continuation retains its SDK provenance
shape, so the comparable invariant is the mandate owner's repository while
the concrete responsibility holder remains the mandate/request object ID and
the transfer's prior holder. These checks direct responsibility back to the
already selected owner; they do not create a new owner or authority.

The first real separately addressable Luna reviewer incarnation then found
three adjacent authority substitutions that the fixed test suite did not
cover. Closeout now loads the exact agent-obligation-v1 artifact and binds the
request authority limit to its responsibility boundary and the request stop
line to the exact mandate. It admits the incarnation permission posture only
when the SDK-owned external-effect, read-only-sandbox, and secret-approval
cross-field invariants hold. Finally, the responsibility transfer must name
both the exact prior return holder and the mandate continuity identity as its
current holder. These checks authenticate already selected owner ceilings and
responsibility identities; they do not add role, model, runtime, or acceptance
authority.

The next exact-head GitHub review found that the pre-launch compiler emitted
the mandate's tool list without comparing it with the selected incarnation
binding. The compiler now requires one exact tool and MCP ceiling across the
binding and mandate before emission, forbids inherited user configuration,
and requires the binding tool profile and top-level runtime-profile ref to be
the same provenance object. A wider host profile therefore cannot run merely
because later closeout would reject its return. This authenticates the already
selected environment and does not grant tool or runtime authority.

A later exact-head review found that goal and lifecycle preservation had been
enforced only after return. The request compiler now requires the mandate goal
and SDK passport route anchor to retain the originating obligation goal, and
requires mandate identity plus continuity posture to retain the obligation
lifecycle before it emits an executable request. This prevents a formed
task-instance duty from being redirected or upgraded into a persistent office
before the closeout compiler ever has a chance to reject its return.
The next review extended that same principle: mandate domain owner and
continuation delegated duty now equal the exact obligation on both passive
request and closeout paths, while the SDK decision must explicitly select
`a2a_remote`. An `either` request alone no longer proves that the SDK chose the
remote surface for this incarnation.

The following exact-head review found that closeout accepted a merely
well-shaped `review_summon_request_ref` without resolving the request that
authorized the independent review. Closeout now requires that exact artifact
and binds its raw digest, terminal-result source, writer path and task, route
anchor, audit closure, distinct read-only verifier, and review outputs to the
same execution. It also requires the allowed SDK decision to supply a nonempty
`cohort_pattern`; the passive adapter preserves that topology and never invents
a local `solo` fallback.

## Consequences

- The execution leaf receives evidence selected by upstream owners without
  becoming a role, model, or runtime selector.
- Runtime and return adapters can verify one evidence chain instead of trusting
  model labels or prose.
- Historical v3 receipts remain inspectable without weakening new execution.
- Domain procedure ownership and A2A authority remain outside `aoa-summon`.

## Source Surfaces

- `skills/aoa-summon/scripts/build_summon_v4_schemas.py`
- `skills/aoa-summon/scripts/compile_external_execution_request.py`
- `skills/aoa-summon/references/summon-request-v4.schema.json`
- `skills/aoa-summon/references/summon-result-v4.schema.json`
- `skills/aoa-summon/references/contract.yaml`
- `tests/test_aoa_agents_skill_tree.py`
- `tests/test_compile_external_execution_request.py`
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
