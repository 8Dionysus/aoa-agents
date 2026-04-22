from __future__ import annotations

import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_common():
    path = ROOT / "scripts" / "_recursor_common.py"
    spec = importlib.util.spec_from_file_location("_recursor_common_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def schema_validator(relative: str) -> Draft202012Validator:
    schema = load_json(relative)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


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
        self.assertEqual(
            {agent["recursor_id"] for agent in projection["candidate_agents"]},
            {"recursor.witness", "recursor.executor"},
        )
        for agent in projection["candidate_agents"]:
            self.assertEqual(agent["activation_status"], "candidate_only")
            self.assertIn("agent_spawn", agent["forbidden"])
            self.assertIn("arena_session", agent["forbidden"])
            self.assertIn("rank_mutation", agent["forbidden"])
            self.assertIn("no_agonic_runtime_claim", agent["activation_requires"])

    def test_boundary_report_has_no_violations(self):
        common = load_common()
        report = common.build_boundary_report(ROOT)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["violations"], [])
        self.assertIn("no_hidden_scheduler", report["checked_stop_lines"])

    def test_projection_rejects_unexpected_candidate_role(self):
        common = load_common()
        projection = json.loads((ROOT / "config" / "codex_recursor_projection.candidate.json").read_text(encoding="utf-8"))
        projection["candidate_agents"].append(
            {
                "recursor_id": "recursor.admin",
                "activation_status": "candidate_only",
                "activation_requires": [
                    "explicit_main_codex_call",
                    "no_agonic_runtime_claim",
                ],
                "forbidden": [
                    "agent_spawn",
                    "arena_session",
                    "verdict",
                    "scar_write",
                    "rank_mutation",
                    "hidden_scheduler",
                ],
            }
        )
        errors = common.validate_projection_candidate(projection)
        self.assertTrue(any(error["kind"] == "unexpected_projection_agent" for error in errors))

    def test_projection_requires_full_forbidden_tokens(self):
        common = load_common()
        projection = json.loads((ROOT / "config" / "codex_recursor_projection.candidate.json").read_text(encoding="utf-8"))
        broken = deepcopy(projection)
        for agent in broken["candidate_agents"]:
            if agent["recursor_id"] == "recursor.executor":
                agent["forbidden"].remove("rank_mutation")
                agent["forbidden"].remove("self_verify_as_final")
        errors = common.validate_projection_candidate(broken)
        messages = " ".join(error["message"] for error in errors)
        self.assertIn("rank_mutation", messages)
        self.assertIn("self_verify_as_final", messages)

    def test_readiness_rejects_missing_recursor_role(self):
        common = load_common()
        roles = load_json("config/recursor_roles.seed.json")
        broken = deepcopy(roles)
        broken["roles"] = [
            role for role in broken["roles"] if role["recursor_id"] != "recursor.executor"
        ]
        errors = common.validate_role_set(broken)
        self.assertTrue(any(error["kind"] == "missing_recursor_role" for error in errors))
        self.assertTrue(any(error["kind"] == "invalid_recursor_role_count" for error in errors))

    def test_readiness_rejects_unexpected_recursor_role(self):
        common = load_common()
        roles = load_json("config/recursor_roles.seed.json")
        broken = deepcopy(roles)
        extra = deepcopy(broken["roles"][0])
        extra["recursor_id"] = "recursor.admin"
        broken["roles"].append(extra)
        errors = common.validate_role_set(broken)
        self.assertTrue(any(error["kind"] == "unexpected_recursor_role" for error in errors))
        self.assertTrue(any(error["kind"] == "invalid_recursor_role_count" for error in errors))

    def test_published_schemas_accept_seed_sources(self):
        projection_validator = schema_validator(
            "schemas/recursor-projection-candidate.v1.schema.json"
        )
        role_validator = schema_validator("schemas/recursor-role-contract.v1.schema.json")
        pair_validator = schema_validator("schemas/recursor-pair-contract.v1.schema.json")
        projection_validator.validate(load_json("config/codex_recursor_projection.candidate.json"))
        pair_validator.validate(load_json("config/recursor_pair.seed.json"))
        for role in load_json("config/recursor_roles.seed.json")["roles"]:
            role_validator.validate(role)

    def test_projection_schema_rejects_unexpected_candidate_role(self):
        validator = schema_validator("schemas/recursor-projection-candidate.v1.schema.json")
        projection = load_json("config/codex_recursor_projection.candidate.json")
        broken = deepcopy(projection)
        broken["candidate_agents"].append(
            {
                "recursor_id": "recursor.admin",
                "activation_status": "candidate_only",
                "activation_requires": [
                    "explicit_main_codex_call",
                    "no_agonic_runtime_claim",
                ],
                "forbidden": [
                    "agent_spawn",
                    "arena_session",
                    "verdict",
                    "scar_write",
                    "rank_mutation",
                    "hidden_scheduler",
                ],
            }
        )
        self.assertTrue(list(validator.iter_errors(broken)))

    def test_projection_schema_rejects_missing_required_guards(self):
        validator = schema_validator("schemas/recursor-projection-candidate.v1.schema.json")
        projection = load_json("config/codex_recursor_projection.candidate.json")
        broken = deepcopy(projection)
        for agent in broken["candidate_agents"]:
            if agent["recursor_id"] == "recursor.witness":
                agent["activation_requires"].remove("no_agonic_runtime_claim")
            if agent["recursor_id"] == "recursor.executor":
                agent["forbidden"].remove("rank_mutation")
                agent["forbidden"].remove("self_verify_as_final")
        self.assertTrue(list(validator.iter_errors(broken)))

    def test_pair_schema_rejects_missing_required_boundary_tokens(self):
        validator = schema_validator("schemas/recursor-pair-contract.v1.schema.json")
        pair = load_json("config/recursor_pair.seed.json")
        broken = deepcopy(pair)
        broken["required_separation"].remove("executor_cannot_close_review")
        broken["handoff_order"].remove("witness_trace_check")
        self.assertTrue(list(validator.iter_errors(broken)))


if __name__ == "__main__":
    unittest.main()
