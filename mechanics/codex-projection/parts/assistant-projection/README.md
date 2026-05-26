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

## Validation

```bash
python scripts/validate_assistant_projection_resolver.py
python scripts/validate_agents.py
python -m pytest -q tests/test_wave1_assistant_projection.py
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
