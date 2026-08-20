#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "active-organ-agent-local-namespace-v0.schema.json"
DEFAULT_INSTANCE = ROOT / "examples" / "active-organ-agent-local-namespace.example.json"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def validate_namespace(
    payload: dict[str, Any],
    *,
    schema: dict[str, Any],
    repo_root: Path = ROOT,
) -> None:
    jsonschema.Draft202012Validator(schema).validate(payload)
    role_ref = repo_root / payload["role_profile_ref"]
    if not role_ref.is_file():
        raise ValueError(f"role_profile_ref does not exist: {payload['role_profile_ref']}")
    role = read_json(role_ref)
    if payload["agent_id"] != role.get("id"):
        raise ValueError("agent_id must equal the referenced role profile id")
    namespace_suffix = payload["namespace_id"].removeprefix("namespace:")
    if not namespace_suffix.startswith(f"{role.get('name')}-"):
        raise ValueError("namespace_id must begin with the referenced role name")
    if payload["rollback"]["target_generation"] >= payload["namespace_generation"]:
        raise ValueError("rollback target_generation must precede namespace_generation")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--instance", type=Path, default=DEFAULT_INSTANCE)
    args = parser.parse_args()
    validate_namespace(
        read_json(args.instance),
        schema=read_json(args.schema),
        repo_root=ROOT,
    )
    print("[ok] active-organ agent-local namespace is role-bound and fail-closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
