# Adoption And Regression Schemas

Part-local schemas for assistant and agent adoption/regression contracts.

| Schema | Contract |
| --- | --- |
| [agent-adoption-participation-record.schema.json](agent-adoption-participation-record.schema.json) | agent adoption participation |
| [agent-adoption-posture-contract.schema.json](agent-adoption-posture-contract.schema.json) | agent adoption posture |
| [assistant-adoption-certification-delta.schema.json](assistant-adoption-certification-delta.schema.json) | certification delta |
| [assistant-adoption-guard.schema.json](assistant-adoption-guard.schema.json) | adoption guard |
| [assistant-adoption-projection.schema.json](assistant-adoption-projection.schema.json) | adoption projection |
| [assistant-adoption-regression-matrix.schema.json](assistant-adoption-regression-matrix.schema.json) | adoption regression matrix |
| [assistant-adoption-release-candidate.schema.json](assistant-adoption-release-candidate.schema.json) | release candidate |
| [assistant-adoption-rollback-marker.schema.json](assistant-adoption-rollback-marker.schema.json) | rollback marker |
| [assistant-pattern-adoption-request.schema.json](assistant-pattern-adoption-request.schema.json) | pattern adoption request |
| [assistant-pattern-release-delta.schema.json](assistant-pattern-release-delta.schema.json) | pattern release delta |
| [assistant-shared-pattern-adoption.schema.json](assistant-shared-pattern-adoption.schema.json) | shared pattern adoption |

Validate with:

```bash
python scripts/validate_adoption_boundary_contracts.py
```
