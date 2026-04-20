from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_matches_current_v0_2_release_surfaces(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        subject_prep = (REPO_ROOT / "docs" / "AGENT_SUBJECT_PREP.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("v0.2.2", readme)
        self.assertIn("[0.2.2]", changelog)
        self.assertIn("v0.2.x", roadmap)

        for relative_path in (
            "docs/CODEX_SUBAGENT_PROJECTION.md",
            "docs/CODEX_SUBAGENT_REFRESH_LAW.md",
            "config/codex_subagent_wiring.v2.json",
            "generated/runtime_seam_bindings.json",
            "docs/AGENT_STRESS_POSTURE.md",
            "docs/AGENT_STRESS_HANDOFFS.md",
            "docs/QUEST_EXECUTION_PASSPORT.md",
            "generated/quest_catalog.min.json",
            "generated/quest_dispatch.min.json",
            "generated/alpha_reference_routes.min.json",
            "generated/codex_agents/config.subagents.generated.toml",
            "docs/WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md",
            "docs/AGENT_SUBJECT_PREP.md",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)

        self.assertIn("Codex subagent projection", changelog)
        self.assertIn("self-agency continuity posture", changelog)
        self.assertIn("agonic/assistant kind split", roadmap)
        self.assertIn("civil/service", subject_prep)
        self.assertIn("This note does not land any seed pack", subject_prep)
        self.assertIn("future additive adjunct", subject_prep)
        self.assertIn("roadmap drift", roadmap)


if __name__ == "__main__":
    unittest.main()
