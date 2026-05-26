from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "validate_agent_source_home.py"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_agent_source_home", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AgentSourceHomeTests(unittest.TestCase):
    def test_current_agent_source_home_validates(self) -> None:
        module = load_validator_module()
        self.assertEqual(module.validate_manifest(REPO_ROOT), [])

    def test_manifest_covers_expected_source_families(self) -> None:
        manifest = json.loads((REPO_ROOT / "agents" / "source_home.manifest.json").read_text(encoding="utf-8"))
        family_ids = {family["id"] for family in manifest["families"]}
        self.assertEqual(
            family_ids,
            {
                "base_profiles",
                "profile_adjuncts",
                "model_tiers",
                "orchestrator_classes",
                "cohort_patterns",
                "runtime_seam_bindings",
            },
        )

    def test_source_home_has_convex_branches(self) -> None:
        manifest = json.loads((REPO_ROOT / "agents" / "source_home.manifest.json").read_text(encoding="utf-8"))
        branch_ids = {branch["id"] for branch in manifest["branches"]}
        self.assertEqual(branch_ids, {"role_houses", "operating_model"})
        self.assertTrue((REPO_ROOT / "agents" / "roles" / "AGENTS.md").is_file())
        self.assertTrue((REPO_ROOT / "agents" / "operating-model" / "AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
