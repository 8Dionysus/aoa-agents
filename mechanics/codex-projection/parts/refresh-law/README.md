# Refresh Law Part

This part routes `refresh-law` pressure inside `mechanics/codex-projection/`.

## Active Docs

- [Codex Subagent Refresh Law](docs/subagent-refresh-law.md)

## Active Examples

- [Codex Subagent Refresh Law Example](examples/subagent-refresh-law.example.json)

## Validation

```bash
python mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py
python -m unittest discover -s mechanics/codex-projection/parts/refresh-law/tests -p 'test_*.py'
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
