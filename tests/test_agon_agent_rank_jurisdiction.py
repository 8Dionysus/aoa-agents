from __future__ import annotations
import importlib.util
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_registry_matches_seed():
    builder = _load(ROOT / "scripts/build_agon_agent_rank_jurisdiction_registry.py")
    generated = json.loads((ROOT / "generated/agon_agent_rank_jurisdiction_registry.min.json").read_text(encoding="utf-8"))
    assert builder.build_registry() == generated


def test_validator_accepts_registry():
    validator = _load(ROOT / "scripts/validate_agon_agent_rank_jurisdiction.py")
    assert validator.main() == 0


def test_schemas_constrain_entry_and_registry():
    generated = json.loads((ROOT / "generated/agon_agent_rank_jurisdiction_registry.min.json").read_text(encoding="utf-8"))
    entry_schema = json.loads((ROOT / "schemas/agon-agent-rank-jurisdiction.schema.json").read_text(encoding="utf-8"))
    registry_schema = json.loads((ROOT / "schemas/agon-agent-rank-jurisdiction-registry.schema.json").read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(entry_schema)
    Draft202012Validator.check_schema(registry_schema)
    assert list(Draft202012Validator(entry_schema).iter_errors({}))
    assert list(Draft202012Validator(registry_schema).iter_errors({}))
    Draft202012Validator(entry_schema).validate(generated["entries"][0])
    Draft202012Validator(registry_schema).validate(generated)
