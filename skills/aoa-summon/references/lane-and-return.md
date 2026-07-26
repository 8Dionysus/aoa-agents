# Lane, execution, and return

## Lane decision

If the literal request fails the request ABI, no lane exists yet. Return
`lane: null`, `allowed: false`, `decision_state: blocked`, and
`runtime_state.state: not_run`; do not manufacture a routing lane merely to
satisfy the result shape.

| Passport and posture | Lane |
|---|---|
| `d0_probe` or `d1_patch`, low risk, clear anchor and outputs | `codex_local_leaf` |
| bounded `d2_slice`, low risk, narrowing reviewer/evaluator/verifier | `codex_local_reviewed` |
| separate endpoint or execution surface is truly required | `remote_reviewed` |
| `d3+` still unsplit | `split_required` |
| required progression/self-agent/approval evidence missing | `human_gate` |
| stress says `stop_before_mutation` | non-mutating narrowing child or `human_gate` |

Branch choice must already be settled. Default transport is the local host
child-agent interface.

## Execute mode

1. Build a child passport containing parent anchor, one bounded task, expected
   outputs, allowed tools/effects, evidence inputs, stop line, and return owner.
2. Resolve the host binding before claiming execution. Record interface name,
   availability, and any runtime constraints.
3. Launch exactly one child and record `child_handle` or canonical task name.
4. Track `launched` and `running` only from host state. Await or retrieve the
   terminal result; do not fabricate status from the request packet.
5. On return, check every expected output, source ref, scope boundary, actual
   effect, uncertainty, and stop condition. Represent the request's complete
   `expected_outputs` list as exactly one ordered `output_checks` record per
   named output; reject or narrow any missing, extra, duplicate, or incomplete
   output.
6. Produce the parent closeout handoff: accepted outputs, rejected claims,
   residual risk, checkpoint consequence, optional memo candidate route, owner
   publication route, and whether parent work may continue.

Decision-only output does not need a host probe. If no probe occurred, set
`binding.inspected: false` and `binding.available: null`. A concrete
`available` value requires an actual interface inspection; launched, running,
returned, or accepted runtime state additionally requires
`binding.available: true`, a non-empty binding interface, and a non-empty child
handle. An `accepted` state additionally requires successful return validation,
at least one output check, and concrete parent-owner and next-route closeout
fields. Every accepted output check is received, artifact-linked, and accepted.
A `decided` or `not_run` state has no child handle, no output checks, no
accepted return, and no actual effects. A non-allowed decision remains
`not_run`; an inspected unavailable binding carries a non-empty reason.
Aggregate return acceptance implies the `accepted` runtime state. An available
inspected binding names its concrete interface. `split_required` and
`human_gate` decisions use only their matching lanes in both directions, and
every allowed decision requires parent closeout.

## Required result additions

- `decision_state`: `allowed`, `blocked`, `split_required`, or `human_gate`
- `binding`: interface, availability, and reason when unavailable
- `runtime_state`: state, child handle, launch/return timestamps or `not_run`
- `return_validation`: one ordered check per requested output and aggregate acceptance
- `closeout_handoff`: parent owner, checkpoint, residual risk, next route
- `actual_effects` and `stop_line`

The nullable lane is reserved for pre-admission request failure. Once the
request ABI passes, select one concrete lane from the table.

Blocked, failed, and narrowed children return through the same parent surface.
Raw traces may help review but never become proof, memory canon, or owner truth.
