from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_active_organ_agent_local_namespace import validate_namespace


SCHEMA_PATH = ROOT / "schemas" / "active-organ-agent-local-namespace-v0.schema.json"
EXAMPLE_PATH = ROOT / "examples" / "active-organ-agent-local-namespace.example.json"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(payload: dict[str, object]) -> None:
    jsonschema.Draft202012Validator(load(SCHEMA_PATH)).validate(payload)


def test_agent_local_namespace_example_is_strict_and_role_bound() -> None:
    payload = load(EXAMPLE_PATH)
    validate_namespace(payload, schema=load(SCHEMA_PATH), repo_root=ROOT)
    role_ref = ROOT / str(payload["role_profile_ref"])
    role = load(role_ref)
    assert payload["agent_id"] == role["id"]
    assert payload["shared_promotion"]["right"] == "nominate_only"
    assert payload["shared_promotion"]["direct_shared_write"] == "forbidden"
    assert payload["degraded_mode"]["shared_organ_available"] is True


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("isolation", "cross_agent_read"), "allowed"),
        (("isolation", "private_to_shared_default"), "allowed"),
        (("ranking_adaptation", "max_absolute_weight_delta"), 0.9),
        (("ranking_adaptation", "access_count_as_utility"), "allowed"),
        (("shared_promotion", "right"), "publish"),
        (("shared_promotion", "review_required"), False),
        (("rollback", "shared_ledger_effect"), "delete"),
        (("degraded_mode", "shared_organ_available"), False),
        (("authority", "memory_object_truth"), "allowed"),
    ],
)
def test_agent_local_namespace_rejects_authority_and_isolation_drift(
    path: tuple[str, ...],
    value: object,
) -> None:
    payload = copy.deepcopy(load(EXAMPLE_PATH))
    cursor: dict[str, object] = payload
    for key in path[:-1]:
        cursor = cursor[key]  # type: ignore[assignment,index]
    cursor[path[-1]] = value
    with pytest.raises(jsonschema.ValidationError):
        validate(payload)


def test_namespace_identity_cannot_be_reused_for_another_agent() -> None:
    payload = load(EXAMPLE_PATH)
    payload["agent_id"] = "AOA-A-0003"
    validate(payload)
    with pytest.raises(ValueError, match="role profile id"):
        validate_namespace(payload, schema=load(SCHEMA_PATH), repo_root=ROOT)
