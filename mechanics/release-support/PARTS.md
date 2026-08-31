# Release Support Parts

Parts are the active execution map for this mechanic. Each part lists package-local docs first, then any source/support surfaces that still live in their owning districts.

| Part | Active package docs | Support surfaces |
| --- | --- | --- |
| `assistant-release-watch` | Unmaterialized route. | Route to Experience [watch-and-rollback](../experience/parts/watch-and-rollback/README.md); retain the name here without a placeholder README. |
| `changelog-posture` | Unmaterialized route. | Route to root [CHANGELOG.md](../../CHANGELOG.md); retain the name here without a placeholder README. |
| `published-readiness` | Unmaterialized route. | Route to [repo-release-gate](parts/repo-release-gate/README.md), generated readers, and [current contour](../../docs/CURRENT_CONTOUR.md); retain the name here without a placeholder README. |
| `repo-release-gate` | [Releasing `aoa-agents`](parts/repo-release-gate/docs/releasing.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |
| `runtime-release-hold` | [Agent Release Hold Policy](parts/runtime-release-hold/docs/agent-release-hold-policy.md) | [schema set](parts/runtime-release-hold/schemas/README.md)<br>[example set](parts/runtime-release-hold/examples/README.md)<br>Old path lookup routes through `PROVENANCE.md`. |

## Provenance Bridge

Use [PROVENANCE.md](PROVENANCE.md) only when a task must audit former root paths, source accounting, or distillation history.
