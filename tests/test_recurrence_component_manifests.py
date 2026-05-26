from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_recurrence_component_manifests.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_recurrence_component_manifests", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_current_recurrence_component_manifests_validate():
    validator = _load_validator()

    validator.validate_recurrence_component_manifests(ROOT)


def test_active_payload_text_rejects_old_manifest_namespace():
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

    assert errors
