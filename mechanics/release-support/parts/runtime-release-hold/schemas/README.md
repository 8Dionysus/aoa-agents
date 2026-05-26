# Runtime Release Hold Schemas

Part-local schema for release-hold decisions that support agent-layer
publication and release readiness without becoming CI or runtime deployment
authority.

| Schema | Contract |
| --- | --- |
| [agent-release-hold.schema.json](agent-release-hold.schema.json) | release hold policy packet |

Validate with:

```bash
python scripts/validate_agent_service_contracts.py
```
