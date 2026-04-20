from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class Wave1RouteSurfacesTestCase(unittest.TestCase):
    def test_readme_and_docs_map_route_wave1_surfaces(self) -> None:
        readme = read_text("README.md")
        docs_readme = read_text("docs/README.md")

        self.assertIn("docs/AGONIC_ACTOR_RECHARTERING.md", readme)
        self.assertIn("generated/agent_agonic_formation_index.min.json", readme)
        self.assertIn("python scripts/validate_agent_agonic_formation.py", readme)
        self.assertIn("AGONIC_ACTOR_RECHARTERING", docs_readme)
        self.assertIn("AGENT_KIND_MODEL", docs_readme)
        self.assertIn("AGENT_RESISTANCE_REVISION_POSTURE", docs_readme)

    def test_local_guides_name_wave1_companion_surfaces(self) -> None:
        profiles_agents = read_text("profiles/AGENTS.md")
        generated_agents = read_text("generated/AGENTS.md")
        examples_agents = read_text("examples/AGENTS.md")

        self.assertIn("profiles/adjuncts/*", profiles_agents)
        self.assertIn("generated/agent_agonic_formation_index.min.json", profiles_agents)
        self.assertIn("generated/agent_agonic_formation_index.min.json", generated_agents)
        self.assertIn("scripts/build_agent_agonic_formation_index.py", generated_agents)
        self.assertIn("agent_agonic_formation.example.json", examples_agents)
        self.assertIn("validate_agent_agonic_formation.py", examples_agents)


if __name__ == "__main__":
    unittest.main()
