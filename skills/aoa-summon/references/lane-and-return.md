# Lane, execution, and return

## Lane decision

If the literal request fails the request ABI, no lane exists yet. Return
`lane: null`, `allowed: false`, `decision_state: blocked`, and
`runtime_state.state: not_run`; do not manufacture a routing lane merely to
satisfy the result shape.

The request has exactly one expected-output list at its top level. Preserve a
content-addressed `request_ref`; compute `request_digest` as SHA-256 over
canonical JSON with the digest field omitted. Every result copies the ref,
digest, and intent. Before aggregate acceptance, resolve that request, verify
its digest, and require exact key-set equality between request
`expected_outputs` and result `return_validation.output_checks`.

| Passport and posture | Lane |
|---|---|
| `d0_probe` or `d1_patch`, low risk, clear anchor and outputs | `codex_local_leaf` |
| bounded `d2_slice`, low risk, narrowing reviewer/evaluator/verifier | `codex_local_reviewed` |
| complete `aoa-agents-skills` actor packet with an admitted distinct-holder responsibility transfer, exact role resolution, model-fit query and selected projection, SDK incarnation v2, and separate CLI runtime launch | `external_cli_reviewed` |
| separate endpoint or execution surface is truly required | `remote_reviewed` |
| `d3+` still unsplit | `split_required` |
| required progression/self-agent/approval evidence missing | `human_gate` |
| stress says `stop_before_mutation` | non-mutating narrowing child or `human_gate` |

Branch choice must already be settled. The local host child-agent interface is
the compatibility default for explicit child requests only. A source-authorized
external actor packet selects `external_cli_reviewed`; it may not fall back to
a built-in child lane.

### Mode: decide

Validate one complete request, select a lawful lane, preserve the immutable
request identity and named return map, and stop without probing or launching a
host binding. An allowed decision is not execution evidence.

### Mode: execute

1. Build a child passport containing parent anchor, one bounded task, expected
   outputs, allowed tools/effects, evidence inputs, stop line, and return owner.
2. Resolve the host binding before claiming execution. Record interface name,
   availability, binding kind, runtime owner, and any runtime constraints. The
   external lane additionally resolves exact role resolution, model-fit query,
   selected fit projection, incarnation v2, canonical SDK summon
   request/decision, admitted `aoa-agents` responsibility-transfer ref and its
   ordered distinct holder pair, and runtime-profile refs, and confirms
   built-in Codex subagents are disabled.
3. Launch exactly one runtime. Record the compatibility `child_handle` where
   material; for the external lane also record canonical actor, process,
   session, and continuation handles.
4. Track `launched` and `running` only from host state. Await or retrieve the
   terminal result; do not fabricate status from the request packet.
5. On return, check every expected output, source ref, scope boundary, actual
   effect, uncertainty, and stop condition. Represent the request's complete
   `expected_outputs` list as an `output_checks` object with exactly one key per
   named output; reject or narrow any missing, extra, or incomplete output.
   For the external lane, resolve the exact runtime-owned terminal result,
   reviewed A2A return, and usage observation. Keep them as refs: the
   `aoa-summon` result is an actor-execution/closeout receipt, not a fork of the
   SDK A2A schema or the runtime result schema.
6. Produce the parent closeout handoff: accepted outputs, rejected claims,
   residual risk, checkpoint consequence, optional memo candidate route, owner
   publication route, and whether parent work may continue.

Decision-only output does not need a host probe. If no probe occurred, set
`binding.inspected: false` and `binding.available: null`. A concrete
`available` value requires an actual interface inspection; launched, running,
returned, or accepted runtime state additionally requires
`binding.available: true` and a non-empty binding interface. Compatibility
child lanes additionally require a non-empty child handle; the external lane
requires its canonical actor, process, session, and continuation handles. An
`accepted` state additionally requires successful return validation,
at least one output check, and concrete parent-owner and next-route closeout
fields. Every accepted output check is received, artifact-linked, and accepted.
A `decided` state is reserved for `decide` intent, has no child handle or
actual effects, and carries the complete
named output map with unreceived values. A `not_run` state has no child handle,
output checks, accepted return, or actual effects and is never allowed. An
inspected unavailable binding carries a non-empty reason; an inspected available
binding carries no failure reason.
An allowed `execute` result must be launched, running, returned, accepted, or
failed; it cannot stop as a plan. A failed compatibility-child result retains
the inspected binding, child handle, and `child-agent-runtime` effect. A failed
external result instead retains its canonical external handles, runtime result
and usage refs, and `external-actor-runtime` effect. The retired result-side
`expected_outputs` field is invalid; output identity exists only in the
immutable request and the keyed validation map.
Aggregate return acceptance implies the `accepted` runtime state. An available
inspected binding names its concrete interface. `split_required` and
`human_gate` decisions use only their matching lanes in both directions, and
every allowed decision preserves the named outputs plus a concrete parent owner
and next route. Gate lanes carry no executable target. Launched and running
states carry no return checks yet. Every launched, running, returned, or
accepted compatibility-child state records `child-agent-runtime`; external
states record `external-actor-runtime` as specified below.

## Required result additions

- `decision_state`: `allowed`, `blocked`, `split_required`, or `human_gate`
- `binding`: interface, availability, and reason when unavailable
- `runtime_state`: state, child handle, launch/return timestamps or `not_run`
- `return_validation`: one uniquely keyed check per requested output and aggregate acceptance
- `closeout_handoff`: parent owner, checkpoint, residual risk, next route
- `actual_effects` and `stop_line`
- immutable request ref, digest, and copied intent

The nullable lane is reserved for pre-admission request failure. Once the
request ABI passes, select one concrete lane from the table.

For `external_cli_reviewed`, every post-launch state carries
`external-actor-runtime`, an `external_cli_incarnation` binding, the exact
`aoa-sdk` incarnation, summon request, summon decision, and runtime-profile
refs plus the exact role-resolution, model-fit query, and selected fit
projection refs, runtime owner, and all four canonical handles. Returned or accepted
states also carry exact runtime result, reviewed A2A-return, and usage refs; a
failed terminal state carries the exact runtime result and usage refs without
inventing a reviewed return. Usage remains observe-only counting and never
becomes a caller-authored execution budget.

`summon-request-v3` and `summon-result-v3` remain frozen historical read
contracts. New decisions and executions use v4; a v3 receipt may be inspected
for compatibility but cannot authorize a fresh launch.

Blocked, failed, and narrowed actors return through the same responsibility
surface.
Raw traces may help review but never become proof, memory canon, or owner truth.

## Passive request compilation

`compile_external_execution_request.py` is the pre-launch adapter for an
already selected `external_cli_reviewed` incarnation. Before emitting a
request it validates the SDK-owned permission-posture shape and its
external-effect, read-only-sandbox, and secret-approval cross-field
invariants. The exact allowed effect classes must also equal both the runtime
task effect and actor-mandate ceiling. The binding's exact tool and MCP sets
must equal the actor-mandate environment, its tool profile must name the same
runtime profile, and it cannot inherit user configuration. The mandate goal
and SDK quest-passport route anchor must retain the originating obligation
goal, while mandate identity and continuity posture must retain the obligation
lifecycle. The mandate also retains the obligation domain owner, the
continuation retains its exact duty, the mandate stop line retains the
obligation stop line, its model-fit relation is authorized by the current
obligation holder, and the SDK decision must explicitly
select `a2a_remote`. The supplied incarnation binding must pass the complete
aoa-sdk v2 owner schema and its SDK-canonical semantic self-digest before any
subset relation is considered. The schema bytes are pinned to the reviewed
aoa-sdk owner artifact rather than trusted by `$id` or caller path. The run
plan also passes the complete generated SDK `RunPlan` schema pinned by
canonical content, and retains fresh SDK-canonical snapshot and plan digests
before any snapshot input is consulted. A contradiction stops before launch;
the compiler does not select a narrower posture or rewrite owner authority.

## Passive result compilation

`compile_external_execution_result.py` is the closeout adapter for a returned
`external_cli_reviewed` lane. It accepts only a terminal
`abyss_stack_external_codex_result_v2`, the exact SDK request and transport
decision named by the summon request, the exact agent-obligation-v1,
actor-mandate-v1, aoa-role-resolution-v1, and incarnation-binding-v2
artifacts, an exact
runtime-profile-v2 ref, and a reviewed
`abyss_stack_external_codex_a2a_return_v1` whose disposition is `proceed`,
plus the exact review summon request named by that return. It
first admits the owner request against the generated
`summon-request-v4` schema, then verifies the semantic digest, the SDK request
digest recorded by the SDK decision, the complete owner summon body and
passport under the one documented transport-only translation, distinct
responsibility holders, one admitted `read_only` or `repo_mutation` effect,
disabled built-in subagents, and exact output
keys. Closeout also loads the exact agent-obligation-v1 and
actor-mandate-v1 artifacts: the request authority limit and stop line must
equal their owner ceilings, the mandate goal and quest-passport route anchor
must equal the obligation goal, mandate identity and continuity posture must
preserve the obligation lifecycle, and the mandate domain owner plus delegated
continuation duty must equal the exact obligation. The mandate stop line must
equal the obligation stop line and its model-fit relation authority must equal
the current obligation holder. Its complete role binding must equal the
independently loaded exact role-resolution artifact. The transfer holders must
equal the return owner and mandate continuity identity, the SDK continuation must retain that same
concrete return-holder identity and digest rather than merely its repository,
and the incarnation permission posture must
satisfy the aoa-sdk cross-field invariants. The terminal runtime
owner-admission ref must address the exact owner
request bytes, which binds that result to the selected runtime launch and
continuity chain. The incarnation artifact digest and its incarnation,
continuation, effect, and tool-profile fields must match the request, runtime,
and supplied runtime-profile ref exactly. The reviewed return must carry its
runtime-owned schema provenance,
agree with that provenance in its unwrapped payload schema, bind the complete
original SDK summon-request ref,
reference the exact terminal runtime-result digest, bind
`remote_task.task_id` and `remote_task.agent_id` exactly to the terminal
runtime `task_id` and `incarnation_id`, and agree with the runtime's canonical
`result.validated`/`validated-completion` wake event.
The review request digest, runtime-result source ref, writer path, writer task,
route anchor, verifier identity, read-only risk, audit closure, and review
output closure must all describe this exact execution. Its quest passport
must authorize that same exact review output closure rather than carrying a
parallel artifact list. The admitted SDK
decision must provide its own nonempty cohort pattern; this adapter does not
default missing SDK topology to `solo`.
Missing, stale, mismatched, nonterminal, unreviewed, or wider evidence fails
closed.

The compiler preserves authenticated stronger-owner objects as
content-addressed refs. An actor-safe immutable-input envelope is instead
addressed by its exact derivative bytes: its embedded source digest is
provenance, not stronger-owner authentication. Every envelope must retain a
nonempty source schema ref, and its provenance schema version must equal the
payload schema version or, for an intentionally schema-less payload, the
explicit expected owner schema version. It does not copy their protocol fields
into the owner receipt by default. The runtime result ref and reviewed A2A ref
use their terminal identities and source digests; the usage ref is exactly
`runtime-result-id#/usage_observation` with the digest of the runtime-owned
observation-shaped JSON subtree at that pointer. An opt-in compiler projection
may additionally copy a bounded, observe-only snapshot from the exact
runtime-result-v2 bytes after checking the runtime-result, task, usage-pointer,
and usage-subtree digests. That projection never replaces the stronger runtime
refs, and it cannot make a model-fit, benefit, success, proof, review-approval,
owner-acceptance, budget, or limiting claim.
The observation passes the canonical status/gap law: `complete` means no gaps
and `partial` means one or more canonical gaps. Returned artifacts must be
the exact unique requested output identities; path basename inference and
unrequested extras are rejected. Actor, session, continuation, and process
handles are derived only from the runtime's incarnation/session/thread/process-identity
evidence. The logical continuation remains bound by the exact owner request and
incarnation artifact; the physical continuation handle is accepted only when
the terminal `thread_id` equals every runtime invocation's `thread_id`. The
runtime owner-admission ref likewise names the exact owner request identity and
bytes. The exact actor mandate passes its owner schema and semantic self-digest;
the request selects that semantic identity while the incarnation binding also
binds its exact artifact bytes. The incarnation binding likewise names the
exact obligation, role resolution, model-fit query and projection, SDK task
request, continuation inputs without stale same-identity refs, and child
identity carried by the owner request. It must retain the complete strict
owner-v2 shape and semantic digest, including run-plan and model-realization
refs, and the realization must share the fit projection's aoa-models source.
The owner request carries both exact refs and must match the binding, rather
than relying on the binding's recomputable digest alone.
The exact mandate separately binds the same obligation, role resolution,
selected role, and ordered domain-procedure set. The CLI may load an exact assertion
through `--usage-observation-ref` and refuses to replace an existing output.
The emitted receipt is a summon responsibility-closeout record, not
stats admission, runtime success proof, model-fit proof, or owner acceptance.

## Actor responsibility observation and publication

The owner-local observation route is separate from external execution
closeout. `scripts/compile_actor_responsibility_receipt.py` validates one
exact external-lane `summon-result-v4` and explicit observation coordinates,
then emits the admitted `actor_responsibility_execution_receipt` envelope.
The caller must also provide the canonical artifact ref for those exact input
bytes; the request ref is retained separately and is never reused as the
source-result ref.
The payload schema is owned by `aoa-agents`; it retains exact stronger-owner
references and the result-byte digest without copying SDK, runtime, A2A, or
stats authority into a competing protocol. Runtime refs follow the source
state: returned and accepted preserve result, reviewed A2A-return, and usage;
failed preserves result and usage without inventing an A2A return; launched and
running preserve no return refs until the runtime supplies them.

The event identity is deterministic over the exact result digest, canonical
receipt payload projection, and explicit observation inputs (`observed_at`,
`run_ref`, `session_ref`, `actor_ref`, and `object_ref`). A caller-supplied
digest or event ID is an assertion, not an override, and mismatches fail
closed.

The receipt projection keeps `execution.runtime_state` equal to
`owner_evidence.runtime_state.state`. The source `blocked_actions` and
`reason_codes` arrays are compacted before strict payload validation by dropping
empty strings and later duplicates while preserving first-seen order; the
receipt schema still rejects an uncompact direct publisher input.

When a live usage report is required, the compiler accepts `--runtime-result`
and `--expected-runtime-result-digest`. The runtime path must be a regular
file whose bytes match the terminal `runtime_result_ref` (or an exact actor-safe
runtime envelope whose payload does), whose A2A task identity is checked
independently from an optional result identity, and whose `/usage_observation`
subtree matches the accepted `usage_observation_ref`. The resulting
`usage_observation` payload is a bounded snapshot of model, reasoning, token,
timing, activity, outcome, and observe-only metering fields; missing or
non-reported values remain null and are named in `unknown_fields`. A repaired
snapshot may use `--supersedes` to append a new event without rewriting the
older accepted receipt.

Publication is an explicit second action through
`scripts/publish_actor_responsibility_receipts.py`. It validates every input
and every existing JSONL line, skips already-seen event IDs, and refuses to
append when the existing log is malformed. Its default path is
`.aoa/live_receipts/actor-responsibility-execution-receipts.jsonl`; the owner
root resolves through a complete same-bundle source handle or an explicit
`--owner-root`; an installed v2 handle must include its bundle version and
provenance identity dimensions, and a test-local path must be supplied for
tests. The compiler projects only the canonical parent-owner, residual-risk,
and next-route closeout fields; source-schema extensions do not widen the
strict receipt. Nothing in summon execution or compilation
automatically appends to a live feed. The publisher takes a POSIX advisory
exclusive lock at `<log-path>.lock` before reading existing IDs and holds it
through the append, so independent sessions sharing one path cannot race the
event-ID deduplication. The lock file is owner-local coordination rather than
receipt source data; unsupported lock hosts fail closed.

The receipt records observation posture only. It must not be read as a claim
of benefit, model fit, task success, proof, reviewer approval, or owner
acceptance; those remain separate owner decisions and evidence.
