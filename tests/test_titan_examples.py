from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_titan_examples.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_titan_examples", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_current_titan_examples_validate() -> None:
    validator = _load_validator()

    validator.validate_titan_examples(ROOT)


def test_active_example_path_rejects_former_root_namespace() -> None:
    validator = _load_validator()
    errors: list[str] = []

    validator.validate_active_example_path(
        Path("examples") / ("titan_" + "bearer_identity.v0.json"),
        errors,
    )

    assert errors


def test_active_example_path_rejects_old_titan_prefix() -> None:
    validator = _load_validator()
    errors: list[str] = []

    validator.validate_active_example_path(
        Path("mechanics/titan/parts/role-bearing/examples") / ("titan_" + "bearer_identity.v0.json"),
        errors,
    )

    assert errors
