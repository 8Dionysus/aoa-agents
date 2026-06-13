# AGENTS.md

## Applies to

This card applies to `aoa-agents/evals/` and every file below it.

## Role

This skeleton port captures agent-layer eval pressure before it is accepted,
rejected, or normalized by `aoa-evals`.

`aoa-evals` owns central verdict, scoring, regression, and proof doctrine
authority. This port owns only agent-local intake, cases, fixtures, suites,
reports, and source refs.

## Read before editing

Read the root `AGENTS.md`, then this card, `README.md`, `PORT.yaml`, and the
nearest intake, suites, or reports surface you will touch. For central proof
adoption rules, read the local eval-port standard in `aoa-evals`.

## Boundaries

- Keep role profiles, handoff posture, memory posture, checkpoint posture, and
  projection boundaries in `aoa-agents`.
- Keep proof doctrine, verdicts, scoring, and regression authority in
  `aoa-evals`.
- Do not treat an intake packet as proof acceptance or a central eval verdict.
- Do not place private traces, secrets, or unreduced operator evidence here.

## Validation

```bash
python ../aoa-evals/scripts/validate_local_eval_port.py --target-root .
```

## Closeout

Report changed eval surfaces, current `PORT.yaml` status, validation run, any
skipped central proof adoption, and the next route into `aoa-evals` when needed.
