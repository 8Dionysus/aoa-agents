# AGENTS.md

## Applies To

This card applies to the `aoa-agents` owner capability home under
`capabilities/`.

## Role

This home owns the semantic tree and typed relations used to discover and
compose agent-layer obligations, role formation, incarnation handoff,
responsibility transfer, return, wake, summon, and progression procedures.

It does not own domain workflows, model-fit evidence, runtime dispatch, CLI
processes, A2A transport, task-local DAG instances, proof, or memory truth.

## Editing posture

- Keep every node owned by `aoa-agents` and bind stronger-owner dependencies
  through typed inputs, provenance, and handoff contracts.
- Give every node one primary navigation parent; use relations for cross-tree
  flow and compatibility.
- Keep model brands, reasoning modes, runtime handles, raw trials, and concrete
  goal DAGs out of authored capability source.
- Do not advertise a skill until manual trigger, ABI, effect, binding, return,
  and held-out evidence supports admission.
- Rebuild generated projections; never hand-edit them as authority.

## Validation

From the canonical `aoa-skills` checkout, run:

```bash
PYTHONPATH=scripts python scripts/validate_capability_home_port.py --owner-root /path/to/aoa-agents
PYTHONPATH=scripts python scripts/build_capability_home_projection.py --owner-root /path/to/aoa-agents
PYTHONPATH=scripts python scripts/build_capability_home_projection.py --owner-root /path/to/aoa-agents --check
PYTHONPATH=scripts python scripts/validate_capability_home_port.py --owner-root /path/to/aoa-agents --check-generated
```

