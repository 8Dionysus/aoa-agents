from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_builder():
    path = ROOT / "scripts" / "build_agent_formation_trial.py"
    spec = importlib.util.spec_from_file_location("agent_formation_trial_builder_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_formation_trial_generated_surface_is_current():
    builder = load_builder()
    expected = builder.build_index(ROOT)
    actual = json.loads((ROOT / builder.OUTPUT).read_text(encoding="utf-8"))
    assert actual == expected
    assert actual["global_verdict"] == "pass_pre_protocol_formation_trial"
    assert actual["readiness_summary"]["split_form_survivors"] == 5


def test_formation_trial_validator_passes():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_agent_formation_trial.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
