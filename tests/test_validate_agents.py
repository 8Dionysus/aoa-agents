from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_agents


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")


def valid_memory_rights() -> dict[str, object]:
    return {
        "default_read_bands": ["core"],
        "default_write_bands": ["hot"],
        "allowed_recall_scopes": ["repo"],
        "promotion_rights": {
            "can_nominate": True,
            "can_confirm": True,
            "can_promote": True,
            "can_demote": False,
            "can_retire": False,
            "can_rescue": False,
            "allowed_transitions": ["hot_to_warm"],
        },
        "freeze_rights": {
            "can_recommend": True,
            "can_prepare": False,
            "can_finalize": False,
        },
    }


def transition_decision_schema() -> dict[str, object]:
    schema = validate_agents.read_json(
        REPO_ROOT / "schemas" / "artifact.transition_decision.schema.json"
    )
    assert isinstance(schema, dict)
    return schema


def valid_transition_return_payload() -> dict[str, object]:
    return {
        "artifact_type": "transition_decision",
        "decision": "return",
        "reason": "Verification detected scope drift and requires bounded re-entry.",
        "next_hop": "planner",
        "anchor_artifact": "bounded_plan",
        "reentry_note": "Re-enter from the last valid bounded plan without widening scope.",
    }


class ValidateAgentsTests(unittest.TestCase):
    def test_validate_memory_rights_rejects_non_string_band_without_typeerror(self) -> None:
        memory_rights = valid_memory_rights()
        memory_rights["default_read_bands"] = [[]]

        with self.assertRaises(validate_agents.ValidationError) as ctx:
            validate_agents.validate_memory_rights("profiles[0]", memory_rights)

        self.assertIn(
            "profiles[0].memory_rights.default_read_bands must contain only strings",
            str(ctx.exception),
        )

    def test_validate_memory_rights_rejects_non_string_allowed_transition_without_typeerror(self) -> None:
        memory_rights = valid_memory_rights()
        promotion_rights = dict(memory_rights["promotion_rights"])
        promotion_rights["allowed_transitions"] = [["hot_to_warm"]]
        memory_rights["promotion_rights"] = promotion_rights

        with self.assertRaises(validate_agents.ValidationError) as ctx:
            validate_agents.validate_memory_rights("profiles[0]", memory_rights)

        self.assertIn(
            "profiles[0].memory_rights.promotion_rights.allowed_transitions must contain only strings",
            str(ctx.exception),
        )

    def test_resolve_aoa_agents_repo_ref_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "aoa-agents"
            repo_root.mkdir()
            (repo_root / "profiles").mkdir()
            (repo_root / "profiles" / "architect.profile.json").write_text("{}", encoding="utf-8")
            (repo_root.parent / "escape.json").write_text("{}", encoding="utf-8")

            with patch.object(validate_agents, "REPO_ROOT", repo_root):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.resolve_aoa_agents_repo_ref("repo:aoa-agents/../escape.json")

        self.assertIn("aoa-agents repo ref must stay inside this repository", str(ctx.exception))

    def test_optional_consumer_smoke_checks_ignore_non_aoa_agents_eval_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            repo_root = temp_root / "aoa-agents"
            evals_root = temp_root / "aoa-evals"

            (repo_root / "docs").mkdir(parents=True)
            (repo_root / "docs" / "AGENT_PROFILE_SURFACE.md").write_text("# Agent Profile\n", encoding="utf-8")

            payload = {
                "artifact_contract_refs": [
                    "repo:aoa-evals/generated/eval_catalog.min.json",
                    "repo:aoa-agents/docs/AGENT_PROFILE_SURFACE.md",
                ]
            }
            write_json(
                evals_root
                / "examples"
                / "artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
                payload,
            )

            with patch.object(validate_agents, "REPO_ROOT", repo_root):
                with patch.dict(
                    os.environ,
                    {
                        "AOA_PLAYBOOKS_ROOT": "",
                        "AOA_EVALS_ROOT": str(evals_root),
                        "AOA_MEMO_ROOT": "",
                        "AOA_ROUTING_ROOT": "",
                    },
                    clear=False,
                ):
                    checked = validate_agents.validate_optional_consumer_smoke_checks({}, {})

        self.assertEqual(checked, ["aoa-evals"])

    def test_transition_decision_schema_accepts_return_with_anchor_and_reentry(self) -> None:
        validate_agents.validate_instance_against_schema(
            valid_transition_return_payload(),
            transition_decision_schema(),
            "transition_decision",
        )

    def test_transition_decision_schema_rejects_return_without_anchor_artifact(self) -> None:
        payload = valid_transition_return_payload()
        del payload["anchor_artifact"]

        with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
            validate_agents.validate_instance_against_schema(
                payload,
                transition_decision_schema(),
                "transition_decision",
            )

        self.assertEqual(ctx.exception.code, "missing_required_field")
        self.assertIn("anchor_artifact", str(ctx.exception))

    def test_transition_decision_schema_rejects_return_without_reentry_note(self) -> None:
        payload = valid_transition_return_payload()
        del payload["reentry_note"]

        with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
            validate_agents.validate_instance_against_schema(
                payload,
                transition_decision_schema(),
                "transition_decision",
            )

        self.assertEqual(ctx.exception.code, "missing_required_field")
        self.assertIn("reentry_note", str(ctx.exception))

    def test_transition_decision_baseline_example_still_validates(self) -> None:
        payload = validate_agents.read_json(
            REPO_ROOT / "examples" / "runtime_artifacts" / "transition_decision.example.json"
        )
        self.assertIsInstance(payload, dict)
        validate_agents.validate_instance_against_schema(
            payload,
            transition_decision_schema(),
            "transition_decision.example",
        )

    def test_validate_runtime_artifact_examples_checks_supplemental_transition_examples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            examples_dir = temp_root / "examples"
            examples_dir.mkdir()
            write_json(
                examples_dir / "transition_decision.example.json",
                {
                    "artifact_type": "transition_decision",
                    "decision": "continue",
                    "reason": "Verification passed and the route can continue safely.",
                    "next_hop": "archivist",
                },
            )
            write_json(
                examples_dir / "transition_decision.return.example.json",
                {
                    "artifact_type": "transition_decision",
                    "decision": "return",
                    "reason": "Scope drift requires bounded re-entry.",
                    "next_hop": "planner",
                },
            )

            with patch.object(validate_agents, "RUNTIME_ARTIFACT_EXAMPLES_DIR", examples_dir):
                with patch.object(
                    validate_agents,
                    "RUNTIME_ARTIFACT_SCHEMA_PATHS",
                    {
                        "transition_decision": REPO_ROOT
                        / "schemas"
                        / "artifact.transition_decision.schema.json"
                    },
                ):
                    with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
                        validate_agents.validate_runtime_artifact_examples()

        self.assertEqual(ctx.exception.code, "missing_required_field")
        self.assertIn("anchor_artifact", str(ctx.exception))

    def test_validate_negative_runtime_artifact_examples_accepts_expanded_fixture_set(self) -> None:
        validate_agents.validate_negative_runtime_artifact_examples()


if __name__ == "__main__":
    unittest.main()
