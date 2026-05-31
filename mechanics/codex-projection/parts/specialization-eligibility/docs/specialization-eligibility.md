# Codex Specialization Eligibility

## Purpose

This document defines the first reviewed gate between role-local
specializations and installed Codex custom agents.

The gate exists because `agents/roles/*/specializations/*/specialization.json`
records are source-layer actor contracts. They can carry narrower permission,
tool, skill, technique, memory, proof, and projection posture, but that does
not make them installable Codex agents by default.

## Boundary Rule

Keep this order:

1. source role specialization
2. capability pack reference
3. specialization eligibility record
4. future projection builder change
5. generated Codex agent TOML
6. workspace `.codex/agents/` install

The eligibility record sits at step 3. It is not step 4, 5, or 6.

Current source eligibility records live under
`mechanics/codex-projection/parts/specialization-eligibility/records/`.
The generated readiness reader lives at
`mechanics/codex-projection/parts/specialization-eligibility/generated/specialization-eligibility-readiness.min.json`.

## What The Gate Must Name

An eligibility record must name:

- the specialization source path and specialization id;
- the base role that the specialization inherits from;
- the capability pack it relies on;
- the proposed Codex install identity;
- the requested permission posture;
- tool, skill, technique, memory, and proof refs that shape operation;
- owner consent requirements;
- proof evidence already observed and proof evidence still missing;
- the refresh law that would govern future projection;
- guardrails that prevent the record from being treated as an install.

## Decision States

Current states:

- `candidate_only`: the specialization is being discussed, not projected.
- `eligible`: the specialization has enough review evidence to be projected in
  a later builder change.
- `rejected`: the specialization must not be projected.
- `retired`: the eligibility record is historical.

Only a later projection-builder change may consume an `eligible` record.
This part intentionally has no projection builder.

## Owner Consent

The minimum owner consent set is:

- `aoa-agents`, for specialization and projection contract ownership;
- `workspace-codex`, for install-surface acceptance;
- `aoa-skills`, when skill refs become operational requirements;
- `aoa-techniques`, when technique refs become operational requirements;
- `aoa-memo`, when memory routes become operational requirements;
- `aoa-evals`, when proof routes become operational requirements.

Owner consent is recorded as data here. Durable truth stays with the owning
repository or workspace surface.

## Example Posture

The first example uses `coder.repo-refactor` as a candidate-only record.
It deliberately remains `not_projected` and keeps the repo manifest scope at
`base_role_profiles_only`.

That lets future agents inspect the shape of a promotion packet without
accidentally installing a specialized agent.

## Readiness Queue

The active queue records every current role-local specialization:

- `architect.topology-steward`
- `coder.repo-refactor`
- `evaluator.release-readiness`
- `memory-keeper.writeback-steward`
- `reviewer.route-drift-review`

All five records currently remain `candidate_only` and `not_projected`.
Their missing evidence keeps the next move explicit: workspace Codex install
consent, repeatable successful use evidence, and reviewed proof routing.

The readiness reader is generated from the records. It is useful for scanning
candidate state, but it does not own projection decisions.

## Validation

Run:

```bash
python mechanics/codex-projection/parts/specialization-eligibility/scripts/build_specialization_eligibility_readiness.py --check
python mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py
python -m unittest discover -s mechanics/codex-projection/parts/specialization-eligibility/tests -p "test_*.py"
```

The validator checks the schema, example, source specialization links,
capability pack links, record coverage for every current specialization,
readiness-reader freshness, projection-scope boundary, and non-install
guardrails.

Active schema and example:

- `mechanics/codex-projection/parts/specialization-eligibility/schemas/specialization-eligibility.schema.json`
- `mechanics/codex-projection/parts/specialization-eligibility/examples/specialization-eligibility.example.json`
- `mechanics/codex-projection/parts/specialization-eligibility/records/`
- `mechanics/codex-projection/parts/specialization-eligibility/generated/specialization-eligibility-readiness.min.json`
