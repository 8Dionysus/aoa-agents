# 2026-05-26: Titan Example Localization

## Status

Accepted.

## Context

Titan already had active docs and config under `mechanics/titan/parts/`, but
its schema-backed public examples still lived in the root example district.
That kept Titan role-bearing, lineage, incarnation, roster, service-cohort,
and summon-boundary contracts split between active parts and a root support
surface.

Root `examples/` remains valid for shared examples, but these Titan examples
now have clear part owners and a bounded validation route.

## Decision

Move the active Titan examples into `mechanics/titan/parts/*/examples/` using
part-local names. Keep the shared schemas in root `schemas/` for this slice.

Add `scripts/validate_titan_examples.py` and wire it into
`scripts/validate_agents.py` so the active file set, schema alignment, lineage
config references, and old active filename shape are checked explicitly.

Preserve former root lookup only through Titan `PROVENANCE.md` and `legacy/`.

## Consequences

- Titan parts now own their public-safe contract examples alongside docs and
  config.
- Root `examples/` no longer carries Titan-specific examples.
- Titan schemas remain shared root contract surfaces until a later schema
  localization decision exists.
- Old root example names remain historical lookup facts only.

## Verification

```bash
python scripts/validate_titan_examples.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python -m pytest -q tests
python scripts/release_check.py
```
