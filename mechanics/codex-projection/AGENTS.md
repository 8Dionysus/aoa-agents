# AGENTS.md

## Applies To

This card applies to `mechanics/codex-projection/` and descendants until a
nearer `AGENTS.md` narrows the route.

## Role

`mechanics/codex-projection/` routes projection from source agent profiles into
Codex-facing subagent surfaces. It owns projection posture, specialization
eligibility, refresh law, and wiring route inside `aoa-agents`; it does not own
Codex runtime behavior.

## Operating Card

| Field | Route |
| --- | --- |
| role | Codex-facing projection operation package |
| input | profile, specialization, wiring, generated subagent, refresh-law, manifest, and projection-boundary pressure |
| output | refreshed projection route, eligibility record, generated manifest, compatibility note, or runtime/config handoff |
| owner | this package for projection routing; `agents/roles/` and part-local wiring config own source inputs |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, Codex projection builders, `mechanics/agon/` |
| tools | Codex projection validator, refresh-law validator, repo validators |
| validation | Codex projection checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `agents/roles/AGENTS.md` when profile source affects projection
8. `PROVENANCE.md` for provenance accounting

## Boundaries

- Codex runtime, host config, and editor behavior do not live here.
- OpenAI product guidance does not live here.
- Runtime service ownership routes away from `aoa-agents`.
- Generated projection manifests are evidence, not authority.

## Validation

```bash
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python -m unittest discover -s mechanics/codex-projection/parts/subagent-projection/tests -p "test_*.py"
python mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py
python -m unittest discover -s mechanics/codex-projection/parts/specialization-eligibility/tests -p "test_*.py"
python mechanics/codex-projection/parts/assistant-projection/scripts/validate_assistant_projection_resolver.py
python mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed projection part, source profile or generated surface
affected, builders run, checks skipped, and any runtime or config handoff.
