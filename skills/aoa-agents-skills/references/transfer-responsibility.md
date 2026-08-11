### Mode: transfer-responsibility

Establish a situational A2A responsibility relation and use one external
execution leaf to incarnate it. The relation is not the launcher transport.

## Input

Require a `responsibility-transfer-request-v1` containing the exact obligation,
actor mandate, evidence-complete incarnation binding v2, task-local DAG node, current holder,
intended holder, named outputs, domain procedure refs, authority/effects,
return owner, refusal/escalation rules, and stop line.

## Procedure

1. Confirm the current holder may transfer this responsibility and that the
   receiving actor may refuse or narrow it.
2. Record the A2A relation: obligation held, mandate boundaries, accepted
   authority, expected return, refusal/escalation, pause/resume, and wake
   rights. Do not encode transport details as the relation's meaning.
3. Select an execution leaf only after the relation and incarnation binding
   are complete.
4. Use `aoa-summon` only through an external CLI lane that consumes the exact
   incarnation binding v2, role-resolution and model-fit refs, canonical SDK
   summon request/decision, and runtime launch refs, and returns a real
   separate process/session handle. Never
   satisfy this route with its built-in Codex child-agent lanes.
5. Launch once, record the holder transition and runtime evidence, then leave
   execution state with the runtime owner. Do not claim completion from a
   process start.
6. On return, keep the SDK A2A decision and `abyss-stack` terminal/A2A-return
   artifacts under their owners. The execution leaf may issue its own
   responsibility-closeout receipt only by referencing those exact bytes; it
   must not fork their protocols.

## Output

Return `responsibility-transfer-v1` with prior and current holders, obligation,
mandate, incarnation and task-local DAG refs, accepted/narrowed/refused state,
authority, named outputs, runtime process/session/continuation handles when
launched, domain procedure refs, return and wake rules, actual effects, usage
receipt posture, evidence classes, and stop line.
