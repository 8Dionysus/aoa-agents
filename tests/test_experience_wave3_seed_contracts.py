from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_adoption_boundary_contracts.py"
sys.path.insert(0, str(ROOT / "scripts"))


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_adoption_boundary_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_wave3_adoption_boundary_contracts_validate() -> None:
    validator = _load_validator()

    validator.validate_adoption_boundary_contracts(ROOT)


def test_wave3_adoption_boundary_contracts_are_part_local() -> None:
    validator = _load_validator()

    for contract in validator.CONTRACTS:
        assert not (ROOT / "schemas" / contract.former_schema_name).exists()
        assert not (ROOT / "examples" / contract.former_example_name).exists()
        assert (ROOT / contract.schema_rel).is_file()
        assert (ROOT / contract.example_rel).is_file()
