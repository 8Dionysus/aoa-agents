# Assistant Projection Part

This part routes `assistant-projection` pressure inside `mechanics/codex-projection/`.

No package-local docs moved into this part in the 2026-05-26 docs slice. The
active narrative anchor remains the Wave 1 section in
`../subagent-projection/docs/subagent-projection.md`.

## Active Schemas

- [Assistant Projection Resolver Schema](schemas/assistant-projection-resolver.schema.json)
- [Assistant Projection Resolver V1 Schema](schemas/assistant-projection-resolver-v1.schema.json)

## Active Example

- [Assistant Projection Resolver Example](examples/assistant-projection-resolver.example.json)

## Active Checks

- [Assistant Projection Resolver Validator](scripts/validate_assistant_projection_resolver.py)
- [Assistant Projection Resolver Tests](tests/test_assistant_projection_resolver.py)

## Validation

```bash
python mechanics/codex-projection/parts/assistant-projection/scripts/validate_assistant_projection_resolver.py
python -m unittest discover -s mechanics/codex-projection/parts/assistant-projection/tests -p 'test_*.py'
python scripts/validate_agents.py
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
