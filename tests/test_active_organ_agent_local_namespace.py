from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_active_organ_agent_local_namespace import validate_namespace


SCHEMA_PATH = ROOT / "schemas" / "active-organ-agent-local-namespace-v0.schema.json"
EXAMPLE_PATH = ROOT / "examples" / "active-organ-agent-local-namespace.example.json"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(payload: dict[str, object]) -> None:
    jsonschema.Draft202012Validator(load(SCHEMA_PATH)).validate(payload)


class ActiveOrganAgentLocalNamespaceTests(unittest.TestCase):
    def test_agent_local_namespace_example_is_strict_and_role_bound(self) -> None:
        payload = load(EXAMPLE_PATH)
        validate_namespace(payload, schema=load(SCHEMA_PATH), repo_root=ROOT)
        role_ref = ROOT / str(payload["role_profile_ref"])
        role = load(role_ref)
        self.assertEqual(payload["agent_id"], role["id"])
        self.assertEqual(payload["shared_promotion"]["right"], "nominate_only")
        self.assertEqual(payload["shared_promotion"]["direct_shared_write"], "forbidden")
        self.assertTrue(payload["degraded_mode"]["shared_organ_available"])

    def test_agent_local_namespace_rejects_authority_and_isolation_drift(self) -> None:
        cases = [
            (("isolation", "cross_agent_read"), "allowed"),
            (("isolation", "private_to_shared_default"), "allowed"),
            (("ranking_adaptation", "max_absolute_weight_delta"), 0.9),
            (("ranking_adaptation", "access_count_as_utility"), "allowed"),
            (("shared_promotion", "right"), "publish"),
            (("shared_promotion", "review_required"), False),
            (("rollback", "shared_ledger_effect"), "delete"),
            (("degraded_mode", "shared_organ_available"), False),
            (("authority", "memory_object_truth"), "allowed"),
        ]
        for path, value in cases:
            with self.subTest(path=path, value=value):
                payload = copy.deepcopy(load(EXAMPLE_PATH))
                cursor: dict[str, object] = payload
                for key in path[:-1]:
                    cursor = cursor[key]  # type: ignore[assignment,index]
                cursor[path[-1]] = value
                with self.assertRaises(jsonschema.ValidationError):
                    validate(payload)

    def test_namespace_identity_cannot_be_reused_for_another_agent(self) -> None:
        payload = load(EXAMPLE_PATH)
        payload["agent_id"] = "AOA-A-0003"
        validate(payload)
        with self.assertRaisesRegex(ValueError, "role profile id"):
            validate_namespace(payload, schema=load(SCHEMA_PATH), repo_root=ROOT)

    def test_rollback_cannot_target_a_future_generation(self) -> None:
        payload = load(EXAMPLE_PATH)
        payload["rollback"]["target_generation"] = 4
        validate(payload)
        with self.assertRaisesRegex(ValueError, "target_generation"):
            validate_namespace(payload, schema=load(SCHEMA_PATH), repo_root=ROOT)
