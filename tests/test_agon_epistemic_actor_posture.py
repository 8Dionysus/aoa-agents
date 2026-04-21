from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class AgonEpistemicActorPostureTests(unittest.TestCase):
    def test_generated_registry_shape(self) -> None:
        reg = json.loads(
            (
                ROOT / "generated/agon_epistemic_actor_posture_registry.min.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(reg["wave"], "XV")
        self.assertIn(
            reg["runtime_posture"],
            ("candidate_only", "pre_protocol_candidate_only"),
        )
        self.assertEqual(reg["count"], 5)
        self.assertEqual(len(reg["postures"]), 5)
        for item in reg["postures"]:
            self.assertIs(item["live_protocol"], False)
            self.assertIn("auto_doctrine_rewrite", item.get("forbidden_effects", []))

    def test_builder_check_and_validator(self) -> None:
        build = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/build_agon_epistemic_actor_posture_registry.py"),
                "--check",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(build.returncode, 0, build.stderr + build.stdout)
        validate = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_agon_epistemic_actor_posture.py"),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(validate.returncode, 0, validate.stderr + validate.stdout)


if __name__ == "__main__":
    unittest.main()
