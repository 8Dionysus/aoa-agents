from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_recursor_contracts.py"
sys.path.insert(0, str(ROOT / "scripts"))


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_recursor_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_recursor_contracts_validate() -> None:
    validator = _load_validator()

    validator.validate_recursor_contracts(ROOT)


def test_recursor_contracts_are_part_local() -> None:
    former_paths = (
        Path("schemas") / ("recursor-" + "role-contract.v1.schema.json"),
        Path("schemas") / ("recursor-" + "projection-candidate.v1.schema.json"),
        Path("schemas") / ("recursor-" + "boundary-report.v1.schema.json"),
        Path("examples") / ("recursor" + "_session_intent.example.json"),
        Path("examples") / ("recursor" + "_boundary_report.example.json"),
    )

    for relative_path in former_paths:
        assert not (ROOT / relative_path).exists()
