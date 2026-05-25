# Titan Parts

`mechanics/titan/parts/` is the lower index for active Titan role-bearing
operation parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `role-bearing/` | Titan bearer ontology and role classes | `role-bearing/README.md` |
| `lineage-ledger/` | lineage preservation for role-bearing surfaces | `lineage-ledger/README.md` |
| `summon-boundary/` | bounded summon protocol posture | `summon-boundary/README.md` |
| `runtime-roster/` | runtime-facing roster contract without owning runtime execution | `runtime-roster/README.md` |
| `incarnation-spine/` | incarnation, praxis, and operator-facing role surfaces | `incarnation-spine/README.md` |
| `service-cohort/` | service cohort, recall, memory loom, swarm, reviewer/judge posture | `service-cohort/README.md` |
| `codex-projection/` | Titan projection into Codex-facing generated agents | `codex-projection/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
