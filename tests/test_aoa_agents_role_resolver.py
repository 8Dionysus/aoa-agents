from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESOLVER_PATH = (
    ROOT / "skills" / "aoa-agents-skills" / "scripts" / "resolve_role_binding.py"
)
SPEC = importlib.util.spec_from_file_location("aoa_agents_role_resolver", RESOLVER_PATH)
assert SPEC is not None and SPEC.loader is not None
RESOLVER = importlib.util.module_from_spec(SPEC)
_previous_dont_write_bytecode = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    SPEC.loader.exec_module(RESOLVER)
finally:
    sys.dont_write_bytecode = _previous_dont_write_bytecode


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _owner_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "aoa-agents"
    root.mkdir()
    shutil.copytree(ROOT / "agents", root / "agents")
    shutil.copytree(ROOT / "schemas", root / "schemas")
    _git(root, "init", "-b", "main")
    _git(root, "config", "user.name", "Fixture")
    _git(root, "config", "user.email", "fixture@example.invalid")
    _git(root, "add", "agents", "schemas")
    _git(root, "commit", "-m", "fixture owner source")
    return root


class RoleResolverTests(unittest.TestCase):
    def test_resolves_exact_coder_specialization_chain_without_selecting_compute(
        self,
    ) -> None:
        result = RESOLVER.resolve_role_binding(
            ROOT,
            role_id="coder",
            specialization_id="coder.repo-refactor",
            tier_id="executor",
        )

        self.assertEqual(result["role_id"], "coder")
        self.assertEqual(result["specialization_id"], "coder.repo-refactor")
        self.assertEqual(
            result["base_role_ref"]["artifact_ref"], "agents/roles/coder/profile.json"
        )
        self.assertTrue(
            result["specialization_ref"]["artifact_ref"].endswith(
                "/coder/specializations/repo-refactor/specialization.json"
            )
        )
        self.assertTrue(
            result["tier_ref"]["artifact_ref"].endswith("/executor.tier.json")
        )
        self.assertTrue(
            result["capability_pack_refs"][0]["artifact_ref"].endswith(
                "/repo-refactor.workspace-write.capability.json"
            )
        )
        self.assertEqual(
            result["selection_authority"],
            {
                "semantic_selection_performed": False,
                "model_selection_performed": False,
                "runtime_activation_performed": False,
            },
        )
        self.assertNotIn("luna", json.dumps(result).lower())
        self.assertNotIn("budget", json.dumps(result).lower())
        RESOLVER.assert_resolution_digest(result)

    def test_base_role_resolution_has_no_invented_capability_pack(self) -> None:
        result = RESOLVER.resolve_role_binding(
            ROOT,
            role_id="memory-keeper",
            tier_id="archivist",
        )

        self.assertIsNone(result["specialization_id"])
        self.assertIsNone(result["specialization_ref"])
        self.assertEqual(result["capability_pack_refs"], [])

    def test_rejects_specialization_from_another_role(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            root = _owner_fixture(Path(temp_root))
            path = (
                root
                / "agents/roles/coder/specializations/repo-refactor/specialization.json"
            )
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["role_id"] = "evaluator"
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            _git(root, "add", str(path.relative_to(root)))
            _git(root, "commit", "-m", "mismatched specialization")

            with self.assertRaisesRegex(
                RESOLVER.RoleResolutionError,
                "does not belong to role coder",
            ):
                RESOLVER.resolve_role_binding(
                    root,
                    role_id="coder",
                    specialization_id="coder.repo-refactor",
                    tier_id="executor",
                )

    def test_rejects_dirty_selected_owner_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            root = _owner_fixture(Path(temp_root))
            profile = root / "agents/roles/coder/profile.json"
            profile.write_text(
                profile.read_text(encoding="utf-8") + "\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(
                RESOLVER.RoleResolutionError,
                "selected aoa-agents role sources are dirty",
            ):
                RESOLVER.resolve_role_binding(
                    root,
                    role_id="coder",
                    specialization_id="coder.repo-refactor",
                    tier_id="executor",
                )

    def test_rejects_tier_not_declared_by_selected_role(self) -> None:
        with self.assertRaisesRegex(
            RESOLVER.RoleResolutionError,
            "tier archivist is not declared by base role coder",
        ):
            RESOLVER.resolve_role_binding(
                ROOT,
                role_id="coder",
                specialization_id="coder.repo-refactor",
                tier_id="archivist",
            )

    def test_digest_tampering_fails_closed(self) -> None:
        result = RESOLVER.resolve_role_binding(
            ROOT,
            role_id="evaluator",
            specialization_id="evaluator.release-readiness",
            tier_id="deep",
        )
        result["role_id"] = "coder"

        with self.assertRaisesRegex(RESOLVER.RoleResolutionError, "digest mismatch"):
            RESOLVER.assert_resolution_digest(result)
