# Release Support Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `repo-release-gate` | release validation and publication readiness | `docs/RELEASING.md`; `scripts/release_check.py`; release tests |
| `changelog-posture` | preserve release history and current change surface | `CHANGELOG.md`; release notes docs |
| `published-readiness` | compatibility of published agent contracts and generated readers | `docs/PUBLISHED_CONTRACT_COMPATIBILITY.md`; generated registries/readers; cross-route to `mechanics/boundary-bridge/` |
| `assistant-release-watch` | assistant release watches that affect service experience | `docs/ASSISTANT_RELEASE_CANDIDATE.md`; `docs/ASSISTANT_VERSION_RUNBOOK.md`; `docs/ASSISTANT_POST_RELEASE_WATCHES.md`; cross-route to `mechanics/experience/` |
| `runtime-release-hold` | release holds that affect runtime-facing role contracts | `docs/ASSISTANT_RUNTIME_RELEASE_HOLDS.md`; cross-route to `mechanics/runtime-seam/` |

## Move Posture

Keep this package as a release route map. Do not move `CHANGELOG.md`,
`docs/RELEASING.md`, or `scripts/release_check.py` unless the repo's release
tooling is updated in the same slice.
