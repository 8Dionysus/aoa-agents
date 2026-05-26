from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "mechanics" / "titan" / "scripts" / "validate_titan_schemas.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_titan_schemas", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TitanSchemaValidatorTests(unittest.TestCase):
    def test_current_titan_schemas_validate(self) -> None:
        validator = _load_validator()

        validator.validate_titan_schemas(ROOT)

    def test_active_schema_path_rejects_former_root_namespace(self) -> None:
        validator = _load_validator()
        errors: list[str] = []

        validator.validate_active_schema_path(Path("schemas") / ("titan_" + "role_class.schema.json"), errors)

        self.assertTrue(errors)

    def test_active_schema_path_rejects_old_titan_prefix(self) -> None:
        validator = _load_validator()
        errors: list[str] = []

        validator.validate_active_schema_path(
            Path("mechanics/titan/parts/role-bearing/schemas") / ("titan_" + "role_class.schema.json"),
            errors,
        )

        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
