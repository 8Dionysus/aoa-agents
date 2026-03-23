from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = REPO_ROOT / "profiles"
AGENT_REGISTRY_PATH = REPO_ROOT / "generated" / "agent_registry.min.json"
PROFILE_SUFFIX = ".profile.json"
REGISTRY_FIELDS = (
    "id",
    "name",
    "role",
    "status",
    "summary",
    "preferred_skill_families",
    "memory_posture",
    "memory_rights",
    "evaluation_posture",
    "handoff_rule",
)


class BuildError(RuntimeError):
    pass


def describe_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BuildError(f"missing required file: {describe_path(path)}") from exc
    except json.JSONDecodeError as exc:
        raise BuildError(f"invalid JSON in {describe_path(path)}: {exc}") from exc


def iter_profile_paths(profile_dir: Path = PROFILES_DIR) -> list[Path]:
    if not profile_dir.is_dir():
        raise BuildError(f"missing required directory: {describe_path(profile_dir)}")
    paths = sorted(profile_dir.glob(f"*{PROFILE_SUFFIX}"))
    if not paths:
        raise BuildError(f"no source-authored agent profiles found in {describe_path(profile_dir)}")
    return paths


def load_profiles(profile_dir: Path = PROFILES_DIR) -> list[dict[str, object]]:
    profiles: list[dict[str, object]] = []
    for path in iter_profile_paths(profile_dir):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise BuildError(f"{describe_path(path)} must contain a JSON object")
        expected_name = path.name[: -len(PROFILE_SUFFIX)]
        actual_name = payload.get("name")
        if not isinstance(actual_name, str):
            raise BuildError(f"{describe_path(path)} must declare a string 'name'")
        if actual_name != expected_name:
            raise BuildError(
                f"{describe_path(path)} name '{actual_name}' must match file stem '{expected_name}'"
            )
        profiles.append(payload)
    profiles.sort(key=lambda profile: (str(profile.get("id", "")), str(profile.get("name", ""))))
    return profiles


def build_agent_registry_payload(profiles: list[dict[str, object]]) -> dict[str, object]:
    agents: list[dict[str, object]] = []
    for profile in profiles:
        entry: dict[str, object] = {}
        for key in REGISTRY_FIELDS:
            if key not in profile:
                raise BuildError(f"source profile '{profile.get('name', '<unknown>')}' is missing required key '{key}'")
            entry[key] = profile[key]
        agents.append(entry)
    return {
        "version": 1,
        "layer": "aoa-agents",
        "agents": agents,
    }


def write_agent_registry(path: Path = AGENT_REGISTRY_PATH) -> dict[str, object]:
    profiles = load_profiles()
    payload = build_agent_registry_payload(profiles)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
