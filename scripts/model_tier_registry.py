from __future__ import annotations

import json
from pathlib import Path

from agent_profile_registry import BuildError, describe_path, read_json
from artifact_identity import build_generated_registry_artifact_identity

REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_TIERS_DIR = REPO_ROOT / "agents" / "operating-model" / "tiers"
MODEL_TIER_REGISTRY_PATH = REPO_ROOT / "generated" / "model_tier_registry.json"
MODEL_TIER_SUFFIX = ".tier.json"
MODEL_TIER_ORDER = (
    "router",
    "planner",
    "executor",
    "verifier",
    "conductor",
    "deep",
    "archivist",
)
REGISTRY_FIELDS = (
    "id",
    "status",
    "summary",
    "primary_duty",
    "output_contract",
    "default_memory_scope",
    "handoff_targets",
    "artifact_requirement",
    "activation_conditions",
)
MODEL_TIER_REGISTRY_ARTIFACT_IDENTITY = build_generated_registry_artifact_identity(
    artifact_class="agent_model_tier_registry",
    surface_state="public_generated_agent_operating_model_registry",
    authority_ref="agents/operating-model/tiers/AGENTS.md",
    producer=(
        "scripts/build_published_surfaces.py via scripts/model_tier_registry.py "
        "from agents/operating-model/tiers/*.tier.json"
    ),
    consumer_expectation=(
        "Verify version, layer, artifact_identity, source tier objects, artifact "
        "requirements, schema, builder parity, and validate_agents before using "
        "this as tier orientation; do not treat tiers as vendor model brands, "
        "routing policy, playbook canon, or runtime implementation."
    ),
    content_identity=(
        "generated/model_tier_registry.json rebuilt from "
        "agents/operating-model/tiers/*.tier.json and compared by scripts/validate_agents.py."
    ),
    abi_epoch="aoa_agents_model_tier_registry_v1",
    contract_version="schemas/model-tier-registry.schema.json@aoa_agents_model_tier_registry_v1#artifact_identity",
)


def iter_model_tier_paths(model_tiers_dir: Path = MODEL_TIERS_DIR) -> list[Path]:
    if not model_tiers_dir.is_dir():
        raise BuildError(f"missing required directory: {describe_path(model_tiers_dir)}")
    paths = sorted(model_tiers_dir.glob(f"*{MODEL_TIER_SUFFIX}"))
    if not paths:
        raise BuildError(f"no source-authored model tiers found in {describe_path(model_tiers_dir)}")
    return paths


def load_model_tiers(model_tiers_dir: Path = MODEL_TIERS_DIR) -> list[dict[str, object]]:
    tiers: list[dict[str, object]] = []
    order_index = {tier_id: index for index, tier_id in enumerate(MODEL_TIER_ORDER)}
    for path in iter_model_tier_paths(model_tiers_dir):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise BuildError(f"{describe_path(path)} must contain a JSON object")
        expected_id = path.name[: -len(MODEL_TIER_SUFFIX)]
        actual_id = payload.get("id")
        if not isinstance(actual_id, str):
            raise BuildError(f"{describe_path(path)} must declare a string 'id'")
        if actual_id != expected_id:
            raise BuildError(f"{describe_path(path)} id '{actual_id}' must match file stem '{expected_id}'")
        if actual_id not in order_index:
            raise BuildError(f"{describe_path(path)} uses unsupported model tier id '{actual_id}'")
        tiers.append(payload)
    tiers.sort(key=lambda tier: order_index[str(tier.get("id", ""))])
    return tiers


def build_model_tier_registry_payload(tiers: list[dict[str, object]]) -> dict[str, object]:
    model_tiers: list[dict[str, object]] = []
    for tier in tiers:
        entry: dict[str, object] = {}
        for key in REGISTRY_FIELDS:
            if key not in tier:
                raise BuildError(f"source model tier '{tier.get('id', '<unknown>')}' is missing required key '{key}'")
            entry[key] = tier[key]
        model_tiers.append(entry)
    return {
        "version": 1,
        "layer": "aoa-agents",
        "artifact_identity": MODEL_TIER_REGISTRY_ARTIFACT_IDENTITY,
        "model_tiers": model_tiers,
    }


def write_model_tier_registry(path: Path = MODEL_TIER_REGISTRY_PATH) -> dict[str, object]:
    tiers = load_model_tiers()
    payload = build_model_tier_registry_payload(tiers)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
