from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT = (
    ROOT
    / "mechanics"
    / "recurrence"
    / "parts"
    / "component-manifests"
    / "scripts"
    / "validate_recurrence_component_manifests.py"
)
FORMER_ROOT_TEST_PATH = ROOT / "tests" / "test_recurrence_component_manifests.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_recurrence_component_manifests", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RecurrenceComponentManifestTests(unittest.TestCase):
    def test_current_recurrence_component_manifests_validate(self) -> None:
        validator = _load_validator()

        validator.validate_recurrence_component_manifests(ROOT)

    def test_active_payload_text_rejects_old_manifest_namespace(self) -> None:
        validator = _load_validator()
        errors: list[str] = []
        old_ref = (
            "component"
            + ".agon."
            + "wave16"
            + ".aoa_agents"
        )

        validator.validate_active_payload_text(
            old_ref,
            label="test payload",
            errors=errors,
        )

        self.assertTrue(errors)

    def test_former_root_test_is_not_active(self) -> None:
        self.assertFalse(FORMER_ROOT_TEST_PATH.exists())


if __name__ == "__main__":
    unittest.main()
