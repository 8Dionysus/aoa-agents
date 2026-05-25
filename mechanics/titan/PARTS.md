# Titan Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `role-bearing` | Titan bearer ontology and role classes | `docs/TITAN_ROLE_BEARER_ONTOLOGY.md`; `config/titan_bearers.v0.json`; `config/titan_role_classes.v0.json`; Titan role schemas/examples |
| `lineage-ledger` | lineage preservation for role-bearing surfaces | `docs/TITAN_LINEAGE_LEDGER.md`; `config/titan_lineage_ledger.v0.json`; generated Titan lineage readers |
| `summon-boundary` | keep summon protocol bounded to agent role posture | `docs/TITAN_SUMMON_BOUNDARY.md`; `docs/TITAN_SUMMON_PROTOCOL.md` |
| `runtime-roster` | runtime-facing roster contract without owning runtime execution | `docs/TITAN_RUNTIME_ROSTER.md`; `docs/TITAN_APPSERVER_BRIDGE.md`; cross-route to `mechanics/runtime-seam/` |
| `incarnation-spine` | incarnation, praxis, and operator-facing role surfaces | `docs/TITAN_INCARNATION_SPINE.md`; `docs/TITAN_PRAXIS_PLANE.md`; `docs/TITAN_OPERATOR_CONSOLE.md` |
| `service-cohort` | service cohort, recall, memory loom, swarm, reviewer/judge posture | `docs/TITAN_SERVICE_COHORT.md`; `docs/TITAN_RECALL.md`; `docs/TITAN_MEMORY_LOOM.md`; `docs/TITAN_SWARM.md`; `docs/TITAN_REVIEWER_JUDGE_COMPRESSION.md` |
| `codex-projection` | Titan projection into Codex-facing generated agents | `generated/titan_codex_agents/`; Titan projection builders/tests; cross-route to `mechanics/codex-projection/` |

## Move Posture

Titan has enough local pressure for a package, but source config and generated
readers stay in `config/` and `generated/` until package-local validation is
introduced.
