# 2026-05-26: Antifragility Stress Payload Localization

## Status

Accepted.

## Context

Antifragility stress docs already live under
`mechanics/antifragility/parts/stress-posture/`, but their schema-backed public
adjuncts still lived in root `schemas/` and `examples/`. That kept a named
repeatable operation split between active part docs and root support payloads.

The two schemas and two examples are not shared profile, model-tier,
checkpoint, runtime-artifact, or reference-route contracts. They describe the
stress-posture part's own role narrowing bands and bounded handoff envelope.

## Decision

Move stress-posture schemas and examples into
`mechanics/antifragility/parts/stress-posture/{schemas,examples}/` using
part-local names. Keep stable schema `$id` values unchanged because they are
public contract identifiers, not active repository path authority.

Add `scripts/validate_antifragility_stress.py` and wire the same file-set,
schema, example, and old-route checks into `scripts/validate_agents.py`.

Preserve former root lookup only through antifragility `PROVENANCE.md` and
`legacy/`.

## Consequences

- The `stress-posture` part now co-locates docs, schemas, and examples.
- Root `schemas/` and `examples/` remain active for shared or not-yet-localized
  contracts.
- Existing schema `$id` values remain stable for consumers.
- Old root stress payload names remain historical lookup facts only.

## Verification

```bash
python scripts/validate_antifragility_stress.py
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python -m pytest -q tests/test_antifragility_public_surface.py
python -m pytest -q tests
python scripts/release_check.py
```
