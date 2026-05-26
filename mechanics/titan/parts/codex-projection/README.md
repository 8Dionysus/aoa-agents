# Codex Projection Part

This part routes Titan-specific Codex projection pressure inside
`mechanics/titan/`.

## Operating Card

| Field | Route |
| --- | --- |
| role | Titan Codex projection builder and freshness check |
| input | active Titan bearer records and role-class records |
| output | generated Codex custom-agent companions under `generated/titan_codex_agents/` |
| owner | this part owns the Titan-specific builder; `generated/` owns published output edit law |
| next route | role-bearing config, generated Titan Codex agents, release check |
| tools | [scripts/render_titan_codex_agents.py](scripts/render_titan_codex_agents.py) |
| validation | builder `--check`, part tests, `scripts/validate_agents.py`, `scripts/release_check.py` |

## Source Surfaces

- [../role-bearing/config/role-classes.v0.json](../role-bearing/config/role-classes.v0.json)
- [../role-bearing/config/bearers.v0.json](../role-bearing/config/bearers.v0.json)

The projection keeps Codex-visible identities aligned with named Titan bearers:
Atlas, Sentinel, Mneme, Forge, and Delta. Role classes remain source metadata,
not generated agent names.

## Published Output

- [../../../../generated/titan_codex_agents/agents](../../../../generated/titan_codex_agents/agents)
- [../../../../generated/titan_codex_agents/projection_manifest.json](../../../../generated/titan_codex_agents/projection_manifest.json)

These outputs are root-published so workspace install and low-context Codex
consumers can find them. They are still derived; edit the source configs or the
builder instead of hand-editing generated TOML.

## Validation

```bash
python mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --out-dir generated/titan_codex_agents/agents --manifest generated/titan_codex_agents/projection_manifest.json --prune --check
python -m unittest discover -s mechanics/titan/parts/codex-projection/tests -p "test_*.py"
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent
[PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
