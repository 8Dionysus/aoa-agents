from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "mechanics" / "titan" / "scripts" / "validate_titan_examples.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_titan_examples", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TitanExampleValidatorTests(unittest.TestCase):
    def test_current_titan_examples_validate(self) -> None:
        validator = _load_validator()

        validator.validate_titan_examples(ROOT)

    def test_active_example_path_rejects_former_root_namespace(self) -> None:
        validator = _load_validator()
        errors: list[str] = []

        validator.validate_active_example_path(
            Path("examples") / ("titan_" + "bearer_identity.v0.json"),
            errors,
        )

        self.assertTrue(errors)

    def test_active_example_path_rejects_old_titan_prefix(self) -> None:
        validator = _load_validator()
        errors: list[str] = []

        validator.validate_active_example_path(
            Path("mechanics/titan/parts/role-bearing/examples") / ("titan_" + "bearer_identity.v0.json"),
            errors,
        )

        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
