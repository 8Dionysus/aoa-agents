from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
WAVE2_PREFIXES = ("assistant_",)


def wave2_pairs() -> tuple[list[tuple[Path, Path]], list[str]]:
    pairs: list[tuple[Path, Path]] = []
    missing_pairs: list[str] = []
    for example_path in sorted((ROOT / "examples").glob("*.example.json")):
        stem = example_path.name.removesuffix(".example.json")
        if not stem.startswith(WAVE2_PREFIXES):
            continue
        schema_path = ROOT / "schemas" / f"{stem}_v1.json"
        if schema_path.exists():
            pairs.append((schema_path, example_path))
        else:
            missing_pairs.append(f"{example_path.relative_to(ROOT)} -> {schema_path.relative_to(ROOT)}")
    return pairs, missing_pairs


class ExperienceWave2SeedContractTests(unittest.TestCase):
    def test_experience_wave2_examples_match_schemas(self) -> None:
        pairs, missing_pairs = wave2_pairs()
        self.assertFalse(missing_pairs, "missing wave2 schema pair(s): " + ", ".join(missing_pairs))
        self.assertTrue(pairs)
        for schema_path, example_path in pairs:
            with self.subTest(example=example_path.name):
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                example = json.loads(example_path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                errors = sorted(
                    Draft202012Validator(schema).iter_errors(example),
                    key=lambda error: list(error.path),
                )
                self.assertFalse(
                    errors,
                    f"{example_path.name}: {errors[0].message if errors else ''}",
                )


if __name__ == "__main__":
    unittest.main()
