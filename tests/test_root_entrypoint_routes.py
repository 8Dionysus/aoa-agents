from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROADMAP_LINK = "[ROADMAP.md](ROADMAP.md)"
NON_AGENTS_VALIDATION_SURFACES = (
    "README.md",
    "DESIGN.AGENTS.md",
    "docs/CURRENT_CONTOUR.md",
    "docs/decisions/AOA-AG-D-0058-root-document-entry-contour-refactor.md",
)


class RootEntrypointRoutesTestCase(unittest.TestCase):
    def test_root_entrypoints_route_to_roadmap(self) -> None:
        roadmap_path = REPO_ROOT / "ROADMAP.md"
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertTrue(roadmap_path.is_file())
        self.assertIn(ROADMAP_LINK, readme)
        self.assertIn(ROADMAP_LINK, agents)

    def test_validation_commands_live_in_on_demand_map(self) -> None:
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        validation = (REPO_ROOT / "VALIDATION.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/validate_semantic_agents.py", validation)
        self.assertIn("python scripts/validate_agents.py", validation)
        self.assertNotIn("```", agents)

        for relative_path in NON_AGENTS_VALIDATION_SURFACES:
            with self.subTest(path=relative_path):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                self.assertNotIn("```bash\npython ", text)
                self.assertNotIn("```sh\npython ", text)
                self.assertNotIn("python scripts/validate_", text)
                self.assertNotIn("python -m pytest", text)

    def test_agents_cards_have_no_fenced_command_blocks(self) -> None:
        for relative_path in REPO_ROOT.glob("**/AGENTS.md"):
            with self.subTest(path=relative_path):
                self.assertNotIn("```", relative_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
