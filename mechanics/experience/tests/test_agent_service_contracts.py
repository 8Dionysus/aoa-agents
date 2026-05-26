from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "mechanics" / "experience" / "scripts" / "validate_agent_service_contracts.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_agent_service_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AgentServiceContractTests(unittest.TestCase):
    def test_agent_service_contracts_validate(self) -> None:
        validator = _load_validator()

        errors = validator.collect_agent_service_contract_errors(ROOT)
        self.assertFalse(errors, "\n".join(errors))

    def test_former_root_contract_paths_are_absent(self) -> None:
        validator = _load_validator()

        for former_path in validator.FORMER_CHECK_PATHS:
            with self.subTest(former_path=former_path.as_posix()):
                self.assertFalse((ROOT / former_path).exists())

        self.assertTrue(validator.CONTRACTS)
        for contract in validator.CONTRACTS:
            with self.subTest(active_stem=contract.active_stem):
                self.assertFalse((ROOT / "schemas" / contract.former_schema_name).exists())
                self.assertFalse((ROOT / "examples" / contract.former_example_name).exists())


if __name__ == "__main__":
    unittest.main()
