# Arena Exclusion Schemas

These schemas define assistant arena-exclusion contracts inside the Experience
mechanic. They keep assistant service forms outside contestant, judge, closer,
scar-writer, and ToS-promotion authority unless a stronger Agon recharter
route explicitly changes that posture.

| Schema | Contract |
| --- | --- |
| [agent-kind-conflict-case.schema.json](agent-kind-conflict-case.schema.json) | kind-boundary conflict case |
| [arena-exclusion.schema.json](arena-exclusion.schema.json) | assistant arena-exclusion adjunct |
| [assistant-recharter-request.schema.json](assistant-recharter-request.schema.json) | reviewed assistant recharter request |

Validate with:

```bash
python mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py
python mechanics/experience/scripts/validate_agent_service_contracts.py
```
