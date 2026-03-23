#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "generated" / "agent_registry.min.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent-registry.schema.json"
MODEL_TIER_REGISTRY_PATH = REPO_ROOT / "generated" / "model_tier_registry.json"
MODEL_TIER_SCHEMA_PATH = REPO_ROOT / "schemas" / "model-tier-registry.schema.json"
COHORT_COMPOSITION_REGISTRY_PATH = REPO_ROOT / "generated" / "cohort_composition_registry.json"
COHORT_COMPOSITION_SCHEMA_PATH = REPO_ROOT / "schemas" / "cohort-composition-registry.schema.json"
RUNTIME_SEAM_BINDINGS_PATH = REPO_ROOT / "generated" / "runtime_seam_bindings.json"
RUNTIME_SEAM_BINDINGS_SCHEMA_PATH = REPO_ROOT / "schemas" / "runtime-seam-bindings.schema.json"
RUNTIME_ARTIFACT_EXAMPLES_DIR = REPO_ROOT / "examples" / "runtime_artifacts"
RUNTIME_ARTIFACT_INVALID_DIR = RUNTIME_ARTIFACT_EXAMPLES_DIR / "invalid"
RUNTIME_ARTIFACT_SCHEMA_PATHS = {
    "route_decision": REPO_ROOT / "schemas" / "artifact.route_decision.schema.json",
    "bounded_plan": REPO_ROOT / "schemas" / "artifact.bounded_plan.schema.json",
    "work_result": REPO_ROOT / "schemas" / "artifact.work_result.schema.json",
    "verification_result": REPO_ROOT / "schemas" / "artifact.verification_result.schema.json",
    "transition_decision": REPO_ROOT / "schemas" / "artifact.transition_decision.schema.json",
    "deep_synthesis_note": REPO_ROOT / "schemas" / "artifact.deep_synthesis_note.schema.json",
    "distillation_pack": REPO_ROOT / "schemas" / "artifact.distillation_pack.schema.json",
}

ALLOWED_STATUS = {"active", "planned", "experimental", "deprecated"}
ALLOWED_MEMORY_POSTURE = {"none", "light_recall", "bounded_recall", "deep_recall"}
ALLOWED_MEMORY_BANDS = {"core", "hot", "warm", "cool", "cold", "frozen"}
ALLOWED_RECALL_SCOPES = {"repo", "project", "ecosystem"}
ALLOWED_PROMOTION_TRANSITIONS = {"hot_to_warm", "warm_to_cool", "cool_to_cold", "cold_to_cool"}
ALLOWED_EVAL_POSTURE = {"minimal", "required", "strict", "paired_eval"}
ALLOWED_HANDOFF = {"solo_ok", "handoff_on_ambiguity", "handoff_on_risk", "review_required"}
REQUIRED_MODEL_TIERS = {"router", "planner", "executor", "verifier", "conductor", "deep", "archivist"}
REQUIRED_COHORT_PATTERNS = {"solo", "pair", "checkpoint_cohort", "orchestrated_loop"}
ALLOWED_TIER_MEMORY_SCOPE = {
    "core",
    "selected_hot",
    "selected_warm",
    "selected_cool",
    "selected_cold",
    "selected_frozen",
}
ALLOWED_RUNTIME_PHASES = ("route", "plan", "do", "verify", "transition", "deep", "distill")
PUBLIC_LOOP = "route -> plan -> do -> verify -> deep? -> distill"
EXPECTED_INVALID_FIXTURES = {
    "route_decision.wrong_artifact_type.json": ("route_decision", "wrong_artifact_type"),
    "bounded_plan.missing_required_field.json": ("bounded_plan", "missing_required_field"),
    "verification_result.forbidden_extra_property.json": ("verification_result", "forbidden_extra_property"),
}
EXPECTED_RUNTIME_SEAM_BINDINGS = [
    {
        "phase": "route",
        "tier_id": "router",
        "role_names": ["architect"],
        "artifact_type": "route_decision",
    },
    {
        "phase": "plan",
        "tier_id": "planner",
        "role_names": ["architect"],
        "artifact_type": "bounded_plan",
    },
    {
        "phase": "do",
        "tier_id": "executor",
        "role_names": ["coder"],
        "artifact_type": "work_result",
    },
    {
        "phase": "verify",
        "tier_id": "verifier",
        "role_names": ["reviewer"],
        "artifact_type": "verification_result",
    },
    {
        "phase": "transition",
        "tier_id": "conductor",
        "role_names": ["architect", "reviewer"],
        "artifact_type": "transition_decision",
    },
    {
        "phase": "deep",
        "tier_id": "deep",
        "role_names": ["evaluator", "architect"],
        "artifact_type": "deep_synthesis_note",
    },
    {
        "phase": "distill",
        "tier_id": "archivist",
        "role_names": ["memory-keeper"],
        "artifact_type": "distillation_pack",
    },
]
EXPECTED_SEAM_BINDING_LINES = (
    "- `router + architect -> route_decision`",
    "- `planner + architect -> bounded_plan`",
    "- `executor + coder -> work_result`",
    "- `verifier + reviewer -> verification_result`",
    "- `conductor + architect/reviewer -> transition_decision`",
    "- `deep + evaluator/architect -> deep_synthesis_note`",
    "- `archivist + memory-keeper -> distillation_pack`",
)
REQUIRED_COHORT_DOC_SNIPPETS = (
    "- `solo`",
    "- `pair`",
    "- `checkpoint_cohort`",
    "- `orchestrated_loop`",
    "Composition hints do not replace `aoa-playbooks`.",
)
REQUIRED_SELF_AGENT_COHORT_SNIPPET = "The portable self-agent cohort pattern is the canonical `checkpoint_cohort` pattern."


class ValidationError(RuntimeError):
    pass


class SchemaValidationError(ValidationError):
    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code


def fail(message: str) -> None:
    raise ValidationError(message)


def describe_path(path: Path, *, root: Path = REPO_ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path, *, root: Path = REPO_ROOT) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {describe_path(path, root=root)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {describe_path(path, root=root)}: {exc}")


def read_text(path: Path, *, root: Path = REPO_ROOT) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {describe_path(path, root=root)}")


def fail_schema(message: str, *, code: str | None = None) -> None:
    raise SchemaValidationError(message, code=code)


def validate_schema_surface() -> None:
    validate_json_schema_surface(SCHEMA_PATH, "schema")


def validate_model_tier_schema_surface() -> None:
    validate_json_schema_surface(MODEL_TIER_SCHEMA_PATH, "model-tier schema")


def validate_cohort_composition_schema_surface() -> None:
    validate_json_schema_surface(COHORT_COMPOSITION_SCHEMA_PATH, "cohort composition schema")


def validate_runtime_seam_bindings_schema_surface() -> None:
    validate_json_schema_surface(RUNTIME_SEAM_BINDINGS_SCHEMA_PATH, "runtime-seam-bindings schema")


def validate_json_schema_surface(path: Path, label: str) -> dict[str, object]:
    schema = read_json(path)
    if not isinstance(schema, dict):
        fail(f"{label} file must contain a JSON object")
    required_top_level = {"$schema", "$id", "title", "type", "properties", "required"}
    missing = sorted(required_top_level - set(schema))
    if missing:
        fail(f"{label} is missing required top-level keys: {', '.join(missing)}")
    return schema


def validate_instance_against_schema(instance: object, schema: dict[str, object], location: str) -> None:
    schema_type = schema.get("type")

    if schema_type == "object":
        if not isinstance(instance, dict):
            fail_schema(f"{location} must be an object")
        properties = schema.get("properties")
        if not isinstance(properties, dict):
            fail_schema(f"{location} object schema must declare properties")
        required = schema.get("required")
        if not isinstance(required, list):
            fail_schema(f"{location} object schema must declare required keys as a list")
        for key in required:
            if key not in instance:
                code = "missing_required_field" if key != "artifact_type" else None
                fail_schema(f"{location} is missing required key '{key}'", code=code)
        if schema.get("additionalProperties") is False:
            unexpected = sorted(set(instance) - set(properties))
            if unexpected:
                fail_schema(
                    f"{location} contains unexpected key '{unexpected[0]}'",
                    code="forbidden_extra_property",
                )
        for key, value in instance.items():
            if key in properties:
                property_schema = properties[key]
                if not isinstance(property_schema, dict):
                    fail_schema(f"{location}.{key} schema entry must be an object")
                validate_instance_against_schema(value, property_schema, f"{location}.{key}")
        return

    if schema_type == "array":
        if not isinstance(instance, list):
            fail_schema(f"{location} must be an array")
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            fail_schema(f"{location} must contain at least {min_items} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                validate_instance_against_schema(item, item_schema, f"{location}[{index}]")
        return

    if schema_type == "string":
        if not isinstance(instance, str):
            fail_schema(f"{location} must be a string")
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(instance) < min_length:
            fail_schema(f"{location} must have minLength {min_length}")
        if "const" in schema and instance != schema["const"]:
            code = "wrong_artifact_type" if location.endswith(".artifact_type") else None
            fail_schema(f"{location} must equal constant '{schema['const']}'", code=code)
        enum_values = schema.get("enum")
        if isinstance(enum_values, list) and instance not in enum_values:
            fail_schema(f"{location} must be one of: {', '.join(str(item) for item in enum_values)}")
        return

    if schema_type == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            fail_schema(f"{location} must be an integer")
        return

    if schema_type == "boolean":
        if not isinstance(instance, bool):
            fail_schema(f"{location} must be a boolean")
        return

    fail_schema(f"{location} uses unsupported schema type '{schema_type}'")


def validate_runtime_artifact_schema_surfaces() -> None:
    for artifact_name, path in RUNTIME_ARTIFACT_SCHEMA_PATHS.items():
        schema = validate_json_schema_surface(path, f"runtime artifact schema '{artifact_name}'")
        if schema.get("type") != "object":
            fail(f"runtime artifact schema '{artifact_name}' must declare type 'object'")
        properties = schema.get("properties")
        if not isinstance(properties, dict) or "artifact_type" not in properties:
            fail(f"runtime artifact schema '{artifact_name}' must expose an artifact_type property")
        artifact_type = properties["artifact_type"]
        if not isinstance(artifact_type, dict) or artifact_type.get("const") != artifact_name:
            fail(f"runtime artifact schema '{artifact_name}' must pin artifact_type.const to '{artifact_name}'")


def validate_runtime_artifact_examples() -> None:
    for artifact_name, schema_path in RUNTIME_ARTIFACT_SCHEMA_PATHS.items():
        example_path = RUNTIME_ARTIFACT_EXAMPLES_DIR / f"{artifact_name}.example.json"
        schema = read_json(schema_path)
        payload = read_json(example_path)
        if not isinstance(schema, dict):
            fail(f"runtime artifact schema '{artifact_name}' must remain a JSON object")
        validate_instance_against_schema(payload, schema, describe_path(example_path))


def validate_negative_runtime_artifact_examples() -> None:
    if not RUNTIME_ARTIFACT_INVALID_DIR.is_dir():
        fail(f"missing required directory: {describe_path(RUNTIME_ARTIFACT_INVALID_DIR)}")

    actual_files = {path.name for path in RUNTIME_ARTIFACT_INVALID_DIR.glob("*.json")}
    expected_files = set(EXPECTED_INVALID_FIXTURES)
    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        extra = sorted(actual_files - expected_files)
        details: list[str] = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(extra)}")
        fail(f"runtime artifact invalid fixtures drifted ({'; '.join(details)})")

    for file_name, (artifact_name, expected_code) in EXPECTED_INVALID_FIXTURES.items():
        fixture_path = RUNTIME_ARTIFACT_INVALID_DIR / file_name
        schema = read_json(RUNTIME_ARTIFACT_SCHEMA_PATHS[artifact_name])
        payload = read_json(fixture_path)
        if not isinstance(schema, dict):
            fail(f"runtime artifact schema '{artifact_name}' must remain a JSON object")
        try:
            validate_instance_against_schema(payload, schema, describe_path(fixture_path))
        except SchemaValidationError as exc:
            if exc.code != expected_code:
                fail(
                    f"{describe_path(fixture_path)} failed with unexpected error class '{exc.code}' instead of '{expected_code}'"
                )
        else:
            fail(f"{describe_path(fixture_path)} unexpectedly passed validation")


def validate_registry() -> set[str]:
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

    return seen_names


def validate_model_tier_registry() -> dict[str, dict[str, object]]:
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
    tiers_by_id: dict[str, dict[str, object]] = {}
    known_artifact_names = set(RUNTIME_ARTIFACT_SCHEMA_PATHS)
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
        tiers_by_id[tier_id] = tier

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
        if artifact_requirement not in known_artifact_names:
            fail(f"{location}.artifact_requirement '{artifact_requirement}' does not resolve to a known artifact schema")

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

    for tier_id, tier in tiers_by_id.items():
        for handoff_target in tier["handoff_targets"]:
            if handoff_target not in tiers_by_id:
                fail(f"model tier '{tier_id}' points at unknown handoff target '{handoff_target}'")

    return tiers_by_id


def validate_cohort_composition_registry(agent_names: set[str], tiers_by_id: dict[str, dict[str, object]]) -> None:
    validate_cohort_composition_schema_surface()
    schema = read_json(COHORT_COMPOSITION_SCHEMA_PATH)
    payload = read_json(COHORT_COMPOSITION_REGISTRY_PATH)
    if not isinstance(schema, dict):
        fail("cohort composition schema must remain a JSON object")
    if not isinstance(payload, dict):
        fail("cohort composition registry must be a JSON object")
    validate_instance_against_schema(payload, schema, describe_path(COHORT_COMPOSITION_REGISTRY_PATH))

    version = payload.get("version")
    if not isinstance(version, int) or version < 1:
        fail("cohort composition registry 'version' must be an integer >= 1")
    if payload.get("layer") != "aoa-agents":
        fail("cohort composition registry 'layer' must equal 'aoa-agents'")

    cohort_patterns = payload.get("cohort_patterns")
    if not isinstance(cohort_patterns, list) or not cohort_patterns:
        fail("cohort composition registry 'cohort_patterns' must be a non-empty list")

    seen_ids: set[str] = set()
    for index, pattern in enumerate(cohort_patterns):
        location = f"cohort_patterns[{index}]"
        if not isinstance(pattern, dict):
            fail(f"{location} must be an object")

        pattern_id = pattern.get("id")
        if not isinstance(pattern_id, str):
            fail(f"{location}.id must be a string")
        if pattern_id in seen_ids:
            fail(f"duplicate cohort pattern id in registry: '{pattern_id}'")
        seen_ids.add(pattern_id)

        allowed_role_sets = pattern.get("allowed_role_sets")
        preferred_tier_ids = pattern.get("preferred_tier_ids")

        for field_name, value in (
            ("activation_conditions", pattern.get("activation_conditions")),
            ("required_handoffs", pattern.get("required_handoffs")),
        ):
            if not isinstance(value, list) or not value:
                fail(f"{location}.{field_name} must be a non-empty list")
            for item in value:
                if not isinstance(item, str) or len(item) < 3:
                    fail(f"{location}.{field_name} contains an invalid entry")

        if not isinstance(allowed_role_sets, list) or not allowed_role_sets:
            fail(f"{location}.allowed_role_sets must be a non-empty list")
        for set_index, role_set in enumerate(allowed_role_sets):
            role_location = f"{location}.allowed_role_sets[{set_index}]"
            if not isinstance(role_set, list) or not role_set:
                fail(f"{role_location} must be a non-empty list")
            seen_roles: set[str] = set()
            for role_name in role_set:
                if role_name in seen_roles:
                    fail(f"{role_location} contains duplicate role '{role_name}'")
                seen_roles.add(role_name)
                if role_name not in agent_names:
                    fail(f"{role_location} contains unknown agent '{role_name}'")

        if not isinstance(preferred_tier_ids, list) or not preferred_tier_ids:
            fail(f"{location}.preferred_tier_ids must be a non-empty list")
        for tier_id in preferred_tier_ids:
            if not isinstance(tier_id, str) or len(tier_id) < 2:
                fail(f"{location}.preferred_tier_ids contains an invalid entry")
            if tier_id not in tiers_by_id:
                fail(f"{location}.preferred_tier_ids contains unknown tier '{tier_id}'")

    missing_patterns = sorted(REQUIRED_COHORT_PATTERNS - seen_ids)
    if missing_patterns:
        fail(f"cohort composition registry is missing required patterns: {', '.join(missing_patterns)}")


def validate_runtime_seam_bindings(agent_names: set[str], tiers_by_id: dict[str, dict[str, object]]) -> None:
    validate_runtime_seam_bindings_schema_surface()
    schema = read_json(RUNTIME_SEAM_BINDINGS_SCHEMA_PATH)
    payload = read_json(RUNTIME_SEAM_BINDINGS_PATH)
    if not isinstance(schema, dict):
        fail("runtime-seam-bindings schema must remain a JSON object")
    if not isinstance(payload, dict):
        fail("runtime seam bindings must be a JSON object")
    validate_instance_against_schema(payload, schema, describe_path(RUNTIME_SEAM_BINDINGS_PATH))

    version = payload.get("version")
    if not isinstance(version, int) or version < 1:
        fail("runtime seam bindings 'version' must be an integer >= 1")
    if payload.get("layer") != "aoa-agents":
        fail("runtime seam bindings 'layer' must equal 'aoa-agents'")

    bindings = payload.get("bindings")
    if not isinstance(bindings, list):
        fail("runtime seam bindings 'bindings' must be a list")
    if bindings != EXPECTED_RUNTIME_SEAM_BINDINGS:
        fail("generated/runtime_seam_bindings.json drifted from the current public role × tier contract")

    seen_artifact_types: set[str] = set()
    for index, binding in enumerate(bindings):
        location = f"bindings[{index}]"
        phase = binding["phase"]
        tier_id = binding["tier_id"]
        artifact_type = binding["artifact_type"]
        role_names = binding["role_names"]

        if phase not in ALLOWED_RUNTIME_PHASES:
            fail(f"{location}.phase '{phase}' is not allowed")
        if tier_id not in tiers_by_id:
            fail(f"{location}.tier_id '{tier_id}' is not present in the model-tier registry")
        if artifact_type not in RUNTIME_ARTIFACT_SCHEMA_PATHS:
            fail(f"{location}.artifact_type '{artifact_type}' does not resolve to a known artifact schema")
        if artifact_type in seen_artifact_types:
            fail(f"runtime seam bindings duplicate artifact coverage for '{artifact_type}'")
        seen_artifact_types.add(artifact_type)

        if not isinstance(role_names, list) or not role_names:
            fail(f"{location}.role_names must be a non-empty list")
        for role_name in role_names:
            if role_name not in agent_names:
                fail(f"{location}.role_names contains unknown agent '{role_name}'")

        tier_artifact_requirement = tiers_by_id[tier_id]["artifact_requirement"]
        if tier_artifact_requirement != artifact_type:
            fail(
                f"{location}.artifact_type '{artifact_type}' conflicts with model tier '{tier_id}' artifact_requirement '{tier_artifact_requirement}'"
            )

    if seen_artifact_types != set(RUNTIME_ARTIFACT_SCHEMA_PATHS):
        missing = sorted(set(RUNTIME_ARTIFACT_SCHEMA_PATHS) - seen_artifact_types)
        fail(f"runtime seam bindings do not cover all published artifact schemas: {', '.join(missing)}")


def validate_runtime_seam_doc_coherence() -> None:
    cohort_patterns = read_text(REPO_ROOT / "docs" / "AGENT_COHORT_PATTERNS.md")
    agent_runtime_seam = read_text(REPO_ROOT / "docs" / "AGENT_RUNTIME_SEAM.md")
    model_tier_model = read_text(REPO_ROOT / "docs" / "MODEL_TIER_MODEL.md")
    runtime_transitions = read_text(REPO_ROOT / "docs" / "RUNTIME_ARTIFACT_TRANSITIONS.md")
    self_agent_checkpoint = read_text(REPO_ROOT / "docs" / "SELF_AGENT_CHECKPOINT_STACK.md")

    if PUBLIC_LOOP not in agent_runtime_seam:
        fail("docs/AGENT_RUNTIME_SEAM.md must preserve the public loop string")
    if PUBLIC_LOOP not in model_tier_model:
        fail("docs/MODEL_TIER_MODEL.md must preserve the public loop string")
    if PUBLIC_LOOP not in runtime_transitions:
        fail("docs/RUNTIME_ARTIFACT_TRANSITIONS.md must preserve the public loop string")

    for line in EXPECTED_SEAM_BINDING_LINES:
        if line not in agent_runtime_seam:
            fail(f"docs/AGENT_RUNTIME_SEAM.md is missing runtime seam binding line: {line}")

    for snippet in REQUIRED_COHORT_DOC_SNIPPETS:
        if snippet not in cohort_patterns:
            fail(f"docs/AGENT_COHORT_PATTERNS.md is missing required cohort guidance: {snippet}")

    required_transition_snippets = (
        "`transition_decision` is a governance artifact between phases.",
        "`work_result` and `deep_synthesis_note` remain agent-layer artifacts",
        "`AOA-P-0008` and `AOA-P-0009` remain reference scenarios only.",
    )
    for snippet in required_transition_snippets:
        if snippet not in runtime_transitions:
            fail(f"docs/RUNTIME_ARTIFACT_TRANSITIONS.md is missing required transition guidance: {snippet}")
    if REQUIRED_SELF_AGENT_COHORT_SNIPPET not in self_agent_checkpoint:
        fail("docs/SELF_AGENT_CHECKPOINT_STACK.md must map the portable route to `checkpoint_cohort`")


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


def env_repo_root(name: str) -> Path | None:
    raw_value = os.environ.get(name)
    if not raw_value:
        return None
    root = Path(raw_value)
    if not root.exists():
        fail(f"{name} points at a missing path: {root}")
    return root


def iter_string_values(payload: object) -> list[str]:
    values: list[str] = []
    if isinstance(payload, str):
        values.append(payload)
    elif isinstance(payload, list):
        for item in payload:
            values.extend(iter_string_values(item))
    elif isinstance(payload, dict):
        for item in payload.values():
            values.extend(iter_string_values(item))
    return values


def resolve_aoa_agents_repo_ref(ref: str) -> Path:
    prefix = "repo:aoa-agents/"
    if not ref.startswith(prefix):
        fail(f"unsupported aoa-agents repo ref: {ref}")
    relative_path = ref.removeprefix(prefix)
    target = REPO_ROOT / relative_path
    if not target.exists():
        fail(f"aoa-agents repo ref does not resolve to an existing public surface: {ref}")
    return target


def validate_optional_consumer_smoke_checks() -> list[str]:
    checked: list[str] = []
    known_artifact_names = set(RUNTIME_ARTIFACT_SCHEMA_PATHS)

    playbooks_root = env_repo_root("AOA_PLAYBOOKS_ROOT")
    if playbooks_root is not None:
        payload = read_json(playbooks_root / "generated" / "playbook_registry.min.json", root=playbooks_root)
        if not isinstance(payload, dict) or not isinstance(payload.get("playbooks"), list):
            fail("aoa-playbooks generated/playbook_registry.min.json must expose a playbooks list")
        playbook = next((item for item in payload["playbooks"] if item.get("id") == "AOA-P-0008"), None)
        if not isinstance(playbook, dict):
            fail("aoa-playbooks registry is missing playbook 'AOA-P-0008'")
        expected_artifacts = playbook.get("expected_artifacts")
        if not isinstance(expected_artifacts, list) or not expected_artifacts:
            fail("aoa-playbooks AOA-P-0008 must expose expected_artifacts")
        invalid = sorted(set(expected_artifacts) - known_artifact_names)
        if invalid:
            fail(
                "aoa-playbooks AOA-P-0008 expected_artifacts are not a subset of aoa-agents artifact names: "
                + ", ".join(invalid)
            )
        checked.append("aoa-playbooks")

    evals_root = env_repo_root("AOA_EVALS_ROOT")
    if evals_root is not None:
        payload = read_json(
            evals_root / "examples" / "artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
            root=evals_root,
        )
        if not isinstance(payload, dict):
            fail("aoa-evals long-horizon hook example must be a JSON object")
        refs = payload.get("artifact_contract_refs")
        if not isinstance(refs, list) or not refs:
            fail("aoa-evals long-horizon hook example must expose artifact_contract_refs")
        for ref in refs:
            if not isinstance(ref, str):
                fail("aoa-evals artifact_contract_refs must contain strings")
            resolve_aoa_agents_repo_ref(ref)
        checked.append("aoa-evals")

    memo_root = env_repo_root("AOA_MEMO_ROOT")
    if memo_root is not None:
        payload = read_json(memo_root / "examples" / "checkpoint_to_memory_contract.example.json", root=memo_root)
        refs = sorted({value for value in iter_string_values(payload) if value.startswith("repo:aoa-agents/")})
        if not refs:
            fail("aoa-memo checkpoint_to_memory_contract example does not contain any aoa-agents refs to smoke-check")
        for ref in refs:
            resolve_aoa_agents_repo_ref(ref)
        checked.append("aoa-memo")

    return checked


def main() -> int:
    try:
        validate_schema_surface()
        validate_model_tier_schema_surface()
        validate_cohort_composition_schema_surface()
        validate_runtime_artifact_schema_surfaces()
        validate_runtime_artifact_examples()
        validate_negative_runtime_artifact_examples()
        agent_names = validate_registry()
        tiers_by_id = validate_model_tier_registry()
        validate_cohort_composition_registry(agent_names, tiers_by_id)
        validate_runtime_seam_bindings(agent_names, tiers_by_id)
        validate_runtime_seam_doc_coherence()
        checked_roots = validate_optional_consumer_smoke_checks()
    except ValidationError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[ok] validated agent registry schema surface")
    print("[ok] validated model-tier registry schema surface")
    print("[ok] validated cohort composition schema surface")
    print("[ok] validated runtime artifact schema surfaces")
    print("[ok] validated runtime artifact examples")
    print("[ok] validated runtime seam bindings")
    print("[ok] validated generated/agent_registry.min.json")
    print("[ok] validated generated/model_tier_registry.json")
    print("[ok] validated generated/cohort_composition_registry.json")
    if checked_roots:
        print(f"[ok] validated optional consumer smoke checks against: {', '.join(checked_roots)}")
    else:
        print("[ok] optional consumer smoke checks skipped (env roots not set)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
