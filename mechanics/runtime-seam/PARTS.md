# Runtime Seam Parts

Parts are the active execution map for this mechanic. Each part lists package-local docs first, then any source/support surfaces that still live in their owning districts.

| Part | Active package docs | Support surfaces |
| --- | --- | --- |
| `artifact-contracts` | [Agent Authority Claim Runtime](parts/artifact-contracts/docs/authority-claim-runtime.md) | Active schemas: [parts/artifact-contracts/schemas/](parts/artifact-contracts/schemas/). Active examples: [parts/artifact-contracts/examples/](parts/artifact-contracts/examples/), including the runtime-readable authority-claim contract. |
| `published-registry` | No package-local docs in this slice. | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |
| `role-tier-bindings` | [Agent Runtime Seam](parts/role-tier-bindings/docs/agent-runtime-seam.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |
| `transition-discipline` | [Kind Safe Runtime Enforcement](parts/transition-discipline/docs/kind-safe-runtime-enforcement.md)<br>[Runtime Artifact Transitions](parts/transition-discipline/docs/runtime-artifact-transitions.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |

## Provenance Bridge

Use [PROVENANCE.md](PROVENANCE.md) only when a task must audit former root paths, source accounting, or distillation history.
