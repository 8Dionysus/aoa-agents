from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_codex_subagents_v2.py"
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "validate_codex_subagents.py"
PROFILES_ROOT = REPO_ROOT / "profiles"
WIRING_PATH = REPO_ROOT / "config" / "codex_subagent_wiring.v2.json"


class CodexSubagentProjectionTests(unittest.TestCase):
    def test_generator_emits_five_agents(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-agents-codex-projection-") as temp_dir:
            root = Path(temp_dir)
            agents_dir = root / "agents"
            config_snippet = root / "config.subagents.generated.toml"
            manifest = root / "projection_manifest.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--profiles-root",
                    str(PROFILES_ROOT),
                    "--wiring",
                    str(WIRING_PATH),
                    "--output-dir",
                    str(agents_dir),
                    "--emit-config-snippet",
                    str(config_snippet),
                    "--emit-manifest",
                    str(manifest),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            emitted = sorted(path.name for path in agents_dir.glob("*.toml"))
            self.assertEqual(
                emitted,
                [
                    "architect.toml",
                    "coder.toml",
                    "evaluator.toml",
                    "memory-keeper.toml",
                    "reviewer.toml",
                ],
            )

    def test_coder_is_workspace_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-agents-codex-projection-") as temp_dir:
            root = Path(temp_dir)
            agents_dir = root / "agents"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--profiles-root",
                    str(PROFILES_ROOT),
                    "--wiring",
                    str(WIRING_PATH),
                    "--output-dir",
                    str(agents_dir),
                    "--emit-config-snippet",
                    str(root / "config.toml"),
                    "--emit-manifest",
                    str(root / "manifest.json"),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            coder = (agents_dir / "coder.toml").read_text(encoding="utf-8")
            architect = (agents_dir / "architect.toml").read_text(encoding="utf-8")
            self.assertIn('sandbox_mode = "workspace-write"', coder)
            self.assertIn('sandbox_mode = "read-only"', architect)

    def test_config_snippet_uses_config_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-agents-codex-projection-") as temp_dir:
            root = Path(temp_dir)
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--profiles-root",
                    str(PROFILES_ROOT),
                    "--wiring",
                    str(WIRING_PATH),
                    "--output-dir",
                    str(root / "agents"),
                    "--emit-config-snippet",
                    str(root / "config.subagents.generated.toml"),
                    "--emit-manifest",
                    str(root / "manifest.json"),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            config_text = (root / "config.subagents.generated.toml").read_text(encoding="utf-8")
            self.assertIn('config_file = "agents/architect.toml"', config_text)
            self.assertNotIn(".codex/agents/architect.toml", config_text)

    def test_manifest_links_back_to_source_profiles(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-agents-codex-projection-") as temp_dir:
            root = Path(temp_dir)
            manifest = root / "projection_manifest.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--profiles-root",
                    str(PROFILES_ROOT),
                    "--wiring",
                    str(WIRING_PATH),
                    "--output-dir",
                    str(root / "agents"),
                    "--emit-config-snippet",
                    str(root / "config.toml"),
                    "--emit-manifest",
                    str(manifest),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            generated_agents = {entry["name"]: entry for entry in payload["generated_agents"]}
            self.assertIn("architect", generated_agents)
            self.assertIn("memory-keeper", generated_agents)
            self.assertTrue(all("source_profile" in entry for entry in generated_agents.values()))
            self.assertEqual(generated_agents["architect"]["config_path"], "agents/architect.toml")
            self.assertEqual(
                generated_agents["architect"]["mcp_affinity"],
                ["aoa_workspace", "aoa_stats"],
            )
            self.assertEqual(
                generated_agents["memory-keeper"]["mcp_affinity"],
                ["aoa_workspace", "aoa_stats", "dionysus"],
            )

    def test_validator_accepts_generated_projection(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aoa-agents-codex-projection-") as temp_dir:
            root = Path(temp_dir)
            agents_dir = root / "agents"
            config_snippet = root / "config.toml"
            manifest = root / "manifest.json"
            build = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--profiles-root",
                    str(PROFILES_ROOT),
                    "--wiring",
                    str(WIRING_PATH),
                    "--output-dir",
                    str(agents_dir),
                    "--emit-config-snippet",
                    str(config_snippet),
                    "--emit-manifest",
                    str(manifest),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(build.returncode, 0, msg=build.stderr)

            validate = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATE_SCRIPT),
                    "--profiles-root",
                    str(PROFILES_ROOT),
                    "--wiring",
                    str(WIRING_PATH),
                    "--agents-dir",
                    str(agents_dir),
                    "--config-snippet",
                    str(config_snippet),
                    "--manifest",
                    str(manifest),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(validate.returncode, 0, msg=validate.stderr)


if __name__ == "__main__":
    unittest.main()
