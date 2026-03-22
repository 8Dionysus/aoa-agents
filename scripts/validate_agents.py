#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "generated" / "agent_registry.min.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent-registry.schema.json"
MODEL_TIER_REGISTRY_PATH = REPO_ROOT / "generated" / "model_tier_registry.json"
MODEL_TIER_SCHEMA_PATH = REPO_ROOT / "schemas" / "model-tier-registry.schema.json"

ALLOWED_STATUS = {"active", "planned", "experimental", "deprecated"}
ALLOWED_MEMORY_POSTURE = {"none", "light_recall", "bounded_recall", "deep_recall"}
ALLOWED_MEMORY_BANDS = {"core", "hot", "warm", "cool", "cold", "frozen"}
ALLOWED_RECALL_SCOPES = {"repo", "project", "ecosystem"}
ALLOWED_PROMOTION_TRANSITIONS = {"hot_to_warm", "warm_to_cool", "cool_to_cold", "cold_to_cool"}
ALLOWED_EVAL_POSTURE = {"minimal", "required", "strict", "paired_eval"}
ALLOWED_HANDOFF = {"solo_ok", "handoff_on_ambiguity", "handoff_on_risk", "review_required"}
REQUIRED_MODEL_TIERS = {"router", "planner", "executor", "verifier", "conductor", "deep", "archivist"}
ALLOWED_TIER_MEMORY_SCOPE = {
    "core",
    "selected_hot",
    "selected_warm",
    "selected_cool",
    "selected_cold",
    "selected_frozen",
}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(REPO_ROOT).as_posix()}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(REPO_ROOT).as_posix()}: {exc}")


def validate_schema_surface() -> None:
    schema = read_json(SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("schema file must contain a JSON object")
    required_top_level = {"$schema", "$id", "title", "type", "properties", "required"}
    missing = sorted(required_top_level - set(schema))
    if missing:
        fail(f"schema is missing required top-level keys: {', '.join(missing)}")


def validate_model_tier_schema_surface() -> None:
    schema = read_json(MODEL_TIER_SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("model-tier schema file must contain a JSON object")
    required_top_level = {"$schema", "$id", "title", "type", "properties", "required"}
    missing = sorted(required_top_level - set(schema))
    if missing:
        fail(f"model-tier schema is missing required top-level keys: {', '.join(missing)}")


def validate_registry() -> None:
    payload = read_json(REGISTRY_PATH)
    if not isinstance(payload, dict):
        fail("agent registry must be a JSON object")

    for key in ("version", "layer", "agents"):
        if key not in payload:
            fail(f"agent registry is missing required key '{key}'")

    if not isinstance(payload["version"], int) or payload["version"] < 1:
        fail("registry 'version' must be an integer >= 1")
    if payload["layer"] != "aoa-agents":
        fail("registry 'layer' must equal 'aoa-agents'")

    agents = payload["agents"]
    if not isinstance(agents, list) or not agents:
        fail("registry 'agents' must be a non-empty list")

    seen_ids: set[str] = set()
    required_seed = {"architect", "coder", "reviewer", "evaluator", "memory-keeper"}
    seen_names: set[str] = set()

    for index, agent in enumerate(agents):
        location = f"agents[{index}]"
        if not isinstance(agent, dict):
            fail(f"{location} must be an object")

        for key in (
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
        ):
            if key not in agent:
                fail(f"{location} is missing required key '{key}'")

        agent_id = agent["id"]
        name = agent["name"]
        role = agent["role"]
        status = agent["status"]
        summary = agent["summary"]
        preferred_skill_families = agent["preferred_skill_families"]
        memory_posture = agent["memory_posture"]
        memory_rights = agent["memory_rights"]
        evaluation_posture = agent["evaluation_posture"]
        handoff_rule = agent["handoff_rule"]

        if not isinstance(agent_id, str) or len(agent_id) < 3:
            fail(f"{location}.id must be a string of length >= 3")
        if agent_id in seen_ids:
            fail(f"duplicate agent id in registry: '{agent_id}'")
        seen_ids.add(agent_id)

        if not isinstance(name, str) or len(name) < 3:
            fail(f"{location}.name must be a string of length >= 3")
        seen_names.add(name)
        if not isinstance(role, str) or len(role) < 3:
            fail(f"{location}.role must be a string of length >= 3")
        if status not in ALLOWED_STATUS:
            fail(f"{location}.status '{status}' is not allowed")
        if not isinstance(summary, str) or len(summary) < 10:
            fail(f"{location}.summary must be a string of length >= 10")
        if not isinstance(preferred_skill_families, list) or not preferred_skill_families:
            fail(f"{location}.preferred_skill_families must be a non-empty list")
        for skill_family in preferred_skill_families:
            if not isinstance(skill_family, str) or len(skill_family) < 2:
                fail(f"{location}.preferred_skill_families contains an invalid entry")
        if memory_posture not in ALLOWED_MEMORY_POSTURE:
            fail(f"{location}.memory_posture '{memory_posture}' is not allowed")
        validate_memory_rights(location, memory_rights)
        if evaluation_posture not in ALLOWED_EVAL_POSTURE:
            fail(f"{location}.evaluation_posture '{evaluation_posture}' is not allowed")
        if handoff_rule not in ALLOWED_HANDOFF:
            fail(f"{location}.handoff_rule '{handoff_rule}' is not allowed")

    missing_seed = sorted(required_seed - seen_names)
    if missing_seed:
        fail(f"agent registry is missing required seed agents: {', '.join(missing_seed)}")


def validate_model_tier_registry() -> None:
    payload = read_json(MODEL_TIER_REGISTRY_PATH)
    if not isinstance(payload, dict):
        fail("model-tier registry must be a JSON object")

    for key in ("version", "layer", "model_tiers"):
        if key not in payload:
            fail(f"model-tier registry is missing required key '{key}'")

    if not isinstance(payload["version"], int) or payload["version"] < 1:
        fail("model-tier registry 'version' must be an integer >= 1")
    if payload["layer"] != "aoa-agents":
        fail("model-tier registry 'layer' must equal 'aoa-agents'")

    model_tiers = payload["model_tiers"]
    if not isinstance(model_tiers, list) or not model_tiers:
        fail("model-tier registry 'model_tiers' must be a non-empty list")

    seen_ids: set[str] = set()
    for index, tier in enumerate(model_tiers):
        location = f"model_tiers[{index}]"
        if not isinstance(tier, dict):
            fail(f"{location} must be an object")

        for key in (
            "id",
            "status",
            "summary",
            "primary_duty",
            "output_contract",
            "default_memory_scope",
            "handoff_targets",
            "artifact_requirement",
        ):
            if key not in tier:
                fail(f"{location} is missing required key '{key}'")

        tier_id = tier["id"]
        status = tier["status"]
        summary = tier["summary"]
        primary_duty = tier["primary_duty"]
        output_contract = tier["output_contract"]
        default_memory_scope = tier["default_memory_scope"]
        handoff_targets = tier["handoff_targets"]
        artifact_requirement = tier["artifact_requirement"]

        if not isinstance(tier_id, str) or len(tier_id) < 3:
            fail(f"{location}.id must be a string of length >= 3")
        if tier_id in seen_ids:
            fail(f"duplicate model tier id in registry: '{tier_id}'")
        seen_ids.add(tier_id)

        if status not in ALLOWED_STATUS:
            fail(f"{location}.status '{status}' is not allowed")
        if not isinstance(summary, str) or len(summary) < 10:
            fail(f"{location}.summary must be a string of length >= 10")
        if not isinstance(primary_duty, str) or len(primary_duty) < 3:
            fail(f"{location}.primary_duty must be a string of length >= 3")
        if not isinstance(output_contract, str) or len(output_contract) < 5:
            fail(f"{location}.output_contract must be a string of length >= 5")
        if not isinstance(artifact_requirement, str) or len(artifact_requirement) < 3:
            fail(f"{location}.artifact_requirement must be a string of length >= 3")

        for array_name, value in (
            ("default_memory_scope", default_memory_scope),
            ("handoff_targets", handoff_targets),
        ):
            if not isinstance(value, list) or not value:
                fail(f"{location}.{array_name} must be a non-empty list")
            for item in value:
                if not isinstance(item, str) or len(item) < 2:
                    fail(f"{location}.{array_name} contains an invalid entry")
                if array_name == "default_memory_scope" and item not in ALLOWED_TIER_MEMORY_SCOPE:
                    fail(f"{location}.{array_name} contains unsupported scope '{item}'")

        if "activation_conditions" in tier:
            activation_conditions = tier.get("activation_conditions")
            if not isinstance(activation_conditions, list):
                fail(f"{location}.activation_conditions must be a list when present")
            for item in activation_conditions:
                if not isinstance(item, str) or len(item) < 3:
                    fail(f"{location}.activation_conditions contains an invalid entry")

    missing_tiers = sorted(REQUIRED_MODEL_TIERS - seen_ids)
    if missing_tiers:
        fail(f"model-tier registry is missing required tiers: {', '.join(missing_tiers)}")


def validate_memory_rights(location: str, memory_rights: object) -> None:
    if not isinstance(memory_rights, dict):
        fail(f"{location}.memory_rights must be an object")

    required_keys = {
        "default_read_bands",
        "default_write_bands",
        "allowed_recall_scopes",
        "promotion_rights",
        "freeze_rights",
    }
    missing = sorted(required_keys - set(memory_rights))
    if missing:
        fail(f"{location}.memory_rights is missing required keys: {', '.join(missing)}")

    for array_name, allowed_values in (
        ("default_read_bands", ALLOWED_MEMORY_BANDS),
        ("default_write_bands", ALLOWED_MEMORY_BANDS),
        ("allowed_recall_scopes", ALLOWED_RECALL_SCOPES),
    ):
        value = memory_rights[array_name]
        if not isinstance(value, list) or not value:
            fail(f"{location}.memory_rights.{array_name} must be a non-empty list")
        for item in value:
            if item not in allowed_values:
                fail(f"{location}.memory_rights.{array_name} contains unsupported value '{item}'")

    promotion_rights = memory_rights["promotion_rights"]
    if not isinstance(promotion_rights, dict):
        fail(f"{location}.memory_rights.promotion_rights must be an object")
    for key in (
        "can_nominate",
        "can_confirm",
        "can_promote",
        "can_demote",
        "can_retire",
        "can_rescue",
        "allowed_transitions",
    ):
        if key not in promotion_rights:
            fail(f"{location}.memory_rights.promotion_rights is missing required key '{key}'")
    for key in ("can_nominate", "can_confirm", "can_promote", "can_demote", "can_retire", "can_rescue"):
        if not isinstance(promotion_rights[key], bool):
            fail(f"{location}.memory_rights.promotion_rights.{key} must be a boolean")
    allowed_transitions = promotion_rights["allowed_transitions"]
    if not isinstance(allowed_transitions, list):
        fail(f"{location}.memory_rights.promotion_rights.allowed_transitions must be a list")
    for item in allowed_transitions:
        if item not in ALLOWED_PROMOTION_TRANSITIONS:
            fail(
                f"{location}.memory_rights.promotion_rights.allowed_transitions contains unsupported value '{item}'"
            )

    freeze_rights = memory_rights["freeze_rights"]
    if not isinstance(freeze_rights, dict):
        fail(f"{location}.memory_rights.freeze_rights must be an object")
    for key in ("can_recommend", "can_prepare", "can_finalize"):
        if key not in freeze_rights:
            fail(f"{location}.memory_rights.freeze_rights is missing required key '{key}'")
        if not isinstance(freeze_rights[key], bool):
            fail(f"{location}.memory_rights.freeze_rights.{key} must be a boolean")


def main() -> int:
    try:
        validate_schema_surface()
        validate_model_tier_schema_surface()
        validate_registry()
        validate_model_tier_registry()
    except ValidationError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[ok] validated agent registry schema surface")
    print("[ok] validated model-tier registry schema surface")
    print("[ok] validated generated/agent_registry.min.json")
    print("[ok] validated generated/model_tier_registry.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
