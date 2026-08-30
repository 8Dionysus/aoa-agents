from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import ModuleType
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/aoa-summon/scripts/compile_external_execution_request.py"
SPEC = importlib.util.spec_from_file_location("external_request_compiler", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
COMPILER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPILER)


def valid_chain() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    binding = {
        "permission_posture": {
            "sandbox_mode": "workspace_write",
            "approval_policy": "never",
            "allowed_effect_classes": ["repo_mutation"],
            "network_access": "disabled",
            "external_effects": False,
            "secret_access": False,
        }
    }
    runtime_task = {"allowed_effect_class": "repo_mutation"}
    mandate = {"authority": {"allowed_effects": ["repo_mutation"]}}
    return binding, runtime_task, mandate


def valid_tool_chain() -> tuple[dict[str, object], dict[str, object]]:
    profile_ref = {
        "artifact_ref": "runtime-profile:review",
        "owner_repo": "abyss-stack",
        "schema_version": "abyss_stack_external_codex_runtime_profile_v2",
    }
    binding = {
        "runtime_profile_ref": copy.deepcopy(profile_ref),
        "tool_profile": {
            "profile_id": "review-readonly-v2",
            "profile_ref": profile_ref,
            "required_tool_ids": ["shell-read"],
            "required_mcp_server_ids": [],
            "inherit_user_configuration": False,
        },
    }
    mandate = {
        "environment": {
            "required_tools": ["shell-read"],
            "required_mcp_servers": [],
        }
    }
    return binding, mandate


def valid_obligation_mandate_chain() -> tuple[
    dict[str, object], dict[str, object], dict[str, object], dict[str, object]
]:
    goal_ref = {
        "object_id": "goal:exact",
        "owner_repo": "codex-goal",
        "schema_version": "goal-anchor-v1",
        "digest": "sha256:" + "1" * 64,
    }
    obligation = {
        "goal_ref": copy.deepcopy(goal_ref),
        "lifecycle_posture": "task-instance",
        "domain_owner": "aoa-agents",
        "duty": "Perform the exact bounded obligation.",
        "stop_line": "Stop at exact ambiguity.",
        "current_holder": {"object_id": "holder:exact"},
    }
    mandate = {
        "goal_ref": copy.deepcopy(goal_ref),
        "identity_posture": "task-instance",
        "continuity": {"posture": "task-instance"},
        "domain_owner": "aoa-agents",
        "authority": {"stop_line": "Stop at exact ambiguity."},
        "model_fit_relation": {
            "relation_authority_ref": {"object_id": "holder:exact"}
        },
    }
    sdk_request = {"quest_passport": {"route_anchor": "goal:exact"}}
    binding = {
        "continuation": {
            "delegated_obligation": "Perform the exact bounded obligation."
        }
    }
    return obligation, mandate, sdk_request, binding


def valid_sdk_decision() -> tuple[dict[str, object], str]:
    request_digest = "sha256:" + "2" * 64
    return (
        {
            "schema_version": "urn:aoa-sdk:a2a:summon-result:v4",
            "allowed": True,
            "capability_execution_claimed": False,
            "request_artifact_digest": request_digest,
            "execution_surface": "a2a_remote",
            "cohort_pattern": "pair",
        },
        request_digest,
    )


class CompileExternalExecutionRequestTests(unittest.TestCase):
    def test_pinned_schemas_match_checked_out_sdk_owner(self) -> None:
        sdk_root_value = os.environ.get("AOA_SDK_ROOT")
        if not sdk_root_value:
            self.skipTest("AOA_SDK_ROOT is not configured")
        sdk_root = Path(sdk_root_value)
        schema_path = (
            sdk_root
            / "mechanics/boundary-bridge/parts/agent-incarnation-binding"
            / "schemas/agent-incarnation-binding-v2.schema.json"
        )
        schema_raw = schema_path.read_bytes()
        self.assertEqual(
            COMPILER.digest_bytes(schema_raw),
            COMPILER.SDK_BINDING_V2_SCHEMA_DIGEST,
        )
        sdk_package_root = sdk_root / "src" / "aoa_sdk"
        package_name = "aoa_sdk_pin_contract_owner"
        package = ModuleType(package_name)
        package.__path__ = [str(sdk_package_root)]
        contracts_package = ModuleType(f"{package_name}.contracts")
        contracts_package.__path__ = [str(sdk_package_root / "contracts")]
        sys.modules[package_name] = package
        sys.modules[f"{package_name}.contracts"] = contracts_package
        for module_name, module_path in (
            (f"{package_name}.errors", sdk_package_root / "errors.py"),
            (
                f"{package_name}.contracts.control_plane",
                sdk_package_root / "contracts" / "control_plane.py",
            ),
        ):
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            assert spec is not None and spec.loader is not None
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        control_plane = sys.modules[f"{package_name}.contracts.control_plane"]
        run_plan_schema = control_plane.RunPlan.model_json_schema()
        self.assertEqual(
            COMPILER.digest_bytes(COMPILER.canonical_bytes(run_plan_schema)),
            COMPILER.SDK_RUN_PLAN_SCHEMA_DIGEST,
        )

    def test_runtime_subject_chain_must_remain_exact(self) -> None:
        subject = {
            "kind": "content_addressed_runtime_package",
            "source": "codex-cli-standalone/current-package",
            "digest": "sha256:" + "3" * 64,
        }
        query = {"query": {"runtime_subject": copy.deepcopy(subject)}}
        candidate = {"runtime_subject": copy.deepcopy(subject)}
        binding = {"runtime_subject": copy.deepcopy(subject)}

        COMPILER._validate_runtime_subject_chain(query, candidate, binding)
        candidate["runtime_subject"]["digest"] = "sha256:" + "4" * 64
        with self.assertRaisesRegex(
            COMPILER.ExternalExecutionRequestError,
            "runtime subject differs across",
        ):
            COMPILER._validate_runtime_subject_chain(query, candidate, binding)

    def test_run_plan_requires_pinned_full_schema_and_fresh_digests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "run-plan.schema.json"
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "schema_version": {"const": "aoa_control_plane_v1"},
                    "plan_id": {"type": "string", "minLength": 1},
                    "snapshot": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "source_refs": {"type": "array"},
                            "snapshot_digest": {"type": "string"},
                        },
                        "required": ["source_refs", "snapshot_digest"],
                    },
                    "plan_digest": {"type": "string"},
                },
                "required": [
                    "schema_version",
                    "plan_id",
                    "snapshot",
                    "plan_digest",
                ],
            }
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            plan = {
                "schema_version": "aoa_control_plane_v1",
                "plan_id": "run-plan:exact",
                "snapshot": {
                    "source_refs": [{"owner_repo": "aoa-sdk"}],
                    "snapshot_digest": "",
                },
                "plan_digest": "",
            }
            plan["snapshot"]["snapshot_digest"] = (
                COMPILER.sdk_semantic_excluding_digest(
                    plan["snapshot"], "snapshot_digest"
                )
            )
            plan["plan_digest"] = COMPILER.sdk_semantic_excluding_digest(
                plan, "plan_digest"
            )

            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionRequestError,
                "differs from the pinned owner contract",
            ):
                COMPILER._validate_sdk_run_plan_artifact(
                    plan,
                    schema_path=schema_path,
                )

            pinned_digest = COMPILER.digest_bytes(COMPILER.canonical_bytes(schema))
            with mock.patch.object(
                COMPILER,
                "SDK_RUN_PLAN_SCHEMA_DIGEST",
                pinned_digest,
            ):
                COMPILER._validate_sdk_run_plan_artifact(
                    plan,
                    schema_path=schema_path,
                )
                stale = copy.deepcopy(plan)
                stale["snapshot"]["source_refs"].append(
                    {"owner_repo": "different-owner"}
                )
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionRequestError,
                    "snapshot semantic digest mismatch",
                ):
                    COMPILER._validate_sdk_run_plan_artifact(
                        stale,
                        schema_path=schema_path,
                    )

    def test_incarnation_binding_requires_full_sdk_shape_and_fresh_digest(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            schema_path = Path(directory) / "binding-v2.schema.json"
            schema_path.write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "$id": "urn:aoa-sdk:agent-incarnation-binding:v2",
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "schema_version": {
                                "const": "aoa_agent_incarnation_binding_v2"
                            },
                            "binding_digest": {"type": "string"},
                            "wake_policy": {"type": "object"},
                            "stop_conditions": {
                                "type": "array",
                                "minItems": 1,
                            },
                        },
                        "required": [
                            "schema_version",
                            "binding_digest",
                            "wake_policy",
                            "stop_conditions",
                        ],
                    }
                )
            )
            binding = {
                "schema_version": "aoa_agent_incarnation_binding_v2",
                "binding_digest": "",
                "wake_policy": {},
                "stop_conditions": ["stop"],
            }
            binding["binding_digest"] = COMPILER.sdk_semantic_excluding_digest(
                binding,
                "binding_digest",
            )
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionRequestError,
                "differs from the pinned SDK v2 owner contract",
            ):
                COMPILER._validate_incarnation_binding_artifact(
                    binding,
                    schema_path=schema_path,
                )

            stale = copy.deepcopy(binding)
            stale["wake_policy"]["default_action"] = "wake"
            with self.assertRaisesRegex(
                COMPILER.ExternalExecutionRequestError,
                "semantic digest mismatch",
            ):
                COMPILER._validate_incarnation_binding_semantic_digest(stale)

    def test_valid_obligation_goal_and_lifecycle_are_preserved_before_launch(
        self,
    ) -> None:
        COMPILER._validate_obligation_mandate_chain(
            *valid_obligation_mandate_chain()
        )

    def test_obligation_goal_and_lifecycle_substitutions_fail_before_launch(
        self,
    ) -> None:
        cases = (
            (
                "mandate goal",
                lambda obligation, mandate, sdk_request, binding: mandate[
                    "goal_ref"
                ].update({"object_id": "goal:other"}),
                "mandate goal and originating obligation goal differs",
            ),
            (
                "request route anchor",
                lambda obligation, mandate, sdk_request, binding: sdk_request[
                    "quest_passport"
                ].update({"route_anchor": "goal:other"}),
                "SDK route anchor and originating obligation goal differs",
            ),
            (
                "mandate identity posture",
                lambda obligation, mandate, sdk_request, binding: mandate.update(
                    {"identity_posture": "persistent-office"}
                ),
                "mandate identity and obligation lifecycle posture differs",
            ),
            (
                "mandate continuity posture",
                lambda obligation, mandate, sdk_request, binding: mandate[
                    "continuity"
                ].update({"posture": "persistent-office"}),
                "mandate continuity and obligation lifecycle posture differs",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name):
                obligation, mandate, sdk_request, binding = (
                    valid_obligation_mandate_chain()
                )
                mutate(obligation, mandate, sdk_request, binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionRequestError,
                    message,
                ):
                    COMPILER._validate_obligation_mandate_chain(
                        obligation, mandate, sdk_request, binding
                    )

    def test_domain_owner_and_delegated_duty_substitutions_fail_before_launch(
        self,
    ) -> None:
        cases = (
            (
                "domain owner",
                lambda obligation, mandate, sdk_request, binding: mandate.update(
                    {"domain_owner": "aoa-models"}
                ),
                "mandate and obligation domain owner differs",
            ),
            (
                "delegated duty",
                lambda obligation, mandate, sdk_request, binding: binding[
                    "continuation"
                ].update({"delegated_obligation": "Perform another duty."}),
                "delegated and originating obligation duty differs",
            ),
            (
                "stop line",
                lambda obligation, mandate, sdk_request, binding: mandate[
                    "authority"
                ].update({"stop_line": "Continue through ambiguity."}),
                "mandate and obligation stop line differs",
            ),
            (
                "model-fit authority",
                lambda obligation, mandate, sdk_request, binding: mandate[
                    "model_fit_relation"
                ].update(
                    {"relation_authority_ref": {"object_id": "holder:other"}}
                ),
                "model-fit relation authority and current obligation holder differs",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name):
                obligation, mandate, sdk_request, binding = (
                    valid_obligation_mandate_chain()
                )
                mutate(obligation, mandate, sdk_request, binding)
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionRequestError,
                    message,
                ):
                    COMPILER._validate_obligation_mandate_chain(
                        obligation, mandate, sdk_request, binding
                    )

    def test_sdk_decision_must_select_remote_surface_before_launch(self) -> None:
        decision, request_digest = valid_sdk_decision()
        COMPILER._validate_sdk_decision(
            decision,
            sdk_request_digest=request_digest,
        )
        for value in (None, "codex_local"):
            with self.subTest(value=value):
                candidate = copy.deepcopy(decision)
                if value is None:
                    candidate.pop("execution_surface")
                else:
                    candidate["execution_surface"] = value
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionRequestError,
                    "does not select the remote execution surface",
                ):
                    COMPILER._validate_sdk_decision(
                        candidate,
                        sdk_request_digest=request_digest,
                    )

    def test_valid_permission_posture_binds_both_owner_effect_ceilings(self) -> None:
        COMPILER._validate_permission_posture(*valid_chain())

    def test_permission_cross_field_invariants_fail_closed(self) -> None:
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
            with self.subTest(name=name):
                binding, runtime_task, mandate = valid_chain()
                posture = copy.deepcopy(binding["permission_posture"])
                mutate(posture)
                binding["permission_posture"] = posture
                with self.assertRaisesRegex(
                    COMPILER.ExternalExecutionRequestError,
                    message,
                ):
                    COMPILER._validate_permission_posture(
                        binding, runtime_task, mandate
                    )

    def test_runtime_task_effect_must_match_permission_posture(self) -> None:
        binding, runtime_task, mandate = valid_chain()
        runtime_task["allowed_effect_class"] = "read_only"
        with self.assertRaisesRegex(
            COMPILER.ExternalExecutionRequestError,
            "differs from runtime task or actor mandate",
        ):
            COMPILER._validate_permission_posture(binding, runtime_task, mandate)

    def test_actor_mandate_effect_must_match_permission_posture(self) -> None:
        binding, runtime_task, mandate = valid_chain()
        mandate["authority"]["allowed_effects"] = ["read_only"]
        with self.assertRaisesRegex(
            COMPILER.ExternalExecutionRequestError,
            "differs from runtime task or actor mandate",
        ):
            COMPILER._validate_permission_posture(binding, runtime_task, mandate)

    def test_valid_tool_profile_binds_actor_mandate_before_launch(self) -> None:
        COMPILER._validate_tool_profile(*valid_tool_chain())

    def test_tool_profile_cannot_widen_actor_mandate(self) -> None:
        binding, mandate = valid_tool_chain()
        binding["tool_profile"]["required_tool_ids"].append("network")
        with self.assertRaisesRegex(
            COMPILER.ExternalExecutionRequestError,
            "tool ceiling differs from actor mandate",
        ):
            COMPILER._validate_tool_profile(binding, mandate)

    def test_mcp_profile_cannot_widen_actor_mandate(self) -> None:
        binding, mandate = valid_tool_chain()
        binding["tool_profile"]["required_mcp_server_ids"].append("github")
        with self.assertRaisesRegex(
            COMPILER.ExternalExecutionRequestError,
            "MCP ceiling differs from actor mandate",
        ):
            COMPILER._validate_tool_profile(binding, mandate)

    def test_tool_profile_must_name_the_bound_runtime_profile(self) -> None:
        binding, mandate = valid_tool_chain()
        binding["runtime_profile_ref"]["artifact_ref"] = "runtime-profile:other"
        with self.assertRaisesRegex(
            COMPILER.ExternalExecutionRequestError,
            "tool profile ref differs from runtime profile ref",
        ):
            COMPILER._validate_tool_profile(binding, mandate)

    def test_tool_profile_cannot_inherit_user_configuration(self) -> None:
        binding, mandate = valid_tool_chain()
        binding["tool_profile"]["inherit_user_configuration"] = True
        with self.assertRaisesRegex(
            COMPILER.ExternalExecutionRequestError,
            "cannot inherit user configuration",
        ):
            COMPILER._validate_tool_profile(binding, mandate)


if __name__ == "__main__":
    unittest.main()
