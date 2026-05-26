# 2026-05-26: Recursor Generated Reader Localization

## Status

Accepted.

## Context

Recursor configs, schemas, examples, and component manifests already live in
active Recurrence part-local routes. Four derived readers still remained in
root `generated/`:

```text
generated/recursor_role_readiness.min.json
generated/recursor_pair_contract.min.json
generated/recursor_projection_candidates.min.json
generated/recursor_agon_boundary_report.min.json
```

Those readers summarize Recurrence part-local source truth. Keeping them in
root `generated/` blurred repo-wide published registries with part-local
mechanic companions.

## Decision

Move the recursor generated readers into their owning Recurrence parts:

```text
mechanics/recurrence/parts/recursor-readiness/generated/role-readiness.min.json
mechanics/recurrence/parts/recursor-readiness/generated/pair-contract.min.json
mechanics/recurrence/parts/codex-recursor-projection/generated/projection-candidates.min.json
mechanics/recurrence/parts/agon-recursor-boundary/generated/boundary-report.min.json
```

Teach the recursor builders, validators, tests, and recurrence component
manifests the part-local routes. Guard former root generated paths through
`mechanics/recurrence/scripts/validate_recursor_contracts.py`.

## Consequences

Root `generated/` continues to own repo-level registries, formation readers,
quest readers, and Codex projection outputs that still have root publication
posture. Recursor readers now live beside the config and contract surfaces
they summarize.

Recurrence `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md` preserve old-path lookup. Active docs should
reference the part-local paths.

## Validation

```bash
python mechanics/recurrence/scripts/build_recursor_role_readiness.py --check
python mechanics/recurrence/scripts/build_recursor_projection_candidates.py --check
python mechanics/recurrence/scripts/validate_recursor_contracts.py
python mechanics/recurrence/scripts/validate_recursor_role_readiness.py
python mechanics/recurrence/scripts/validate_recursor_boundary.py
python scripts/validate_recurrence_component_manifests.py
python scripts/validate_agents.py
```
