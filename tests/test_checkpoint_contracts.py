from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_checkpoint_contracts.py"
sys.path.insert(0, str(ROOT / "scripts"))


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_checkpoint_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_checkpoint_contracts_validate() -> None:
    validator = _load_validator()

    validator.validate_checkpoint_contracts(ROOT)


def test_checkpoint_contracts_are_part_local() -> None:
    former_paths = (
        Path("schemas") / "self-agent-checkpoint.schema.json",
        Path("schemas") / "self-agency-continuity-window.schema.json",
        Path("examples") / ("self" + "_agent" + "_checkpoint"),
    )

    for relative_path in former_paths:
        assert not (ROOT / relative_path).exists()
