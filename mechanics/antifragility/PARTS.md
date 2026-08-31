# Antifragility Parts

Parts are the active execution map for this mechanic. Each part lists package-local docs first, then any source/support surfaces that still live in their owning districts.

| Part | Active package docs | Support surfaces |
| --- | --- | --- |
| `checkpoint-survival` | Unmaterialized route. | Route to [stress posture](parts/stress-posture/README.md) plus checkpoint owners; retain the name here without a placeholder README. |
| `scar-adaptation` | Unmaterialized route. | Route to Agon [adoption-retention](../agon/parts/adoption-retention/README.md) and shared-scar sources; retain the name here without a placeholder README. |
| `stress-posture` | [Agent Stress Handoffs](parts/stress-posture/docs/stress-handoffs.md)<br>[Agent Stress Posture](parts/stress-posture/docs/stress-posture.md) | Part-local [schemas](parts/stress-posture/schemas/), [examples](parts/stress-posture/examples/), [validator](parts/stress-posture/scripts/validate_stress_posture.py), and [tests](parts/stress-posture/tests/); old path lookup routes through `PROVENANCE.md`. |
| `via-negativa` | [Via Negativa Checklist](parts/via-negativa/docs/via-negativa-checklist.md) | See source/support owners and parent package README; old path lookup routes through `PROVENANCE.md`. |

## Provenance Bridge

Use [PROVENANCE.md](PROVENANCE.md) only when a task must audit former root paths, source accounting, or distillation history.
