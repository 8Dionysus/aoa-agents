# 2026-05-26: Titan Example Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0009
- Original date: 2026-05-26
- Surface classes: mechanic part, example/source
- Agent facets: mechanics atlas, titan role-bearing
- Mechanic parents: titan
- Guard families: part-local artifact, example validation
- Posture: accepted

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
part-local names. At landing time, schemas remained in root `schemas/`; the
later Titan schema localization moved the Titan-specific schemas beside the
examples.

Add a Titan example validator and wire it into `scripts/validate_agents.py` so
the active file set, schema alignment, lineage config references, and old
active filename shape are checked explicitly.

Preserve former root lookup only through Titan `PROVENANCE.md` and `legacy/`.

## Consequences

- Titan parts now own their public-safe contract examples alongside docs and
  config.
- Root `examples/` no longer carries Titan-specific examples.
- Titan-specific schemas are now routed by the later Titan schema localization
  decision.
- Old root example names remain historical lookup facts only.

## Verification

```bash
python mechanics/titan/scripts/validate_titan_examples.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python -m unittest discover -s mechanics/titan/tests -p "test_*.py"
python -m unittest discover -s tests -p "test_*.py"
python scripts/release_check.py
```
