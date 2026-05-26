from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_experience_assistant_civil_contracts.py"
sys.path.insert(0, str(ROOT / "scripts"))


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_experience_assistant_civil_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_experience_assistant_civil_contracts_validate() -> None:
    validator = _load_validator()

    validator.validate_experience_assistant_civil_contracts(ROOT)


def test_experience_assistant_civil_contracts_are_part_local() -> None:
    former_paths = (
        Path("schemas") / ("assistant" + "_variant_v1.json"),
        Path("schemas") / ("assistant" + "_service_identity_v1.json"),
        Path("schemas") / ("assistant" + "_service_contract_v1.json"),
        Path("schemas") / ("assistant" + "_service_governance_v1.json"),
        Path("schemas") / ("assistant" + "_service_certification_v1.json"),
        Path("schemas") / ("assistant" + "_civil_formation_v1.json"),
        Path("schemas") / ("assistant" + "_arena_exclusion_v1.json"),
        Path("examples") / ("assistant" + "_civil_formation.example.json"),
    )

    for relative_path in former_paths:
        assert not (ROOT / relative_path).exists()
