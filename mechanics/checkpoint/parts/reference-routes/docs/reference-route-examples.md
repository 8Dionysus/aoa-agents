# Reference Route Examples

## Purpose

`mechanics/checkpoint/parts/reference-routes/examples/` contains example-only, non-normative route packs.
`mechanics/questbook/parts/alpha-reference-routes/examples/` contains playbook-facing Alpha reference-route surfaces for the curated readiness lane.
`mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json` is the compact published adjunct view over those Alpha example sources.

These route packs make the public loop inspectable through small manifest-driven examples that stay inside existing artifact schemas and runtime seam bindings.

## Core rule

They are not playbooks.
They are not routing policy.
They are not runtime canon.

They exist as teaching and validation surfaces only.

## Manifest surface

Each route pack is anchored by `manifest.json`.

The manifest exposes:

- `route_id`
- `cohort_pattern`
- `role_set`
- `steps`

Each step must name:

- `phase`
- `tier_id`
- `role_name`
- `artifact_path`

The artifact files referenced by `artifact_path` must use only the
already-published
`mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.*.schema.json`
contracts.

## Current route packs

The current bounded set uses kebab-case package routes while preserving the
stable manifest `route_id` values:

- `solo-bounded-route` with `route_id: solo_bounded_route`
- `pair-change-route` with `route_id: pair_change_route`
- `checkpoint-self-change-route` with `route_id: checkpoint_self_change_route`
- `orchestrated-loop-route` with `route_id: orchestrated_loop_route`

Together they show bounded role posture, review edges, governed self-change posture, and the full orchestrated loop without adding runtime logic.

The Alpha companion set is:

- `local-stack-diagnosis.example.json`
- `self-agent-checkpoint-rollout.example.json`
- `validation-driven-remediation.example.json`
- `long-horizon-model-tier-orchestra.example.json`
- `restartable-inquiry-loop.example.json`

These Alpha surfaces stay playbook-facing and state exact phase order,
required artifacts, allowed re-entry modes, memo writeback kinds, and eval
anchors for the curated readiness lane.

## Boundaries to preserve

- do not turn these examples into scenario canon
- do not add hidden transport, tool wiring, or runtime logs
- do not let manifests replace `aoa-playbooks` or `aoa-routing`
- keep the surface public-safe and portable

## Validation

The checkpoint contract validator covers the manifest schema, route-pack
coverage, cohort fit, tier path fit, runtime-seam fit, and every referenced
artifact instance.

For the Alpha companion set, the Questbook validator checks that
`mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json`
stays aligned with
`mechanics/questbook/parts/alpha-reference-routes/examples/*.example.json`.
The repository release gate owns the wider check.
