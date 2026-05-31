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

    def test_validation_command_blocks_live_in_agents_surfaces(self) -> None:
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("```bash\npython scripts/validate_semantic_agents.py", agents)
        self.assertIn("python scripts/validate_agents.py", agents)

        for relative_path in NON_AGENTS_VALIDATION_SURFACES:
            with self.subTest(path=relative_path):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                self.assertNotIn("```bash\npython ", text)
                self.assertNotIn("```sh\npython ", text)
                self.assertNotIn("python scripts/validate_", text)
                self.assertNotIn("python -m pytest", text)


if __name__ == "__main__":
    unittest.main()
