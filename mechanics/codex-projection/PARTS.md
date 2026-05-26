# Codex Projection Parts

Parts are the active execution map for this mechanic. Each part lists package-local docs first, then any source/support surfaces that still live in their owning districts.

| Part | Active package docs | Support surfaces |
| --- | --- | --- |
| `agon-boundary` | [Codex Projection Agon Boundary](parts/agon-boundary/docs/projection-agon-boundary.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |
| `assistant-projection` | No package-local docs in this slice. | Part-local [schemas](parts/assistant-projection/schemas/) and [example](parts/assistant-projection/examples/assistant-projection-resolver.example.json); old path lookup routes through `PROVENANCE.md`. |
| `refresh-law` | [Codex Subagent Refresh Law](parts/refresh-law/docs/subagent-refresh-law.md) | [example set](parts/refresh-law/examples/README.md)<br>Old path lookup routes through `PROVENANCE.md`. |
| `specialization-eligibility` | [Codex Specialization Eligibility](parts/specialization-eligibility/docs/specialization-eligibility.md)<br>[Specialization Eligibility Part](parts/specialization-eligibility/README.md) | [schema](parts/specialization-eligibility/schemas/specialization-eligibility.schema.json)<br>[example](parts/specialization-eligibility/examples/specialization-eligibility.example.json)<br>[validator](parts/specialization-eligibility/scripts/validate_specialization_eligibility.py)<br>[tests](parts/specialization-eligibility/tests/test_specialization_eligibility.py)<br>No generated agent output in this slice. |
| `subagent-projection` | [Codex Subagent Projection](parts/subagent-projection/docs/subagent-projection.md)<br>[Subagent Projection Part](parts/subagent-projection/README.md) | [config/wiring.v2.json](parts/subagent-projection/config/wiring.v2.json)<br>[scripts/build_codex_subagents_v2.py](parts/subagent-projection/scripts/build_codex_subagents_v2.py)<br>[scripts/codex_subagent_projection.py](parts/subagent-projection/scripts/codex_subagent_projection.py)<br>[scripts/validate_codex_subagents.py](parts/subagent-projection/scripts/validate_codex_subagents.py)<br>[tests/test_codex_subagent_projection.py](parts/subagent-projection/tests/test_codex_subagent_projection.py)<br>Root-published generated companions: `generated/codex_agents/`.<br>Old path lookup routes through `PROVENANCE.md`. |
| `titan-projection` | No package-local docs in this slice. | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |

## Provenance Bridge

Use [PROVENANCE.md](PROVENANCE.md) only when a task must audit former root paths, source accounting, or distillation history.
