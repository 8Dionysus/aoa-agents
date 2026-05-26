# Capability Packs

`agents/operating-model/capabilities/` holds reusable operating bundles for
role specializations.

The branch exists so `agents/roles/<role>/specializations/` can stay attached
to the role that owns identity, while cross-role permission/tool/skill/memory
posture is reused through compact packs.

## Branches

| Branch | Role |
| --- | --- |
| `packs/` | source-authored capability packs used by role specializations |

Generated readers under `generated/` are derived from these packs and must not
be hand-authored as truth.
