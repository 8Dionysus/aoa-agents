# 2026-05-30: Specialization Eligibility Registry

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0056
- Original date: 2026-05-30
- Surface classes: codex projection, role specialization, generated/readout
- Agent facets: codex projection, role specialization
- Mechanic parents: codex-projection
- Guard families: projection guard, specialization boundary, generated/read-model
- Posture: accepted

## Context

`aoa-agents` already has role-local specializations, capability packs, and a
Codex specialization eligibility gate. The first gate landed as a schema,
example, validator, and decision record, but it only demonstrated the packet
shape with `coder.repo-refactor`.

That left an awkward middle state: the repo could say that specializations are
not projected, but it did not have a live queue showing the projection
readiness of every current specialization.

The next step should harden the review path without widening Codex projection.

## Decision

Add a source eligibility registry under:

```text
mechanics/codex-projection/parts/specialization-eligibility/records/
```

Each current role-local specialization receives one `*.eligibility.json`
record. The records remain `candidate_only` and `not_projected`.

Add a generated readiness reader under:

```text
mechanics/codex-projection/parts/specialization-eligibility/generated/specialization-eligibility-readiness.min.json
```

The readiness reader summarizes decision status, install state, consent state,
missing evidence, and proposed Codex install names. It is generated from the
records and does not own projection decisions.

## Consequences

- Every current role specialization now has an explicit Codex projection
  readiness posture.
- Future work can inspect missing evidence before touching the projection
  builder.
- `generated/codex_agents/` and workspace `.codex/agents/` remain unchanged.
- The validator now proves record coverage and generated readiness freshness.
- A later builder change is still required before any specialization becomes an
  installed Codex custom agent.

## Verification

```bash
python mechanics/codex-projection/parts/specialization-eligibility/scripts/build_specialization_eligibility_readiness.py --check
python mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py
python -m unittest discover -s mechanics/codex-projection/parts/specialization-eligibility/tests -p "test_*.py"
python scripts/validate_agents.py
python scripts/release_check.py
```
