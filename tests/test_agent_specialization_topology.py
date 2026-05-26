from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class AgentSpecializationTopologyTests(unittest.TestCase):
    def test_specializations_stay_inside_role_houses(self) -> None:
        paths = sorted((REPO_ROOT / "agents" / "roles").glob("*/specializations/*/specialization.json"))
        self.assertGreaterEqual(len(paths), 5)

        for path in paths:
            payload = json.loads(path.read_text(encoding="utf-8"))
            role_id = path.parents[2].name
            slug = path.parent.name
            self.assertEqual(payload["role_id"], role_id)
            self.assertEqual(payload["slug"], slug)
            self.assertEqual(payload["id"], f"{role_id}.{slug}")
            self.assertEqual(payload["inherits_from"], f"agents/roles/{role_id}/profile.json")
            self.assertTrue((REPO_ROOT / payload["inherits_from"]).is_file())

    def test_capability_refs_resolve_to_operating_model_packs(self) -> None:
        capability_paths = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in (REPO_ROOT / "agents" / "operating-model" / "capabilities" / "packs").glob(
                "*.capability.json"
            )
        }
        self.assertGreaterEqual(len(capability_paths), 5)

        for path in sorted((REPO_ROOT / "agents" / "roles").glob("*/specializations/*/specialization.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn(payload["capability_pack_ref"], capability_paths)

    def test_generated_readers_are_declared_by_source_home(self) -> None:
        manifest = json.loads((REPO_ROOT / "agents" / "source_home.manifest.json").read_text(encoding="utf-8"))
        families = {family["id"]: family for family in manifest["families"]}
        self.assertEqual(
            families["role_specializations"]["publishes_to"],
            ["generated/role_specialization_catalog.min.json"],
        )
        self.assertEqual(
            families["capability_packs"]["publishes_to"],
            ["generated/capability_pack_registry.min.json"],
        )


if __name__ == "__main__":
    unittest.main()
