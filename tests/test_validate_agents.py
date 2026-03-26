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


if __name__ == "__main__":
    unittest.main()
