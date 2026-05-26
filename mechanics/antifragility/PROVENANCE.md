# Antifragility Provenance Bridge

`PROVENANCE.md` is the single active bridge from current mechanic routes into legacy accounting.

Use active surfaces first:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

Open `legacy/` only for former path lookup, raw receipt intake, or distillation history. Former root file names stay historical here; active parts use their current route names.

## 2026-05-26 Root Docs Move

3 mechanics-facing docs moved from `docs/` into `antifragility/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/AGENT_STRESS_HANDOFFS.md` | [parts/stress-posture/docs/stress-handoffs.md](parts/stress-posture/docs/stress-handoffs.md) | `stress-posture` |
| `docs/AGENT_STRESS_POSTURE.md` | [parts/stress-posture/docs/stress-posture.md](parts/stress-posture/docs/stress-posture.md) | `stress-posture` |
| `docs/VIA_NEGATIVA_CHECKLIST.md` | [parts/via-negativa/docs/via-negativa-checklist.md](parts/via-negativa/docs/via-negativa-checklist.md) | `via-negativa` |

## 2026-05-26 Stress Payload Move

2 stress-posture schemas and 2 examples moved from root support districts into
`parts/stress-posture/`. Stable schema `$id` values remain public contract
identifiers, not active repo paths.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/agent_stress_posture_v1.json` | [parts/stress-posture/schemas/agent-stress-posture.schema.json](parts/stress-posture/schemas/agent-stress-posture.schema.json) | `stress-posture` |
| `schemas/stress_handoff_envelope_v1.json` | [parts/stress-posture/schemas/stress-handoff-envelope.schema.json](parts/stress-posture/schemas/stress-handoff-envelope.schema.json) | `stress-posture` |
| `examples/agent_stress_posture.example.json` | [parts/stress-posture/examples/agent-stress-posture.example.json](parts/stress-posture/examples/agent-stress-posture.example.json) | `stress-posture` |
| `examples/stress_handoff_envelope.example.json` | [parts/stress-posture/examples/stress-handoff-envelope.example.json](parts/stress-posture/examples/stress-handoff-envelope.example.json) | `stress-posture` |
