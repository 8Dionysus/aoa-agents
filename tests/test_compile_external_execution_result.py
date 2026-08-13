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


def ref(
    owner: str, object_id: str, schema_version: str, digest: str = ZERO
) -> dict[str, str]:
    return {
        "object_id": object_id,
        "owner_repo": owner,
        "schema_version": schema_version,
        "digest": digest,
    }


def write_json(path: Path, payload: dict[str, object]) -> str:
    raw = (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode()
        + b"\n"
    )
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
        "execution_surface": "a2a_remote",
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
    role_resolution_ref = ref(
        "aoa-agents", "role-resolution:coder:executor", "aoa_role_resolution_v1"
    )
    model_fit_query_ref = ref(
        "aoa-models", "fit-query:landing", "aoa_model_fit_query_result_v2"
    )
    model_fit_projection_ref = ref(
        "aoa-models", "fit-projection:landing", "aoa_model_fit_projection_v1"
    )
    model_realization_ref = ref(
        "aoa-models",
        "model-realization:landing",
        "aoa_model_realization_v1",
    )
    run_plan_ref = ref(
        "aoa-sdk",
        "run-plan:landing",
        "aoa_control_plane_v1",
    )
    sdk_request_ref = ref(
        "aoa-sdk",
        "sdk-request:landing",
        "urn:aoa-sdk:a2a:summon-request:v4",
        sdk_request_digest,
    )
    sdk_decision_ref = ref(
        "aoa-sdk",
        "sdk-decision:landing",
        "urn:aoa-sdk:a2a:summon-result:v4",
        sdk_decision_digest,
    )
    task_local_dag_ref = ref("aoa-skills", "dag:landing", "aoa-task-local-dag-v2")
    responsibility_transfer_ref = ref(
        "aoa-agents", "transfer:landing", "responsibility-transfer-v1"
    )
    domain_procedure_ref = ref("aoa-agents", "procedure:landing", "owner-procedure-v1")

    def provenance(value: dict[str, str]) -> dict[str, str]:
        return {
            "artifact_ref": value["object_id"],
            "owner_repo": value["owner_repo"],
            "source_ref": "0" * 40,
            "schema_ref": f"schemas/{value['schema_version']}.schema.json",
            "schema_version": value["schema_version"],
            "artifact_digest": value["digest"],
        }

    role_provenance = {
        "owner_repo": "aoa-agents",
        "artifact_ref": "agents/roles/coder/profile.json",
        "source_ref": "0" * 40,
        "artifact_digest": ZERO,
        "schema_ref": "schemas/agent-profile.schema.json",
        "schema_version": "agent_profile_v1",
    }
    obligation = {
        "schema_version": "agent-obligation-v1",
        "obligation_id": "obligation:landing",
        "goal_ref": ref("codex-goal", "goal:landing", "goal-v1"),
        "phase": "execution",
        "duty": "Perform one bounded landing obligation.",
        "domain_owner": "aoa-agents",
        "current_holder": ref("codex-goal", "holder:goal", "holder-v1"),
        "responsibility_boundary": "No commit, push, merge, publication, or owner acceptance.",
        "missed_consequence": "The landing obligation remains unowned.",
        "independence_findings": {
            "positive_signals": ["A separate holder owns the bounded work."],
            "negative_signals": [],
            "rejected_ordinary_step": "The duty carries an independent return.",
        },
        "trigger": {
            "strength": "required_branch",
            "authority_ref": ref("codex-goal", "goal:landing", "goal-v1"),
        },
        "expected_outcomes": ["Return one reviewed external execution result."],
        "return_owner": ref("codex-goal", "holder:goal", "holder-v1"),
        "lifecycle_posture": "task-instance",
        "stop_line": "Stop at owner ambiguity.",
        "evidence_refs": [],
        "uncertainty": [],
        "next_route": "form_actor",
        "obligation_digest": ZERO,
    }
    obligation["obligation_digest"] = COMPILER.semantic_self_digest(
        obligation, "obligation_digest"
    )
    obligation_ref["digest"] = obligation["obligation_digest"]
    obligation_path = temp / "obligation.json"
    write_json(obligation_path, obligation)
    mandate = {
        "schema_version": "actor-mandate-v1",
        "mandate_id": "mandate:landing",
        "obligation_ref": obligation_ref,
        "goal_ref": ref("codex-goal", "goal:landing", "goal-v1"),
        "role_resolution_ref": role_resolution_ref,
        "role_binding": {
            "role_id": "coder",
            "specialization_id": None,
            "tier_id": "executor",
            "base_role_ref": role_provenance,
            "specialization_ref": None,
            "tier_ref": role_provenance,
            "capability_pack_refs": [],
        },
        "identity_posture": "task-instance",
        "domain_owner": "aoa-agents",
        "domain_procedure_refs": [domain_procedure_ref],
        "required_executor_properties": [
            {
                "property_id": "bounded-work",
                "requirement": "Perform bounded work.",
                "verification_route": "Run the owner test.",
            }
        ],
        "model_fit_relation": {
            "task_family": "landing",
            "relation_to_duty": "Fit the bounded landing duty.",
            "relation_authority_ref": ref(
                "codex-goal", "holder:goal", "holder-v1"
            ),
        },
        "authority": {
            "permissions": ["edit workspace"],
            "allowed_effects": ["repo_mutation"],
            "prohibited_effects": ["external effects"],
            "stop_line": "Stop at owner ambiguity.",
        },
        "environment": {
            "sandbox_mode": "workspace-write",
            "workspace_requirement": "Use the exact workspace.",
            "required_tools": ["shell-read"],
            "required_mcp_servers": [],
            "state_root_posture": "Use dedicated state.",
        },
        "continuity": {
            "posture": "task-instance",
            "identity_key": "actor:landing",
            "state_ref": None,
        },
        "named_outputs": [
            {
                "name": "external_codex_agent_result",
                "description": "Exact runtime result.",
                "acceptance_route": "Owner review.",
            }
        ],
        "return_owner": ref("codex-goal", "holder:goal", "holder-v1"),
        "review_policy": "Owner review is required.",
        "refusal_policy": "Refuse at ambiguity.",
        "wake_policy": "Wake for validated completion.",
        "review_after": "Review after return.",
        "uncertainty": [],
        "compiler_authority": {
            "obligation_detection_performed": False,
            "role_selection_performed": False,
            "model_selection_performed": False,
            "runtime_activation_performed": False,
        },
        "mandate_digest": ZERO,
    }
    mandate["mandate_digest"] = COMPILER.semantic_self_digest(mandate, "mandate_digest")
    mandate_ref["digest"] = mandate["mandate_digest"]
    mandate_path = temp / "mandate.json"
    mandate_artifact_digest = write_json(mandate_path, mandate)

    incarnation_binding = {
        "schema_version": "aoa_agent_incarnation_binding_v2",
        "binding_id": "incarnation-binding:landing",
        "incarnation_id": "incarnation:landing",
        "correlation_id": "correlation:landing",
        "causation_id": "causation:landing",
        "trace_id": "trace:landing",
        "run_plan_ref": run_plan_ref,
        "agent_obligation_ref": obligation_ref,
        "actor_mandate_ref": mandate_ref,
        "role_resolution_ref": role_resolution_ref,
        "model_fit_query_result_ref": model_fit_query_ref,
        "model_fit_projection_ref": {
            **provenance(model_fit_projection_ref),
            "schema_ref": "schemas/model-fit-projection.schema.json",
        },
        "model_realization_ref": {
            **provenance(model_realization_ref),
            "source_ref": provenance(model_fit_projection_ref)["source_ref"],
            "schema_ref": "schemas/model-realization.schema.json",
        },
        "task_request_ref": provenance(sdk_request_ref),
        "role_id": "coder",
        "role_contract_ref": {
            **provenance(mandate_ref),
            "artifact_digest": mandate_artifact_digest,
        },
        "runtime_profile_ref": provenance(runtime_profile_ref),
        "workspace_source_ref": provenance(
            ref(
                "task-local-workspace:landing",
                "workspace:landing",
                "task-local-git-workspace-v1",
            )
        ),
        "continuation": {
            "continuation_id": "continuation:landing",
            "exact_child_identity": "incarnation:landing",
            "parent_objective_ref": provenance(task_local_dag_ref),
            "established_decision_refs": [provenance(sdk_decision_ref)],
            "delegated_obligation": "Perform one bounded landing obligation.",
            "delegation_reason": "The goal assigned a separate landing holder.",
            "owner_scope": ["aoa-agents", "aoa-sdk", "abyss-stack"],
            "immutable_input_refs": [
                provenance(sdk_request_ref),
                provenance(model_fit_projection_ref),
                provenance(task_local_dag_ref),
                provenance(responsibility_transfer_ref),
                provenance(domain_procedure_ref),
            ],
            "expected_output": "summon-result-compiler-implementation",
            "validation_refs": [
                provenance(
                    ref(
                        "abyss-stack",
                        "schema:external-report",
                        "abyss_stack_external_codex_report_v1",
                    )
                )
            ],
            "deferred_parent_decisions": ["Accept or reject the return."],
            "invariants": ["Preserve the owner evidence chain."],
            "stop_condition_ids": ["authority-boundary"],
            "wake_condition_ids": ["validated-completion"],
            "return_owner": provenance(ref("codex-goal", "holder:goal", "holder-v1")),
            "rollback_reentry_anchor": provenance(
                ref(
                    "task-local-workspace:landing",
                    "workspace:landing",
                    "task-local-git-workspace-v1",
                )
            ),
        },
        "permission_posture": {
            "sandbox_mode": "workspace_write",
            "approval_policy": "never",
            "allowed_effect_classes": ["repo_mutation"],
            "network_access": "disabled",
            "external_effects": False,
            "secret_access": False,
        },
        "tool_profile": {
            "profile_id": "runtime-profile:landing",
            "profile_ref": {
                **provenance(runtime_profile_ref),
            },
            "required_tool_ids": ["shell-read"],
            "required_mcp_server_ids": [],
            "inherit_user_configuration": False,
        },
        "usage_metering": {
            "metering_regime": "chatgpt_quota",
            "dimensions": [
                "input_tokens",
                "cached_input_tokens",
                "output_tokens",
                "active_wall_seconds",
                "turn_count",
                "output_bytes",
                "executed_commands",
            ],
            "cost_interpretation": "measurement_owner",
            "execution_limit_policy": "none",
            "mode": "observe_only",
        },
        "stop_conditions": [
            {
                "condition_id": "authority-boundary",
                "kind": "authority_boundary",
                "description": "Stop at the authority boundary.",
                "terminal": True,
            }
        ],
        "expected_result_schema_ref": provenance(
            ref(
                "abyss-stack",
                "schema:external-report",
                "abyss_stack_external_codex_report_v1",
            )
        ),
        "wake_policy": {
            "mode": "event_filtered_reentry",
            "default_action": "stop",
            "conditions": [
                {
                    "condition_id": "validated-completion",
                    "event_kind": "result.validated",
                    "action": "wake_parent",
                    "description": "Wake the parent for a validated result.",
                }
            ],
            "escalation_conditions": ["authority-boundary"],
        },
        "binding_digest": ZERO,
        "provenance": {
            "artifact_ref": "incarnation-binding:landing",
            "owner_repo": "aoa-sdk",
            "source_ref": "0" * 40,
            "artifact_digest": ZERO,
            "schema_ref": "schemas/agent-incarnation-binding-v2.schema.json",
            "schema_version": "aoa_control_plane_v1",
        },
    }
    incarnation_binding["binding_digest"] = COMPILER.semantic_excluding_digest(
        incarnation_binding,
        "binding_digest",
    )
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
        "model_realization_ref": model_realization_ref,
        "run_plan_ref": run_plan_ref,
        "task_local_dag_ref": task_local_dag_ref,
        "incarnation_binding_ref": ref(
            "aoa-sdk",
            "incarnation-binding:landing",
            "aoa_agent_incarnation_binding_v2",
            incarnation_binding_digest,
        ),
        "sdk_summon_request_ref": sdk_request_ref,
        "sdk_summon_decision_ref": sdk_decision_ref,
        "runtime_launch_ref": ref(
            "abyss-stack", "launch:landing", "abyss_stack_external_codex_launch_v1"
        ),
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
        "return_event_schema_ref": ref(
            "abyss-stack",
            "schema:external-event",
            "abyss_stack_external_codex_event_v1",
        ),
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
            "allowed_tools": ["shell-read"],
            "allowed_effects": ["repo_mutation"],
            "authority_limit": "No commit, push, merge, publication, or owner acceptance.",
        },
        "child_stop_line": "Stop at owner ambiguity.",
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
                "process_identity_ref": {"artifact_ref": "process-identity:landing"},
            }
        ],
    }
    runtime_path = temp / "runtime-result.json"
    runtime_digest = write_json(runtime_path, runtime)

    reviewed_artifact_path = str(runtime_path.resolve())
    review_outputs = ["independent_execution_review"]
    review_audit_ref = f"abyss-stack:{reviewed_artifact_path}@{runtime_digest}"
    review_request = {
        "audit_refs": [review_audit_ref],
        "expected_outputs": review_outputs,
        "quest_passport": {
            "control_mode": "codex_supervised",
            "delegate_tier": "verifier",
            "difficulty": "d2_slice",
            "expected_artifacts": review_outputs,
            "risk": "r0_readonly",
            "route_anchor": runtime_digest,
        },
        "reviewed_artifact_path": reviewed_artifact_path,
        "summon_request": {
            "audit_refs": [review_audit_ref],
            "child_agent_id": "incarnation:landing:independent-reviewer",
            "desired_role": "reviewer",
            "expected_outputs": review_outputs,
            "parent_task_id": "actor-task-landing",
            "require_progression": False,
            "review_required": False,
            "reviewed_artifact_path": reviewed_artifact_path,
            "session_ref": "session:landing:independent-reviewer",
            "transport_preference": "codex_local",
        },
    }
    review_request_path = temp / "review-summon-request.json"
    review_request_digest = write_json(review_request_path, review_request)

    a2a = {
        "schema_version": "abyss_stack_external_codex_a2a_return_v1",
        "reviewed": True,
        "review_status": "reviewed",
        "reviewer_status": "completed",
        "reviewer_decision": "proceed",
        "review_outcome": "proceed",
        "evidence_digests": {
            "writer_result": runtime_digest,
            "summon_request": sdk_request_digest,
            "review_summon_request": review_request_digest,
        },
        "reviewed_artifact_path": reviewed_artifact_path,
        "summon_request_ref": provenance(incarnation["sdk_summon_request_ref"]),
        "review_summon_request_ref": {
            "artifact_digest": review_request_digest,
            "artifact_ref": "runtime-studies/landing/reviewer/summon-request.json",
            "owner_repo": "abyss-stack",
            "schema_ref": "mechanics/checkpoint/parts/child-task-reentry/schemas/summon-request-v4.schema.json",
            "schema_version": "urn:aoa-sdk:a2a:summon-request:v4",
            "source_ref": runtime_digest,
        },
        "remote_task": {
            "agent_id": "incarnation:landing",
            "context_id": "session:landing-review",
            "parent_task_id": "goal:landing",
            "task_id": "actor-task-landing",
            "state": "completed",
            "artifact_refs": [reviewed_artifact_path],
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
        "obligation": obligation,
        "obligation_path": obligation_path,
        "mandate": mandate,
        "mandate_path": mandate_path,
        "sdk_request": sdk_request,
        "sdk_request_path": sdk_request_path,
        "sdk_decision_path": sdk_decision_path,
        "runtime": runtime,
        "runtime_path": runtime_path,
        "review_request": review_request,
        "review_request_path": review_request_path,
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
        incarnation_binding["binding_digest"] = COMPILER.semantic_excluding_digest(
            incarnation_binding,
            "binding_digest",
        )
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
    review_request = copy.deepcopy(data["review_request"])
    reviewed_path = review_request["reviewed_artifact_path"]
    review_audit_ref = f"abyss-stack:{reviewed_path}@{runtime_digest}"
    review_request["quest_passport"]["route_anchor"] = runtime_digest
    review_request["audit_refs"] = [review_audit_ref]
    review_request["summon_request"]["audit_refs"] = [review_audit_ref]
    review_request_digest = write_json(
        data["review_request_path"], review_request
    )
    a2a = copy.deepcopy(data["a2a"])
    a2a["evidence_digests"]["writer_result"] = runtime_digest
    a2a["evidence_digests"]["review_summon_request"] = review_request_digest
    a2a["review_summon_request_ref"]["artifact_digest"] = review_request_digest
    a2a["review_summon_request_ref"]["source_ref"] = runtime_digest
    write_json(data["a2a_path"], a2a)
    data["request"] = request
    data["runtime"] = runtime
    data["review_request"] = review_request
    data["a2a"] = a2a


def rewrite_mandate_chain(
    data: dict[str, object],
    mandate: dict[str, object],
) -> None:
    mandate["mandate_digest"] = COMPILER.semantic_self_digest(
        mandate,
        "mandate_digest",
    )
    mandate_artifact_digest = write_json(data["mandate_path"], mandate)
    request = copy.deepcopy(data["request"])
    binding = copy.deepcopy(data["incarnation_binding"])
    request["external_incarnation"]["actor_mandate_ref"]["digest"] = mandate[
        "mandate_digest"
    ]
    binding["actor_mandate_ref"]["digest"] = mandate["mandate_digest"]
    binding["role_contract_ref"]["artifact_digest"] = mandate_artifact_digest
    rewrite_bound_chain(
        data,
        request=request,
        incarnation_binding=binding,
    )
    data["mandate"] = mandate


class CompileExternalExecutionResultTests(unittest.TestCase):
    def compile(self, data: dict[str, object]) -> dict[str, object]:
        return COMPILER.compile_external_execution_result(
            request_path=data["request_path"],
            incarnation_binding_path=data["incarnation_binding_path"],
            obligation_path=data["obligation_path"],
            mandate_path=data["mandate_path"],
            sdk_summon_request_path=data["sdk_request_path"],
            sdk_summon_decision_path=data["sdk_decision_path"],
            runtime_result_path=data["runtime_path"],
            reviewed_a2a_return_path=data["a2a_path"],
            review_summon_request_path=data["review_request_path"],
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
            errors = list(
                Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(first)
            )
            self.assertEqual(errors, [])

    def test_usage_is_a_digest_bound_json_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            result = self.compile(data)
            usage_ref = result["runtime_state"]["usage_observation_ref"]
            self.assertEqual(
                usage_ref["object_id"], "actor-task-landing#/usage_observation"
            )
            self.assertEqual(
                usage_ref["digest"],
                COMPILER.digest_bytes(
                    COMPILER.canonical_bytes(data["runtime"]["usage_observation"])
                ),
            )

    def test_request_digest_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["request_digest"] = ZERO
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "request digest mismatch"
            ):
                self.compile(data)

    def test_request_schema_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["untrusted_extra"] = True
            request["request_digest"] = COMPILER.semantic_request_digest(request)
            write_json(data["request_path"], request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "summon-request-v4 schema"
            ):
                self.compile(data)

    def test_sdk_decision_request_identity_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            decision = {
                "schema_version": "urn:aoa-sdk:a2a:summon-result:v4",
                "allowed": True,
                "capability_execution_claimed": False,
                "request_artifact_digest": ZERO,
            }
            write_json(data["sdk_decision_path"], decision)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "SDK summon decision names"
            ):
                self.compile(data)

    def test_sdk_decision_requires_an_explicit_cohort_pattern(self) -> None:
        for name, value in (("missing", None), ("empty", "")):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                decision = copy.deepcopy(
                    json.loads(data["sdk_decision_path"].read_text())
                )
                if value is None:
                    decision.pop("cohort_pattern")
                else:
                    decision["cohort_pattern"] = value
                decision_digest = write_json(data["sdk_decision_path"], decision)
                request = copy.deepcopy(data["request"])
                request["external_incarnation"]["sdk_summon_decision_ref"][
                    "digest"
                ] = decision_digest
                binding = copy.deepcopy(data["incarnation_binding"])
                binding["continuation"]["established_decision_refs"][0][
                    "artifact_digest"
                ] = decision_digest
                rewrite_bound_chain(
                    data,
                    request=request,
                    incarnation_binding=binding,
                )
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    "cohort pattern",
                ):
                    self.compile(data)

    def test_sdk_decision_must_select_the_remote_execution_surface(self) -> None:
        for name, value in (("missing", None), ("local", "codex_local")):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                decision = copy.deepcopy(
                    json.loads(data["sdk_decision_path"].read_text())
                )
                if value is None:
                    decision.pop("execution_surface")
                else:
                    decision["execution_surface"] = value
                decision_digest = write_json(data["sdk_decision_path"], decision)
                request = copy.deepcopy(data["request"])
                request["external_incarnation"]["sdk_summon_decision_ref"][
                    "digest"
                ] = decision_digest
                binding = copy.deepcopy(data["incarnation_binding"])
                binding["continuation"]["established_decision_refs"][0][
                    "artifact_digest"
                ] = decision_digest
                rewrite_bound_chain(
                    data,
                    request=request,
                    incarnation_binding=binding,
                )
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    "does not select the remote execution surface",
                ):
                    self.compile(data)

    def test_review_request_must_bind_the_exact_reviewed_execution(self) -> None:
        cases = (
            ("reviewed path", "reviewed_artifact_path", "/tmp/unrelated-result.json"),
            ("writer task", "parent_task_id", "actor-task-unrelated"),
            ("route anchor", "route_anchor", "sha256:" + "7" * 64),
            ("passport outputs", "expected_artifacts", ["unrelated-review"]),
        )
        for name, field, value in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                review_request = copy.deepcopy(data["review_request"])
                if field == "reviewed_artifact_path":
                    review_request[field] = value
                    review_request["summon_request"][field] = value
                    audit_ref = (
                        f"abyss-stack:{value}@"
                        f"{data['a2a']['evidence_digests']['writer_result']}"
                    )
                    review_request["audit_refs"] = [audit_ref]
                    review_request["summon_request"]["audit_refs"] = [audit_ref]
                elif field == "parent_task_id":
                    review_request["summon_request"][field] = value
                else:
                    review_request["quest_passport"][field] = value
                review_digest = write_json(
                    data["review_request_path"], review_request
                )
                a2a = copy.deepcopy(data["a2a"])
                a2a["review_summon_request_ref"]["artifact_digest"] = review_digest
                a2a["evidence_digests"]["review_summon_request"] = review_digest
                write_json(data["a2a_path"], a2a)
                with self.assertRaises(COMPILER.ExternalExecutionResultError):
                    self.compile(data)

    def test_review_request_ref_must_match_the_supplied_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["review_summon_request_ref"]["artifact_digest"] = ZERO
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "review request digest differs",
            ):
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
            request["external_incarnation"]["sdk_summon_request_ref"]["digest"] = (
                sdk_digest
            )
            request["external_incarnation"]["sdk_summon_decision_ref"]["digest"] = (
                decision_digest
            )
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
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "nonterminal"
            ):
                self.compile(data)

    def test_runtime_result_v1_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["schema_version"] = "abyss_stack_external_codex_result_v1"
            write_json(data["runtime_path"], runtime)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "runtime result schema"
            ):
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
            runtime["owner_admission_ref"]["artifact_ref"] = "summon-request:other"
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
                binding[field][changed_key] = (
                    "different:object"
                    if changed_key == "object_id"
                    else "sha256:" + "1" * 64
                )
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    f"{field} differs from the request",
                ):
                    self.compile(data)

    def test_incarnation_projection_and_task_refs_must_bind_the_exact_request(
        self,
    ) -> None:
        cases = (
            ("model_fit_projection_ref", "artifact_digest"),
            ("task_request_ref", "artifact_ref"),
        )
        for field, changed_key in cases:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                binding[field][changed_key] = (
                    "different:artifact"
                    if changed_key == "artifact_ref"
                    else "sha256:" + "1" * 64
                )
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    f"{field} differs from the request",
                ):
                    self.compile(data)

    def test_incarnation_binding_requires_complete_owner_v2_shape(self) -> None:
        for field in ("model_realization_ref", "run_plan_ref"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                binding.pop(field)
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    "incarnation binding required fields are absent",
                ):
                    self.compile(data)

    def test_incarnation_binding_rejects_nested_owner_v2_shape_drift(self) -> None:
        cases = (
            (
                "incomplete provenance",
                lambda binding: binding["model_realization_ref"].pop("source_ref"),
                "model realization ref required fields are absent",
            ),
            (
                "invalid sandbox",
                lambda binding: binding["permission_posture"].update(
                    {"sandbox_mode": "workspace-write"}
                ),
                "sandbox mode is invalid",
            ),
            (
                "incomplete metering",
                lambda binding: binding["usage_metering"]["dimensions"].pop(),
                "metering dimensions are incomplete",
            ),
            (
                "invalid wake action",
                lambda binding: binding["wake_policy"]["conditions"][0].update(
                    {"action": "continue_unconditionally"}
                ),
                "wake condition 0.action is invalid",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                mutate(binding)
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    message,
                ):
                    self.compile(data)

    def test_incarnation_permission_cross_field_invariants_fail_closed(self) -> None:
        cases = (
            (
                "external effect flag",
                lambda posture: posture.update({"external_effects": True}),
                "external-effects flag differs",
            ),
            (
                "read-only sandbox",
                lambda posture: posture.update({"sandbox_mode": "read_only"}),
                "read-only sandbox admits non-read-only effects",
            ),
            (
                "secret access without approval",
                lambda posture: posture.update({"secret_access": True}),
                "secret access cannot use approval_policy=never",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                mutate(binding["permission_posture"])
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    message,
                ):
                    self.compile(data)

    def test_incarnation_plan_and_realization_refs_bind_the_exact_request(self) -> None:
        cases = (
            ("run_plan_ref", "object_id", "run_plan_ref differs from the request"),
            (
                "model_realization_ref",
                "artifact_ref",
                "model_realization_ref differs from the request",
            ),
        )
        for field, identity_field, message in cases:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                binding[field][identity_field] = f"{field}:other"
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    message,
                ):
                    self.compile(data)

    def test_model_realization_must_share_the_fit_projection_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["model_realization_ref"]["source_ref"] = "1" * 40
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "model realization differs from the fit projection source",
            ):
                self.compile(data)

    def test_incarnation_continuation_child_must_bind_the_exact_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["continuation"]["exact_child_identity"] = "incarnation:other"
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "continuation child identity differs",
            ):
                self.compile(data)

    def test_incarnation_role_contract_must_name_the_request_mandate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["role_contract_ref"]["artifact_ref"] = "mandate:other"
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "role_contract_ref differs from the exact mandate artifact",
            ):
                self.compile(data)

    def test_actor_mandate_semantic_digest_is_verified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            mandate = copy.deepcopy(data["mandate"])
            mandate["review_policy"] = "A different unbound review policy."
            write_json(data["mandate_path"], mandate)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "actor mandate semantic digest mismatch",
            ):
                self.compile(data)

    def test_actor_mandate_must_authorize_the_exact_incarnation_chain(self) -> None:
        cases = (
            (
                "obligation",
                lambda mandate: mandate["obligation_ref"].update(
                    {"object_id": "obligation:other"}
                ),
                "mandate obligation differs",
            ),
            (
                "role resolution",
                lambda mandate: mandate["role_resolution_ref"].update(
                    {"object_id": "role-resolution:other"}
                ),
                "mandate role resolution differs",
            ),
            (
                "role binding",
                lambda mandate: mandate["role_binding"].update({"role_id": "reviewer"}),
                "mandate role binding differs",
            ),
            (
                "domain procedures",
                lambda mandate: mandate["domain_procedure_refs"][0].update(
                    {"object_id": "procedure:other"}
                ),
                "mandate domain procedures differ",
            ),
            (
                "tool ceiling",
                lambda mandate: mandate["environment"]["required_tools"].append(
                    "workspace-write"
                ),
                "mandate tool ceiling differs",
            ),
            (
                "MCP ceiling",
                lambda mandate: mandate["environment"]["required_mcp_servers"].append(
                    "aoa_stats"
                ),
                "mandate MCP ceiling differs",
            ),
            (
                "effect ceiling",
                lambda mandate: mandate["authority"].update(
                    {"allowed_effects": ["read_only"]}
                ),
                "mandate effect ceiling differs",
            ),
            (
                "sandbox ceiling",
                lambda mandate: mandate["environment"].update(
                    {"sandbox_mode": "read-only"}
                ),
                "mandate sandbox differs",
            ),
            (
                "return owner",
                lambda mandate: mandate["return_owner"].update(
                    {"object_id": "holder:other"}
                ),
                "mandate return owner differs",
            ),
            (
                "goal",
                lambda mandate: mandate["goal_ref"].update(
                    {"object_id": "goal:other"}
                ),
                "mandate goal or request route anchor differs",
            ),
            (
                "lifecycle posture",
                lambda mandate: (
                    mandate.update({"identity_posture": "persistent-office"}),
                    mandate["continuity"].update(
                        {"posture": "persistent-office"}
                    ),
                ),
                "mandate lifecycle posture differs",
            ),
            (
                "domain owner",
                lambda mandate: mandate.update({"domain_owner": "aoa-models"}),
                "mandate domain owner differs",
            ),
            (
                "stop line",
                lambda mandate: mandate["authority"].update(
                    {"stop_line": "Continue through owner ambiguity."}
                ),
                "mandate stop line differs from the exact obligation",
            ),
            (
                "model-fit authority",
                lambda mandate: mandate["model_fit_relation"][
                    "relation_authority_ref"
                ].update({"object_id": "holder:other"}),
                "mandate model-fit authority differs",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                mandate = copy.deepcopy(data["mandate"])
                mutate(mandate)
                rewrite_mandate_chain(data, mandate)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    message,
                ):
                    self.compile(data)

    def test_continuation_delegated_duty_must_equal_the_exact_obligation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["continuation"]["delegated_obligation"] = (
                "Perform an unrelated obligation."
            )
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "delegated obligation differs from the exact obligation duty",
            ):
                self.compile(data)

    def test_request_route_anchor_must_retain_the_exact_obligation_goal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["quest_passport"]["route_anchor"] = "goal:other"

            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "mandate goal or request route anchor differs",
            ):
                COMPILER._validate_mandate_chain(
                    data["obligation"],
                    data["mandate"],
                    binding=data["incarnation_binding"],
                    request=request,
                    incarnation=request["external_incarnation"],
                )

    def test_request_tool_scope_must_equal_the_incarnation_ceiling(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["child_scope"]["allowed_tools"].append("workspace-write")
            rewrite_bound_chain(data, request=request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "incarnation tool ceiling differs from the request",
            ):
                self.compile(data)

    def test_transfer_prior_holder_must_equal_the_request_return_owner(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["external_incarnation"]["responsibility_transfer_ref"][
                "holder_ids"
            ][0] = "holder:other"
            rewrite_bound_chain(data, request=request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "responsibility transfer does not return to the request owner",
            ):
                self.compile(data)

    def test_transfer_current_holder_must_equal_the_mandate_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            request = copy.deepcopy(data["request"])
            request["external_incarnation"]["responsibility_transfer_ref"][
                "holder_ids"
            ][1] = "actor:other"
            rewrite_bound_chain(data, request=request)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "current holder differs from the actor mandate identity",
            ):
                self.compile(data)

    def test_request_authority_and_stop_line_bind_exact_owner_sources(self) -> None:
        cases = (
            (
                "authority limit",
                lambda request: request["child_scope"].update(
                    {"authority_limit": "Widened authority."}
                ),
                "authority limit differs from the exact agent obligation",
            ),
            (
                "stop line",
                lambda request: request.update(
                    {"child_stop_line": "Continue through owner ambiguity."}
                ),
                "stop line differs from the exact actor mandate",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                request = copy.deepcopy(data["request"])
                mutate(request)
                rewrite_bound_chain(data, request=request)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    message,
                ):
                    self.compile(data)

    def test_continuation_return_owner_must_retain_the_exact_mandate_holder(
        self,
    ) -> None:
        cases = (
            ("owner", "owner_repo", "aoa-models"),
            ("holder", "artifact_ref", "holder:other"),
            ("digest", "artifact_digest", "sha256:" + "7" * 64),
            ("schema", "schema_version", "other-holder-v1"),
        )
        for name, field, value in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                binding["continuation"]["return_owner"][field] = value
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    "continuation return owner differs from the exact mandate return owner",
                ):
                    self.compile(data)

    def test_role_contract_must_bind_exact_mandate_artifact_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            binding["role_contract_ref"]["artifact_digest"] = "sha256:" + "1" * 64
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "role_contract_ref differs from the exact mandate artifact",
            ):
                self.compile(data)

    def test_incarnation_continuation_must_preserve_request_chain(self) -> None:
        cases = (
            (
                "parent DAG",
                lambda binding: binding["continuation"]["parent_objective_ref"].update(
                    {"artifact_digest": "sha256:" + "1" * 64}
                ),
                "parent objective differs from the request DAG",
            ),
            (
                "SDK decision",
                lambda binding: binding["continuation"][
                    "established_decision_refs"
                ].clear(),
                "exact SDK summon decision",
            ),
            (
                "immutable SDK request",
                lambda binding: binding["continuation"]["immutable_input_refs"].pop(0),
                "exact SDK summon request",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                data = fixture(Path(directory))
                binding = copy.deepcopy(data["incarnation_binding"])
                mutate(binding)
                rewrite_bound_chain(data, incarnation_binding=binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError, message
                ):
                    self.compile(data)

    def test_incarnation_continuation_rejects_stale_same_identity_ref(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            binding = copy.deepcopy(data["incarnation_binding"])
            stale = copy.deepcopy(binding["continuation"]["immutable_input_refs"][0])
            stale["artifact_digest"] = "sha256:" + "1" * 64
            binding["continuation"]["immutable_input_refs"].append(stale)
            rewrite_bound_chain(data, incarnation_binding=binding)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "exact SDK summon request",
            ):
                self.compile(data)

    def test_usage_locator_and_partial_pointer_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "usage pointer"
            ):
                COMPILER.compile_external_execution_result(
                    request_path=data["request_path"],
                    incarnation_binding_path=data["incarnation_binding_path"],
                    obligation_path=data["obligation_path"],
                    mandate_path=data["mandate_path"],
                    sdk_summon_request_path=data["sdk_request_path"],
                    sdk_summon_decision_path=data["sdk_decision_path"],
                    runtime_result_path=data["runtime_path"],
                    reviewed_a2a_return_path=data["a2a_path"],
                    review_summon_request_path=data["review_request_path"],
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
                COMPILER.digest_bytes(
                    COMPILER.canonical_bytes(data["runtime"]["usage_observation"])
                ),
            )
            result = COMPILER.compile_external_execution_result(
                request_path=data["request_path"],
                incarnation_binding_path=data["incarnation_binding_path"],
                obligation_path=data["obligation_path"],
                mandate_path=data["mandate_path"],
                sdk_summon_request_path=data["sdk_request_path"],
                sdk_summon_decision_path=data["sdk_decision_path"],
                runtime_result_path=data["runtime_path"],
                reviewed_a2a_return_path=data["a2a_path"],
                review_summon_request_path=data["review_request_path"],
                runtime_profile_ref=data["runtime_profile_ref"],
                usage_observation_ref=usage_ref,
            )
            self.assertEqual(
                result["runtime_state"]["usage_observation_ref"], usage_ref
            )

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
                "--request",
                str(root / "request.json"),
                "--incarnation-binding",
                str(root / "incarnation-binding.json"),
                "--obligation",
                str(root / "obligation.json"),
                "--mandate",
                str(root / "mandate.json"),
                "--sdk-summon-request",
                str(root / "sdk-request.json"),
                "--sdk-summon-decision",
                str(root / "sdk-decision.json"),
                "--runtime-result",
                str(root / "runtime.json"),
                "--reviewed-a2a-return",
                str(root / "a2a.json"),
                "--review-summon-request",
                str(root / "review-summon-request.json"),
                "--runtime-profile-ref",
                str(profile_ref_path),
                "--usage-observation-ref",
                str(usage_ref_path),
                "--output",
                str(output),
            ]
            with (
                mock.patch.object(
                    COMPILER,
                    "compile_external_execution_result",
                    return_value=compiled,
                ) as compile_result,
                mock.patch.object(COMPILER, "_write"),
            ):
                self.assertEqual(COMPILER.main(argv), 0)
            self.assertEqual(
                compile_result.call_args.kwargs["usage_observation_ref"],
                usage_ref,
            )
            self.assertEqual(
                compile_result.call_args.kwargs["incarnation_binding_path"],
                root / "incarnation-binding.json",
            )
            self.assertEqual(
                compile_result.call_args.kwargs["mandate_path"],
                root / "mandate.json",
            )
            self.assertEqual(
                compile_result.call_args.kwargs["review_summon_request_path"],
                root / "review-summon-request.json",
            )
            self.assertEqual(
                compile_result.call_args.kwargs["obligation_path"],
                root / "obligation.json",
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
                    COMPILER.digest_bytes(
                        COMPILER.canonical_bytes(data["runtime"]["usage_observation"])
                    ),
                )
                usage_ref[field] = value
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    "differs from the exact runtime observation",
                ):
                    COMPILER.compile_external_execution_result(
                        request_path=data["request_path"],
                        incarnation_binding_path=data["incarnation_binding_path"],
                        obligation_path=data["obligation_path"],
                        mandate_path=data["mandate_path"],
                        sdk_summon_request_path=data["sdk_request_path"],
                        sdk_summon_decision_path=data["sdk_decision_path"],
                        runtime_result_path=data["runtime_path"],
                        reviewed_a2a_return_path=data["a2a_path"],
                        review_summon_request_path=data["review_request_path"],
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
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionResultError,
                    "runtime profile artifact schema",
                ):
                    COMPILER.compile_external_execution_result(
                        request_path=data["request_path"],
                        incarnation_binding_path=data["incarnation_binding_path"],
                        obligation_path=data["obligation_path"],
                        mandate_path=data["mandate_path"],
                        sdk_summon_request_path=data["sdk_request_path"],
                        sdk_summon_decision_path=data["sdk_decision_path"],
                        runtime_result_path=data["runtime_path"],
                        reviewed_a2a_return_path=data["a2a_path"],
                        review_summon_request_path=data["review_request_path"],
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
                **binding["tool_profile"]["profile_ref"],
                "artifact_ref": "runtime-profile:landing-path",
                "artifact_digest": profile_digest,
            }
            binding["runtime_profile_ref"] = copy.deepcopy(
                binding["tool_profile"]["profile_ref"]
            )
            rewrite_bound_chain(data, incarnation_binding=binding)
            result = COMPILER.compile_external_execution_result(
                request_path=data["request_path"],
                incarnation_binding_path=data["incarnation_binding_path"],
                obligation_path=data["obligation_path"],
                mandate_path=data["mandate_path"],
                sdk_summon_request_path=data["sdk_request_path"],
                sdk_summon_decision_path=data["sdk_decision_path"],
                runtime_result_path=data["runtime_path"],
                reviewed_a2a_return_path=data["a2a_path"],
                review_summon_request_path=data["review_request_path"],
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
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "not reviewed"
            ):
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

    def test_actor_envelope_requires_a_source_schema_ref(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            envelope = {
                "$schema": "schemas/external-codex-actor-input-envelope.schema.json",
                "schema_version": "abyss_stack_external_codex_actor_input_envelope_v1",
                "input_id": "reviewed-a2a-return",
                "payload_kind": "json",
                "source_artifact_digest": ZERO,
                "source_schema_ref": None,
                "source_schema_version": "abyss_stack_external_codex_a2a_return_v1",
                "payload": data["a2a"],
            }
            write_json(data["a2a_path"], envelope)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "actor envelope has no source schema ref",
            ):
                self.compile(data)

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
                "provenance schema differs from payload schema",
            ):
                self.compile(data)

    def test_schema_less_sdk_request_envelope_uses_expected_owner_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            envelope = {
                "$schema": "schemas/external-codex-actor-input-envelope.schema.json",
                "schema_version": "abyss_stack_external_codex_actor_input_envelope_v1",
                "input_id": "sdk-summon-request",
                "payload_kind": "json",
                "source_artifact_digest": ZERO,
                "source_schema_ref": "mechanics/checkpoint/parts/child-task-reentry/schemas/summon-request-v4.schema.json",
                "source_schema_version": "urn:aoa-sdk:a2a:summon-request:v4",
                "payload": data["sdk_request"],
            }
            sdk_request_digest = write_json(data["sdk_request_path"], envelope)
            sdk_decision = json.loads(data["sdk_decision_path"].read_text())
            sdk_decision["request_artifact_digest"] = sdk_request_digest
            sdk_decision_digest = write_json(data["sdk_decision_path"], sdk_decision)

            binding = copy.deepcopy(data["incarnation_binding"])
            binding["task_request_ref"]["artifact_digest"] = sdk_request_digest
            binding["continuation"]["immutable_input_refs"][0]["artifact_digest"] = (
                sdk_request_digest
            )
            binding["continuation"]["established_decision_refs"][0][
                "artifact_digest"
            ] = sdk_decision_digest
            request = copy.deepcopy(data["request"])
            request["external_incarnation"]["sdk_summon_request_ref"]["digest"] = (
                sdk_request_digest
            )
            request["external_incarnation"]["sdk_summon_decision_ref"]["digest"] = (
                sdk_decision_digest
            )
            a2a = copy.deepcopy(data["a2a"])
            a2a["summon_request_ref"]["artifact_digest"] = sdk_request_digest
            a2a["evidence_digests"]["summon_request"] = sdk_request_digest
            data["a2a"] = a2a
            rewrite_bound_chain(data, request=request, incarnation_binding=binding)

            result = self.compile(data)
            self.assertEqual(result["runtime_state"]["state"], "accepted")

    def test_schema_less_sdk_request_envelope_rejects_wrong_provenance_schema(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            envelope = {
                "$schema": "schemas/external-codex-actor-input-envelope.schema.json",
                "schema_version": "abyss_stack_external_codex_actor_input_envelope_v1",
                "input_id": "sdk-summon-request",
                "payload_kind": "json",
                "source_artifact_digest": ZERO,
                "source_schema_ref": "mechanics/checkpoint/parts/child-task-reentry/schemas/summon-request-v4.schema.json",
                "source_schema_version": "urn:aoa-sdk:a2a:summon-request:v3",
                "payload": data["sdk_request"],
            }
            write_json(data["sdk_request_path"], envelope)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "provenance schema differs from the expected owner schema",
            ):
                self.compile(data)

    def test_reviewed_a2a_schema_version_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["schema_version"] = "abyss_stack_external_codex_a2a_return_v0"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "schema/version"
            ):
                self.compile(data)

    def test_reviewed_a2a_summon_ref_requires_the_complete_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["summon_request_ref"]["artifact_ref"] = "sdk-request:other"
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
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "result.validated"
            ):
                self.compile(data)

    def test_reviewed_a2a_writer_result_must_bind_terminal_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["evidence_digests"]["writer_result"] = ZERO
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "terminal runtime result"
            ):
                self.compile(data)

    def test_reviewed_a2a_remote_task_id_must_bind_terminal_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["task_id"] = "actor-task-unrelated"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "remote task id.*terminal runtime task id",
            ):
                self.compile(data)

    def test_reviewed_a2a_agent_id_must_bind_terminal_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["agent_id"] = "incarnation:unrelated"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError,
                "remote task agent id.*terminal runtime incarnation id",
            ):
                self.compile(data)

    def test_review_disposition_cannot_be_widened(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["review_outcome"] = "return_for_repair"
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "not accepting"
            ):
                self.compile(data)

    def test_output_key_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["returned_artifacts"] = [
                "external_codex_agent_result",
                "unexpected-output",
            ]
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "output keys"
            ):
                self.compile(data)

    def test_extra_returned_artifact_fails_closed_when_requested_outputs_exist(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            a2a = copy.deepcopy(data["a2a"])
            a2a["remote_task"]["returned_artifacts"] = [
                *data["request"]["expected_outputs"],
                "unexpected-output",
            ]
            write_json(data["a2a_path"], a2a)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "outside.*closure"
            ):
                self.compile(data)

    def test_resolving_noncanonical_usage_pointer_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data = fixture(Path(directory))
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "canonical /usage_observation"
            ):
                COMPILER.compile_external_execution_result(
                    request_path=data["request_path"],
                    incarnation_binding_path=data["incarnation_binding_path"],
                    obligation_path=data["obligation_path"],
                    mandate_path=data["mandate_path"],
                    sdk_summon_request_path=data["sdk_request_path"],
                    sdk_summon_decision_path=data["sdk_decision_path"],
                    runtime_result_path=data["runtime_path"],
                    reviewed_a2a_return_path=data["a2a_path"],
                    review_summon_request_path=data["review_request_path"],
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
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "effect ceiling"
            ):
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
            mandate = copy.deepcopy(data["mandate"])
            mandate["authority"]["allowed_effects"] = ["read_only"]
            rewrite_mandate_chain(data, mandate)
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
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "runtime profile ref owner"
            ):
                data["runtime_profile_ref"] = bad_profile
                self.compile(data)

            data = fixture(Path(directory))
            runtime = copy.deepcopy(data["runtime"])
            runtime["codex_invocations"][0]["argv"] = [
                "codex",
                "--enable",
                "multi_agent",
            ]
            write_json(data["runtime_path"], runtime)
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionResultError, "disable built-in"
            ):
                self.compile(data)


if __name__ == "__main__":
    unittest.main()
