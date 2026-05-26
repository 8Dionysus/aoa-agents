from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
SCHEMA_PATH = (
    REPO_ROOT
    / "mechanics"
    / "codex-projection"
    / "parts"
    / "assistant-projection"
    / "schemas"
    / "assistant-projection-resolver.schema.json"
)
EXAMPLE_PATH = (
    REPO_ROOT
    / "mechanics"
    / "codex-projection"
    / "parts"
    / "assistant-projection"
    / "examples"
    / "assistant-projection-resolver.example.json"
)
DOC_PATH = REPO_ROOT / "mechanics" / "codex-projection" / "parts" / "subagent-projection" / "docs" / "subagent-projection.md"
FORMER_ROOT_TEST_PATH = REPO_ROOT / "tests" / "test_wave1_assistant_projection.py"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class AssistantProjectionResolverTests(unittest.TestCase):
    def test_projection_resolver_example_validates(self) -> None:
        schema = load_json(SCHEMA_PATH)
        example = load_json(EXAMPLE_PATH)
        doc = DOC_PATH.read_text(encoding="utf-8")

        self.assertIsInstance(schema, dict)
        self.assertIsInstance(example, dict)

        validator = Draft202012Validator(schema)
        errors = [error.message for error in validator.iter_errors(example)]

        self.assertEqual(errors, [])
        self.assertIn("source profile", doc)
        self.assertIn("no-self-rewrite", doc)
        self.assertFalse(example["no_self_rewrite_posture"]["allowed"])

    def test_former_root_test_is_not_active(self) -> None:
        self.assertFalse(FORMER_ROOT_TEST_PATH.exists())


if __name__ == "__main__":
    unittest.main()
