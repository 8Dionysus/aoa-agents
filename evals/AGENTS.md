# AGENTS.md

## Applies to

This card applies to `aoa-agents/evals/` and every file below it.

## Role

This skeleton port captures agent-layer eval pressure before it is accepted,
rejected, or normalized by `aoa-evals`.

`aoa-evals` owns central verdict, scoring, regression, and proof doctrine
authority. This port owns only agent-local intake, cases, fixtures, suites,
reports, and source refs.

## Boundaries

- Keep role profiles, handoff posture, memory posture, checkpoint posture, and
  projection boundaries in `aoa-agents`.
- Keep proof doctrine, verdicts, scoring, and regression authority in
  `aoa-evals`.
- Do not treat an intake packet as proof acceptance or a central eval verdict.
- Do not place private traces, secrets, or unreduced operator evidence here.

## Validation
Use the repository [validation map](../VALIDATION.md) and the nearest owner check when this route is relevant.

## Closeout

Report changed eval surfaces, current `PORT.yaml` status, validation run, any
skipped central proof adoption, and the next route into `aoa-evals` when needed.
