# Specialization Eligibility Part

This part defines the gate that a role-local specialization must pass before it
can be considered for Codex custom-agent projection.

It does not project agents and it does not install anything into workspace
`.codex/agents/`.

## Operating Card

| Field | Route |
| --- | --- |
| role | Codex specialization projection eligibility gate |
| input | role specialization source records, capability-pack refs, owner-consent pressure, proof evidence, and projection-boundary pressure |
| output | schema-backed eligibility record, example, validation result, or stronger-owner handoff |
| owner | this part owns the eligibility contract; `agents/roles/*/specializations/` owns specialization source truth; `subagent-projection/` owns actual Codex projection behavior |
| next route | docs, schema, example, validator, subagent projection boundary, refresh law, owner consent surfaces |
| tools | [scripts/validate_specialization_eligibility.py](scripts/validate_specialization_eligibility.py) |
| validation | validator, part tests, `scripts/validate_agents.py`, `scripts/release_check.py` |

## Active Docs

- [Specialization Eligibility](docs/specialization-eligibility.md)

## Active Schemas And Examples

- [Eligibility schema](schemas/specialization-eligibility.schema.json)
- [Eligibility example](examples/specialization-eligibility.example.json)

## Active Scripts And Tests

- [Eligibility validator](scripts/validate_specialization_eligibility.py)
- [Eligibility tests](tests/test_specialization_eligibility.py)

## Boundary

Eligibility is a promotion gate, not projection itself.

A specialization can be discussed here without becoming a generated Codex
agent. The current generated projection remains `base_role_profiles_only` until
a future reviewed change deliberately widens it.

## Validation

```bash
python mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py
python -m unittest discover -s mechanics/codex-projection/parts/specialization-eligibility/tests -p "test_*.py"
```
