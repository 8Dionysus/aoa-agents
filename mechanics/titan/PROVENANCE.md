# Titan Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

Open `legacy/` only for former path lookup, raw receipt intake, or distillation history. Former root file names stay historical here; active parts use their current route names.

## 2026-05-26 Root Docs Move

16 mechanics-facing docs moved from `docs/` into `titan/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/TITAN_INCARNATION_SPINE.md` | [parts/incarnation-spine/docs/incarnation-spine.md](parts/incarnation-spine/docs/incarnation-spine.md) | `incarnation-spine` |
| `docs/TITAN_OPERATOR_CONSOLE_BOUNDARY.md` | [parts/incarnation-spine/docs/operator-console-boundary.md](parts/incarnation-spine/docs/operator-console-boundary.md) | `incarnation-spine` |
| `docs/TITAN_PRAXIS_PLANE.md` | [parts/incarnation-spine/docs/praxis-plane.md](parts/incarnation-spine/docs/praxis-plane.md) | `incarnation-spine` |
| `docs/TITAN_LINEAGE_LEDGER.md` | [parts/lineage-ledger/docs/lineage-ledger.md](parts/lineage-ledger/docs/lineage-ledger.md) | `lineage-ledger` |
| `docs/TITAN_ROLE_BEARER_ONTOLOGY.md` | [parts/role-bearing/docs/role-bearer-ontology.md](parts/role-bearing/docs/role-bearer-ontology.md) | `role-bearing` |
| `docs/TITAN_AGENT_REPORT_BOUNDARY.md` | [parts/runtime-roster/docs/agent-report-boundary.md](parts/runtime-roster/docs/agent-report-boundary.md) | `runtime-roster` |
| `docs/TITAN_APPSERVER_BRIDGE_BOUNDARY.md` | [parts/runtime-roster/docs/appserver-bridge-boundary.md](parts/runtime-roster/docs/appserver-bridge-boundary.md) | `runtime-roster` |
| `docs/TITAN_RUNTIME_ROSTER.md` | [parts/runtime-roster/docs/runtime-roster.md](parts/runtime-roster/docs/runtime-roster.md) | `runtime-roster` |
| `docs/TITAN_MEMORY_LOOM_BOUNDARY.md` | [parts/service-cohort/docs/memory-loom-boundary.md](parts/service-cohort/docs/memory-loom-boundary.md) | `service-cohort` |
| `docs/TITAN_RECALL_AUTHORITY.md` | [parts/service-cohort/docs/recall-authority.md](parts/service-cohort/docs/recall-authority.md) | `service-cohort` |
| `docs/TITAN_REVIEWER_JUDGE_COMPRESSION_LAW.md` | [parts/service-cohort/docs/reviewer-judge-compression-law.md](parts/service-cohort/docs/reviewer-judge-compression-law.md) | `service-cohort` |
| `docs/TITAN_SERVICE_COHORT.md` | [parts/service-cohort/docs/service-cohort.md](parts/service-cohort/docs/service-cohort.md) | `service-cohort` |
| `docs/TITAN_SWARM_PARTICIPATION.md` | [parts/service-cohort/docs/swarm-participation.md](parts/service-cohort/docs/swarm-participation.md) | `service-cohort` |
| `docs/TITAN_SUMMON_BOUNDARY.md` | [parts/summon-boundary/docs/summon-boundary.md](parts/summon-boundary/docs/summon-boundary.md) | `summon-boundary` |
| `docs/TITAN_SUMMON_PROTOCOL_V2.md` | [parts/summon-boundary/docs/summon-protocol-v2.md](parts/summon-boundary/docs/summon-protocol-v2.md) | `summon-boundary` |
| `docs/WAVE5_A2A_SUMMON_RETURN_ROLE_POSTURE_HOLD.md` | [parts/summon-boundary/docs/wave5-a2a-summon-return-role-posture-hold.md](parts/summon-boundary/docs/wave5-a2a-summon-return-role-posture-hold.md) | `summon-boundary` |

## 2026-05-26 Root Config Move

3 mechanic-specific Titan configs moved from root `config/` into
`titan/parts/*/config/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `config/titan_bearers.v0.json` | [parts/role-bearing/config/bearers.v0.json](parts/role-bearing/config/bearers.v0.json) | `role-bearing` |
| `config/titan_role_classes.v0.json` | [parts/role-bearing/config/role-classes.v0.json](parts/role-bearing/config/role-classes.v0.json) | `role-bearing` |
| `config/titan_lineage_ledger.v0.json` | [parts/lineage-ledger/config/ledger.v0.json](parts/lineage-ledger/config/ledger.v0.json) | `lineage-ledger` |

## 2026-05-26 Root Examples Move

10 schema-backed Titan examples moved from root `examples/` into
`titan/parts/*/examples/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `examples/titan_bearer_identity.v0.json` | [parts/role-bearing/examples/bearer-identity.v0.json](parts/role-bearing/examples/bearer-identity.v0.json) | `role-bearing` |
| `examples/titan_lineage_ledger.v0.json` | [parts/lineage-ledger/examples/lineage-ledger.v0.json](parts/lineage-ledger/examples/lineage-ledger.v0.json) | `lineage-ledger` |
| `examples/titan_incarnation_identity.example.json` | [parts/incarnation-spine/examples/incarnation-identity.example.json](parts/incarnation-spine/examples/incarnation-identity.example.json) | `incarnation-spine` |
| `examples/titan_operator_console_roster.v0.json` | [parts/incarnation-spine/examples/operator-console-roster.v0.json](parts/incarnation-spine/examples/operator-console-roster.v0.json) | `incarnation-spine` |
| `examples/titan_runtime_roster.v0.json` | [parts/runtime-roster/examples/runtime-roster.v0.json](parts/runtime-roster/examples/runtime-roster.v0.json) | `runtime-roster` |
| `examples/titan_appserver_bridge_boundary.v0.json` | [parts/runtime-roster/examples/appserver-bridge-boundary.v0.json](parts/runtime-roster/examples/appserver-bridge-boundary.v0.json) | `runtime-roster` |
| `examples/titan_memory_roster.v0.json` | [parts/service-cohort/examples/memory-roster.v0.json](parts/service-cohort/examples/memory-roster.v0.json) | `service-cohort` |
| `examples/titan_service_cohort.v0.json` | [parts/service-cohort/examples/service-cohort.v0.json](parts/service-cohort/examples/service-cohort.v0.json) | `service-cohort` |
| `examples/titan_compact_review_task.example.json` | [parts/summon-boundary/examples/compact-review-task.example.json](parts/summon-boundary/examples/compact-review-task.example.json) | `summon-boundary` |
| `examples/titan_delta_residual_risk_task.example.json` | [parts/summon-boundary/examples/delta-residual-risk-task.example.json](parts/summon-boundary/examples/delta-residual-risk-task.example.json) | `summon-boundary` |

## 2026-05-26 Root Schemas Move

11 Titan-specific schemas moved from root `schemas/` into
`titan/parts/*/schemas/`. Stable `$id` values remain public contract
identifiers.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/titan_role_class.schema.json` | [parts/role-bearing/schemas/role-class.schema.json](parts/role-bearing/schemas/role-class.schema.json) | `role-bearing` |
| `schemas/titan_bearer_identity.schema.json` | [parts/role-bearing/schemas/bearer-identity.schema.json](parts/role-bearing/schemas/bearer-identity.schema.json) | `role-bearing` |
| `schemas/titan_lineage_ledger.schema.json` | [parts/lineage-ledger/schemas/lineage-ledger.schema.json](parts/lineage-ledger/schemas/lineage-ledger.schema.json) | `lineage-ledger` |
| `schemas/titan_incarnation_identity.schema.json` | [parts/incarnation-spine/schemas/incarnation-identity.schema.json](parts/incarnation-spine/schemas/incarnation-identity.schema.json) | `incarnation-spine` |
| `schemas/titan_operator_console_roster.schema.json` | [parts/incarnation-spine/schemas/operator-console-roster.schema.json](parts/incarnation-spine/schemas/operator-console-roster.schema.json) | `incarnation-spine` |
| `schemas/titan_agent_report.schema.json` | [parts/runtime-roster/schemas/agent-report.schema.json](parts/runtime-roster/schemas/agent-report.schema.json) | `runtime-roster` |
| `schemas/titan_runtime_roster.schema.json` | [parts/runtime-roster/schemas/runtime-roster.schema.json](parts/runtime-roster/schemas/runtime-roster.schema.json) | `runtime-roster` |
| `schemas/titan_appserver_bridge_boundary.schema.json` | [parts/runtime-roster/schemas/appserver-bridge-boundary.schema.json](parts/runtime-roster/schemas/appserver-bridge-boundary.schema.json) | `runtime-roster` |
| `schemas/titan_memory_roster.schema.json` | [parts/service-cohort/schemas/memory-roster.schema.json](parts/service-cohort/schemas/memory-roster.schema.json) | `service-cohort` |
| `schemas/titan_service_cohort.schema.json` | [parts/service-cohort/schemas/service-cohort.schema.json](parts/service-cohort/schemas/service-cohort.schema.json) | `service-cohort` |
| `schemas/titan_agent_role_assignment.schema.json` | [parts/summon-boundary/schemas/agent-role-assignment.schema.json](parts/summon-boundary/schemas/agent-role-assignment.schema.json) | `summon-boundary` |
