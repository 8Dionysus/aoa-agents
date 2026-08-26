# Boundary Bridge Parts

Parts are the active execution map for this mechanic. Each part lists package-local docs first, then any source/support surfaces that still live in their owning districts.

| Part | Active package docs | Support surfaces |
| --- | --- | --- |
| `consumer-handoff` | [Cross Repo Adoption Readiness](parts/consumer-handoff/docs/cross-repo-adoption-readiness.md) | [schema set](parts/consumer-handoff/schemas/README.md)<br>[example set](parts/consumer-handoff/examples/README.md)<br>Old path lookup routes through `PROVENANCE.md`. |
| `participant-relations` | [Goal Participant Relations](parts/participant-relations/docs/goal-participant-relations.md) | [contract](parts/participant-relations/contract.json)<br>[schema set](parts/participant-relations/schemas/)<br>[source feed](parts/participant-relations/records/goal-participant-relations.source.json)<br>[generated reader](parts/participant-relations/generated/goal-participant-graph.min.json)<br>[builder and validator](parts/participant-relations/scripts/)<br>[tests](parts/participant-relations/tests/) |
| `federation-consumer-seams` | [Federation Consumer Seams](parts/federation-consumer-seams/docs/federation-consumer-seams.md)<br>[Federation Projection Boundaries](parts/federation-consumer-seams/docs/federation-projection-boundaries.md) | [schema set](parts/federation-consumer-seams/schemas/README.md)<br>[example set](parts/federation-consumer-seams/examples/README.md)<br>Old path lookup routes through `PROVENANCE.md`. |
| `published-compatibility` | [Agent Install Compatibility](parts/published-compatibility/docs/install-compatibility.md)<br>[Published Contract Compatibility](parts/published-compatibility/docs/published-contract-compatibility.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |
| `source-surface-registry` | [Registry Source Surfaces](parts/source-surface-registry/docs/registry-source-surfaces.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |
| `workspace-trigger` | [Workspace Surface Trigger Posture](parts/workspace-trigger/docs/workspace-surface-trigger-posture.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |

## Provenance Bridge

Use [PROVENANCE.md](PROVENANCE.md) only when a task must audit former root paths, source accounting, or distillation history.
