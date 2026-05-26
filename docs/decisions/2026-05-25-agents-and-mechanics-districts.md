# 2026-05-25: Agents And Mechanics Districts

## Status

Accepted.

## Context

`aoa-agents` had source-authored agent objects in legacy root-level family
directories.

That shape made the role layer valid but less legible than sibling repositories
that had already matured into source-object districts and operation mechanics.
The repo also lacked a `mechanics/` atlas for recurring agent-layer operations
such as formation, projection, runtime-seam binding, checkpoint posture, quest
posture, Titan role-bearing surfaces, and release support.

## Decision

Create `agents/` as the source-authored agent object district and move the
existing source object families under it:

- `agents/roles/`
- `agents/operating-model/tiers/`
- `agents/operating-model/orchestrators/`
- `agents/operating-model/cohorts/`
- `agents/operating-model/runtime-seams/`

Create `mechanics/` as the operation atlas for repeatable agent-layer
mechanics. The first slice activates the atlas and artifact-topology rule, but
does not yet move flat public docs, shared schemas, examples, scripts, tests,
or generated readers into mechanic-local packages.

## Consequences

- Source path references in builders, validators, tests, docs, examples, and
  generated readers now use `agents/...`.
- `agents/` and `mechanics/` both have route cards and design placement.
- New structural route cards use an `Operating Card` table so future agents see
  role, input, output, owner, next route, tools, and validation before local
  boundary detail.
- Later mechanics package moves should be smaller, evidence-backed slices with
  package-local validation instead of one broad flat-doc shuffle.

## Verification

Topology-aware validation should include:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
python -m pytest -q tests
```
