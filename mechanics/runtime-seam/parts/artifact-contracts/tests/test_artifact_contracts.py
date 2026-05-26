from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT = (
    ROOT
    / "mechanics"
    / "runtime-seam"
    / "parts"
    / "artifact-contracts"
    / "scripts"
    / "validate_artifact_contracts.py"
)


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_artifact_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RuntimeArtifactContractsTests(unittest.TestCase):
    def test_runtime_artifact_contracts_validate(self) -> None:
        validator = _load_validator()

        validator.validate_runtime_artifact_contracts(ROOT)

    def test_no_former_runtime_artifact_examples_dir_remains(self) -> None:
        validator = _load_validator()
        errors = validator.collect_runtime_artifact_contract_errors(ROOT)

        self.assertFalse(
            any("former root runtime artifact examples directory is still active" in error for error in errors)
        )

    def test_runtime_artifact_contracts_are_part_local(self) -> None:
        former_paths = (
            Path("schemas") / "artifact.route_decision.schema.json",
            Path("schemas") / "artifact.transition_decision.schema.json",
            Path("examples") / ("runtime" + "_artifacts"),
        )

        for relative_path in former_paths:
            with self.subTest(path=relative_path.as_posix()):
                self.assertFalse((ROOT / relative_path).exists())


if __name__ == "__main__":
    unittest.main()
