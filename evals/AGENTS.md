# AGENTS.md

Local route card for `aoa-agents/evals/`.

This skeleton port captures future role and handoff eval pressure without
making an agent profile a proof bundle.

`aoa-evals` owns central verdict, scoring, regression, and proof doctrine
authority. Keep role truth in `aoa-agents`; route proof adoption to
`aoa-evals`.

Validation:

```bash
python ../aoa-evals/scripts/validate_local_eval_port.py --target-root .
```
