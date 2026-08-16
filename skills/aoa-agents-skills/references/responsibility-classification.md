### Mode: responsibility-classification

Emit one owner-produced negative responsibility result for a presented
agent-tool decision that remains an ordinary local step. This mode does not
select a tool, model, runtime, or domain procedure.

## Input

Require the supplied `goal-pressure-v1` context with:

- the anchored Goal and current responsibility-holder refs;
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
   holder, child-scope digest, reason, evidence, and stop line. Set only
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
Goal, holder, and child-scope digest, `not_independent` disposition, reason,
`codex_local` next route, stop line, evidence refs, and semantic digest.

## Verification

- The schema and compiler digest pass.
- The result names the same Goal and current holder supplied by the pressure.
- The result does not contain a role, model, transport, process, runtime, or
  launch claim.
- The returned ref is carried into a later `summon-request-v4` before any
  Codex-local child lane is considered.
