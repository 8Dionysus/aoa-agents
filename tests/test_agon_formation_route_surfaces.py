from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class AgonFormationRouteSurfacesTestCase(unittest.TestCase):
    def test_docs_map_and_contour_route_agon_formation_surfaces(self) -> None:
        readme = read_text("README.md")
        docs_readme = read_text("docs/README.md")
        contour = read_text("docs/CURRENT_CONTOUR.md")

        self.assertIn("docs/CURRENT_CONTOUR.md", readme)
        self.assertIn("mechanics/agon/parts/formation/docs/actor-rechartering.md", contour)
        self.assertIn("generated/agent_agonic_formation_index.min.json", contour)
        self.assertIn("mechanics/agon/AGENTS.md", contour)
        self.assertIn("Agonic Actor Rechartering", docs_readme)
        self.assertIn("Agent Kind Model", docs_readme)
        self.assertIn("Agent Resistance and Revision Posture", docs_readme)

    def test_local_guides_name_agon_formation_companion_surfaces(self) -> None:
        profiles_agents = read_text("agents/roles/AGENTS.md")
        generated_readme = read_text("generated/README.md")
        examples_readme = read_text("examples/README.md")
        validation = read_text("VALIDATION.md")

        self.assertIn("agents/roles/*/forms/", profiles_agents)
        self.assertIn("generated/agent_agonic_formation_index.min.json", generated_readme)
        self.assertIn("mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py", generated_readme)
        self.assertIn("mechanics/agon/parts/formation/examples/", examples_readme)
        self.assertIn("validate_agent_agonic_formation.py", validation)


if __name__ == "__main__":
    unittest.main()
