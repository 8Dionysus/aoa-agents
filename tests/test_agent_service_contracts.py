from __future__ import annotations

from pathlib import Path
import unittest

from scripts.validate_agent_service_contracts import (
    CONTRACTS,
    collect_agent_service_contract_errors,
)


ROOT = Path(__file__).resolve().parents[1]


class AgentServiceContractTests(unittest.TestCase):
    def test_agent_service_contracts_validate(self) -> None:
        errors = collect_agent_service_contract_errors(ROOT)
        self.assertFalse(errors, "\n".join(errors))

    def test_former_root_contract_paths_are_absent(self) -> None:
        self.assertTrue(CONTRACTS)
        for contract in CONTRACTS:
            with self.subTest(active_stem=contract.active_stem):
                self.assertFalse((ROOT / "schemas" / contract.former_schema_name).exists())
                self.assertFalse((ROOT / "examples" / contract.former_example_name).exists())


if __name__ == "__main__":
    unittest.main()
