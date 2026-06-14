from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
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

    def test_literal_manifest_path_fields_are_validated(self) -> None:
        validator = _load_validator()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir) / "repo"
            shutil.copytree(
                ROOT,
                temp_root,
                ignore=shutil.ignore_patterns(
                    ".git",
                    ".mypy_cache",
                    ".pytest_cache",
                    "__pycache__",
                ),
            )
            missing_paths = [
                "mechanics/agon/parts/missing/school-campaign-posture.md",
                "mechanics/agon/parts/missing/rank-jurisdiction-registry.min.json",
                "mechanics/agon/parts/missing/rank-jurisdiction.seed.json",
            ]

            school_component = (
                temp_root
                / "mechanics"
                / "recurrence"
                / "parts"
                / "component-manifests"
                / "manifests"
                / "components"
                / "agon-school-campaign-posture.json"
            )
            school_payload = json.loads(school_component.read_text(encoding="utf-8"))
            school_payload["surfaces"][0] = missing_paths[0]
            school_component.write_text(json.dumps(school_payload, indent=2) + "\n", encoding="utf-8")

            rank_component = (
                temp_root
                / "mechanics"
                / "recurrence"
                / "parts"
                / "component-manifests"
                / "manifests"
                / "components"
                / "agon-rank-jurisdiction-surfaces.json"
            )
            rank_payload = json.loads(rank_component.read_text(encoding="utf-8"))
            rank_payload["observes"][0] = missing_paths[1]
            rank_component.write_text(json.dumps(rank_payload, indent=2) + "\n", encoding="utf-8")

            rank_hooks = (
                temp_root
                / "mechanics"
                / "recurrence"
                / "parts"
                / "component-manifests"
                / "manifests"
                / "hooks"
                / "agon-rank-jurisdiction-surfaces.json"
            )
            hooks_payload = json.loads(rank_hooks.read_text(encoding="utf-8"))
            hooks_payload["bindings"][1]["source"] = missing_paths[2]
            rank_hooks.write_text(json.dumps(hooks_payload, indent=2) + "\n", encoding="utf-8")

            errors = validator.collect_manifest_errors(temp_root)

        joined_errors = "\n".join(errors)
        for missing_path in missing_paths:
            self.assertIn(f"path does not exist: {missing_path}", joined_errors)

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
