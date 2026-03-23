from __future__ import annotations

import json
from pathlib import Path

from agent_profile_registry import BuildError, describe_path, read_json

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SEAM_DIR = REPO_ROOT / "runtime_seam"
RUNTIME_SEAM_BINDINGS_PATH = REPO_ROOT / "generated" / "runtime_seam_bindings.json"
RUNTIME_SEAM_BINDING_SUFFIX = ".binding.json"
RUNTIME_PHASE_ORDER = (
    "route",
    "plan",
    "do",
    "verify",
    "transition",
    "deep",
    "distill",
)
REGISTRY_FIELDS = (
    "phase",
    "tier_id",
    "role_names",
    "artifact_type",
)


def iter_runtime_seam_binding_paths(runtime_seam_dir: Path = RUNTIME_SEAM_DIR) -> list[Path]:
    if not runtime_seam_dir.is_dir():
        raise BuildError(f"missing required directory: {describe_path(runtime_seam_dir)}")
    paths = sorted(runtime_seam_dir.glob(f"*{RUNTIME_SEAM_BINDING_SUFFIX}"))
    if not paths:
        raise BuildError(f"no source-authored runtime seam bindings found in {describe_path(runtime_seam_dir)}")
    return paths


def load_runtime_seam_bindings(runtime_seam_dir: Path = RUNTIME_SEAM_DIR) -> list[dict[str, object]]:
    bindings: list[dict[str, object]] = []
    order_index = {phase: index for index, phase in enumerate(RUNTIME_PHASE_ORDER)}
    for path in iter_runtime_seam_binding_paths(runtime_seam_dir):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise BuildError(f"{describe_path(path)} must contain a JSON object")
        expected_phase = path.name[: -len(RUNTIME_SEAM_BINDING_SUFFIX)]
        actual_phase = payload.get("phase")
        if not isinstance(actual_phase, str):
            raise BuildError(f"{describe_path(path)} must declare a string 'phase'")
        if actual_phase != expected_phase:
            raise BuildError(f"{describe_path(path)} phase '{actual_phase}' must match file stem '{expected_phase}'")
        if actual_phase not in order_index:
            raise BuildError(f"{describe_path(path)} uses unsupported runtime phase '{actual_phase}'")
        bindings.append(payload)
    bindings.sort(key=lambda binding: order_index[str(binding.get("phase", ""))])
    return bindings


def build_runtime_seam_registry_payload(bindings: list[dict[str, object]]) -> dict[str, object]:
    published_bindings: list[dict[str, object]] = []
    for binding in bindings:
        entry: dict[str, object] = {}
        for key in REGISTRY_FIELDS:
            if key not in binding:
                raise BuildError(
                    f"source runtime seam binding '{binding.get('phase', '<unknown>')}' is missing required key '{key}'"
                )
            entry[key] = binding[key]
        published_bindings.append(entry)
    return {
        "version": 1,
        "layer": "aoa-agents",
        "bindings": published_bindings,
    }


def write_runtime_seam_registry(path: Path = RUNTIME_SEAM_BINDINGS_PATH) -> dict[str, object]:
    bindings = load_runtime_seam_bindings()
    payload = build_runtime_seam_registry_payload(bindings)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
