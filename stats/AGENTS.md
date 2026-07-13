# AGENTS.md

## Applies To

This card applies to `stats/` in `aoa-agents`.

## Role

This directory owns agent-local statistical questions, their embedded
measurement contracts, and evidence-linked reference packets. Shared
statistical grammar and cross-owner composition remain owned by `aoa-stats`.

## Read Before Editing

1. Root `AGENTS.md`, `README.md`, and `DESIGN.md`.
2. `stats/README.md` and `stats/port.manifest.json`.
3. The specialization eligibility records, readiness builder, and generated
   reader under `mechanics/codex-projection/parts/specialization-eligibility/`.
4. The central measurement and packet contracts under `aoa-stats/stats/`.

## Boundaries

- `port.manifest.json` owns the agent-local question and measurement meaning.
- Reference packets are derived snapshots and remain weaker than eligibility
  source records and their owner decision.
- The eligibility ratio reports explicit `eligible` decision labels only. It
  does not establish projection, installability, proof strength, workspace
  acceptance, runtime activation, or generated-agent availability.
- Keep packet refs repository-relative and raw role or evidence content out of
  packets.

## Validation

Inspect the owner read model first:

```bash
python -c 'import json, pathlib; p=json.loads(pathlib.Path("mechanics/codex-projection/parts/specialization-eligibility/generated/specialization-eligibility-readiness.min.json").read_text()); rows=p["records"]; eligible=sum(row["decision_status"] == "eligible" for row in rows); print({"population": len(rows), "eligible": eligible, "ratio": eligible / len(rows)})'
```

Then validate the port and packet with the central contract owner:

```bash
python scripts/validate_local_stats_port.py
```

## Closeout

Report the question or contract changed, owner evidence inspected, whether the
reference packet was refreshed, and which validation route ran.
