# Subagent Projection Part

This part routes source profile to Codex custom-agent projection pressure inside
`mechanics/codex-projection/`.

## Operating Card

| Field | Route |
| --- | --- |
| role | Codex subagent projection builder, module, validator, and freshness tests |
| input | active `agents/roles/*/profile.json` records and part-local wiring config |
| output | root-published generated Codex custom-agent TOML, config snippet, and manifest |
| owner | this part owns projection behavior; `generated/` owns published output edit law |
| next route | source profiles, wiring config, generated Codex agents, refresh law, release check |
| tools | [scripts/build_codex_subagents_v2.py](scripts/build_codex_subagents_v2.py), [scripts/validate_codex_subagents.py](scripts/validate_codex_subagents.py) |
| validation | builder `--check`, projection validator, part tests, `scripts/validate_agents.py`, `scripts/release_check.py` |

## Active Docs

- [Codex Subagent Projection](docs/subagent-projection.md)

## Active Config

- [Codex Subagent Wiring](config/wiring.v2.json)
- [Config Route](config/README.md)

## Active Scripts And Tests

- [Projection builder](scripts/build_codex_subagents_v2.py)
- [Projection module](scripts/codex_subagent_projection.py)
- [Projection validator](scripts/validate_codex_subagents.py)
- [Projection tests](tests/test_codex_subagent_projection.py)

## Published Output

- [../../../../generated/codex_agents/agents](../../../../generated/codex_agents/agents)
- [../../../../generated/codex_agents/config.subagents.generated.toml](../../../../generated/codex_agents/config.subagents.generated.toml)
- [../../../../generated/codex_agents/projection_manifest.json](../../../../generated/codex_agents/projection_manifest.json)

These outputs stay root-published because they are the repo-side install seam
for workspace Codex custom agents. They are still derived readers; edit the
source profiles, wiring config, or projection builder instead of hand-editing
generated TOML.

## Validation

```bash
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python -m unittest discover -s mechanics/codex-projection/parts/subagent-projection/tests -p "test_*.py"
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
