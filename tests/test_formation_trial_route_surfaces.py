from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class FormationTrialRouteSurfacesTestCase(unittest.TestCase):
    def test_docs_map_and_contour_route_formation_trial_surfaces(self) -> None:
        readme = read_text("README.md")
        docs_readme = read_text("docs/README.md")
        contour = read_text("docs/CURRENT_CONTOUR.md")
        subject_prep = read_text("mechanics/agon/parts/formation/docs/subject-prep.md")
        assistant_civil_landing = read_text(
            "mechanics/agon/parts/formation/docs/assistant-civil-rechartering-landing.md"
        )

        self.assertIn("docs/CURRENT_CONTOUR.md", readme)
        self.assertIn("mechanics/agon/parts/formation/docs/formation-trial.md", contour)
        self.assertIn("generated/agent_formation_trial.min.json", contour)
        self.assertIn("mechanics/agon/AGENTS.md", contour)
        self.assertIn("Agent Formation Trial", docs_readme)
        self.assertIn("Formation Trial Landing", docs_readme)
        self.assertIn("Codex Projection Agon Boundary", docs_readme)
        self.assertIn("Formation Trial has now landed", subject_prep)
        self.assertIn("Formation Trial has now landed", assistant_civil_landing)

    def test_local_guides_name_formation_trial_companion_surfaces(self) -> None:
        profiles_agents = read_text("agents/roles/AGENTS.md")
        generated_agents = read_text("generated/AGENTS.md")
        examples_agents = read_text("examples/AGENTS.md")

        self.assertIn("generated/agent_formation_trial.min.json", profiles_agents)
        self.assertIn("validate_agent_formation_trial.py", profiles_agents)
        self.assertIn("generated/agent_formation_trial.min.json", generated_agents)
        self.assertIn("build_agent_formation_trial.py", generated_agents)
        self.assertIn("mechanics/agon/parts/formation/examples/formation-trial.example.json", examples_agents)
        self.assertIn("validate_agent_formation_trial.py", examples_agents)


if __name__ == "__main__":
    unittest.main()
