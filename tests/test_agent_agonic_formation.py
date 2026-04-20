from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_agonic_formation_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_agent_agonic_formation.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_agent_agonic_formation_index_is_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_agent_agonic_formation_index.py", "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stdout + result.stderr
