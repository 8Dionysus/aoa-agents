### Mode: responsibility-classification

Emit an owner-produced negative result only when an explicit caller needs the
typed classification, including the legacy summon local ABI. Ordinary Codex
helpers need neither this operation nor its receipt. This mode does not select
a tool, model, runtime, or domain procedure and grants no execution permission.

## Input

Require the supplied `goal-pressure-v1` context with:

- the anchored Goal and current responsibility-holder refs;
- the execution epoch of that explicit compatibility request;
- the presented agent-tool or delegation decision;
- the positive and negative independence findings;
- the reason the work remains an ordinary local step;
- the bounded stop line and evidence refs.

## Procedure

1. Confirm that an agent-tool responsibility decision was actually presented
   by the owning routing control plane or current holder.
2. Confirm that responsibility does not move: the work remains a local step,
   no independent authority or continuity is required, and no external return
   owner is being created.
3. Build the semantic classification packet with the exact Goal, current
   holder, request execution epoch, child-scope digest, reason, evidence, and
   stop line. Set only
   `disposition: not_independent` and `next_route: codex_local`.
4. Validate and content-address it with the owner compiler:

```bash
python <bundle_dir>/scripts/compile_actor_contract.py classification \
  --input <semantic-classification.json>
```

5. Return the exact result ref to the caller. A prose statement or session
   memory is not a substitute for this packet. Do not invoke a built-in child
   tool from this mode.

## Output

Return `responsibility-classification-v1` with its stable classification id,
Goal, holder, execution epoch, and child-scope digest, `not_independent`
disposition, reason, `codex_local` next route, stop line, evidence refs, and
semantic digest. The explicit compatibility request and its classification
must share an execution epoch; session resumption alone does not mint one or
require a new semantic decision. The local request validator still rejects a
classification from another request epoch. This
is not a one-time-consumption record and does not detect replay within the
same epoch; that state belongs to the routing/runtime owner.

## Verification

- The schema and compiler digest pass.
- The result names the same Goal and current holder supplied by the pressure.
- The result does not contain a role, model, transport, process, runtime, or
  launch claim.
- An explicit legacy `summon-request-v4` local execution must bind the exact
  returned ref; native Codex orchestration does not enter that legacy lane.
