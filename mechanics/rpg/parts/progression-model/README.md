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
python mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py
python -m unittest discover -s mechanics/rpg/parts/progression-model/tests -p 'test_*.py'
python scripts/validate_agents.py
python -m pytest -q tests/test_repo_validator.py
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
