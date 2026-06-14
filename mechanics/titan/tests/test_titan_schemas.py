from __future__ import annotations

import importlib.util
import shutil
import tempfile
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

    def test_schema_discovery_reports_nested_schema_drift(self) -> None:
        validator = _load_validator()
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir) / "repo"
            shutil.copytree(
                ROOT,
                temp_root,
                ignore=shutil.ignore_patterns(".git", ".mypy_cache", ".pytest_cache", "__pycache__"),
            )
            nested_schema = (
                temp_root
                / "mechanics"
                / "titan"
                / "parts"
                / "role-bearing"
                / "schemas"
                / "archive"
                / "foo.schema.json"
            )
            nested_schema.parent.mkdir(parents=True)
            nested_schema.write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n',
                encoding="utf-8",
            )

            errors = validator.collect_titan_schema_errors(temp_root)

        self.assertTrue(
            any(
                "mechanics/titan/parts/role-bearing/schemas/archive/foo.schema.json" in error
                for error in errors
            ),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
