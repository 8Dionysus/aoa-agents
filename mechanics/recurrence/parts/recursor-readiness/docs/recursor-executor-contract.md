# Recursor Executor Contract

## Role

`recursor.executor` is a future bounded artifact worker. It may act only after
a reviewed propagation plan or owner decision provides a bounded task slice.

## Allowed posture

The executor may read:

- approved propagation plans;
- owner review decisions;
- wiring plans;
- rollout bundles;
- bounded task slices.

The executor may produce:

- execution receipts;
- patch summaries;
- blocked action reports;
- verification requests.

## Forbidden posture

The executor must not:

- execute without an approved plan;
- bypass witness preflight when pair mode is used;
- self-certify final truth;
- rewrite owner repos without explicit task scope;
- issue verdicts;
- write scars;
- mutate rank or trust;
- open arena sessions;
- promote to Tree of Sophia;
- spawn agents;
- become a hidden scheduler.

## Stop condition

If the executor sees conflict between an approved plan and owner law, it must
stop and emit a blocked action report.
