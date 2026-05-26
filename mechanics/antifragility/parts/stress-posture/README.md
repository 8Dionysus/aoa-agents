# Stress Posture Part

This part routes `stress-posture` pressure inside `mechanics/antifragility/`.

## Active Docs

- [Agent Stress Handoffs](docs/stress-handoffs.md)
- [Agent Stress Posture](docs/stress-posture.md)

## Active Schemas

- [Agent Stress Posture Schema](schemas/agent-stress-posture.schema.json)
- [Stress Handoff Envelope Schema](schemas/stress-handoff-envelope.schema.json)

## Active Examples

- [Agent Stress Posture Example](examples/agent-stress-posture.example.json)
- [Stress Handoff Envelope Example](examples/stress-handoff-envelope.example.json)

## Validation

```bash
python mechanics/antifragility/parts/stress-posture/scripts/validate_stress_posture.py
python scripts/validate_agents.py
python -m unittest discover -s mechanics/antifragility/parts/stress-posture/tests -p "test_*.py"
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
