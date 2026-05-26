# 2026-05-26: Experience Assistant Civil Contract Localization

## Status

Accepted.

## Context

Wave II assistant civil rechartering had active Experience docs and source
adjuncts, but its schemas and public reader example still lived in root
`schemas/` and `examples/`. That kept assistant service contracts in a shared
root district even after `mechanics/experience/parts/assistant-civil-service/`
and `mechanics/experience/parts/arena-exclusion/` became the owning operation
routes.

The Agon formation contract localization deliberately left this payload family
for a separate Experience-owned pass so Agon would not absorb assistant
service authority.

## Decision

Move the Wave II assistant civil schemas and reader example into Experience
part-local contract routes:

- service-form schemas and the civil formation reader example live under
  `mechanics/experience/parts/assistant-civil-service/`
- arena-exclusion schema lives under
  `mechanics/experience/parts/arena-exclusion/schemas/`
- old root path lookup is preserved through Experience `PROVENANCE.md` and
  `legacy/`

Add `scripts/validate_experience_assistant_civil_contracts.py` to keep the
part-local file set, moved example, source adjunct payloads, and former root
paths bounded.

## Consequences

Experience is now the active lookup route for assistant civil service
contracts. Root `schemas/` and `examples/` no longer act as the active homes
for this Wave II family.

The source adjunct records remain under `agents/profiles/adjuncts/assistant_*`
because they are source-authored agent objects, not mechanic payloads.

Stable schema `$id` and `schema_version` values remain unchanged as public
contract identifiers.

Validation for this route is:

```bash
python scripts/validate_experience_assistant_civil_contracts.py
python scripts/validate_assistant_civil_formation.py
python scripts/build_assistant_civil_formation_index.py --check
python scripts/validate_agents.py
```
