from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = ROOT / "mechanics" / "agon" / "parts" / "formation" / "scripts"


def load_builder():
    path = SCRIPT_DIR / "build_agent_formation_trial.py"
    spec = importlib.util.spec_from_file_location("agent_formation_trial_builder_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentFormationTrialTestCase(unittest.TestCase):
    def test_formation_trial_generated_surface_is_current(self) -> None:
        builder = load_builder()
        expected = builder.build_index(ROOT)
        actual = json.loads((ROOT / builder.OUTPUT).read_text(encoding="utf-8"))
        self.assertEqual(actual, expected)
        self.assertEqual(actual["global_verdict"], "pass_pre_protocol_formation_trial")
        self.assertEqual(actual["readiness_summary"]["split_form_survivors"], 5)

    def test_formation_trial_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "validate_agent_formation_trial.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_role_verdict_rejects_assistant_scar_or_tos_authority(self) -> None:
        builder = load_builder()
        actor = {"readiness": {"agonic_actor_ready": True}}
        assistant = {
            "kind": "assistant",
            "contestant_eligible": False,
            "judge_eligible": False,
            "closer_eligible": False,
            "summon_initiator_eligible": False,
            "scar_writer_eligible": True,
            "tos_promotion_eligible": False,
        }
        self.assertEqual(builder.role_verdict(actor, assistant), "partial_recharter_required")

        assistant["scar_writer_eligible"] = False
        assistant["tos_promotion_eligible"] = True
        self.assertEqual(builder.role_verdict(actor, assistant), "partial_recharter_required")

    def test_global_trial_verdict_escalates_quarantine_to_fail(self) -> None:
        builder = load_builder()
        self.assertEqual(
            builder.global_trial_verdict([{"verdict": "quarantine_from_agon"}], passed=False),
            "fail_quarantine_from_agon",
        )
        self.assertEqual(
            builder.global_trial_verdict([{"verdict": "partial_recharter_required"}], passed=False),
            "partial_recharter_required",
        )
        self.assertEqual(
            builder.global_trial_verdict([{"verdict": "survive_with_split_forms"}], passed=True),
            "pass_pre_protocol_formation_trial",
        )


if __name__ == "__main__":
    unittest.main()
