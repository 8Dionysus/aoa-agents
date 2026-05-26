from __future__ import annotations
import importlib.util
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = ROOT / "mechanics" / "agon" / "parts" / "arena-rank-school" / "scripts"
ARENA_RANK_SCHOOL_SCHEMAS = ROOT / "mechanics/agon/parts/arena-rank-school/schemas"
ARENA_RANK_SCHOOL_GENERATED = ROOT / "mechanics/agon/parts/arena-rank-school/generated"


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AgonAgentRankJurisdictionTestCase(unittest.TestCase):
    def test_generated_registry_matches_seed(self) -> None:
        builder = _load(SCRIPT_DIR / "build_agon_agent_rank_jurisdiction_registry.py")
        generated = json.loads(
            (ARENA_RANK_SCHOOL_GENERATED / "rank-jurisdiction-registry.min.json").read_text(encoding="utf-8")
        )
        self.assertEqual(builder.build_registry(), generated)

    def test_validator_accepts_registry(self) -> None:
        validator = _load(SCRIPT_DIR / "validate_agon_agent_rank_jurisdiction.py")
        self.assertEqual(validator.main(), 0)

    def test_schemas_constrain_entry_and_registry(self) -> None:
        generated = json.loads(
            (ARENA_RANK_SCHOOL_GENERATED / "rank-jurisdiction-registry.min.json").read_text(encoding="utf-8")
        )
        entry_schema = json.loads((ARENA_RANK_SCHOOL_SCHEMAS / "rank-jurisdiction.schema.json").read_text(encoding="utf-8"))
        registry_schema = json.loads(
            (ARENA_RANK_SCHOOL_SCHEMAS / "rank-jurisdiction-registry.schema.json").read_text(encoding="utf-8")
        )

        Draft202012Validator.check_schema(entry_schema)
        Draft202012Validator.check_schema(registry_schema)
        self.assertTrue(list(Draft202012Validator(entry_schema).iter_errors({})))
        self.assertTrue(list(Draft202012Validator(registry_schema).iter_errors({})))
        Draft202012Validator(entry_schema).validate(generated["entries"][0])
        Draft202012Validator(registry_schema).validate(generated)


if __name__ == "__main__":
    unittest.main()
