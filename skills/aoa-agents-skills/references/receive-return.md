### Mode: receive-return

Filter one actor return or runtime event and make responsibility movement
explicit. A completed process does not itself determine acceptance or wake.

## Input

Require `actor-return-event-v1` with obligation, mandate, incarnation,
responsibility-transfer and runtime refs; event kind; named output artifacts;
actual effects and usage receipts; refusal/failure state; current holder;
return owner; and the task-local DAG node awaiting the event.

## Procedure

1. Validate event provenance and bind it to the exact obligation, mandate,
   incarnation, runtime handle, and expected output names.
2. Classify the event as progress, pause, refusal, escalation, failed,
   returned, or return-candidate. Runtime success is only one input.
3. Apply the mandate's return filter. Accept, reject, narrow, or hold each
   named output and effect separately.
4. Decide where responsibility now resides: receiving actor, prior holder,
   reviewer, domain owner, or unresolved hold.
5. Decide whether the task-local DAG advances, adds a review/repair branch,
   closes a branch, or remains unchanged.
6. Emit a wake request only when an exact existing role identity, wake right,
   trigger condition, authority, state root, and runtime re-entry contract are
   present. A wake request is not a launched process.
7. Return residual obligations and closeout routes without promoting raw traces
   into proof or memory truth.

## Output

Return `responsibility-return-disposition-v1` with event disposition, per-output
checks, effect and usage receipts, responsibility holder before and after,
task-local DAG update, accepted/rejected claims, residual obligations,
review/repair/memo/proof handoffs, optional wake request, uncertainty, and stop
line.
