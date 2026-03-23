# RUNTIME ARTIFACT TRANSITIONS

## Purpose

This note makes the public runtime-artifact loop explicit without turning
`aoa-agents` into a runtime implementation repository.

It clarifies how the published artifact contracts relate to the public tier
loop and where `transition_decision` belongs.

## Public Loop

The external public loop remains:

`route -> plan -> do -> verify -> deep? -> distill`

This loop stays small and explicit.
It is a public contract for runtime-facing readers, not a hidden runtime body.

## Transition Decision Is Governance, Not A New Stage

`transition_decision` is a governance artifact between phases.

It tells the route whether to continue, pause, escalate, return to an earlier
phase, or distill.
It does not create a new sovereign stage that sits outside the public loop.

## Artifact Coverage To Preserve

The current artifact coverage is:

- `route_decision` for `route`
- `bounded_plan` for `plan`
- `work_result` for `do`
- `verification_result` for `verify`
- `transition_decision` for explicit governance between phases
- `deep_synthesis_note` for `deep`
- `distillation_pack` for `distill`

`work_result` and `deep_synthesis_note` remain agent-layer artifacts even when
some playbook-facing surfaces do not expose them in `expected_artifacts`.
That omission does not transfer ownership away from `aoa-agents`.

## Reference Scenarios Stay Reference-Only

`AOA-P-0008` and `AOA-P-0009` remain reference scenarios only.

They apply pressure to the seam and help check artifact coverage, but they do
not make scenario canon or run history owned by `aoa-agents`.

## Boundaries

- `aoa-playbooks` may publish scenario-facing subsets of artifact names
- `aoa-evals` may point at published artifact contracts during verdict hooks
- `aoa-memo` may point at published artifact contracts during writeback mapping
- `aoa-agents` keeps the artifact contracts and role × tier binding explicit
- runtime implementation still belongs outside this repository
