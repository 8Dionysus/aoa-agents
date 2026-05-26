from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_agon_formation_contracts.py"
sys.path.insert(0, str(ROOT / "scripts"))


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_agon_formation_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_agon_formation_contracts_validate() -> None:
    validator = _load_validator()

    validator.validate_agon_formation_contracts(ROOT)


def test_agon_formation_contracts_are_part_local() -> None:
    former_paths = (
        Path("schemas") / ("agent" + "_kind_v1.json"),
        Path("schemas") / ("agent" + "_arena_eligibility_v1.json"),
        Path("schemas") / ("agent" + "_formation_trial_v1.json"),
        Path("examples") / ("agent" + "_agonic_formation.example.json"),
        Path("examples") / ("agent" + "_formation_trial.example.json"),
    )

    for relative_path in former_paths:
        assert not (ROOT / relative_path).exists()
