from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT = (
    ROOT
    / "mechanics"
    / "rpg"
    / "parts"
    / "progression-model"
    / "scripts"
    / "validate_rpg_progression.py"
)


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_rpg_progression", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RPGProgressionTests(unittest.TestCase):
    def test_rpg_progression_validates(self) -> None:
        validator = _load_validator()

        validator.validate_rpg_progression(ROOT)

    def test_progression_contract_is_part_local(self) -> None:
        former_paths = (
            Path("schemas") / ("agent" + "_progression.schema.json"),
            Path("examples") / ("agent" + "_progression.example.json"),
            Path("scripts") / "validate_rpg_progression.py",
        )

        for relative_path in former_paths:
            with self.subTest(path=relative_path.as_posix()):
                self.assertFalse((ROOT / relative_path).exists())


if __name__ == "__main__":
    unittest.main()
