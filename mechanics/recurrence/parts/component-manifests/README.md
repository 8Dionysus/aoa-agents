# Component Manifests Part

This part routes `component-manifests` pressure inside `mechanics/recurrence/`.

## Operating Card

| Field | Route |
| --- | --- |
| role | active recurrence component and hook manifest route |
| input | owner-reviewed component declarations for recursor, Agon, and Codex projection recurrence surfaces |
| output | component manifest set, hook binding set, validation signal, or stronger-owner handoff |
| owner | `mechanics/recurrence/parts/component-manifests/` |
| next route | `manifests/components/`, `manifests/hooks/`, parent `PARTS.md`, target mechanic part named by each manifest |
| tools | `scripts/validate_recurrence_component_manifests.py` |
| validation | recurrence component manifest validator plus repo validators |

## Active Manifests

Components:

- [agon-actor-formation-surfaces.json](manifests/components/agon-actor-formation-surfaces.json)
- [agon-epistemic-actor-posture.json](manifests/components/agon-epistemic-actor-posture.json)
- [agon-rank-jurisdiction-surfaces.json](manifests/components/agon-rank-jurisdiction-surfaces.json)
- [agon-school-campaign-posture.json](manifests/components/agon-school-campaign-posture.json)
- [codex-subagent-projection.json](manifests/components/codex-subagent-projection.json)
- [recursor-codex-projection-candidates.json](manifests/components/recursor-codex-projection-candidates.json)
- [recursor-readiness.json](manifests/components/recursor-readiness.json)

Hooks:

- [agon-actor-formation-surfaces.json](manifests/hooks/agon-actor-formation-surfaces.json)
- [agon-epistemic-actor-posture.json](manifests/hooks/agon-epistemic-actor-posture.json)
- [agon-rank-jurisdiction-surfaces.json](manifests/hooks/agon-rank-jurisdiction-surfaces.json)
- [agon-school-campaign-posture.json](manifests/hooks/agon-school-campaign-posture.json)

## Active Checks

- [Component Manifest Validator](scripts/validate_recurrence_component_manifests.py)
- [Component Manifest Tests](tests/test_recurrence_component_manifests.py)

## Boundaries

These manifests describe recurrence observation and refresh posture only. They
do not create hidden schedulers, live recursor execution, arena sessions,
verdicts, scar writes, rank mutation, owner repo rewrites, or workspace
projection installs.

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
