from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_common():
    path = ROOT / "scripts" / "_recursor_common.py"
    spec = importlib.util.spec_from_file_location("_recursor_common_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RecursorRoleReadinessSeedTest(unittest.TestCase):
    def test_recursor_readiness_build_is_deterministic(self):
        common = load_common()
        first = common.build_readiness_index(ROOT)
        second = common.build_readiness_index(ROOT)
        first.pop("generated_at", None)
        second.pop("generated_at", None)
        self.assertEqual(first, second)
        self.assertEqual(first["boundary"]["status"], "pass")

    def test_witness_cannot_mutate_or_write_scar(self):
        roles = json.loads((ROOT / "config" / "recursor_roles.seed.json").read_text(encoding="utf-8"))
        witness = {role["recursor_id"]: role for role in roles["roles"]}["recursor.witness"]
        forbidden = set(witness["forbidden_actions"])
        self.assertIn("apply_patch", forbidden)
        self.assertIn("write_scar", forbidden)
        self.assertIn("issue_verdict", forbidden)
        self.assertFalse(witness["default_form"]["arena_eligible"])

    def test_executor_requires_approved_plan_and_cannot_self_verify_final(self):
        roles = json.loads((ROOT / "config" / "recursor_roles.seed.json").read_text(encoding="utf-8"))
        executor = {role["recursor_id"]: role for role in roles["roles"]}["recursor.executor"]
        self.assertIn("approved_propagation_plan", executor["allowed_inputs"])
        self.assertIn("execute_without_approved_plan", executor["forbidden_actions"])
        self.assertIn("self_verify_final_truth", executor["forbidden_actions"])

    def test_pair_separation_law(self):
        pair = json.loads((ROOT / "config" / "recursor_pair.seed.json").read_text(encoding="utf-8"))
        required = set(pair["required_separation"])
        self.assertEqual(pair["activation_status"], "readiness_only")
        self.assertIn("witness_cannot_apply_mutations", required)
        self.assertIn("executor_cannot_close_review", required)
        self.assertIn("neither_can_spawn_additional_agents", required)

    def test_projection_candidate_disabled_by_default(self):
        projection = json.loads((ROOT / "config" / "codex_recursor_projection.candidate.json").read_text(encoding="utf-8"))
        self.assertEqual(projection["projection_status"], "candidate_only")
        self.assertFalse(projection["install_by_default"])
        self.assertTrue(projection["requires_owner_review"])
        for agent in projection["candidate_agents"]:
            self.assertEqual(agent["activation_status"], "candidate_only")
            self.assertIn("agent_spawn", agent["forbidden"])
            self.assertIn("arena_session", agent["forbidden"])

    def test_boundary_report_has_no_violations(self):
        common = load_common()
        report = common.build_boundary_report(ROOT)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["violations"], [])
        self.assertIn("no_hidden_scheduler", report["checked_stop_lines"])


if __name__ == "__main__":
    unittest.main()
