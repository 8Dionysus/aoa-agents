# Dispatch Reader Part

This part owns the generated quest catalog and dispatch reader contract.

Source quest truth stays in `quests/`. Human open-obligation visibility stays
in `QUESTBOOK.md`. Generated readers remain root-published consumer seams under
`generated/`.

## Source Surfaces

- [QUESTBOOK.md](../../../../QUESTBOOK.md)
- [quests](../../../../quests/README.md)
- [quest catalog](../../../../generated/quest_catalog.min.json)
- [quest dispatch](../../../../generated/quest_dispatch.min.json)
- [quest catalog example](../../../../generated/quest_catalog.min.example.json)
- [quest dispatch example](../../../../generated/quest_dispatch.min.example.json)

## Validation

```bash
python scripts/generate_questbook_readers.py --check
python scripts/validate_agents.py
```

Use parent [PARTS](../../PARTS.md) for the full mechanic map and parent
[PROVENANCE](../../PROVENANCE.md) for former path accounting.
