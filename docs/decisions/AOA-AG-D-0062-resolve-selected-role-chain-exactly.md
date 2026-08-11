# Resolve A Selected Role Chain Exactly

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0062
- Original date: 2026-08-10
- Surface classes: owner skill home, role source, runtime consumer seam
- Agent facets: role contract, specialization, incarnation
- Mechanic parents: cross-mechanic, boundary-bridge
- Guard families: owner boundary, source identity, external incarnation
- Posture: admitted passive resolver inside challenger router

## Context

`aoa-agents-skills` correctly requires `form-actor` to use exact base-role,
specialization, tier, and capability-pack owner refs. The procedure could name
semantic IDs such as `coder.repo-refactor`, but an installed Codex session had
no checked way to turn that already-made semantic choice into exact clean
source refs. Guessing repository paths violates the owner-source gate, while a
hidden semantic router would move role-selection authority into an adapter.

## Options Considered

- Let every caller infer paths from role and specialization names.
- Add a resolver that ranks obligations against roles and chooses one.
- Add a passive resolver that accepts an already-selected role chain, checks
  owner topology, and returns content-addressed refs without choosing anything.

## Decision

Bundle `scripts/resolve_role_binding.py` inside `aoa-agents-skills`. The caller
must first select the smallest fitting existing role through `form-actor`
judgment. The resolver then verifies:

- the selected base role, specialization, tier, and implied capability pack
  exist in the exact `aoa-agents` worktree;
- specialization inheritance and capability-pack linkage are exact;
- the tier is explicitly admitted by the base role;
- every selected source is clean relative to one full Git source ref;
- every returned owner ref carries the exact byte digest and schema identity.

Its `aoa_role_resolution_v1` output explicitly denies semantic selection,
model selection, and runtime activation authority. A base-role-only resolution
does not invent a capability pack, and a specialization may use only the pack
linked by its owner source.

## Rationale

This closes the operational gap without making a deterministic adapter the
source of actor meaning. The model and runtime remain absent from role
resolution, while the next incarnation layer receives exact owner evidence
instead of prose or guessed paths.

## Consequences

- Any installed session can prove an already-chosen role chain from its exact
  owner root.
- A dirty, ambiguous, missing, or inconsistent selected source fails closed.
- Semantic fit still requires agent judgment under `form-actor`; the resolver
  cannot rank roles or create a task-named permanent role.
- Model-fit, SDK binding, runtime launch, and task-local DAG state remain with
  their existing stronger owners.

## Source Surfaces

- `skills/aoa-agents-skills/scripts/resolve_role_binding.py`
- `skills/aoa-agents-skills/references/role-resolution-v1.schema.json`
- `skills/aoa-agents-skills/references/form-actor.md`
- `tests/test_aoa_agents_role_resolver.py`

## Follow-Up Route

The role-resolution digest is now bound into `actor-mandate-v1` by
`AOA-AG-D-0064`. Next preserve the compiled mandate's explicit model-fit family
and selected projection through the `aoa-sdk` incarnation binding and external
execution request. Do not place either selection inside this resolver.

## Verification

Verification routes through the focused resolver tests, owner skill-tree tests,
decision-index checks, semantic agent validators, and repository release gate.
