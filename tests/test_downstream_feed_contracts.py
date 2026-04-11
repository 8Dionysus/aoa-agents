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
            "generated/codex_agents/config.subagents.generated.toml",
            "generated/codex_agents/projection_manifest.json",
            "generated/codex_agents/agents/architect.toml",
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

        known_runtime_roles = {entry["name"] for entry in agent_registry["agents"]}
        known_tier_ids = {entry["id"] for entry in tier_registry["model_tiers"]}

        self.assertEqual(seam_bindings["version"], 1)
        self.assertEqual(seam_bindings["layer"], "aoa-agents")

        for entry in seam_bindings["bindings"]:
            self.assertIn(entry["tier_id"], known_tier_ids)
            self.assertTrue(set(entry["role_names"]).issubset(known_runtime_roles))
            self.assertIn("artifact_type", entry)

    def test_workspace_surface_trigger_posture_is_linked_and_bounded(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        posture = (REPO_ROOT / "docs" / "WORKSPACE_SURFACE_TRIGGER_POSTURE.md").read_text(
            encoding="utf-8"
        )
        seams = (REPO_ROOT / "docs" / "FEDERATION_CONSUMER_SEAMS.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/WORKSPACE_SURFACE_TRIGGER_POSTURE.md", readme)
        self.assertIn("WORKSPACE_SURFACE_TRIGGER_POSTURE", docs_readme)

        for token in (
            "`aoa surfaces detect` is additive and read-only.",
            "`aoa-skills` remains the only immediate activation lane in this slice.",
            "route drift",
            "owner-layer ambiguity",
            "proof need",
            "recall need",
            "role posture pressure",
            "recurring scenario pressure",
            "aoa surfaces detect <repo_root> --root /srv",
        ):
            self.assertIn(token, posture)

        self.assertIn("### `aoa-sdk`", seams)
        self.assertIn("trigger posture", seams)

    def test_codex_subagent_projection_matches_active_agent_names(self) -> None:
        agent_registry = load_json("generated/agent_registry.min.json")
        projection_manifest = load_json("generated/codex_agents/projection_manifest.json")

        active_names = {
            entry["name"] for entry in agent_registry["agents"] if entry["status"] == "active"
        }
        projected_names = {entry["name"] for entry in projection_manifest["generated_agents"]}

        self.assertEqual(active_names, projected_names)


if __name__ == "__main__":
    unittest.main()
