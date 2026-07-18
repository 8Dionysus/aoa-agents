# Lane, execution, and return

## Lane decision

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
   effect, uncertainty, and stop condition. Reject or narrow incomplete output.
6. Produce the parent closeout handoff: accepted outputs, rejected claims,
   residual risk, checkpoint consequence, optional memo candidate route, owner
   publication route, and whether parent work may continue.

## Required result additions

- `decision_state`: `allowed`, `blocked`, `split_required`, or `human_gate`
- `binding`: interface, availability, and reason when unavailable
- `runtime_state`: state, child handle, launch/return timestamps or `not_run`
- `return_validation`: expected versus received outputs and acceptance
- `closeout_handoff`: parent owner, checkpoint, residual risk, next route
- `actual_effects` and `stop_line`

Blocked, failed, and narrowed children return through the same parent surface.
Raw traces may help review but never become proof, memory canon, or owner truth.
