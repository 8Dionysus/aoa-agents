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


if __name__ == "__main__":
    unittest.main()
