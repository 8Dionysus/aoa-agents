from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = ROOT / "mechanics" / "experience" / "parts" / "assistant-civil-service" / "scripts"


class AssistantCivilFormationTestCase(unittest.TestCase):
    def test_assistant_civil_generated_index_is_current(self) -> None:
        script = SCRIPT_DIR / "build_assistant_civil_formation_index.py"
        result = subprocess.run(
            [sys.executable, str(script), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_assistant_civil_surfaces_validate(self) -> None:
        script = SCRIPT_DIR / "validate_assistant_civil_formation.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
