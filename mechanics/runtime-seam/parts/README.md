# Runtime Seam Parts

`mechanics/runtime-seam/parts/` is the lower index for active runtime seam
operation parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `role-tier-bindings/` | source role bindings for the public runtime loop | `role-tier-bindings/README.md` |
| `artifact-contracts/` | contract shape for runtime artifacts | `artifact-contracts/README.md` |
| `transition-discipline/` | transition posture between runtime loop states | `transition-discipline/README.md` |
| `published-registry/` | generated readers for consumers | `published-registry/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
