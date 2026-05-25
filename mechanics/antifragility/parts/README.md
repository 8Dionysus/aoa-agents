# Antifragility Parts

`mechanics/antifragility/parts/` is the lower index for active failure-pressure
and negative-check parts.

## Active Parts

| Part | Operation | Current route |
| --- | --- | --- |
| `stress-posture/` | agent stress posture and handoff | `stress-posture/README.md` |
| `via-negativa/` | negative checklist pressure phrased as operational route alternatives | `via-negativa/README.md` |
| `scar-adaptation/` | shared scar, retention, and adaptation after Agon pressure | `scar-adaptation/README.md` |
| `checkpoint-survival/` | stress that must remain reviewable before promotion | `checkpoint-survival/README.md` |

## Admission Rule

Create child part directories only when package-local contracts or validators
exist. Until then, `../PARTS.md` owns the payload anchor map.
