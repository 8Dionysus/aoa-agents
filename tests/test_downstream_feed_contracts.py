from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class DownstreamFeedContractsTests(unittest.TestCase):
    def test_expected_downstream_feeds_exist(self) -> None:
        for relative_path in (
            "generated/agent_registry.min.json",
            "generated/model_tier_registry.json",
            "generated/runtime_seam_bindings.json",
        ):
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())

    def test_agent_registry_and_tier_registry_publish_expected_shapes(self) -> None:
        agent_registry = load_json("generated/agent_registry.min.json")
        tier_registry = load_json("generated/model_tier_registry.json")

        self.assertEqual(agent_registry["version"], 1)
        self.assertEqual(agent_registry["layer"], "aoa-agents")
        self.assertEqual(tier_registry["version"], 1)
        self.assertEqual(tier_registry["layer"], "aoa-agents")

        agent_ids = [entry["id"] for entry in agent_registry["agents"]]
        tier_ids = [entry["id"] for entry in tier_registry["model_tiers"]]

        self.assertEqual(len(agent_ids), len(set(agent_ids)))
        self.assertEqual(len(tier_ids), len(set(tier_ids)))

        for entry in agent_registry["agents"]:
            self.assertIn("memory_rights", entry)
            self.assertIn("preferred_skill_families", entry)
            self.assertIn("handoff_rule", entry)

        for entry in tier_registry["model_tiers"]:
            self.assertIn("artifact_requirement", entry)
            self.assertIn("output_contract", entry)
            self.assertIn("handoff_targets", entry)

    def test_runtime_seam_bindings_reference_known_tiers(self) -> None:
        agent_registry = load_json("generated/agent_registry.min.json")
        tier_registry = load_json("generated/model_tier_registry.json")
        seam_bindings = load_json("generated/runtime_seam_bindings.json")

        known_roles = {entry["role"] for entry in agent_registry["agents"]}
        known_runtime_roles = {
            role for role in known_roles
        } | {role.replace("_", "-") for role in known_roles}
        known_tier_ids = {entry["id"] for entry in tier_registry["model_tiers"]}

        self.assertEqual(seam_bindings["version"], 1)
        self.assertEqual(seam_bindings["layer"], "aoa-agents")

        for entry in seam_bindings["bindings"]:
            self.assertIn(entry["tier_id"], known_tier_ids)
            self.assertTrue(set(entry["role_names"]).issubset(known_runtime_roles))
            self.assertIn("artifact_type", entry)


if __name__ == "__main__":
    unittest.main()
