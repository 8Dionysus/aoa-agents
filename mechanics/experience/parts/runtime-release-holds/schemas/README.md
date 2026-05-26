# Runtime Release Holds Schemas

Part-local schemas for assistant compatibility, activation, approval,
candidate, service version, service release, and runtime hold contracts.

| Schema | Contract |
| --- | --- |
| [agent-install-compatibility.schema.json](agent-install-compatibility.schema.json) | install compatibility |
| [assistant-office-live-contract.schema.json](assistant-office-live-contract.schema.json) | live office contract |
| [assistant-release-activation.schema.json](assistant-release-activation.schema.json) | release activation |
| [assistant-release-approval.schema.json](assistant-release-approval.schema.json) | release approval |
| [assistant-release-candidate.schema.json](assistant-release-candidate.schema.json) | release candidate |
| [assistant-runtime-hold.schema.json](assistant-runtime-hold.schema.json) | assistant runtime hold |
| [assistant-service-release.schema.json](assistant-service-release.schema.json) | service release |
| [assistant-service-version.schema.json](assistant-service-version.schema.json) | service version |

Validate with:

```bash
python scripts/validate_agent_service_contracts.py
```
