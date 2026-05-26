from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "mechanics" / "experience" / "scripts" / "validate_experience_assistant_civil_contracts.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_experience_assistant_civil_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ExperienceAssistantCivilContractsTestCase(unittest.TestCase):
    def test_experience_assistant_civil_contracts_validate(self) -> None:
        validator = _load_validator()

        validator.validate_experience_assistant_civil_contracts(ROOT)

    def test_experience_assistant_civil_contracts_are_part_local(self) -> None:
        former_paths = (
            Path("schemas") / ("assistant" + "_variant_v1.json"),
            Path("schemas") / ("assistant" + "_service_identity_v1.json"),
            Path("schemas") / ("assistant" + "_service_contract_v1.json"),
            Path("schemas") / ("assistant" + "_service_governance_v1.json"),
            Path("schemas") / ("assistant" + "_service_certification_v1.json"),
            Path("schemas") / ("assistant" + "_civil_formation_v1.json"),
            Path("schemas") / ("assistant" + "_arena_exclusion_v1.json"),
            Path("examples") / ("assistant" + "_civil_formation.example.json"),
            Path("scripts") / "build_assistant_civil_formation_index.py",
            Path("scripts") / "validate_assistant_civil_formation.py",
            Path("scripts") / "validate_experience_assistant_civil_contracts.py",
            Path("tests") / "test_assistant_civil_formation.py",
            Path("tests") / "test_experience_assistant_civil_contracts.py",
        )

        for relative_path in former_paths:
            self.assertFalse((ROOT / relative_path).exists(), str(relative_path))


if __name__ == "__main__":
    unittest.main()
