from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "mechanics" / "experience" / "scripts" / "validate_adoption_boundary_contracts.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_adoption_boundary_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AdoptionBoundarySeedContractTests(unittest.TestCase):
    def test_adoption_boundary_contracts_validate(self) -> None:
        validator = _load_validator()

        validator.validate_adoption_boundary_contracts(ROOT)

    def test_adoption_boundary_contracts_are_part_local(self) -> None:
        validator = _load_validator()

        for former_path in validator.FORMER_CHECK_PATHS:
            with self.subTest(former_path=former_path.as_posix()):
                self.assertFalse((ROOT / former_path).exists())

        for contract in validator.CONTRACTS:
            with self.subTest(active_stem=contract.active_stem):
                self.assertFalse((ROOT / "schemas" / contract.former_schema_name).exists())
                self.assertFalse((ROOT / "examples" / contract.former_example_name).exists())
                self.assertTrue((ROOT / contract.schema_rel).is_file())
                self.assertTrue((ROOT / contract.example_rel).is_file())


if __name__ == "__main__":
    unittest.main()
