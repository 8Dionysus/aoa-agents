from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/aoa-summon/scripts/compile_external_execution_result.py"
SCHEMA = ROOT / "skills/aoa-summon/references/summon-result-v4.schema.json"
SPEC = importlib.util.spec_from_file_location("external_result_compiler", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
COMPILER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPILER)


ZERO = "sha256:" + "0" * 64


def ref(owner: str, object_id: str, schema_version: str, digest: str = ZERO) -> dict[str, str]:
    return {
        "object_id": object_id,
        "owner_repo": owner,
        "schema_version": schema_version,
        "digest": digest,
    }


def write_json(path: Path, payload: dict[str, object]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    path.write_bytes(raw)
    return COMPILER.digest_bytes(raw)


def fixture(temp: Path) -> dict[str, object]:
    outputs = ["external_codex_agent_result", "summon-result-compiler-implementation"]
    sdk_request = {
        "summon_request": {
            "transport_preference": "a2a_remote",
            "parent_task_id": "goal:landing",
        },
        "expected_outputs": outputs,
    }
    sdk_request_path = temp / "sdk-request.json"
    sdk_request_digest = write_json(sdk_request_path, sdk_request)

    sdk_decision = {
        "schema_version": "urn:aoa-sdk:a2a:summon-result:v4",
        "allowed": True,
        "capability_execution_claimed": False,
        "request_artifact_digest": sdk_request_digest,
        "cohort_pattern": "solo",
    }
    sdk_decision_path = temp / "sdk-decision.json"
    sdk_decision_digest = write_json(sdk_decision_path, sdk_decision)

    incarnation = {
        "obligation_ref": ref("aoa-agents", "obligation:landing", "agent-obligation-v1"),
        "actor_mandate_ref": ref("aoa-agents", "mandate:landing", "actor-mandate-v1"),
        "role_resolution_ref": ref("aoa-agents", "role-resolution:coder:executor", "aoa_role_resolution_v1"),
        "model_fit_query_result_ref": ref("aoa-models", "fit-query:landing", "aoa_model_fit_query_result_v2"),
        "model_fit_projection_ref": ref("aoa-models", "fit-projection:landing", "aoa_model_fit_projection_v1"),
        "task_local_dag_ref": ref("aoa-skills", "dag:landing", "aoa-task-local-dag-v2"),
        "incarnation_binding_ref": ref("aoa-sdk", "incarnation-binding:landing", "aoa_agent_incarnation_binding_v2"),
        "sdk_summon_request_ref": ref("aoa-sdk", "sdk-request:landing", "urn:aoa-sdk:a2a:summon-request:v4", sdk_request_digest),
        "sdk_summon_decision_ref": ref("aoa-sdk", "sdk-decision:landing", "urn:aoa-sdk:a2a:summon-result:v4", sdk_decision_digest),
        "runtime_launch_ref": ref("abyss-stack", "launch:landing", "abyss_stack_external_codex_launch_v1"),
        "responsibility_transfer_ref": {
            **ref("aoa-agents", "transfer:landing", "responsibility-transfer-v1"),
            "admitted_state": "accepted",
            "holder_ids": ["holder:goal", "actor:landing"],
        },
        "continuity_ref": ref("aoa-sdk", "continuation:landing", "continuation-obligation-v1"),
        "return_event_schema_ref": ref("abyss-stack", "schema:external-event", "abyss_stack_external_codex_event_v1"),
        "domain_procedure_refs": [ref("aoa-agents", "procedure:landing", "owner-procedure-v1")],
        "runtime_interface": "abyss_stack_external_codex_agent_v1",
        "launches_separate_os_process": True,
        "separate_cli_session": True,
        "uses_builtin_codex_subagents": False,
        "usage_metering": "observe_only_no_budget",
    }
    request = {
        "quest_passport": {
            "difficulty": "d2_slice",
            "risk": "r1_repo_local",
            "control_mode": "codex_supervised",
            "delegate_tier": "executor",
            "route_anchor": "goal:landing",
        },
        "summon_request": {
            "transport_preference": "external_cli",
            "child_agent_id": "incarnation:landing",
            "parent_task_id": "goal:landing",
            "desired_role": "coder",
            "require_progression": False,
        },
        "expected_outputs": outputs,
        "intent": "execute",
        "return_owner": "holder:goal",
        "child_scope": {
            "task": "Implement one bounded owner-local change.",
            "allowed_tools": ["shell-read", "workspace-write"],
            "allowed_effects": ["repo_mutation"],
            "authority_limit": "No commit, push, merge, publication, or owner acceptance.",
        },
        "child_stop_line": "Stop at owner ambiguity or external effect.",
        "child_inputs": [{"kind": "contract", "ref": "procedure:landing"}],
        "request_ref": "summon-request:landing",
        "request_digest": ZERO,
        "external_incarnation": incarnation,
    }
    request["request_digest"] = COMPILER.semantic_request_digest(request)
    request_path = temp / "request.json"
    write_json(request_path, request)

    runtime = {
        "schema_version": "abyss_stack_external_codex_result_v2",
        "task_id": "actor-task-landing",
        "incarnation_id": "incarnation:landing",
        "status": "completed",
        "exit_code": 0,
        "execution_posture": "bounded_execution",
        "admission_class": "owner_contour",
        "session_id": "session:landing",
        "thread_id": "thread:landing",
        "usage_observation": {"status": "complete", "gap_reasons": []},
        "wake_evaluation": {
            "event_kind": "result.validated",
            "condition_id": "validated-completion",
            "action": "wake_parent",
            "wake_parent": True,
            "reason": "validated terminal runtime result",
        },
        "codex_invocations": [
            {
                "argv": ["codex", "--disable", "multi_agent"],
                "process_identity_ref": {
                    "artifact_ref": "process-identity:landing"
                },
            }
        ],
    }
    runtime_path = temp / "runtime-result.json"
    runtime_digest = write_json(runtime_path, runtime)

    a2a = {
        "schema_version": "abyss_stack_external_codex_a2a_return_v1",
        "reviewed": True,
        "review_status": "reviewed",
        "reviewer_status": "completed",
        "reviewer_decision": "proceed",
        "review_outcome": "proceed",
        "evidence_digests": {"writer_result": runtime_digest},
        "reviewed_artifact_path": "runtime-result.json",
        "summon_request_ref": incarnation["sdk_summon_request_ref"],
        "review_summon_request_ref": ref("aoa-sdk", "review-request:landing", "urn:aoa-sdk:a2a:summon-request:v4"),
        "remote_task": {
            "agent_id": "incarnation:landing",
            "context_id": "session:landing-review",
            "parent_task_id": "goal:landing",
            "task_id": "actor-task-landing",
            "state": "completed",
            "artifact_refs": ["runtime-result.json"],
            "returned_artifacts": outputs,
        },
    }
    a2a_path = temp / "a2a-return.json"
    write_json(a2a_path, a2a)

    return {
        "request": request,
        "request_path": request_path,
        "sdk_request": sdk_request,
        "sdk_request_path": sdk_request_path,
        "sdk_decision_path": sdk_decision_path,
        "runtime": runtime,
        "runtime_path": runtime_path,
        "a2a": a2a,
        "a2a_path": a2a_path,
        "runtime_profile_ref": ref("abyss-stack", "runtime-profile:landing", "abyss_stack_external_codex_runtime_profile_v2"),
    }


class CompileExternalExecutionResultTests(unittest.TestCase):
    def compile(self, data: dict[str, object]) -> dict[str, object]:
        return COMPILER.compile_external_execution_result(
            request_path=data["request_path"],
            sdk_summon_request_path=data["sdk_request_path"],
            sdk_summon_decision_path=data["sdk_decision_path"],
            runtime_result_path=data["runtime_path"],
            reviewed_a2a_return_path=data["a2a_path"],
            runtime_profile_ref=data["runtime_profile_ref"],
        )

    def test_positive_result_is_v4_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            first = self.compile(data)
            second = self.compile(data)
            self.assertEqual(first, second)
            self.assertEqual(first["runtime_state"]["state"], "accepted")
            self.assertEqual(
                set(first["return_validation"]["output_checks"]),
                set(data["request"]["expected_outputs"]),
            )
            self.assertNotIn("expected_outputs", first)
            errors = list(Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(first))
            self.assertEqual(errors, [])

    def test_usage_is_a_digest_bound_json_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            result = self.compile(data)
            usage_ref = result["runtime_state"]["usage_observation_ref"]
            self.assertEqual(usage_ref["object_id"], "actor-task-landing#/usage_observation")
            self.assertEqual(
                usage_ref["digest"],
                COMPILER.digest_bytes(COMPILER.canonical_bytes(data["runtime"]["usage_observation"])),
            )

    def test_request_digest_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["request_digest"] = ZERO
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "request digest mismatch"):
                self.compile(data)

    def test_request_schema_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["untrusted_extra"] = True
            request["request_digest"] = COMPILER.semantic_request_digest(request)
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "summon-request-v4 schema"):
                self.compile(data)

    def test_sdk_decision_request_identity_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            decision = {"schema_version": "urn:aoa-sdk:a2a:summon-result:v4", "allowed": True, "capability_execution_claimed": False, "request_artifact_digest": ZERO}
            write_json(data["sdk_decision_path"], decision)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "SDK summon decision names"):
                self.compile(data)

    def test_nonterminal_runtime_result_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["status"] = "paused"
            write_json(data["runtime_path"], runtime)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "nonterminal"):
                self.compile(data)

    def test_runtime_result_v1_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["schema_version"] = "abyss_stack_external_codex_result_v1"
            write_json(data["runtime_path"], runtime)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "runtime result schema"):
                self.compile(data)

    def test_usage_locator_and_partial_pointer_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "usage pointer"):
                COMPILER.compile_external_execution_result(
                    request_path=data["request_path"],
                    sdk_summon_request_path=data["sdk_request_path"],
                    sdk_summon_decision_path=data["sdk_decision_path"],
                    runtime_result_path=data["runtime_path"],
                    reviewed_a2a_return_path=data["a2a_path"],
                    runtime_profile_ref=data["runtime_profile_ref"],
                    usage_pointer="/usage_observation/missing",
                )

    def test_standalone_usage_artifact_can_replace_pointer_locator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            usage_path = Path(directory) / "usage-observation.json"
            write_json(
                usage_path,
                {
                    "usage_observation_id": "usage:landing",
                    "status": "complete",
                    "gap_reasons": [],
                },
            )
            result = COMPILER.compile_external_execution_result(
                request_path=data["request_path"],
                sdk_summon_request_path=data["sdk_request_path"],
                sdk_summon_decision_path=data["sdk_decision_path"],
                runtime_result_path=data["runtime_path"],
                reviewed_a2a_return_path=data["a2a_path"],
                runtime_profile_ref=data["runtime_profile_ref"],
                usage_observation_path=usage_path,
            )
            self.assertEqual(
                result["runtime_state"]["usage_observation_ref"]["object_id"],
                "usage:landing",
            )

    def test_unreviewed_a2a_return_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["reviewed"] = False
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "not reviewed"):
                self.compile(data)

    def test_reviewed_a2a_schema_version_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["schema_version"] = "abyss_stack_external_codex_a2a_return_v0"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "schema/version"):
                self.compile(data)

    def test_reviewed_a2a_requires_runtime_validated_event(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["wake_evaluation"]["event_kind"] = "result.review_required"
            runtime_digest = write_json(data["runtime_path"], runtime)
            a2a = copy.deepcopy(data["a2a"])
            a2a["evidence_digests"]["writer_result"] = runtime_digest
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "result.validated"):
                self.compile(data)

    def test_reviewed_a2a_writer_result_must_bind_terminal_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["evidence_digests"]["writer_result"] = ZERO
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "terminal runtime result"):
                self.compile(data)

    def test_reviewed_a2a_remote_task_id_must_bind_terminal_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["task_id"] = "actor-task-unrelated"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "remote task id.*terminal runtime task id"):
                self.compile(data)

    def test_reviewed_a2a_agent_id_must_bind_terminal_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["agent_id"] = "incarnation:unrelated"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "remote task agent id.*terminal runtime incarnation id"):
                self.compile(data)

    def test_review_disposition_cannot_be_widened(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["review_outcome"] = "return_for_repair"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "not accepting"):
                self.compile(data)

    def test_output_key_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["returned_artifacts"] = ["external_codex_agent_result", "unexpected-output"]
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "output keys"):
                self.compile(data)

    def test_extra_returned_artifact_fails_closed_when_requested_outputs_exist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["returned_artifacts"] = [
                *data["request"]["expected_outputs"],
                "unexpected-output",
            ]
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "outside.*closure"):
                self.compile(data)

    def test_resolving_noncanonical_usage_pointer_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "canonical /usage_observation"):
                COMPILER.compile_external_execution_result(
                    request_path=data["request_path"],
                    sdk_summon_request_path=data["sdk_request_path"],
                    sdk_summon_decision_path=data["sdk_decision_path"],
                    runtime_result_path=data["runtime_path"],
                    reviewed_a2a_return_path=data["a2a_path"],
                    runtime_profile_ref=data["runtime_profile_ref"],
                    usage_pointer="/usage_observation/status",
                )

    def test_effect_ceiling_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["child_scope"]["allowed_effects"] = ["external_effect"]
            request["request_digest"] = COMPILER.semantic_request_digest(request)
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "effect ceiling"):
                self.compile(data)

    def test_runtime_profile_owner_and_builtin_subagent_drift_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            bad_profile = copy.deepcopy(data["runtime_profile_ref"])
            bad_profile["owner_repo"] = "aoa-stats"
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "runtime profile ref owner"):
                data["runtime_profile_ref"] = bad_profile
                self.compile(data)

            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["codex_invocations"][0]["argv"] = ["codex", "--enable", "multi_agent"]
            write_json(data["runtime_path"], runtime)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "disable built-in"):
                self.compile(data)


if __name__ == "__main__":
    unittest.main()
