# Assistant Civil Service Part

This part routes `assistant-civil-service` pressure inside `mechanics/experience/`.

## Active Docs

- [Assistant Kind Model](docs/assistant-kind-model.md)
- [Assistant Certification Authority Seam](docs/certification-authority-seam.md)
- [Assistant Civil Rechartering](docs/civil-rechartering.md)
- [Assistant Governance Appeals](docs/governance-appeals.md)
- [Assistant Service Certification Model](docs/service-certification-model.md)
- [Assistant Service Contract Model](docs/service-contract-model.md)
- [Assistant Service Governance Model](docs/service-governance-model.md)
- [Assistant Service Identity Model](docs/service-identity-model.md)

## Active Schemas

- [Assistant Variant](schemas/assistant-variant.schema.json)
- [Assistant Service Identity](schemas/service-identity.schema.json)
- [Assistant Service Contract](schemas/service-contract.schema.json)
- [Assistant Service Governance](schemas/service-governance.schema.json)
- [Assistant Service Certification](schemas/service-certification.schema.json)
- [Assistant Civil Formation](schemas/civil-formation.schema.json)

## Active Examples

- [Assistant Civil Formation](examples/civil-formation.example.json)

## Generated Reader

- [`generated/assistant_civil_formation_index.min.json`](../../../../generated/assistant_civil_formation_index.min.json)

This reader stays root-published because its source truth is the assistant
adjunct family under `agents/profiles/adjuncts/`, and because downstream role
readiness needs one repo-level formation view. This part owns the assistant
civil service contracts, examples, docs, and stop-lines around that reader; it
does not own the source adjunct records or turn generated output into source
authority.

## Active Checks

- [Formation Builder](scripts/build_assistant_civil_formation_index.py)
- [Formation Validator](scripts/validate_assistant_civil_formation.py)
- [Formation Tests](tests/test_assistant_civil_formation.py)

## Validation

```bash
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py
python -m unittest discover -s mechanics/experience/parts/assistant-civil-service/tests -p 'test_*.py'
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
