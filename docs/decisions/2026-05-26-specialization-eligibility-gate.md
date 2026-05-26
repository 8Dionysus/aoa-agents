# 2026-05-26: Specialization Eligibility Gate

## Status

Accepted.

## Context

`aoa-agents` now has role-local specializations and a protected Codex projection
boundary. The current generated Codex projection remains base-role-only through
`projection_scope: base_role_profiles_only`.

The next risk is the opposite of the previous one: if the repo only says
"specializations are not projected," future work has no structured way to
review when a specialization is mature enough for projection. That can lead to
either permanent stagnation or an unreviewed builder change.

The needed surface is a gate, not a projection builder.

## Decision

Create a new Codex projection part:

```text
mechanics/codex-projection/parts/specialization-eligibility/
```

This part owns a schema-backed eligibility record for future specialized Codex
agents. It records:

- specialization source identity;
- proposed Codex install identity;
- permission posture;
- owner consent requirements;
- observed and missing proof evidence;
- refresh-law reference;
- non-install guardrails.

The first example uses `coder.repo-refactor` as `candidate_only` and
`not_projected`. It does not change `generated/codex_agents/`, workspace
`.codex/agents/`, or any runtime behavior.

## Consequences

- Future specialization projection work has a reviewable packet shape before it
  touches the projection builder.
- `subagent-projection/` remains the only owner of generated Codex agent
  projection behavior.
- Capability-pack projection hints still do not grant install authority.
- Owner consent and proof evidence are named as data here, but durable truth
  stays with the owning repositories and workspace surfaces.
- `scripts/validate_agents.py` and `scripts/release_check.py` now validate the
  eligibility part.

## Verification

```bash
python mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py
python -m unittest discover -s mechanics/codex-projection/parts/specialization-eligibility/tests -p "test_*.py"
python scripts/validate_agents.py
python scripts/release_check.py
```
