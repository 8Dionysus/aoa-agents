### Mode: detect-obligation

Decide whether observed work pressure warrants a distinct bearer of
responsibility. This is not generic task decomposition and does not launch an
actor.

## Input

Require a `goal-pressure-v1` packet containing:

- goal and current responsibility-holder refs;
- planning, execution, or closeout phase;
- observed or anticipated duty and its domain owner;
- consequence if the duty is missed or remains merged into the current actor;
- independence signals: separate authority, conflicting interest, continuity,
  specialist environment, independent review, asynchronous return, or future
  wake;
- known timing, evidence, uncertainty, and existing role candidates.

## Procedure

1. Separate a genuine duty from an implementation step, convenience split, or
   available-model opportunity.
2. Test whether the duty needs its own responsibility holder. Name every
   positive and negative independence signal.
3. Check planning pressure for duties that will predictably arise later. A
   future duty may be admitted before its work is executable.
4. Select exactly one trigger strength: `notice`, `required_branch`,
   `master_decision`, or `preauthorized_reflex`.
5. For `preauthorized_reflex`, require the exact persistent-role identity,
   reviewed trigger contract, authority envelope, rollback, and current
   runtime admissibility. Otherwise narrow to `master_decision`.
6. Return either `not_independent` or one semantic obligation packet. After
   the independence and trigger decisions are complete, use the bundled
   compiler to validate and content-address the admitted packet as
   `agent-obligation-v1`; do not select a model, process, transport, or domain
   procedure implementation.

```bash
python <bundle_dir>/scripts/compile_actor_contract.py obligation \
  --input <semantic-obligation.json>
```

The compiler performs no obligation detection and accepts no model, runtime,
or budget fields.

## Output

`agent-obligation-v1` records:

- task-local obligation ref, goal anchor, phase, duty, and domain owner;
- current holder and intended responsibility boundary;
- independence findings and rejected ordinary-step interpretation;
- trigger strength and its authority source;
- expected outcome, named return owner, lifecycle posture, and stop line;
- evidence, uncertainty, and next route: hold, plan branch, master decision,
  existing-role wake review, or `form-actor`.

An obligation is not an actor, role, model selection, runtime binding, or
permission to launch.
