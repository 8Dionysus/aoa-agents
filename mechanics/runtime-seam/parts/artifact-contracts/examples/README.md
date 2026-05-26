# Runtime Artifact Examples

## Purpose

This directory contains inspectable examples for the public runtime artifact
contracts owned by the `artifact-contracts` part.

Each `*.example.json` aligns with the corresponding schema in sibling
[schemas/](../schemas/) and with `generated/runtime_seam_bindings.json`.

## Active Examples

- [agent-authority-claim.example.json](agent-authority-claim.example.json)
- [route_decision.example.json](route_decision.example.json)
- [bounded_plan.example.json](bounded_plan.example.json)
- [work_result.example.json](work_result.example.json)
- [verification_result.example.json](verification_result.example.json)
- [transition_decision.example.json](transition_decision.example.json)
- [transition_decision.return.example.json](transition_decision.return.example.json)
- [deep_synthesis_note.example.json](deep_synthesis_note.example.json)
- [distillation_pack.example.json](distillation_pack.example.json)

## Invalid fixtures

`invalid/` exists for negative coverage and must stay intentionally invalid.
Do not turn an invalid fixture into a second example.

## Editing posture

Keep examples phase-correct, minimal, and portable.
Do not add tool wiring, transport envelopes, runtime logs, or vendor-specific fields.
Keep coverage aligned with `mechanics/runtime-seam/parts/transition-discipline/docs/runtime-artifact-transitions.md` and `mechanics/runtime-seam/parts/role-tier-bindings/docs/agent-runtime-seam.md`.

## Validation

Run `python -m pip install -r requirements-dev.txt`, then:

```bash
python mechanics/runtime-seam/parts/artifact-contracts/scripts/validate_artifact_contracts.py
python mechanics/experience/scripts/validate_agent_service_contracts.py
python scripts/validate_agents.py
```
