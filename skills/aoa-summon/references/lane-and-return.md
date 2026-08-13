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

## Passive result compilation

`compile_external_execution_result.py` is the closeout adapter for a returned
`external_cli_reviewed` lane. It accepts only a terminal
`abyss_stack_external_codex_result_v2`, the exact SDK request and transport
decision named by the summon request, an exact runtime-profile-v2 ref, and a
reviewed `abyss_stack_external_codex_a2a_return_v1` whose disposition is
`proceed`. It first admits the owner request against the generated
`summon-request-v4` schema, then verifies the semantic digest, the SDK request
digest recorded by the SDK decision, the complete owner summon body and
passport under the one documented transport-only translation, distinct
responsibility holders, one admitted `read_only` or `repo_mutation` effect,
disabled built-in subagents, and exact output
keys. The reviewed return must carry its runtime-owned schema provenance,
reference the exact terminal runtime-result digest, bind
`remote_task.task_id` and `remote_task.agent_id` exactly to the terminal
runtime `task_id` and `incarnation_id`, and agree with the runtime's canonical
`result.validated`/`validated-completion` wake event.
Missing, stale, mismatched, nonterminal, unreviewed, or wider evidence fails
closed.

The compiler preserves authenticated stronger-owner objects as
content-addressed refs. An actor-safe immutable-input envelope is instead
addressed by its exact derivative bytes: its embedded source digest is
provenance, not stronger-owner authentication. It
does not copy their protocol fields into the owner receipt. The runtime result
ref and reviewed A2A ref use their terminal identities and source digests; the
usage ref is exactly `runtime-result-id#/usage_observation` with the digest of
the runtime-owned observation-shaped JSON subtree at that pointer unless a
standalone usage artifact is explicitly supplied. A standalone artifact must
declare `abyss_stack_external_codex_usage_observation_v1`, contain exactly its
usage-observation identity plus `status` and `gap_reasons`, and pass the same
canonical status/gap validation as the embedded observation. Returned artifacts must be
the exact unique requested output identities; path basename inference and
unrequested extras are rejected. Actor, session, continuation, and process
handles are derived only from the runtime's incarnation/session/thread/process-identity
evidence. The CLI loads content refs through `--usage-observation-ref`, loads
standalone artifacts through `--usage-observation`, and refuses to replace an
existing output. The emitted receipt is a summon responsibility-closeout record, not
stats admission, runtime success proof, model-fit proof, or owner acceptance.
