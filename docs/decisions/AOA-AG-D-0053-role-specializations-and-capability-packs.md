# 2026-05-26: Role Specializations and Capability Packs

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0053
- Original date: 2026-05-26
- Surface classes: role specialization, capability pack, generated/readout
- Agent facets: role specialization, capability posture
- Mechanic parents: cross-mechanic
- Guard families: source topology, sibling-owner boundary, generated/read-model
- Posture: accepted

## Context

The convex `agents/` source tree made base role houses visible, but a remaining
topology question was how to represent narrower agents such as a refactor coder,
route-drift reviewer, topology architect, release evaluator, or writeback
memory keeper.

Flattening these into top-level role names would make `roles/` noisy and would
confuse base identity with operating posture. Putting every tool, permission,
skill, technique, memory, and proof ref directly into base profiles would make
profiles heavy and would blur stronger owner boundaries.

## Decision

Keep base role identity stable under `agents/roles/<role>/profile.json`.

Add role-local specializations under:

```text
agents/roles/<role>/specializations/<slug>/specialization.json
```

Each specialization inherits from the base role profile and points to one
capability pack under:

```text
agents/operating-model/capabilities/packs/*.capability.json
```

Capability packs are reusable operating bundles for permission posture, tool
refs, skill refs, technique refs, memory routes, proof routes, projection
hints, owner boundaries, and stop lines. They are references and posture, not
implementations.

Publish separate generated readers:

- `generated/role_specialization_catalog.min.json`
- `generated/capability_pack_registry.min.json`

## Consequences

- `architect`, `coder`, `reviewer`, `evaluator`, and `memory-keeper` remain
  durable base roles.
- Narrower agents become `role.specialization` records, such as
  `coder.repo-refactor`, without flattening the role namespace.
- Reusable operating posture lives in capability packs instead of being copied
  across role houses.
- Validators must prove specialization path, role id, inherited profile, and
  capability-pack refs stay coherent.
- Stronger owners remain explicit: `aoa-skills` owns workflow bodies,
  `aoa-techniques` owns technique bodies, `aoa-memo` owns durable memory canon,
  `aoa-evals` owns proof doctrine, `aoa-routing` owns dispatch policy, and
  `abyss-stack` owns runtime behavior.

## Validation

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agent_source_home.py
python scripts/validate_agents.py
python -m unittest discover -s tests -p 'test_*.py'
python scripts/release_check.py
```
