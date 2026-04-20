from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class Wave2RouteSurfacesTestCase(unittest.TestCase):
    def test_readme_and_docs_map_route_wave2_surfaces(self) -> None:
        readme = read_text("README.md")
        docs_readme = read_text("docs/README.md")
        subject_prep = read_text("docs/AGENT_SUBJECT_PREP.md")
        kind_model = read_text("docs/AGENT_KIND_MODEL.md")

        self.assertIn("docs/ASSISTANT_CIVIL_RECHARTERING.md", readme)
        self.assertIn("generated/assistant_civil_formation_index.min.json", readme)
        self.assertIn("python scripts/validate_assistant_civil_formation.py", readme)
        self.assertIn("ASSISTANT_CIVIL_RECHARTERING", docs_readme)
        self.assertIn("ASSISTANT_SERVICE_CONTRACT_MODEL", docs_readme)
        self.assertIn("ASSISTANT_ESCALATION_TO_AGON", docs_readme)
        self.assertIn("Wave II Assistant Civil Rechartering has now landed", subject_prep)
        self.assertIn("Assistant forms are now landed separately in Wave II", kind_model)

    def test_local_guides_name_wave2_companion_surfaces(self) -> None:
        profiles_agents = read_text("profiles/AGENTS.md")
        generated_agents = read_text("generated/AGENTS.md")
        examples_agents = read_text("examples/AGENTS.md")

        self.assertIn("generated/assistant_civil_formation_index.min.json", profiles_agents)
        self.assertIn("validate_assistant_civil_formation.py", profiles_agents)
        self.assertIn("generated/assistant_civil_formation_index.min.json", generated_agents)
        self.assertIn("build_assistant_civil_formation_index.py", generated_agents)
        self.assertIn("assistant_civil_formation.example.json", examples_agents)
        self.assertIn("validate_assistant_civil_formation.py", examples_agents)


if __name__ == "__main__":
    unittest.main()
