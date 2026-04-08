from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class AntifragilityPublicSurfaceTests(unittest.TestCase):
    def test_stress_schema_examples_validate(self) -> None:
        surfaces = (
            (
                "schemas/agent_stress_posture_v1.json",
                "examples/agent_stress_posture.example.json",
            ),
            (
                "schemas/stress_handoff_envelope_v1.json",
                "examples/stress_handoff_envelope.example.json",
            ),
        )

        for schema_path, example_path in surfaces:
            with self.subTest(schema=schema_path, example=example_path):
                schema = load_json(schema_path)
                example = load_json(example_path)
                self.assertIsInstance(schema, dict)
                Draft202012Validator.check_schema(schema)
                Draft202012Validator(schema).validate(example)

    def test_stress_surfaces_are_discoverable_and_bounded(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        posture = (REPO_ROOT / "docs" / "AGENT_STRESS_POSTURE.md").read_text(encoding="utf-8")
        handoffs = (REPO_ROOT / "docs" / "AGENT_STRESS_HANDOFFS.md").read_text(encoding="utf-8")

        self.assertIn("docs/AGENT_STRESS_POSTURE.md", readme)
        self.assertIn("docs/AGENT_STRESS_HANDOFFS.md", readme)
        self.assertIn("AGENT_STRESS_POSTURE", docs_readme)
        self.assertIn("AGENT_STRESS_HANDOFFS", docs_readme)

        for token in (
            "do not let a stress profile silently widen authority",
            "memory writeback strictness",
            "It does not replace routing, playbooks, evals, or source-owned receipts.",
        ):
            self.assertIn(token, posture)

        for token in (
            "what actions are blocked",
            "what evidence already exists",
            "do not use a handoff envelope as proof",
            "without widening authority",
        ):
            self.assertIn(token, handoffs)

    def test_stress_posture_example_targets_existing_profile(self) -> None:
        payload = load_json("examples/agent_stress_posture.example.json")
        assert isinstance(payload, dict)
        applies_to = payload["applies_to"]
        assert isinstance(applies_to, dict)
        target = REPO_ROOT / applies_to["agent_profile"]
        self.assertTrue(target.is_file())


if __name__ == "__main__":
    unittest.main()
