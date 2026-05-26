from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[5]
SCRIPT = ROOT / "mechanics" / "titan" / "parts" / "codex-projection" / "scripts" / "render_titan_codex_agents.py"
ROLES = ROOT / "mechanics" / "titan" / "parts" / "role-bearing" / "config" / "role-classes.v0.json"
BEARERS = ROOT / "mechanics" / "titan" / "parts" / "role-bearing" / "config" / "bearers.v0.json"
OUT_DIR = ROOT / "generated" / "titan_codex_agents" / "agents"
MANIFEST = ROOT / "generated" / "titan_codex_agents" / "projection_manifest.json"


def _load_renderer():
    spec = importlib.util.spec_from_file_location("render_titan_codex_agents", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TitanCodexProjectionTests(unittest.TestCase):
    def test_current_projection_is_fresh(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--roles",
                str(ROLES),
                "--bearers",
                str(BEARERS),
                "--out-dir",
                str(OUT_DIR),
                "--manifest",
                str(MANIFEST),
                "--prune",
                "--check",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout)

    def test_projection_uses_named_titan_bearers(self) -> None:
        renderer = _load_renderer()
        roles_doc = renderer.load(ROLES)
        bearers_doc = renderer.load(BEARERS)
        manifest, rendered_agents = renderer.build_projection(roles_doc, bearers_doc)

        names = {agent["codex_name"] for agent in manifest["agents"]}
        self.assertEqual(names, {"Atlas", "Sentinel", "Mneme", "Forge", "Delta"})
        self.assertNotIn("architect.toml", rendered_agents)
        self.assertNotIn("reviewer.toml", rendered_agents)
        self.assertNotIn("memory-keeper.toml", rendered_agents)


if __name__ == "__main__":
    unittest.main()
