from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "mechanics" / "recurrence" / "scripts" / "validate_recursor_contracts.py"
sys.path.insert(0, str(ROOT / "mechanics" / "recurrence" / "scripts"))


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
        Path("generated") / ("recursor" + "_role_readiness.min.json"),
        Path("generated") / ("recursor" + "_pair_contract.min.json"),
        Path("generated") / ("recursor" + "_projection_candidates.min.json"),
        Path("generated") / ("recursor" + "_agon_boundary_report.min.json"),
    )

    for relative_path in former_paths:
        assert not (ROOT / relative_path).exists()

    active_paths = (
        Path("mechanics/recurrence/parts/recursor-readiness/generated/role-readiness.min.json"),
        Path("mechanics/recurrence/parts/recursor-readiness/generated/pair-contract.min.json"),
        Path("mechanics/recurrence/parts/codex-recursor-projection/generated/projection-candidates.min.json"),
        Path("mechanics/recurrence/parts/agon-recursor-boundary/generated/boundary-report.min.json"),
    )

    for relative_path in active_paths:
        assert (ROOT / relative_path).is_file()
