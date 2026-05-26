from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT = "mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py"
BUILDER = "mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py"


class AgentAgonicFormationTestCase(unittest.TestCase):
    def test_agent_agonic_formation_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, SCRIPT],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_agent_agonic_formation_index_is_current(self) -> None:
        result = subprocess.run(
            [sys.executable, BUILDER, "--check"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
