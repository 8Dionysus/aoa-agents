from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class Wave25RouteSurfacesTestCase(unittest.TestCase):
    def test_readme_and_docs_map_route_wave2_5_surfaces(self) -> None:
        readme = read_text("README.md")
        docs_readme = read_text("docs/README.md")
        subject_prep = read_text("docs/AGENT_SUBJECT_PREP.md")
        wave2_landing = read_text("docs/AGON_WAVE2_LANDING.md")

        self.assertIn("docs/AGENT_FORMATION_TRIAL.md", readme)
        self.assertIn("generated/agent_formation_trial.min.json", readme)
        self.assertIn("python scripts/validate_agent_formation_trial.py", readme)
        self.assertIn("AGENT_FORMATION_TRIAL", docs_readme)
        self.assertIn("AGON_WAVE2_5_LANDING", docs_readme)
        self.assertIn("CODEX_PROJECTION_AGON_BOUNDARY", docs_readme)
        self.assertIn("Wave II.5 Formation Trial has now landed", subject_prep)
        self.assertIn("Wave II.5 Formation Trial has now landed", wave2_landing)

    def test_local_guides_name_wave2_5_companion_surfaces(self) -> None:
        profiles_agents = read_text("profiles/AGENTS.md")
        generated_agents = read_text("generated/AGENTS.md")
        examples_agents = read_text("examples/AGENTS.md")

        self.assertIn("generated/agent_formation_trial.min.json", profiles_agents)
        self.assertIn("validate_agent_formation_trial.py", profiles_agents)
        self.assertIn("generated/agent_formation_trial.min.json", generated_agents)
        self.assertIn("build_agent_formation_trial.py", generated_agents)
        self.assertIn("agent_formation_trial.example.json", examples_agents)
        self.assertIn("validate_agent_formation_trial.py", examples_agents)


if __name__ == "__main__":
    unittest.main()
