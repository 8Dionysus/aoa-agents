from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


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


class CompileExternalExecutionRequestTests(unittest.TestCase):
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
