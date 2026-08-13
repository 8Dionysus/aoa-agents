from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

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
    passport = {
        "difficulty": "d2_slice",
        "risk": "r1_repo_local",
        "control_mode": "codex_supervised",
        "delegate_tier": "executor",
        "route_anchor": "goal:landing",
    }
    sdk_request = {
        "quest_passport": passport,
        "summon_request": {
            "transport_preference": "a2a_remote",
            "child_agent_id": "incarnation:landing",
            "parent_task_id": "goal:landing",
            "desired_role": "coder",
            "require_progression": False,
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

    runtime_profile_ref = ref(
        "abyss-stack",
        "runtime-profile:landing",
        "abyss_stack_external_codex_runtime_profile_v2",
    )
    obligation_ref = ref("aoa-agents", "obligation:landing", "agent-obligation-v1")
    mandate_ref = ref("aoa-agents", "mandate:landing", "actor-mandate-v1")
    role_resolution_ref = ref("aoa-agents", "role-resolution:coder:executor", "aoa_role_resolution_v1")
    model_fit_query_ref = ref("aoa-models", "fit-query:landing", "aoa_model_fit_query_result_v2")
    model_fit_projection_ref = ref("aoa-models", "fit-projection:landing", "aoa_model_fit_projection_v1")
    sdk_request_ref = ref("aoa-sdk", "sdk-request:landing", "urn:aoa-sdk:a2a:summon-request:v4", sdk_request_digest)
    sdk_decision_ref = ref("aoa-sdk", "sdk-decision:landing", "urn:aoa-sdk:a2a:summon-result:v4", sdk_decision_digest)
    task_local_dag_ref = ref("aoa-skills", "dag:landing", "aoa-task-local-dag-v2")
    responsibility_transfer_ref = ref("aoa-agents", "transfer:landing", "responsibility-transfer-v1")
    domain_procedure_ref = ref("aoa-agents", "procedure:landing", "owner-procedure-v1")

    def provenance(value: dict[str, str]) -> dict[str, str]:
        return {
            "artifact_ref": value["object_id"],
            "owner_repo": value["owner_repo"],
            "schema_version": value["schema_version"],
            "artifact_digest": value["digest"],
        }

    incarnation_binding = {
        "schema_version": "aoa_agent_incarnation_binding_v2",
        "binding_id": "incarnation-binding:landing",
        "incarnation_id": "incarnation:landing",
        "agent_obligation_ref": obligation_ref,
        "actor_mandate_ref": mandate_ref,
        "role_resolution_ref": role_resolution_ref,
        "model_fit_query_result_ref": model_fit_query_ref,
        "model_fit_projection_ref": provenance(model_fit_projection_ref),
        "task_request_ref": provenance(sdk_request_ref),
        "role_contract_ref": provenance(mandate_ref),
        "runtime_profile_ref": {
            "artifact_ref": runtime_profile_ref["object_id"],
            "owner_repo": runtime_profile_ref["owner_repo"],
            "schema_version": runtime_profile_ref["schema_version"],
            "artifact_digest": runtime_profile_ref["digest"],
        },
        "continuation": {
            "continuation_id": "continuation:landing",
            "exact_child_identity": "incarnation:landing",
            "parent_objective_ref": provenance(task_local_dag_ref),
            "established_decision_refs": [provenance(sdk_decision_ref)],
            "immutable_input_refs": [
                provenance(sdk_request_ref),
                provenance(model_fit_projection_ref),
                provenance(task_local_dag_ref),
                provenance(responsibility_transfer_ref),
                provenance(domain_procedure_ref),
            ],
        },
        "permission_posture": {"allowed_effect_classes": ["repo_mutation"]},
        "tool_profile": {
            "profile_ref": {
                "artifact_ref": runtime_profile_ref["object_id"],
                "owner_repo": runtime_profile_ref["owner_repo"],
                "schema_version": runtime_profile_ref["schema_version"],
                "artifact_digest": runtime_profile_ref["digest"],
            }
        },
        "provenance": {
            "artifact_ref": "incarnation-binding:landing",
            "owner_repo": "aoa-sdk",
        },
    }
    incarnation_binding_path = temp / "incarnation-binding.json"
    incarnation_binding_digest = write_json(
        incarnation_binding_path, incarnation_binding
    )
    incarnation = {
        "obligation_ref": obligation_ref,
        "actor_mandate_ref": mandate_ref,
        "role_resolution_ref": role_resolution_ref,
        "model_fit_query_result_ref": model_fit_query_ref,
        "model_fit_projection_ref": model_fit_projection_ref,
        "task_local_dag_ref": task_local_dag_ref,
        "incarnation_binding_ref": ref(
            "aoa-sdk",
            "incarnation-binding:landing",
            "aoa_agent_incarnation_binding_v2",
            incarnation_binding_digest,
        ),
        "sdk_summon_request_ref": sdk_request_ref,
        "sdk_summon_decision_ref": sdk_decision_ref,
        "runtime_launch_ref": ref("abyss-stack", "launch:landing", "abyss_stack_external_codex_launch_v1"),
        "responsibility_transfer_ref": {
            **responsibility_transfer_ref,
            "admitted_state": "accepted",
            "holder_ids": ["holder:goal", "actor:landing"],
        },
        "continuity_ref": ref(
            "aoa-sdk",
            "continuation:landing",
            "continuation-obligation-v1",
            incarnation_binding_digest,
        ),
        "return_event_schema_ref": ref("abyss-stack", "schema:external-event", "abyss_stack_external_codex_event_v1"),
        "domain_procedure_refs": [domain_procedure_ref],
        "runtime_interface": "abyss_stack_external_codex_agent_v1",
        "launches_separate_os_process": True,
        "separate_cli_session": True,
        "uses_builtin_codex_subagents": False,
        "usage_metering": "observe_only_no_budget",
    }
    request = {
        "quest_passport": passport,
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
    request_artifact_digest = write_json(request_path, request)

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
        "owner_admission_ref": {
            "artifact_ref": "summon-request:landing",
            "owner_repo": "aoa-agents",
            "artifact_digest": request_artifact_digest,
        },
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
                "thread_id": "thread:landing",
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
        "incarnation_binding": incarnation_binding,
        "incarnation_binding_path": incarnation_binding_path,
        "sdk_request": sdk_request,
        "sdk_request_path": sdk_request_path,
        "sdk_decision_path": sdk_decision_path,
        "runtime": runtime,
        "runtime_path": runtime_path,
        "a2a": a2a,
        "a2a_path": a2a_path,
        "runtime_profile_ref": runtime_profile_ref,
    }


def rewrite_bound_chain(
    data: dict[str, object],
    *,
    request: dict[str, object] | None = None,
    incarnation_binding: dict[str, object] | None = None,
) -> None:
    request = copy.deepcopy(request if request is not None else data["request"])
    if incarnation_binding is not None:
        binding_digest = write_json(
            data["incarnation_binding_path"], incarnation_binding
        )
        request["external_incarnation"]["incarnation_binding_ref"]["digest"] = (
            binding_digest
        )
        request["external_incarnation"]["continuity_ref"]["digest"] = binding_digest
        data["incarnation_binding"] = incarnation_binding
    request["request_digest"] = COMPILER.semantic_request_digest(request)
    request_artifact_digest = write_json(data["request_path"], request)
    runtime = copy.deepcopy(data["runtime"])
    runtime["owner_admission_ref"]["artifact_digest"] = request_artifact_digest
    runtime_digest = write_json(data["runtime_path"], runtime)
    a2a = copy.deepcopy(data["a2a"])
    a2a["evidence_digests"]["writer_result"] = runtime_digest
    write_json(data["a2a_path"], a2a)
    data["request"] = request
    data["runtime"] = runtime
    data["a2a"] = a2a


class CompileExternalExecutionResultTests(unittest.TestCase):
    def compile(self, data: dict[str, object]) -> dict[str, object]:
        return COMPILER.compile_external_execution_result(
            request_path=data["request_path"],
            incarnation_binding_path=data["incarnation_binding_path"],
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

    def test_owner_summon_body_must_be_the_sdk_transport_translation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["summon_request"]["child_agent_id"] = "incarnation:other"
            request["request_digest"] = COMPILER.semantic_request_digest(request)
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "owner summon request differs",
            ):
                self.compile(data)

    def test_sdk_request_cannot_arrive_pretranslated_to_external_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            sdk_request = copy.deepcopy(data["sdk_request"])
            sdk_request["summon_request"]["transport_preference"] = "external_cli"
            sdk_digest = write_json(data["sdk_request_path"], sdk_request)

            decision = json.loads(data["sdk_decision_path"].read_text())
            decision["request_artifact_digest"] = sdk_digest
            decision_digest = write_json(data["sdk_decision_path"], decision)

            request = copy.deepcopy(data["request"])
            request["external_incarnation"]["sdk_summon_request_ref"]["digest"] = sdk_digest
            request["external_incarnation"]["sdk_summon_decision_ref"]["digest"] = decision_digest
            request["request_digest"] = COMPILER.semantic_request_digest(request)
            write_json(data["request_path"], request)

            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "external A2A transport",
            ):
                self.compile(data)

    def test_owner_passport_must_match_the_sdk_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["quest_passport"]["route_anchor"] = "goal:other"
            request["request_digest"] = COMPILER.semantic_request_digest(request)
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "quest passport differs",
            ):
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

    def test_runtime_result_must_bind_the_exact_owner_request_and_launch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["external_incarnation"]["runtime_launch_ref"]["digest"] = (
                "sha256:" + "1" * 64
            )
            request["request_digest"] = COMPILER.semantic_request_digest(request)
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "selected owner request and launch",
            ):
                self.compile(data)

    def test_runtime_owner_admission_must_name_the_exact_owner_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["owner_admission_ref"]["artifact_ref"] = (
                "summon-request:other"
            )
            runtime_digest = write_json(data["runtime_path"], runtime)
            a2a = copy.deepcopy(data["a2a"])
            a2a["evidence_digests"]["writer_result"] = runtime_digest
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "selected owner request and launch",
            ):
                self.compile(data)

    def test_runtime_thread_must_bind_physical_invocation_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["thread_id"] = "thread:other"
            runtime_digest = write_json(data["runtime_path"], runtime)
            a2a = copy.deepcopy(data["a2a"])
            a2a["evidence_digests"]["writer_result"] = runtime_digest
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "physical invocation evidence",
            ):
                self.compile(data)

    def test_each_runtime_invocation_must_bind_the_same_thread(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["codex_invocations"].append(
                {
                    "argv": ["codex", "--disable", "multi_agent"],
                    "thread_id": None,
                    "process_identity_ref": {
                        "artifact_ref": "process-identity:landing-resume"
                    },
                }
            )
            runtime_digest = write_json(data["runtime_path"], runtime)
            a2a = copy.deepcopy(data["a2a"])
            a2a["evidence_digests"]["writer_result"] = runtime_digest
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "physical invocation evidence",
            ):
                self.compile(data)

    def test_incarnation_continuation_must_bind_the_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["continuation"]["continuation_id"] = "continuation:other"
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "continuation differs",
            ):
                self.compile(data)

    def test_incarnation_binding_provenance_must_bind_the_request_ref(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["provenance"]["artifact_ref"] = "incarnation-binding:other"
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "binding provenance differs",
            ):
                self.compile(data)

    def test_incarnation_owner_refs_must_bind_the_exact_request(self) -> None:
        cases = (
            ("agent_obligation_ref", "object_id"),
            ("actor_mandate_ref", "digest"),
            ("role_resolution_ref", "object_id"),
            ("model_fit_query_result_ref", "digest"),
        )
        for field, changed_key in cases:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                binding[field][changed_key] = "different:object" if changed_key == "object_id" else "sha256:" + "1" * 64
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, f"{field} differs from the request"):
                    self.compile(data)

    def test_incarnation_projection_and_task_refs_must_bind_the_exact_request(self) -> None:
        cases = (
            ("model_fit_projection_ref", "artifact_digest"),
            ("task_request_ref", "artifact_ref"),
        )
        for field, changed_key in cases:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                binding[field][changed_key] = "different:artifact" if changed_key == "artifact_ref" else "sha256:" + "1" * 64
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, f"{field} differs from the request"):
                    self.compile(data)

    def test_incarnation_continuation_child_must_bind_the_exact_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["continuation"]["exact_child_identity"] = "incarnation:other"
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "continuation child identity differs"):
                self.compile(data)

    def test_incarnation_role_contract_must_name_the_request_mandate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["role_contract_ref"]["artifact_ref"] = "mandate:other"
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "role_contract_ref names another mandate"):
                self.compile(data)

    def test_incarnation_continuation_must_preserve_request_chain(self) -> None:
        cases = (
            ("parent DAG", lambda binding: binding["continuation"]["parent_objective_ref"].update({"artifact_digest": "sha256:" + "1" * 64}), "parent objective differs from the request DAG"),
            ("SDK decision", lambda binding: binding["continuation"]["established_decision_refs"].clear(), "exact SDK summon decision"),
            ("immutable SDK request", lambda binding: binding["continuation"]["immutable_input_refs"].pop(0), "exact SDK summon request"),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                mutate(binding)
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, message):
                    self.compile(data)

    def test_usage_locator_and_partial_pointer_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "usage pointer"):
                COMPILER.compile_external_execution_result(
                    request_path=data["request_path"],
                    incarnation_binding_path=data["incarnation_binding_path"],
                    sdk_summon_request_path=data["sdk_request_path"],
                    sdk_summon_decision_path=data["sdk_decision_path"],
                    runtime_result_path=data["runtime_path"],
                    reviewed_a2a_return_path=data["a2a_path"],
                    runtime_profile_ref=data["runtime_profile_ref"],
                    usage_pointer="/usage_observation/missing",
                )

    def test_exact_usage_ref_can_assert_pointer_locator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            usage_ref = ref(
                "abyss-stack",
                "actor-task-landing#/usage_observation",
                "abyss_stack_external_codex_usage_observation_v1",
                COMPILER.digest_bytes(COMPILER.canonical_bytes(data["runtime"]["usage_observation"])),
            )
            result = COMPILER.compile_external_execution_result(
                request_path=data["request_path"],
                incarnation_binding_path=data["incarnation_binding_path"],
                sdk_summon_request_path=data["sdk_request_path"],
                sdk_summon_decision_path=data["sdk_decision_path"],
                runtime_result_path=data["runtime_path"],
                reviewed_a2a_return_path=data["a2a_path"],
                runtime_profile_ref=data["runtime_profile_ref"],
                usage_observation_ref=usage_ref,
            )
            self.assertEqual(result["runtime_state"]["usage_observation_ref"], usage_ref)

    def test_cli_loads_usage_ref_as_a_ref_not_an_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            usage_ref = ref(
                "abyss-stack",
                "usage:landing",
                "abyss_stack_external_codex_usage_observation_v1",
            )
            usage_ref_path = root / "usage-ref.json"
            write_json(usage_ref_path, usage_ref)
            profile_ref_path = root / "profile-ref.json"
            write_json(
                profile_ref_path,
                ref(
                    "abyss-stack",
                    "profile:landing",
                    "abyss_stack_external_codex_runtime_profile_v2",
                ),
            )
            output = root / "result.json"
            compiled = {
                "request_ref": "summon-request:landing",
                "request_digest": ZERO,
                "runtime_state": {"state": "accepted"},
                "closeout_handoff": {"next_route": "aoa-agents:review"},
            }
            argv = [
                "--request", str(root / "request.json"),
                "--incarnation-binding", str(root / "incarnation-binding.json"),
                "--sdk-summon-request", str(root / "sdk-request.json"),
                "--sdk-summon-decision", str(root / "sdk-decision.json"),
                "--runtime-result", str(root / "runtime.json"),
                "--reviewed-a2a-return", str(root / "a2a.json"),
                "--runtime-profile-ref", str(profile_ref_path),
                "--usage-observation-ref", str(usage_ref_path),
                "--output", str(output),
            ]
            with mock.patch.object(
                COMPILER,
                "compile_external_execution_result",
                return_value=compiled,
            ) as compile_result, mock.patch.object(COMPILER, "_write"):
                self.assertEqual(COMPILER.main(argv), 0)
            self.assertEqual(
                compile_result.call_args.kwargs["usage_observation_ref"],
                usage_ref,
            )
            self.assertEqual(
                compile_result.call_args.kwargs["incarnation_binding_path"],
                root / "incarnation-binding.json",
            )

    def test_usage_ref_cannot_replace_the_exact_runtime_observation(self) -> None:
        cases = (
            ("object_id", "usage:unrelated"),
            ("digest", "sha256:" + "1" * 64),
        )
        for field, value in cases:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                usage_ref = ref(
                    "abyss-stack",
                    "actor-task-landing#/usage_observation",
                    "abyss_stack_external_codex_usage_observation_v1",
                    COMPILER.digest_bytes(COMPILER.canonical_bytes(data["runtime"]["usage_observation"])),
                )
                usage_ref[field] = value
                with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "differs from the exact runtime observation"):
                    COMPILER.compile_external_execution_result(
                        request_path=data["request_path"],
                        incarnation_binding_path=data["incarnation_binding_path"],
                        sdk_summon_request_path=data["sdk_request_path"],
                        sdk_summon_decision_path=data["sdk_decision_path"],
                        runtime_result_path=data["runtime_path"],
                        reviewed_a2a_return_path=data["a2a_path"],
                        runtime_profile_ref=data["runtime_profile_ref"],
                        usage_observation_ref=usage_ref,
                    )

    def test_usage_status_must_agree_with_gap_presence(self) -> None:
        cases = (
            (
                "complete with gap",
                "complete",
                [
                    {
                        "attempt_id": "attempt:landing",
                        "reason": "controlled_interruption_before_turn_usage",
                        "event_sequence": 4,
                    }
                ],
            ),
            ("partial without gap", "partial", []),
        )
        for name, status, gaps in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                runtime = copy.deepcopy(data["runtime"])
                runtime["usage_observation"] = {
                    "status": status,
                    "gap_reasons": gaps,
                }
                runtime_digest = write_json(data["runtime_path"], runtime)
                a2a = copy.deepcopy(data["a2a"])
                a2a["evidence_digests"]["writer_result"] = runtime_digest
                write_json(data["a2a_path"], a2a)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    "status and gaps contradict",
                ):
                    self.compile(data)

    def test_path_loaded_runtime_profile_requires_v2_schema(self) -> None:
        for name, schema_version in (
            ("wrong schema", "abyss_stack_external_codex_runtime_profile_v1"),
            ("missing schema", None),
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                profile_path = Path(directory) / "runtime-profile.json"
                profile = {"profile_id": "runtime-profile:landing"}
                if schema_version is not None:
                    profile["schema_version"] = schema_version
                write_json(profile_path, profile)
                with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "runtime profile artifact schema"):
                    COMPILER.compile_external_execution_result(
                        request_path=data["request_path"],
                        incarnation_binding_path=data["incarnation_binding_path"],
                        sdk_summon_request_path=data["sdk_request_path"],
                        sdk_summon_decision_path=data["sdk_decision_path"],
                        runtime_result_path=data["runtime_path"],
                        reviewed_a2a_return_path=data["a2a_path"],
                        runtime_profile_path=profile_path,
                    )

    def test_path_loaded_runtime_profile_v2_emits_v2_ref(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            profile_path = Path(directory) / "runtime-profile.json"
            profile_digest = write_json(
                profile_path,
                {
                    "schema_version": "abyss_stack_external_codex_runtime_profile_v2",
                    "profile_id": "runtime-profile:landing-path",
                },
            )
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["tool_profile"]["profile_ref"] = {
                "artifact_ref": "runtime-profile:landing-path",
                "owner_repo": "abyss-stack",
                "schema_version": "abyss_stack_external_codex_runtime_profile_v2",
                "artifact_digest": profile_digest,
            }
            binding["runtime_profile_ref"] = copy.deepcopy(
                binding["tool_profile"]["profile_ref"]
            )
            rewrite_bound_chain(data, incarnation_binding=binding)
            result = COMPILER.compile_external_execution_result(
                request_path=data["request_path"],
                incarnation_binding_path=data["incarnation_binding_path"],
                sdk_summon_request_path=data["sdk_request_path"],
                sdk_summon_decision_path=data["sdk_decision_path"],
                runtime_result_path=data["runtime_path"],
                reviewed_a2a_return_path=data["a2a_path"],
                runtime_profile_path=profile_path,
            )
            self.assertEqual(
                result["binding"]["runtime_profile_ref"],
                {
                    "object_id": "runtime-profile:landing-path",
                    "owner_repo": "abyss-stack",
                    "schema_version": "abyss_stack_external_codex_runtime_profile_v2",
                    "digest": COMPILER.digest_bytes(profile_path.read_bytes()),
                },
            )

    def test_runtime_profile_must_match_the_incarnation_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            data["runtime_profile_ref"] = ref(
                "abyss-stack",
                "runtime-profile:other",
                "abyss_stack_external_codex_runtime_profile_v2",
                "sha256:" + "2" * 64,
            )
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "runtime profile differs from the incarnation binding",
            ):
                self.compile(data)

    def test_runtime_profile_must_match_the_binding_top_level_ref(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["runtime_profile_ref"]["artifact_ref"] = "runtime-profile:other"
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "runtime profile differs from the incarnation binding",
            ):
                self.compile(data)

    def test_unreviewed_a2a_return_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["reviewed"] = False
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "not reviewed"):
                self.compile(data)

    def test_actor_envelope_is_addressed_as_the_exact_derivative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            envelope = {
                "$schema": "schemas/external-codex-actor-input-envelope.schema.json",
                "schema_version": "abyss_stack_external_codex_actor_input_envelope_v1",
                "input_id": "reviewed-a2a-return",
                "payload_kind": "json",
                "source_artifact_digest": ZERO,
                "source_schema_ref": "runtime/schemas/external-codex-a2a-return.schema.json",
                "source_schema_version": "abyss_stack_external_codex_a2a_return_v1",
                "payload": data["a2a"],
            }
            envelope_digest = write_json(data["a2a_path"], envelope)
            result = self.compile(data)
            observed = result["runtime_state"]["runtime_a2a_return_ref"]["digest"]
            self.assertEqual(observed, envelope_digest)
            self.assertNotEqual(observed, envelope["source_artifact_digest"])

    def test_actor_envelope_cannot_substitute_the_payload_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            payload = copy.deepcopy(data["a2a"])
            payload["schema_version"] = "abyss_stack_external_codex_a2a_return_v0"
            envelope = {
                "$schema": "schemas/external-codex-actor-input-envelope.schema.json",
                "schema_version": "abyss_stack_external_codex_actor_input_envelope_v1",
                "input_id": "reviewed-a2a-return",
                "payload_kind": "json",
                "source_artifact_digest": ZERO,
                "source_schema_ref": "runtime/schemas/external-codex-a2a-return.schema.json",
                "source_schema_version": "abyss_stack_external_codex_a2a_return_v1",
                "payload": payload,
            }
            write_json(data["a2a_path"], envelope)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "payload schema/version",
            ):
                self.compile(data)

    def test_reviewed_a2a_schema_version_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["schema_version"] = "abyss_stack_external_codex_a2a_return_v0"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(COMPILER.ExternalExecutionResultError, "schema/version"):
                self.compile(data)

    def test_reviewed_a2a_summon_ref_requires_the_complete_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["summon_request_ref"]["object_id"] = "sdk-request:other"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "another summon request ref",
            ):
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
                    incarnation_binding_path=data["incarnation_binding_path"],
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

    def test_read_only_effect_ceiling_is_admitted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["child_scope"]["allowed_effects"] = ["read_only"]
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["permission_posture"]["allowed_effect_classes"] = ["read_only"]
            rewrite_bound_chain(
                data,
                request=request,
                incarnation_binding=binding,
            )
            result = self.compile(data)
            self.assertEqual(result["runtime_state"]["state"], "accepted")

    def test_request_effect_must_match_the_incarnation_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["child_scope"]["allowed_effects"] = ["read_only"]
            rewrite_bound_chain(data, request=request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "effect posture differs",
            ):
                self.compile(data)

    def test_write_refuses_to_replace_an_existing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            output.write_text("preserve me\n", encoding="utf-8")
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "output must be a new file",
            ):
                COMPILER._write(output, {"replacement": True})
            self.assertEqual(output.read_text(encoding="utf-8"), "preserve me\n")

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
