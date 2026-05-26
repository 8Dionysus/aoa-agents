from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = (
    REPO_ROOT
    / "mechanics"
    / "codex-projection"
    / "parts"
    / "specialization-eligibility"
)
SCHEMA_PATH = PART_ROOT / "schemas" / "specialization-eligibility.schema.json"
EXAMPLE_PATH = PART_ROOT / "examples" / "specialization-eligibility.example.json"
VALIDATOR_PATH = PART_ROOT / "scripts" / "validate_specialization_eligibility.py"
MANIFEST_PATH = REPO_ROOT / "generated" / "codex_agents" / "projection_manifest.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class SpecializationEligibilityTests(unittest.TestCase):
    def test_example_validates_against_schema(self) -> None:
        schema = load_json(SCHEMA_PATH)
        example = load_json(EXAMPLE_PATH)

        self.assertIsInstance(schema, dict)
        self.assertIsInstance(example, dict)

        errors = [error.message for error in Draft202012Validator(schema).iter_errors(example)]
        self.assertEqual(errors, [])

    def test_example_is_candidate_only_and_not_projected(self) -> None:
        example = load_json(EXAMPLE_PATH)
        manifest = load_json(MANIFEST_PATH)
        generated_names = {entry["name"] for entry in manifest["generated_agents"]}

        self.assertEqual(example["projection_scope"], "base_role_profiles_only")
        self.assertEqual(example["decision"]["status"], "candidate_only")
        self.assertEqual(example["codex_install"]["install_state"], "not_projected")
        self.assertNotIn(example["codex_install"]["proposed_agent_name"], generated_names)
        self.assertTrue(example["guardrails"]["no_generated_agent_change"])
        self.assertTrue(example["guardrails"]["no_workspace_install"])
        self.assertTrue(example["guardrails"]["no_runtime_activation"])

    def test_validator_accepts_part(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)


if __name__ == "__main__":
    unittest.main()
