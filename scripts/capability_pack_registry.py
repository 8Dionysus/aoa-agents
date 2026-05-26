from __future__ import annotations

import json
from pathlib import Path

from agent_profile_registry import BuildError, describe_path, read_json

REPO_ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_PACKS_DIR = REPO_ROOT / "agents" / "operating-model" / "capabilities" / "packs"
CAPABILITY_PACK_REGISTRY_PATH = REPO_ROOT / "generated" / "capability_pack_registry.min.json"
CAPABILITY_PACK_SUFFIX = ".capability.json"
REGISTRY_FIELDS = (
    "id",
    "status",
    "summary",
    "permission_posture",
    "tool_refs",
    "skill_refs",
    "technique_refs",
    "memory_routes",
    "proof_routes",
    "projection_hints",
    "owner_boundaries",
    "stop_lines",
)


def iter_capability_pack_paths(capability_packs_dir: Path = CAPABILITY_PACKS_DIR) -> list[Path]:
    if not capability_packs_dir.is_dir():
        raise BuildError(f"missing required directory: {describe_path(capability_packs_dir)}")
    paths = sorted(capability_packs_dir.glob(f"*{CAPABILITY_PACK_SUFFIX}"))
    if not paths:
        raise BuildError(f"no source-authored capability packs found in {describe_path(capability_packs_dir)}")
    return paths


def load_capability_packs(capability_packs_dir: Path = CAPABILITY_PACKS_DIR) -> list[dict[str, object]]:
    packs: list[dict[str, object]] = []
    for path in iter_capability_pack_paths(capability_packs_dir):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise BuildError(f"{describe_path(path)} must contain a JSON object")
        expected_id = path.name[: -len(CAPABILITY_PACK_SUFFIX)]
        actual_id = payload.get("id")
        if not isinstance(actual_id, str):
            raise BuildError(f"{describe_path(path)} must declare a string 'id'")
        if actual_id != expected_id:
            raise BuildError(f"{describe_path(path)} id '{actual_id}' must match file stem '{expected_id}'")
        packs.append(payload)
    packs.sort(key=lambda pack: str(pack.get("id", "")))
    return packs


def build_capability_pack_registry_payload(packs: list[dict[str, object]]) -> dict[str, object]:
    capability_packs: list[dict[str, object]] = []
    for pack in packs:
        entry: dict[str, object] = {}
        for key in REGISTRY_FIELDS:
            if key not in pack:
                raise BuildError(
                    f"source capability pack '{pack.get('id', '<unknown>')}' is missing required key '{key}'"
                )
            entry[key] = pack[key]
        pack_id = str(pack["id"])
        entry["source_path"] = (
            f"agents/operating-model/capabilities/packs/{pack_id}{CAPABILITY_PACK_SUFFIX}"
        )
        capability_packs.append(entry)
    return {
        "version": 1,
        "layer": "aoa-agents",
        "family": "capability_packs",
        "capability_packs": capability_packs,
    }


def write_capability_pack_registry(path: Path = CAPABILITY_PACK_REGISTRY_PATH) -> dict[str, object]:
    packs = load_capability_packs()
    payload = build_capability_pack_registry_payload(packs)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
