from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/aoa-summon/scripts/compile_actor_responsibility_receipt.py"
SPEC = importlib.util.spec_from_file_location("actor_receipt_compiler", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
COMPILER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPILER)


ZERO = "sha256:" + "0" * 64


def ref(owner: str, object_id: str, schema_version: str) -> dict[str, str]:
    return {
        "object_id": object_id,
        "owner_repo": owner,
        "schema_version": schema_version,
        "digest": ZERO,
    }


def summon_result() -> dict[str, object]:
    binding = {
        "interface": "abyss_stack_external_codex_agent_v1",
        "inspected": True,
        "available": True,
        "reason": None,
        "binding_kind": "external_cli_incarnation",
        "runtime_owner": "abyss-stack",
        "role_resolution_ref": ref("aoa-agents", "role-resolution:coder:executor", "aoa_role_resolution_v1"),
        "model_fit_query_result_ref": ref("aoa-models", "fit-query:actor", "aoa_model_fit_query_result_v2"),
        "model_fit_projection_ref": ref("aoa-models", "fit-projection:actor", "aoa_model_fit_projection_v1"),
        "model_realization_ref": ref("aoa-models", "model-realization:actor", "aoa_model_realization_v1"),
        "run_plan_ref": ref("aoa-sdk", "run-plan:actor", "aoa_control_plane_v1"),
        "incarnation_binding_ref": ref("aoa-sdk", "incarnation-binding:actor", "aoa_agent_incarnation_binding_v2"),
        "sdk_summon_request_ref": ref("aoa-sdk", "summon-request:actor", "urn:aoa-sdk:a2a:summon-request:v4"),
        "sdk_summon_decision_ref": ref("aoa-sdk", "summon-decision:actor", "urn:aoa-sdk:a2a:summon-result:v4"),
        "runtime_profile_ref": ref("abyss-stack", "runtime-profile:actor", "abyss_stack_external_codex_runtime_profile_v2"),
        "uses_builtin_codex_subagents": False,
    }
    runtime_state = {
        "state": "returned",
        "actor_handle": "incarnation:actor",
        "process_handle": "process:actor",
        "session_handle": "session:actor",
        "continuation_handle": "continuation:actor",
        "runtime_result_ref": ref("abyss-stack", "runtime-result:actor", "abyss_stack_external_codex_result_v2"),
        "runtime_a2a_return_ref": ref("abyss-stack", "runtime-a2a:actor", "abyss_stack_external_codex_a2a_return_v1"),
        "usage_observation_ref": ref("abyss-stack", "runtime-result:actor#/usage_observation", "abyss_stack_external_codex_usage_observation_v1"),
    }
    return {
        "schema_version": "urn:aoa-agents:aoa-summon:result:v4",
        "allowed": True,
        "lane": "external_cli_reviewed",
        "execution_surface": "abyss_stack_external_codex_agent_v1",
        "cohort_pattern": "one external writer",
        "closeout_required": True,
        "decision_state": "allowed",
        "binding": binding,
        "runtime_state": runtime_state,
        "return_validation": {
            "output_checks": {
                "writer-output": {
                    "received": True,
                    "artifact_ref": "artifact://writer-output",
                    "accepted": False,
                }
            },
            "accepted": False,
        },
        "closeout_handoff": {
            "parent_owner": "holder:goal",
            "residual_risk": "Independent review and owner acceptance remain open.",
            "next_route": "aoa-agents:review",
        },
        "actual_effects": ["external-actor-runtime"],
        "stop_line": "No publication, owner acceptance, or stronger-owner inference.",
        "request_ref": "summon-request:actor",
        "request_digest": ZERO,
        "request_intent": "execute",
        "checkpoint_required": True,
        "progression_required": False,
        "blocked_actions": ["publication", "owner_acceptance"],
        "reason_codes": ["returned", "owner_acceptance_not_claimed"],
        "requested_posture": "bounded_execution_with_independent_review",
        "owner_publication_plan": [],
    }


def write_result(path: Path, result: dict[str, object]) -> str:
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    path.write_bytes(raw)
    return "sha256:" + hashlib.sha256(raw).hexdigest()


class ActorResponsibilityReceiptCompilerTests(unittest.TestCase):
    def compile(self, result_path: Path, **overrides: object) -> dict[str, object]:
        values: dict[str, object] = {
            "summon_result_path": result_path,
            "observed_at": "2026-08-14T12:00:00Z",
            "run_ref": "run:actor-receipt-test",
            "session_ref": "session:actor-receipt-test",
            "actor_ref": "incarnation:actor",
            "object_ref": {
                "repo": "aoa-agents",
                "kind": "actor-responsibility-execution",
                "id": "summon-request:actor",
                "version": "v1",
            },
        }
        values.update(overrides)
        return COMPILER.compile_actor_responsibility_receipt(**values)

    def test_compiles_strict_stats_envelope_and_preserves_owner_refs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result.json"
            result = summon_result()
            digest = write_result(result_path, result)
            receipt = self.compile(result_path, expected_result_digest=digest)

            self.assertEqual(receipt["event_kind"], "actor_responsibility_execution_receipt")
            self.assertTrue(receipt["event_id"].startswith("actor-responsibility-execution:"))
            payload = receipt["payload"]
            self.assertEqual(payload["source_result"]["artifact_digest"], digest)
            self.assertEqual(
                payload["owner_evidence"]["binding"]["role_resolution_ref"],
                result["binding"]["role_resolution_ref"],
            )
            self.assertEqual(
                payload["owner_evidence"]["runtime_state"]["runtime_a2a_return_ref"],
                result["runtime_state"]["runtime_a2a_return_ref"],
            )
            self.assertEqual(payload["authority_posture"]["model_fit"], "not_inferred")
            self.assertEqual(payload["authority_posture"]["owner_acceptance"], "not_claimed")

    def test_compilation_is_deterministic_for_exact_bytes_and_observations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result.json"
            write_result(result_path, summon_result())
            first = self.compile(result_path)
            second = self.compile(result_path)
            self.assertEqual(first, second)

    def test_digest_and_event_identity_assertions_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result.json"
            digest = write_result(result_path, summon_result())
            with self.assertRaisesRegex(COMPILER.ActorResponsibilityReceiptError, "expected_result_digest"):
                self.compile(result_path, expected_result_digest=ZERO)
            with self.assertRaisesRegex(COMPILER.ActorResponsibilityReceiptError, "event_id"):
                self.compile(result_path, event_id="actor-responsibility-execution:forged")
            self.assertNotEqual(digest, ZERO)

    def test_missing_owner_evidence_and_inference_widening_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result.json"
            result = summon_result()
            del result["binding"]["runtime_profile_ref"]
            write_result(result_path, result)
            with self.assertRaises(COMPILER.ActorResponsibilityReceiptError):
                self.compile(result_path)

            widened = summon_result()
            widened["binding"]["uses_builtin_codex_subagents"] = True
            write_result(result_path, widened)
            with self.assertRaises(COMPILER.ActorResponsibilityReceiptError):
                self.compile(result_path)

    def test_evidence_refs_cannot_be_rebound_after_compilation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result.json"
            write_result(result_path, summon_result())
            receipt = self.compile(result_path)
            receipt["evidence_refs"][0]["ref"] = "forged-ref"
            with self.assertRaisesRegex(COMPILER.ActorResponsibilityReceiptError, "evidence_refs"):
                COMPILER.validate_receipt(receipt)

    def test_runtime_state_controls_preserved_runtime_refs(self) -> None:
        expected_refs = {
            "returned": {"runtime_result_ref", "runtime_a2a_return_ref", "usage_observation_ref"},
            "accepted": {"runtime_result_ref", "runtime_a2a_return_ref", "usage_observation_ref"},
            "failed": {"runtime_result_ref", "usage_observation_ref"},
            "launched": set(),
            "running": set(),
        }
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result.json"
            for state, required_refs in expected_refs.items():
                with self.subTest(state=state):
                    result = summon_result()
                    result["runtime_state"]["state"] = state
                    if state in {"launched", "running"}:
                        result["runtime_state"].pop("runtime_result_ref")
                        result["runtime_state"].pop("runtime_a2a_return_ref")
                        result["runtime_state"].pop("usage_observation_ref")
                        result["return_validation"] = {
                            "output_checks": {
                                "writer-output": {
                                    "received": False,
                                    "artifact_ref": None,
                                    "accepted": False,
                                }
                            },
                            "accepted": False,
                        }
                    elif state == "failed":
                        result["runtime_state"].pop("runtime_a2a_return_ref")
                    elif state == "accepted":
                        result["return_validation"] = {
                            "output_checks": {
                                "writer-output": {
                                    "received": True,
                                    "artifact_ref": "artifact://writer-output",
                                    "accepted": True,
                                }
                            },
                            "accepted": True,
                        }
                    write_result(result_path, result)

                    receipt = self.compile(result_path)
                    runtime_state = receipt["payload"]["owner_evidence"]["runtime_state"]
                    self.assertEqual(
                        {field for field in runtime_state if field.endswith("_ref")},
                        required_refs,
                    )

    def test_runtime_state_rejects_missing_state_specific_refs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result.json"
            returned = summon_result()
            returned["runtime_state"].pop("runtime_a2a_return_ref")
            write_result(result_path, returned)
            with self.assertRaisesRegex(COMPILER.ActorResponsibilityReceiptError, "runtime_a2a_return_ref"):
                self.compile(result_path)

            failed = summon_result()
            failed["runtime_state"]["state"] = "failed"
            failed["runtime_state"].pop("runtime_result_ref")
            failed["runtime_state"].pop("runtime_a2a_return_ref")
            write_result(result_path, failed)
            with self.assertRaisesRegex(COMPILER.ActorResponsibilityReceiptError, "runtime_result_ref"):
                self.compile(result_path)

    def test_actor_safe_envelope_is_addressed_by_its_exact_envelope_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result_path = Path(directory) / "summon-result-envelope.json"
            envelope = {
                "$schema": "schemas/external-codex-actor-input-envelope.schema.json",
                "input_id": "sample-summon-result-v4",
                "payload": summon_result(),
                "payload_kind": "json",
                "schema_version": "abyss_stack_external_codex_actor_input_envelope_v1",
                "source_artifact_digest": ZERO,
                "source_schema_ref": "skills/aoa-summon/references/summon-result-v4.schema.json",
                "source_schema_version": "urn:aoa-agents:aoa-summon:result:v4",
            }
            digest = write_result(result_path, envelope)
            receipt = self.compile(result_path)
            self.assertEqual(receipt["payload"]["source_result"]["artifact_digest"], digest)
            self.assertNotEqual(digest, envelope["source_artifact_digest"])


if __name__ == "__main__":
    unittest.main()
