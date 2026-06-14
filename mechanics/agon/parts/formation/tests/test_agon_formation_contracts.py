from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT = ROOT / "mechanics" / "agon" / "parts" / "formation" / "scripts" / "validate_agon_formation_contracts.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_agon_formation_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AgonFormationContractsTestCase(unittest.TestCase):
    def test_agon_formation_contracts_validate(self) -> None:
        validator = _load_validator()
        validator.validate_agon_formation_contracts(ROOT)

    def test_dependency_validation_uses_requested_root(self) -> None:
        validator = _load_validator()
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir) / "repo"
            shutil.copytree(
                ROOT,
                temp_root,
                ignore=shutil.ignore_patterns(".git", ".mypy_cache", ".pytest_cache", "__pycache__"),
            )
            wave_i_doc = temp_root / "mechanics" / "agon" / "parts" / "formation" / "docs" / "actor-rechartering.md"
            wave_i_doc.unlink()

            errors = validator._collect_dependency_errors(temp_root)

        self.assertIn("validate_agent_agonic_formation.py failed", errors)

    def test_agon_formation_contracts_are_part_local(self) -> None:
        former_paths = (
            Path("schemas") / ("agent" + "_kind_v1.json"),
            Path("schemas") / ("agent" + "_arena_eligibility_v1.json"),
            Path("schemas") / ("agent" + "_formation_trial_v1.json"),
            Path("examples") / ("agent" + "_agonic_formation.example.json"),
            Path("examples") / ("agent" + "_formation_trial.example.json"),
            Path("scripts") / "build_agent_agonic_formation_index.py",
            Path("scripts") / "validate_agent_agonic_formation.py",
            Path("scripts") / "build_agent_formation_trial.py",
            Path("scripts") / "validate_agent_formation_trial.py",
            Path("scripts") / "validate_agon_formation_contracts.py",
            Path("tests") / "test_agent_agonic_formation.py",
            Path("tests") / "test_agent_formation_trial.py",
            Path("tests") / "test_agon_formation_contracts.py",
        )

        for relative_path in former_paths:
            self.assertFalse((ROOT / relative_path).exists(), str(relative_path))


if __name__ == "__main__":
    unittest.main()
