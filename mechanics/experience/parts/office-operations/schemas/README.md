# Office Operations Schemas

Part-local schemas for office adoption, service, install, pairing, and train
release contracts.

| Schema | Contract |
| --- | --- |
| [agent-office-charter-change.schema.json](agent-office-charter-change.schema.json) | office charter change |
| [assistant-multi-office-release-result.schema.json](assistant-multi-office-release-result.schema.json) | multi-office release result |
| [assistant-office-install-profile.schema.json](assistant-office-install-profile.schema.json) | office install profile |
| [assistant-office-live-profile.schema.json](assistant-office-live-profile.schema.json) | office live profile |
| [assistant-office-pairing.schema.json](assistant-office-pairing.schema.json) | office pairing |
| [assistant-office-revision-ledger-entry.schema.json](assistant-office-revision-ledger-entry.schema.json) | office revision ledger entry |
| [assistant-office-service-contract.schema.json](assistant-office-service-contract.schema.json) | office service contract |
| [assistant-train-release-participant.schema.json](assistant-train-release-participant.schema.json) | train release participant |
| [office-adoption-posture.schema.json](office-adoption-posture.schema.json) | office adoption posture |
| [office-pair-adoption-policy.schema.json](office-pair-adoption-policy.schema.json) | pair office adoption policy |
| [office-pattern-compatibility.schema.json](office-pattern-compatibility.schema.json) | office pattern compatibility |

Validate with:

```bash
python mechanics/experience/scripts/validate_adoption_boundary_contracts.py
python mechanics/experience/scripts/validate_agent_service_contracts.py
```
