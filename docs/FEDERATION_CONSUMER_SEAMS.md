# FEDERATION CONSUMER SEAMS

## Purpose

This document records the current bounded consumer seams between `aoa-agents`
and neighboring AoA repositories.

It exists to keep published agent-layer contracts visible to consumers without
letting `aoa-agents` absorb neighboring routing, playbook, eval, or memo
meaning.

## Core rule

`aoa-agents` may publish reusable role, tier, artifact, and cohort surfaces.
Neighboring repositories may consume those surfaces through bounded contracts.

Those consumers keep their own meaning.
They do not move their canon into `aoa-agents`.

## Current consumer seams

- `aoa-playbooks` consumes agent names, model-tier artifacts, and a bounded
  cohort-compatible reference subset
- `aoa-evals` consumes artifact schema refs only
- `aoa-memo` owns memory-object canon and recall meaning; `aoa-agents` may
  consume published object recall seams as role posture only
- `aoa-routing` consumes model-tier registry for tier hints and selects the next
  memo path
- `aoa-sdk` may consume agent-layer workspace trigger posture as additive
  guidance for when `aoa surfaces detect` should open after ingress and guard
- `aoa-agents` may read routing-published memo recall entrypoints as bounded
  consumer guidance, where doctrine recall stays the default tiny-model path and
  `memory_objects` stays an explicit parallel family

## Consumer Check Matrix

### `aoa-playbooks`

Promise:
- `aoa-agents` publishes agent names, artifact names, and the bounded
  `checkpoint_cohort` / `orchestrated_loop` compatibility slice

Validator confirms:
- `AOA-P-0006` matches `checkpoint_cohort.allowed_role_sets[0]`
- `AOA-P-0008` matches one of `orchestrated_loop.allowed_role_sets`
- `AOA-P-0008.expected_artifacts` stays inside published artifact names

Out of scope:
- full playbook doctrine
- universal playbook-to-cohort mapping
- scenario ownership

### `aoa-evals`

Promise:
- `aoa-agents` publishes artifact schema refs that eval surfaces may point at

Validator confirms:
- eval example refs that target `repo:aoa-agents/...` resolve to existing
  public surfaces

Out of scope:
- verdict logic
- proof doctrine
- cohort awareness inside `aoa-evals`

### `aoa-memo`

Promise:
- `aoa-agents` publishes role posture and may consume memo-owned recall seams as
  bounded consumer guidance

Validator confirms:
- writeback-facing examples can resolve public `aoa-agents` refs
- object recall contracts keep inspect/expand/capsule surfaces aligned

Out of scope:
- memory-object canon
- recall doctrine ownership
- memo lifecycle policy

### `aoa-routing`

Promise:
- `aoa-agents` publishes the model-tier registry and may read routing-published
  memo entry surfaces as consumer guidance only

Validator confirms:
- routing tier hints resolve back to the published tier registry
- doctrine-default memo recall entrypoints remain intact
- `memory_objects` remains a parallel recall family

Out of scope:
- dispatch policy
- recall-family selection policy
- cohort-aware routing in this slice

### `aoa-sdk`

Promise:
- `aoa-agents` may publish bounded workspace trigger posture for when additive
  `aoa surfaces detect` should open after ingress and mutation gate passes

Validator confirms:
- the trigger posture keeps `aoa skills enter`, `aoa skills guard`, and
  `aoa surfaces detect` in explicit order
- the trigger posture keeps shortlist and ambiguity hints advisory-only
- `aoa-skills` remains the only immediate activation lane in this slice

Out of scope:
- routing verdicts
- non-skill activation
- playbook promotion doctrine
- owner-layer truth

## Bounded playbook-compatible cohort subset

This slice treats only two playbooks as cohort-compatible reference routes:

- `AOA-P-0006 -> checkpoint_cohort`
- `AOA-P-0008 -> orchestrated_loop`

These checks stay bounded:

- `AOA-P-0006` should match `checkpoint_cohort.allowed_role_sets[0]`
- `AOA-P-0008` should match one of `orchestrated_loop.allowed_role_sets`

Playbooks outside this reference subset may remain valid without a cohort
mapping in this slice.

## Routing seam

`aoa-routing` currently consumes `generated/model_tier_registry.json` through
`generated/task_to_tier_hints.json`.

The bounded routing contract for this slice is:

- `source_of_truth.tier_registry_repo == "aoa-agents"`
- `source_of_truth.tier_registry_path == "generated/model_tier_registry.json"`
- `preferred_tier` resolves in the model-tier registry
- `fallback_tier`, when present, resolves in the model-tier registry
- `output_artifact` matches the `artifact_requirement` of the `preferred_tier`

Router remains tier-aware, not cohort-aware, in this slice.

`aoa-agents` may also read routing-published memo recall entry surfaces through:

- `generated/task_to_surface_hints.json`
- `generated/tiny_model_entrypoints.json`

The bounded memo-facing routing contract for this slice is:

- root memo `inspect` and `expand` remain doctrine-first
- doctrine recall stays the default tiny-model memo path
- doctrine and object-facing semantic or lineage recall may publish
  `capsule_surfaces_by_mode` so consumers hydrate capsules before full section
  expansion
- `memory_objects` remains a parallel recall family selected explicitly through
  `recall_family`
- `aoa-agents` reads these surfaces as consumer guidance only and does not own
  dispatch policy, memo truth, or family selection rules

## Eval and memo seams

`aoa-evals` continues to consume published artifact contract refs.
It does not consume cohort patterns in this slice.

`aoa-memo` continues to consume published writeback-facing refs and runtime
boundary docs.
It does not consume cohort patterns in this slice.
`aoa-agents` does not define memory-object canon or recall meaning in this slice.

## Optional smoke-check posture

After `python -m pip install -r requirements-dev.txt`, `python scripts/validate_agents.py`
may smoke-check the bounded consumer seams below when the corresponding roots are supplied:

- `AOA_PLAYBOOKS_ROOT`
- `AOA_EVALS_ROOT`
- `AOA_MEMO_ROOT`
- `AOA_ROUTING_ROOT`

These checks confirm bounded consumer contract reachability only.
They do not validate whole neighboring repositories or import their meaning.
`AOA_MEMO_ROOT` also confirms published object recall surface reachability for
`aoa-agents` consumer posture only.

The workspace-trigger posture for `aoa-sdk` remains a docs-level consumer seam
rather than an optional smoke-check target.

## Boundaries to preserve

- do not require new fields in neighboring repos for this slice
- do not make `aoa-routing` consume the cohort registry
- do not make `aoa-evals` or `aoa-memo` cohort-aware here
- do not widen reference playbook checks into universal playbook doctrine
- do not move tiny-model recall-family selection policy into `aoa-agents`
