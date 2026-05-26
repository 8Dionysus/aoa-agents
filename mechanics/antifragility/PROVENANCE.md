# Antifragility Provenance Bridge

This is the only active bridge from current mechanic docs into source and
archive accounting. Use it when auditing how former root paths or raw receipts
feed active parts, not when you need the current operating contract.

## Current Route First

Start with active surfaces:

- [README.md](README.md)
- [PARTS.md](PARTS.md)
- [parts/](parts/)

If those surfaces answer the task, stop there. Do not pull old-path
inventories into active route cards.

## Archive Route

- [legacy index](legacy/INDEX.md): old-path lookup mapped to active part routes.
- [distillation log](legacy/DISTILLATION_LOG.md): dated accounting for
  raw-to-active movement.
- [raw receipts](legacy/raw/README.md): preserved raw inputs when a migration
  has real source payloads.

The dated sections below preserve audit and accounting facts. Former root file
names stay historical here; active parts use current route names.

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

## Distillation Rule

When archived or former-path material changes current behavior, update the
relevant active part first. Then update this bridge and the package archive
index/log if route accounting changed. Active part docs must not grow
per-source inventories.
