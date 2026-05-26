# Recurrence Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

Open `legacy/` only for former path lookup, raw receipt intake, or distillation history. Former root file names stay historical here; active parts use their current route names.

## 2026-05-26 Root Docs Move

6 mechanics-facing docs moved from `docs/` into `recurrence/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/RECURRENCE_DISCIPLINE.md` | [parts/anchor-return/docs/recurrence-discipline.md](parts/anchor-return/docs/recurrence-discipline.md) | `anchor-return` |
| `docs/CODEX_RECURSOR_PROJECTION_BOUNDARY.md` | [parts/codex-recursor-projection/docs/codex-recursor-projection-boundary.md](parts/codex-recursor-projection/docs/codex-recursor-projection-boundary.md) | `codex-recursor-projection` |
| `docs/RECURSOR_AGENT_READINESS.md` | [parts/recursor-readiness/docs/recursor-agent-readiness.md](parts/recursor-readiness/docs/recursor-agent-readiness.md) | `recursor-readiness` |
| `docs/RECURSOR_EXECUTOR_CONTRACT.md` | [parts/recursor-readiness/docs/recursor-executor-contract.md](parts/recursor-readiness/docs/recursor-executor-contract.md) | `recursor-readiness` |
| `docs/RECURSOR_PAIR_SEPARATION_LAW.md` | [parts/recursor-readiness/docs/recursor-pair-separation-law.md](parts/recursor-readiness/docs/recursor-pair-separation-law.md) | `recursor-readiness` |
| `docs/RECURSOR_WITNESS_CONTRACT.md` | [parts/recursor-readiness/docs/recursor-witness-contract.md](parts/recursor-readiness/docs/recursor-witness-contract.md) | `recursor-readiness` |

## 2026-05-26 Root Config Move

3 mechanic-specific seed and candidate configs moved from root `config/` into
`recurrence/parts/*/config/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `config/codex_recursor_projection.candidate.json` | [parts/codex-recursor-projection/config/projection-candidate.json](parts/codex-recursor-projection/config/projection-candidate.json) | `codex-recursor-projection` |
| `config/recursor_pair.seed.json` | [parts/recursor-readiness/config/pair.seed.json](parts/recursor-readiness/config/pair.seed.json) | `recursor-readiness` |
| `config/recursor_roles.seed.json` | [parts/recursor-readiness/config/roles.seed.json](parts/recursor-readiness/config/roles.seed.json) | `recursor-readiness` |

## 2026-05-26 Root Recursor Contract Move

7 recursor schemas and 4 recursor examples moved from root `schemas/` and
`examples/` into recurrence part-local contract routes.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/recursor-role-contract.v1.schema.json` | [parts/recursor-readiness/schemas/role-contract.schema.json](parts/recursor-readiness/schemas/role-contract.schema.json) | `recursor-readiness` |
| `schemas/recursor-pair-contract.v1.schema.json` | [parts/recursor-readiness/schemas/pair-contract.schema.json](parts/recursor-readiness/schemas/pair-contract.schema.json) | `recursor-readiness` |
| `schemas/recursor-readiness-index.v1.schema.json` | [parts/recursor-readiness/schemas/readiness-index.schema.json](parts/recursor-readiness/schemas/readiness-index.schema.json) | `recursor-readiness` |
| `schemas/recursor-handoff-ledger.v1.schema.json` | [parts/recursor-readiness/schemas/handoff-ledger.schema.json](parts/recursor-readiness/schemas/handoff-ledger.schema.json) | `recursor-readiness` |
| `schemas/recursor-session-intent.v1.schema.json` | [parts/recursor-readiness/schemas/session-intent.schema.json](parts/recursor-readiness/schemas/session-intent.schema.json) | `recursor-readiness` |
| `schemas/recursor-projection-candidate.v1.schema.json` | [parts/codex-recursor-projection/schemas/projection-candidate.schema.json](parts/codex-recursor-projection/schemas/projection-candidate.schema.json) | `codex-recursor-projection` |
| `schemas/recursor-boundary-report.v1.schema.json` | [parts/agon-recursor-boundary/schemas/boundary-report.schema.json](parts/agon-recursor-boundary/schemas/boundary-report.schema.json) | `agon-recursor-boundary` |
| `examples/recursor_session_intent.example.json` | [parts/recursor-readiness/examples/session-intent.example.json](parts/recursor-readiness/examples/session-intent.example.json) | `recursor-readiness` |
| `examples/recursor_witness_handoff.example.json` | [parts/recursor-readiness/examples/witness-handoff.example.json](parts/recursor-readiness/examples/witness-handoff.example.json) | `recursor-readiness` |
| `examples/recursor_executor_receipt.example.json` | [parts/recursor-readiness/examples/executor-receipt.example.json](parts/recursor-readiness/examples/executor-receipt.example.json) | `recursor-readiness` |
| `examples/recursor_boundary_report.example.json` | [parts/agon-recursor-boundary/examples/boundary-report.example.json](parts/agon-recursor-boundary/examples/boundary-report.example.json) | `agon-recursor-boundary` |

## 2026-05-26 Root Manifest Move

11 recurrence component and hook manifests moved from root `manifests/` into
`recurrence/parts/component-manifests/manifests/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `manifests/recurrence/component.agents.recursor-codex-projection-candidates.json` | [parts/component-manifests/manifests/components/recursor-codex-projection-candidates.json](parts/component-manifests/manifests/components/recursor-codex-projection-candidates.json) | `component-manifests` |
| `manifests/recurrence/component.agents.recursor-readiness.json` | [parts/component-manifests/manifests/components/recursor-readiness.json](parts/component-manifests/manifests/components/recursor-readiness.json) | `component-manifests` |
| `manifests/recurrence/component.agon.actor-formation-surfaces.json` | [parts/component-manifests/manifests/components/agon-actor-formation-surfaces.json](parts/component-manifests/manifests/components/agon-actor-formation-surfaces.json) | `component-manifests` |
| `manifests/recurrence/component.agon.agent-rank-jurisdiction-surfaces.json` | [parts/component-manifests/manifests/components/agon-rank-jurisdiction-surfaces.json](parts/component-manifests/manifests/components/agon-rank-jurisdiction-surfaces.json) | `component-manifests` |
| `manifests/recurrence/component.agon.epistemic-actor-posture.json` | [parts/component-manifests/manifests/components/agon-epistemic-actor-posture.json](parts/component-manifests/manifests/components/agon-epistemic-actor-posture.json) | `component-manifests` |
| `manifests/recurrence/component.agon.wave16.aoa_agents.json` | [parts/component-manifests/manifests/components/agon-school-campaign-posture.json](parts/component-manifests/manifests/components/agon-school-campaign-posture.json) | `component-manifests` |
| `manifests/recurrence/component.codex-subagents.projection.json` | [parts/component-manifests/manifests/components/codex-subagent-projection.json](parts/component-manifests/manifests/components/codex-subagent-projection.json) | `component-manifests` |
| `manifests/recurrence/hooks/component.agon.actor-formation-surfaces.hooks.json` | [parts/component-manifests/manifests/hooks/agon-actor-formation-surfaces.json](parts/component-manifests/manifests/hooks/agon-actor-formation-surfaces.json) | `component-manifests` |
| `manifests/recurrence/hooks/component.agon.agent-rank-jurisdiction-surfaces.hooks.json` | [parts/component-manifests/manifests/hooks/agon-rank-jurisdiction-surfaces.json](parts/component-manifests/manifests/hooks/agon-rank-jurisdiction-surfaces.json) | `component-manifests` |
| `manifests/recurrence/hooks/component.agon.epistemic-actor-posture.hooks.json` | [parts/component-manifests/manifests/hooks/agon-epistemic-actor-posture.json](parts/component-manifests/manifests/hooks/agon-epistemic-actor-posture.json) | `component-manifests` |
| `manifests/recurrence/hooks/component.agon.wave16.aoa_agents.hooks.json` | [parts/component-manifests/manifests/hooks/agon-school-campaign-posture.json](parts/component-manifests/manifests/hooks/agon-school-campaign-posture.json) | `component-manifests` |

## 2026-05-26 Root Recursor Generated Reader Move

4 recursor generated readers moved from root `generated/` into recurrence
part-local generated routes.

| Former root path | Active route | Part |
| --- | --- | --- |
| `generated/recursor_role_readiness.min.json` | [parts/recursor-readiness/generated/role-readiness.min.json](parts/recursor-readiness/generated/role-readiness.min.json) | `recursor-readiness` |
| `generated/recursor_pair_contract.min.json` | [parts/recursor-readiness/generated/pair-contract.min.json](parts/recursor-readiness/generated/pair-contract.min.json) | `recursor-readiness` |
| `generated/recursor_projection_candidates.min.json` | [parts/codex-recursor-projection/generated/projection-candidates.min.json](parts/codex-recursor-projection/generated/projection-candidates.min.json) | `codex-recursor-projection` |
| `generated/recursor_agon_boundary_report.min.json` | [parts/agon-recursor-boundary/generated/boundary-report.min.json](parts/agon-recursor-boundary/generated/boundary-report.min.json) | `agon-recursor-boundary` |
