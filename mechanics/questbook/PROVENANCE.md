# Questbook Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into
legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)
- [QUESTBOOK.md](../../QUESTBOOK.md)
- [quests/](../../quests/)

Open `legacy/` only for former path lookup, raw receipt intake, or
distillation history. Former root file names stay historical here; active
parts use their current route names.

## 2026-05-26 Root Docs Move

1 mechanics-facing doc moved from `docs/` into `questbook/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/QUEST_EXECUTION_PASSPORT.md` | [parts/execution-passport/docs/quest-execution-passport.md](parts/execution-passport/docs/quest-execution-passport.md) | `execution-passport` |

## 2026-05-26 Questbook Source Store Topology Repair

The root human index and root lane-first quest store are active source
surfaces. The earlier part-local source-store move is superseded by the
source split used in `Agents-of-Abyss`, `aoa-memo`, and `aoa-evals`.

| Former flat path | Active route | Owner route |
| --- | --- | --- |
| `QUESTBOOK.md` | [../../QUESTBOOK.md](../../QUESTBOOK.md) | root human index, routed by `public-index` |
| `quests/AOA-AG-Q-0001.yaml` | [../../quests/agents/done/AOA-AG-Q-0001.yaml](../../quests/agents/done/AOA-AG-Q-0001.yaml) | `quests/agents/done/` |
| `quests/AOA-AG-Q-0002.yaml` | [../../quests/agents/triaged/AOA-AG-Q-0002.yaml](../../quests/agents/triaged/AOA-AG-Q-0002.yaml) | `quests/agents/triaged/` |
| `quests/AOA-AG-Q-0003.yaml` | [../../quests/agents/captured/AOA-AG-Q-0003.yaml](../../quests/agents/captured/AOA-AG-Q-0003.yaml) | `quests/agents/captured/` |
| `quests/AOA-AG-Q-0004.yaml` | [../../quests/agents/ready/AOA-AG-Q-0004.yaml](../../quests/agents/ready/AOA-AG-Q-0004.yaml) | `quests/agents/ready/` |
| `quests/AOA-AG-Q-0005.yaml` | [../../quests/agents/ready/AOA-AG-Q-0005.yaml](../../quests/agents/ready/AOA-AG-Q-0005.yaml) | `quests/agents/ready/` |
| `quests/AOA-AG-Q-0006.yaml` | [../../quests/agents/ready/AOA-AG-Q-0006.yaml](../../quests/agents/ready/AOA-AG-Q-0006.yaml) | `quests/agents/ready/` |
| `quests/AOA-AG-Q-0007.yaml` | [../../quests/agents/done/AOA-AG-Q-0007.yaml](../../quests/agents/done/AOA-AG-Q-0007.yaml) | `quests/agents/done/` |
| `quests/AOA-AG-Q-0008.yaml` | [../../quests/agents/reanchor/AOA-AG-Q-0008.yaml](../../quests/agents/reanchor/AOA-AG-Q-0008.yaml) | `quests/agents/reanchor/` |
| `quests/AOA-AG-Q-0009.yaml` | [../../quests/agents/reanchor/AOA-AG-Q-0009.yaml](../../quests/agents/reanchor/AOA-AG-Q-0009.yaml) | `quests/agents/reanchor/` |
| `quests/AOA-AG-Q-AGON-0002-agonic-actor-recharter.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0002-agonic-actor-recharter.md](../../quests/agon/captured/AOA-AG-Q-AGON-0002-agonic-actor-recharter.md) | `quests/agon/captured/` |
| `quests/AOA-AG-Q-AGON-0003-formation-index-integration.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0003-formation-index-integration.md](../../quests/agon/captured/AOA-AG-Q-AGON-0003-formation-index-integration.md) | `quests/agon/captured/` |
| `quests/AOA-AG-Q-AGON-0004-assistant-civil-recharter.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0004-assistant-civil-recharter.md](../../quests/agon/captured/AOA-AG-Q-AGON-0004-assistant-civil-recharter.md) | `quests/agon/captured/` |
| `quests/AOA-AG-Q-AGON-0005-assistant-formation-index-integration.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0005-assistant-formation-index-integration.md](../../quests/agon/captured/AOA-AG-Q-AGON-0005-assistant-formation-index-integration.md) | `quests/agon/captured/` |
| `quests/AOA-AG-Q-AGON-0006-assistant-projection-boundary.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0006-assistant-projection-boundary.md](../../quests/agon/captured/AOA-AG-Q-AGON-0006-assistant-projection-boundary.md) | `quests/agon/captured/` |
| `quests/AOA-AG-Q-AGON-0007-formation-trial.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0007-formation-trial.md](../../quests/agon/captured/AOA-AG-Q-AGON-0007-formation-trial.md) | `quests/agon/captured/` |
| `quests/AOA-AG-Q-AGON-0008-formation-trial-validation-integration.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0008-formation-trial-validation-integration.md](../../quests/agon/captured/AOA-AG-Q-AGON-0008-formation-trial-validation-integration.md) | `quests/agon/captured/` |
| `quests/AOA-AG-Q-AGON-0009-pre-protocol-agent-boundary.md` | [../../quests/agon/captured/AOA-AG-Q-AGON-0009-pre-protocol-agent-boundary.md](../../quests/agon/captured/AOA-AG-Q-AGON-0009-pre-protocol-agent-boundary.md) | `quests/agon/captured/` |
| `quests/AOAG-Q-AGON-0010-rank-jurisdiction-surfaces.md` | [../../quests/agon/captured/AOAG-Q-AGON-0010-rank-jurisdiction-surfaces.md](../../quests/agon/captured/AOAG-Q-AGON-0010-rank-jurisdiction-surfaces.md) | `quests/agon/captured/` |
| `quests/AOAG-Q-AGON-0011-epistemic-actor-posture.md` | [../../quests/agon/captured/AOAG-Q-AGON-0011-epistemic-actor-posture.md](../../quests/agon/captured/AOAG-Q-AGON-0011-epistemic-actor-posture.md) | `quests/agon/captured/` |
| `quests/AOAG-Q-AGON-0012-school-campaign-posture.md` | [../../quests/agon/captured/AOAG-Q-AGON-0012-school-campaign-posture.md](../../quests/agon/captured/AOAG-Q-AGON-0012-school-campaign-posture.md) | `quests/agon/captured/` |

## 2026-05-26 Alpha Reference Route Contract Move

1 Alpha reference-route schema and 6 Alpha route README/example files moved from
root `schemas/` and `examples/` into the questbook `alpha-reference-routes`
part.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/alpha-reference-route.schema.json` | [parts/alpha-reference-routes/schemas/alpha-reference-route.schema.json](parts/alpha-reference-routes/schemas/alpha-reference-route.schema.json) | `alpha-reference-routes` |
| `examples/alpha_reference_routes/AGENTS.md` | [parts/alpha-reference-routes/examples/README.md](parts/alpha-reference-routes/examples/README.md) | `alpha-reference-routes` |
| `examples/alpha_reference_routes/local-stack-diagnosis.example.json` | [parts/alpha-reference-routes/examples/local-stack-diagnosis.example.json](parts/alpha-reference-routes/examples/local-stack-diagnosis.example.json) | `alpha-reference-routes` |
| `examples/alpha_reference_routes/long-horizon-model-tier-orchestra.example.json` | [parts/alpha-reference-routes/examples/long-horizon-model-tier-orchestra.example.json](parts/alpha-reference-routes/examples/long-horizon-model-tier-orchestra.example.json) | `alpha-reference-routes` |
| `examples/alpha_reference_routes/restartable-inquiry-loop.example.json` | [parts/alpha-reference-routes/examples/restartable-inquiry-loop.example.json](parts/alpha-reference-routes/examples/restartable-inquiry-loop.example.json) | `alpha-reference-routes` |
| `examples/alpha_reference_routes/self-agent-checkpoint-rollout.example.json` | [parts/alpha-reference-routes/examples/self-agent-checkpoint-rollout.example.json](parts/alpha-reference-routes/examples/self-agent-checkpoint-rollout.example.json) | `alpha-reference-routes` |
| `examples/alpha_reference_routes/validation-driven-remediation.example.json` | [parts/alpha-reference-routes/examples/validation-driven-remediation.example.json](parts/alpha-reference-routes/examples/validation-driven-remediation.example.json) | `alpha-reference-routes` |

## 2026-05-26 Alpha Reference Route Generated Reader Move

1 Alpha reference-route generated reader moved from root `generated/` into the
Questbook `alpha-reference-routes` part after the part-local schema and
examples became the reader's only source truth.

| Former root path | Active route | Part |
| --- | --- | --- |
| `generated/alpha_reference_routes.min.json` | [parts/alpha-reference-routes/generated/alpha-reference-routes.min.json](parts/alpha-reference-routes/generated/alpha-reference-routes.min.json) | `alpha-reference-routes` |

## Active Root Quest Generated Readers

Quest catalog and dispatch readers are active root-published read models:

- [../../generated/quest_catalog.min.json](../../generated/quest_catalog.min.json)
- [../../generated/quest_catalog.min.example.json](../../generated/quest_catalog.min.example.json)
- [../../generated/quest_dispatch.min.json](../../generated/quest_dispatch.min.json)
- [../../generated/quest_dispatch.min.example.json](../../generated/quest_dispatch.min.example.json)

They are derived from root `quests/` through
`scripts/generate_questbook_readers.py`.
