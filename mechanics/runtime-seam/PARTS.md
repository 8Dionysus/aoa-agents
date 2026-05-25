# Runtime Seam Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `role-tier-bindings` | source role bindings for the public runtime loop | `agents/runtime_seam/*.binding.json`; `agents/runtime_seam/AGENTS.md`; `generated/runtime_seam_bindings.json` |
| `artifact-contracts` | contract shape for runtime artifacts | `docs/RUNTIME_ARTIFACTS.md`; `examples/runtime_artifacts/`; `schemas/runtime_artifacts/` |
| `transition-discipline` | transition posture between runtime loop states | `docs/RUNTIME_ARTIFACT_TRANSITIONS.md`; `agents/runtime_seam/transition.binding.json` |
| `published-registry` | generated readers for consumers | `generated/runtime_seam_bindings.json`; `scripts/runtime_seam_registry.py` |

## Move Posture

The source bindings already live under `agents/runtime_seam/`. Shared runtime
artifact schemas and examples stay in root districts until a package-local
schema route preserves public compatibility.
