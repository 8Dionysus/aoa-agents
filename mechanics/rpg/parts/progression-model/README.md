# Progression Model Part

This part routes `progression-model` pressure inside `mechanics/rpg/`.

## Active Docs

- [Agent Progression Model](docs/agent-progression-model.md)

## Active Schema

- [Agent Progression Schema](schemas/agent-progression.schema.json)

## Active Example

- [Agent Progression Example](examples/agent-progression.example.json)

## Validation

```bash
python scripts/validate_rpg_progression.py
python scripts/validate_agents.py
python -m pytest -q tests/test_validate_agents.py
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
