# aoa-agents local stats port

This directory exposes statistical questions whose domain meaning belongs to
`aoa-agents`. It uses the shared `aoa-stats` measurement grammar without moving
role, specialization, projection, or runtime truth into the central organ.

## Current Reference Measurement

| Measurement | Question | Reference value |
| --- | --- | --- |
| `aoa-agents/specialization-projection-eligible-ratio` | What fraction of current role-specialization eligibility records have the explicit owner decision `eligible`? | `0 / 5` at source revision `7837d8951b68a47d576fa0495ab36650f770e0da` |

The reference packet is a census of `records[]` in the generated specialization
eligibility readiness reader. The owner validator keeps that reader aligned
with every current role-local specialization and its source eligibility record.
Only an exact `decision_status` of `eligible` enters the numerator;
`candidate_only` remains an observed non-eligible state rather than missing
data.

## Authority

The ratio reports owner-recorded eligibility labels at one source revision. It
does not establish projection, installability, external owner consent, proof
strength, successful use, workspace acceptance, runtime activation, or
generated-agent availability. `aoa-stats` may validate and compose the packet
without redefining role or projection meaning.

## Surfaces

- `port.manifest.json` declares the local question, measurement contract, and
  export.
- `packets/specialization-projection-eligible-ratio.reference.json` records the
  evidence-linked reference observation.
- The specialization eligibility readiness reader is the immediate owner read
  model.
- The specialization eligibility part owns source records, derivation, schema,
  and decision-state meaning.
