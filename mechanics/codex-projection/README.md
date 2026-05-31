# Codex Projection Mechanic

Status: active package.

`mechanics/codex-projection/` routes projection from agent source profiles into
Codex-facing subagent surfaces. It owns projection posture, specialization
eligibility, refresh law, and wiring route; it does not own Codex runtime
behavior.

## Operating Card

| Field | Route |
| --- | --- |
| role | Codex-facing projection operation package |
| input | profile, specialization, wiring, generated subagent, refresh-law, manifest, and projection-boundary pressure |
| output | refreshed projection route, eligibility record, generated eligibility readiness reader, generated manifest, compatibility note, or runtime/config handoff |
| owner | this package for projection routing; `agents/roles/` and `parts/subagent-projection/config/` for source inputs |
| next route | `PARTS.md`, Codex projection builders, `mechanics/agon/` for Agon projection boundaries |
| validation | Codex projection validators plus repo validators |

## Agent Layer Owns

- role-profile projection posture
- specialization eligibility posture before future projection
- specialization eligibility records and readiness readers that stay non-installing
- wiring and generated Codex agent compatibility inside `aoa-agents`
- refresh law that keeps projections source-owned and repeatable
- generated projection manifests as evidence, not authority

## Stronger Owner Split

- Codex runtime, host config, and editor behavior do not live here.
- OpenAI product guidance does not live here.
- Runtime service ownership routes away from `aoa-agents`.

## Validation

```bash
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python -m unittest discover -s mechanics/codex-projection/parts/subagent-projection/tests -p "test_*.py"
python mechanics/codex-projection/parts/specialization-eligibility/scripts/build_specialization_eligibility_readiness.py --check
python mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py
python -m unittest discover -s mechanics/codex-projection/parts/specialization-eligibility/tests -p "test_*.py"
python mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```
