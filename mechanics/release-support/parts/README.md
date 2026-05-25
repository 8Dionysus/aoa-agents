# Release Support Parts

`mechanics/release-support/parts/` is the lower index for active release and
publication support parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `repo-release-gate/` | release validation and publication readiness | `repo-release-gate/README.md` |
| `changelog-posture/` | preserve release history and current change surface | `changelog-posture/README.md` |
| `published-readiness/` | compatibility of published agent contracts and generated readers | `published-readiness/README.md` |
| `assistant-release-watch/` | assistant release watches that affect service experience | `assistant-release-watch/README.md` |
| `runtime-release-hold/` | release holds that affect runtime-facing role contracts | `runtime-release-hold/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
