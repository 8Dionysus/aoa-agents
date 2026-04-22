from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "assistant-projection-resolver.schema.json"
EXAMPLE_PATH = REPO_ROOT / "examples" / "assistant_projection_resolver.example.json"
DOC_PATH = REPO_ROOT / "docs" / "CODEX_SUBAGENT_PROJECTION.md"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def test_assistant_projection_resolver_example_validates() -> None:
    schema = load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)
    doc = DOC_PATH.read_text(encoding="utf-8")

    assert isinstance(schema, dict)
    assert isinstance(example, dict)

    validator = Draft202012Validator(schema)
    errors = [error.message for error in validator.iter_errors(example)]

    assert errors == []
    assert "source profile" in doc
    assert "no-self-rewrite" in doc
    assert example["no_self_rewrite_posture"]["allowed"] is False
