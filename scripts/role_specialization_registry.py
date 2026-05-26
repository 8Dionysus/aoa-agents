from __future__ import annotations

import json
from pathlib import Path

from agent_profile_registry import BuildError, ROLES_DIR, describe_path, read_json

REPO_ROOT = Path(__file__).resolve().parents[1]
ROLE_SPECIALIZATION_CATALOG_PATH = REPO_ROOT / "generated" / "role_specialization_catalog.min.json"
ROLE_ORDER = ("architect", "coder", "reviewer", "evaluator", "memory-keeper")
REGISTRY_FIELDS = (
    "id",
    "role_id",
    "slug",
    "status",
    "summary",
    "inherits_from",
    "capability_pack_ref",
    "activation_triggers",
    "allowed_forms",
    "skill_refs",
    "technique_refs",
    "memory_route_refs",
    "proof_routes",
    "projection_notes",
    "stronger_owner_routes",
    "stop_lines",
)


def iter_role_specialization_paths(roles_dir: Path = ROLES_DIR) -> list[Path]:
    if not roles_dir.is_dir():
        raise BuildError(f"missing required directory: {describe_path(roles_dir)}")
    paths = sorted(roles_dir.glob("*/specializations/*/specialization.json"))
    if not paths:
        raise BuildError(f"no source-authored role specializations found in {describe_path(roles_dir)}")
    return paths


def load_role_specializations(roles_dir: Path = ROLES_DIR) -> list[dict[str, object]]:
    specializations: list[dict[str, object]] = []
    for path in iter_role_specialization_paths(roles_dir):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise BuildError(f"{describe_path(path)} must contain a JSON object")
        role_id = path.parents[2].name
        slug = path.parent.name
        expected_id = f"{role_id}.{slug}"
        if payload.get("role_id") != role_id:
            raise BuildError(f"{describe_path(path)} role_id must match parent role '{role_id}'")
        if payload.get("slug") != slug:
            raise BuildError(f"{describe_path(path)} slug must match parent specialization '{slug}'")
        if payload.get("id") != expected_id:
            raise BuildError(f"{describe_path(path)} id must equal '{expected_id}'")
        specializations.append(payload)
    role_index = {role: index for index, role in enumerate(ROLE_ORDER)}
    specializations.sort(
        key=lambda item: (
            role_index.get(str(item.get("role_id", "")), len(ROLE_ORDER)),
            str(item.get("slug", "")),
        )
    )
    return specializations


def build_role_specialization_catalog_payload(specializations: list[dict[str, object]]) -> dict[str, object]:
    role_specializations: list[dict[str, object]] = []
    for specialization in specializations:
        entry: dict[str, object] = {}
        for key in REGISTRY_FIELDS:
            if key not in specialization:
                raise BuildError(
                    "source role specialization "
                    f"'{specialization.get('id', '<unknown>')}' is missing required key '{key}'"
                )
            entry[key] = specialization[key]
        role_id = str(specialization["role_id"])
        slug = str(specialization["slug"])
        entry["source_path"] = f"agents/roles/{role_id}/specializations/{slug}/specialization.json"
        role_specializations.append(entry)
    return {
        "version": 1,
        "layer": "aoa-agents",
        "family": "role_specializations",
        "role_specializations": role_specializations,
    }


def write_role_specialization_catalog(path: Path = ROLE_SPECIALIZATION_CATALOG_PATH) -> dict[str, object]:
    specializations = load_role_specializations()
    payload = build_role_specialization_catalog_payload(specializations)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
