from __future__ import annotations

import json
from pathlib import Path

from agent_profile_registry import BuildError, describe_path, read_json

REPO_ROOT = Path(__file__).resolve().parents[1]
COHORT_PATTERNS_DIR = REPO_ROOT / "cohort_patterns"
COHORT_REGISTRY_PATH = REPO_ROOT / "generated" / "cohort_composition_registry.json"
COHORT_PATTERN_SUFFIX = ".pattern.json"
COHORT_PATTERN_ORDER = (
    "solo",
    "pair",
    "checkpoint_cohort",
    "orchestrated_loop",
)
REGISTRY_FIELDS = (
    "id",
    "status",
    "summary",
    "allowed_role_sets",
    "preferred_tier_ids",
    "activation_conditions",
    "required_handoffs",
    "boundary_note",
)


def iter_cohort_pattern_paths(cohort_patterns_dir: Path = COHORT_PATTERNS_DIR) -> list[Path]:
    if not cohort_patterns_dir.is_dir():
        raise BuildError(f"missing required directory: {describe_path(cohort_patterns_dir)}")
    paths = sorted(cohort_patterns_dir.glob(f"*{COHORT_PATTERN_SUFFIX}"))
    if not paths:
        raise BuildError(f"no source-authored cohort patterns found in {describe_path(cohort_patterns_dir)}")
    return paths


def load_cohort_patterns(cohort_patterns_dir: Path = COHORT_PATTERNS_DIR) -> list[dict[str, object]]:
    patterns: list[dict[str, object]] = []
    order_index = {pattern_id: index for index, pattern_id in enumerate(COHORT_PATTERN_ORDER)}
    for path in iter_cohort_pattern_paths(cohort_patterns_dir):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise BuildError(f"{describe_path(path)} must contain a JSON object")
        expected_id = path.name[: -len(COHORT_PATTERN_SUFFIX)]
        actual_id = payload.get("id")
        if not isinstance(actual_id, str):
            raise BuildError(f"{describe_path(path)} must declare a string 'id'")
        if actual_id != expected_id:
            raise BuildError(f"{describe_path(path)} id '{actual_id}' must match file stem '{expected_id}'")
        if actual_id not in order_index:
            raise BuildError(f"{describe_path(path)} uses unsupported cohort pattern id '{actual_id}'")
        patterns.append(payload)
    patterns.sort(key=lambda pattern: order_index[str(pattern.get("id", ""))])
    return patterns


def build_cohort_registry_payload(patterns: list[dict[str, object]]) -> dict[str, object]:
    cohort_patterns: list[dict[str, object]] = []
    for pattern in patterns:
        entry: dict[str, object] = {}
        for key in REGISTRY_FIELDS:
            if key not in pattern:
                raise BuildError(
                    f"source cohort pattern '{pattern.get('id', '<unknown>')}' is missing required key '{key}'"
                )
            entry[key] = pattern[key]
        cohort_patterns.append(entry)
    return {
        "version": 1,
        "layer": "aoa-agents",
        "cohort_patterns": cohort_patterns,
    }


def write_cohort_registry(path: Path = COHORT_REGISTRY_PATH) -> dict[str, object]:
    patterns = load_cohort_patterns()
    payload = build_cohort_registry_payload(patterns)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
