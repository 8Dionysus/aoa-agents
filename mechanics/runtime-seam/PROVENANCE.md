# Runtime Seam Provenance Bridge

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

4 mechanics-facing docs moved from `docs/` into `runtime-seam/parts/*/docs/`.

| Former root path | Active route | Part |
| --- | --- | --- |
| `docs/AGENT_AUTHORITY_CLAIM_RUNTIME.md` | [parts/artifact-contracts/docs/authority-claim-runtime.md](parts/artifact-contracts/docs/authority-claim-runtime.md) | `artifact-contracts` |
| `docs/AGENT_RUNTIME_SEAM.md` | [parts/role-tier-bindings/docs/agent-runtime-seam.md](parts/role-tier-bindings/docs/agent-runtime-seam.md) | `role-tier-bindings` |
| `docs/KIND_SAFE_RUNTIME_ENFORCEMENT.md` | [parts/transition-discipline/docs/kind-safe-runtime-enforcement.md](parts/transition-discipline/docs/kind-safe-runtime-enforcement.md) | `transition-discipline` |
| `docs/RUNTIME_ARTIFACT_TRANSITIONS.md` | [parts/transition-discipline/docs/runtime-artifact-transitions.md](parts/transition-discipline/docs/runtime-artifact-transitions.md) | `transition-discipline` |

## 2026-05-26 Runtime Artifact Contract Move

7 runtime artifact schemas and 13 example-route, example, and fixture files
moved from root `schemas/` and `examples/` into the `artifact-contracts` part.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/artifact.route_decision.schema.json` | [parts/artifact-contracts/schemas/artifact.route_decision.schema.json](parts/artifact-contracts/schemas/artifact.route_decision.schema.json) | `artifact-contracts` |
| `schemas/artifact.bounded_plan.schema.json` | [parts/artifact-contracts/schemas/artifact.bounded_plan.schema.json](parts/artifact-contracts/schemas/artifact.bounded_plan.schema.json) | `artifact-contracts` |
| `schemas/artifact.work_result.schema.json` | [parts/artifact-contracts/schemas/artifact.work_result.schema.json](parts/artifact-contracts/schemas/artifact.work_result.schema.json) | `artifact-contracts` |
| `schemas/artifact.verification_result.schema.json` | [parts/artifact-contracts/schemas/artifact.verification_result.schema.json](parts/artifact-contracts/schemas/artifact.verification_result.schema.json) | `artifact-contracts` |
| `schemas/artifact.transition_decision.schema.json` | [parts/artifact-contracts/schemas/artifact.transition_decision.schema.json](parts/artifact-contracts/schemas/artifact.transition_decision.schema.json) | `artifact-contracts` |
| `schemas/artifact.deep_synthesis_note.schema.json` | [parts/artifact-contracts/schemas/artifact.deep_synthesis_note.schema.json](parts/artifact-contracts/schemas/artifact.deep_synthesis_note.schema.json) | `artifact-contracts` |
| `schemas/artifact.distillation_pack.schema.json` | [parts/artifact-contracts/schemas/artifact.distillation_pack.schema.json](parts/artifact-contracts/schemas/artifact.distillation_pack.schema.json) | `artifact-contracts` |
| `examples/runtime_artifacts/AGENTS.md` | [parts/artifact-contracts/examples/README.md](parts/artifact-contracts/examples/README.md) | `artifact-contracts` |
| `examples/runtime_artifacts/route_decision.example.json` | [parts/artifact-contracts/examples/route_decision.example.json](parts/artifact-contracts/examples/route_decision.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/bounded_plan.example.json` | [parts/artifact-contracts/examples/bounded_plan.example.json](parts/artifact-contracts/examples/bounded_plan.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/work_result.example.json` | [parts/artifact-contracts/examples/work_result.example.json](parts/artifact-contracts/examples/work_result.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/verification_result.example.json` | [parts/artifact-contracts/examples/verification_result.example.json](parts/artifact-contracts/examples/verification_result.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/transition_decision.example.json` | [parts/artifact-contracts/examples/transition_decision.example.json](parts/artifact-contracts/examples/transition_decision.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/transition_decision.return.example.json` | [parts/artifact-contracts/examples/transition_decision.return.example.json](parts/artifact-contracts/examples/transition_decision.return.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/deep_synthesis_note.example.json` | [parts/artifact-contracts/examples/deep_synthesis_note.example.json](parts/artifact-contracts/examples/deep_synthesis_note.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/distillation_pack.example.json` | [parts/artifact-contracts/examples/distillation_pack.example.json](parts/artifact-contracts/examples/distillation_pack.example.json) | `artifact-contracts` |
| `examples/runtime_artifacts/invalid/route_decision.wrong_artifact_type.json` | [parts/artifact-contracts/examples/invalid/route_decision.wrong_artifact_type.json](parts/artifact-contracts/examples/invalid/route_decision.wrong_artifact_type.json) | `artifact-contracts` |
| `examples/runtime_artifacts/invalid/bounded_plan.missing_required_field.json` | [parts/artifact-contracts/examples/invalid/bounded_plan.missing_required_field.json](parts/artifact-contracts/examples/invalid/bounded_plan.missing_required_field.json) | `artifact-contracts` |
| `examples/runtime_artifacts/invalid/verification_result.forbidden_extra_property.json` | [parts/artifact-contracts/examples/invalid/verification_result.forbidden_extra_property.json](parts/artifact-contracts/examples/invalid/verification_result.forbidden_extra_property.json) | `artifact-contracts` |
| `examples/runtime_artifacts/invalid/transition_decision.return.invalid.missing_anchor.json` | [parts/artifact-contracts/examples/invalid/transition_decision.return.invalid.missing_anchor.json](parts/artifact-contracts/examples/invalid/transition_decision.return.invalid.missing_anchor.json) | `artifact-contracts` |

Stable schema `$id` values remain public contract identifiers, not active repo
path authority.

## 2026-05-26 Runtime Artifact Check Move

The runtime artifact contract validator and focused tests moved from root
support districts into the owning `artifact-contracts` part.

| Former root path | Active route | Part |
| --- | --- | --- |
| `scripts/validate_runtime_artifact_contracts.py` | [parts/artifact-contracts/scripts/validate_artifact_contracts.py](parts/artifact-contracts/scripts/validate_artifact_contracts.py) | `artifact-contracts` |
| `tests/test_runtime_artifact_contracts.py` | [parts/artifact-contracts/tests/test_artifact_contracts.py](parts/artifact-contracts/tests/test_artifact_contracts.py) | `artifact-contracts` |

## 2026-05-26 Agent Authority Claim Contract Move

The runtime-readable authority claim schema/example moved from root
`schemas/` and `examples/` into the `artifact-contracts` part. It is validated
with `scripts/validate_agent_service_contracts.py` alongside the runtime
artifact route check.

| Former root path | Active route | Part |
| --- | --- | --- |
| `schemas/agent_authority_claim_v1.json` | [parts/artifact-contracts/schemas/agent-authority-claim.schema.json](parts/artifact-contracts/schemas/agent-authority-claim.schema.json) | `artifact-contracts` |
| `examples/agent_authority_claim_v1.example.json` | [parts/artifact-contracts/examples/agent-authority-claim.example.json](parts/artifact-contracts/examples/agent-authority-claim.example.json) | `artifact-contracts` |

## Distillation Rule

When archived or former-path material changes current behavior, update the
relevant active part first. Then update this bridge and the package archive
index/log if route accounting changed. Active part docs must not grow
per-source inventories.
