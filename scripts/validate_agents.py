#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from agent_profile_registry import BuildError, PROFILES_DIR, build_agent_registry_payload, load_profiles
from cohort_registry import COHORT_PATTERNS_DIR, build_cohort_registry_payload, load_cohort_patterns
from model_tier_registry import MODEL_TIERS_DIR, build_model_tier_registry_payload, load_model_tiers
from runtime_seam_registry import RUNTIME_SEAM_DIR, build_runtime_seam_registry_payload, load_runtime_seam_bindings
from validate_nested_agents import NestedAgentsValidationError, validate_nested_agents_docs

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "generated" / "agent_registry.min.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent-registry.schema.json"
PROFILE_SCHEMA_PATH = REPO_ROOT / "schemas" / "agent-profile.schema.json"
MODEL_TIER_REGISTRY_PATH = REPO_ROOT / "generated" / "model_tier_registry.json"
MODEL_TIER_SCHEMA_PATH = REPO_ROOT / "schemas" / "model-tier-registry.schema.json"
MODEL_TIER_ITEM_SCHEMA_PATH = REPO_ROOT / "schemas" / "model-tier.schema.json"
COHORT_COMPOSITION_REGISTRY_PATH = REPO_ROOT / "generated" / "cohort_composition_registry.json"
COHORT_COMPOSITION_SCHEMA_PATH = REPO_ROOT / "schemas" / "cohort-composition-registry.schema.json"
COHORT_PATTERN_SCHEMA_PATH = REPO_ROOT / "schemas" / "cohort-pattern.schema.json"
RUNTIME_SEAM_BINDINGS_PATH = REPO_ROOT / "generated" / "runtime_seam_bindings.json"
RUNTIME_SEAM_BINDINGS_SCHEMA_PATH = REPO_ROOT / "schemas" / "runtime-seam-bindings.schema.json"
RUNTIME_SEAM_BINDING_ITEM_SCHEMA_PATH = REPO_ROOT / "schemas" / "runtime-seam-binding.schema.json"
SELF_AGENT_CHECKPOINT_SCHEMA_PATH = REPO_ROOT / "schemas" / "self-agent-checkpoint.schema.json"
RUNTIME_ARTIFACT_EXAMPLES_DIR = REPO_ROOT / "examples" / "runtime_artifacts"
RUNTIME_ARTIFACT_INVALID_DIR = RUNTIME_ARTIFACT_EXAMPLES_DIR / "invalid"
SELF_AGENT_CHECKPOINT_EXAMPLES_DIR = REPO_ROOT / "examples" / "self_agent_checkpoint"
SELF_AGENT_CHECKPOINT_EXAMPLE_PATH = SELF_AGENT_CHECKPOINT_EXAMPLES_DIR / "self_agent_checkpoint.example.json"
SELF_AGENT_CHECKPOINT_INVALID_DIR = SELF_AGENT_CHECKPOINT_EXAMPLES_DIR / "invalid"
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
    "transition_decision.return.invalid.missing_anchor.json": ("transition_decision", "missing_required_field"),
}
SUPPLEMENTAL_RUNTIME_ARTIFACT_EXAMPLE_GLOBS = {
    "transition_decision": "transition_decision.*.example.json",
}
EXPECTED_SELF_AGENT_CHECKPOINT_INVALID_FIXTURES = {
    "self_agent_checkpoint.missing_required_field.json": "missing_required_field",
    "self_agent_checkpoint.invalid_approval_mode.json": "invalid_enum_value",
    "self_agent_checkpoint.max_iterations_below_minimum.json": "below_minimum",
}
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
REQUIRED_FEDERATION_DOC_SNIPPETS = (
    "- `aoa-playbooks` consumes agent names, model-tier artifacts, and a bounded",
    "- `aoa-memo` owns memory-object canon and recall meaning; `aoa-agents` may",
    "- `aoa-routing` consumes model-tier registry for tier hints and selects the next",
    "- `aoa-agents` may read routing-published memo recall entrypoints as bounded",
    "- `AOA-P-0006 -> checkpoint_cohort`",
    "- `AOA-P-0008 -> orchestrated_loop`",
    "Router remains tier-aware, not cohort-aware, in this slice.",
    "`memory_objects` remains a parallel recall family selected explicitly through",
    "`aoa-agents` does not define memory-object canon or recall meaning in this slice.",
)

REQUIRED_AGENT_MEMORY_POSTURE_SNIPPETS = (
    "`aoa-memo` owns memory-object canon, memory doctrine, and recall meaning.",
    "`aoa-routing` selects the next memo path.",
    "`aoa-agents` only states which roles may use published or routed object recall seams.",
    "the default memo path and `memory_objects` remains an explicit parallel family",
)
REQUIRED_AGENT_RUNTIME_RECURRENCE_SNIPPETS = (
    "Return remains a governance move carried by `transition_decision`.",
    "It is a re-entry between phases, not a new sovereign stage.",
    "The agent layer may publish the public return contract, but runtime context rebuild still belongs outside this repository.",
)
REQUIRED_TRANSITION_RECURRENCE_SNIPPETS = (
    "## Return Must Point To An Anchor",
    "- `anchor_artifact`",
    "- `reentry_note`",
)
REQUIRED_RECURRENCE_DISCIPLINE_SNIPPETS = (
    "This document defines recurrence discipline at the agent layer.",
    "`return` is carried by `transition_decision`.",
    "`decision = \"return\"` should be able to name:",
    "- `abyss-stack` still owns runtime context rebuild, retries, wrapper policy, and infrastructure implementation",
)
REQUIRED_SELF_AGENT_RETURN_SNIPPETS = (
    "If a governed self-agent route loses the bounded change axis, it should return to the last approved anchor before more change work occurs.",
    "It is better to re-enter from a valid anchor than to continue under drift.",
)

MEMO_OBJECT_SURFACE_PATHS = (
    "generated/memory_object_catalog.min.json",
    "generated/memory_object_capsules.json",
    "generated/memory_object_sections.full.json",
)

MEMO_OBJECT_RECALL_CONTRACTS = (
    ("examples/recall_contract.object.working.json", "working"),
    ("examples/recall_contract.object.semantic.json", "semantic"),
    ("examples/recall_contract.object.lineage.json", "lineage"),
)

MEMO_OBJECT_INSPECT_SURFACE = "generated/memory_object_catalog.min.json"
MEMO_OBJECT_CAPSULE_SURFACE = "generated/memory_object_capsules.json"
MEMO_OBJECT_EXPAND_SURFACE = "generated/memory_object_sections.full.json"
MEMO_CAPSULE_REQUIRED_MODES = {"semantic", "lineage"}
ROUTING_TASK_TO_SURFACE_HINTS_PATH = "generated/task_to_surface_hints.json"
ROUTING_TINY_MODEL_ENTRYPOINTS_PATH = "generated/tiny_model_entrypoints.json"
ROUTING_MEMO_OBJECT_RECALL_FAMILY = "memory_objects"
ROUTING_MEMO_DOCTRINE_INSPECT_SURFACE = "generated/memory_catalog.min.json"
ROUTING_MEMO_DOCTRINE_CAPSULE_SURFACE = "generated/memory_capsules.json"
ROUTING_MEMO_DOCTRINE_EXPAND_SURFACE = "generated/memory_sections.full.json"


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


def validate_model_tier_item_schema_surface() -> None:
    validate_json_schema_surface(MODEL_TIER_ITEM_SCHEMA_PATH, "model-tier item schema")


def validate_agent_profile_schema_surface() -> None:
    validate_json_schema_surface(PROFILE_SCHEMA_PATH, "agent-profile schema")


def validate_cohort_composition_schema_surface() -> None:
    validate_json_schema_surface(COHORT_COMPOSITION_SCHEMA_PATH, "cohort composition schema")


def validate_cohort_pattern_schema_surface() -> None:
    validate_json_schema_surface(COHORT_PATTERN_SCHEMA_PATH, "cohort-pattern schema")


def validate_runtime_seam_bindings_schema_surface() -> None:
    validate_json_schema_surface(RUNTIME_SEAM_BINDINGS_SCHEMA_PATH, "runtime-seam-bindings schema")


def validate_runtime_seam_binding_item_schema_surface() -> None:
    validate_json_schema_surface(RUNTIME_SEAM_BINDING_ITEM_SCHEMA_PATH, "runtime-seam-binding schema")


def validate_self_agent_checkpoint_schema_surface() -> None:
    validate_json_schema_surface(SELF_AGENT_CHECKPOINT_SCHEMA_PATH, "self-agent-checkpoint schema")


def validate_json_schema_surface(path: Path, label: str) -> dict[str, object]:
    schema = read_json(path)
    if not isinstance(schema, dict):
        fail(f"{label} file must contain a JSON object")
    required_top_level = {"$schema", "$id", "title", "type", "properties", "required"}
    missing = sorted(required_top_level - set(schema))
    if missing:
        fail(f"{label} is missing required top-level keys: {', '.join(missing)}")
    return schema


def infer_schema_type(instance: object, schema: dict[str, object]) -> str | None:
    schema_type = schema.get("type")
    if isinstance(schema_type, str):
        return schema_type
    if any(key in schema for key in ("properties", "required", "additionalProperties")):
        return "object"
    if "items" in schema:
        return "array"
    if any(key in schema for key in ("const", "enum", "minLength")):
        if isinstance(instance, str):
            return "string"
        if isinstance(instance, bool):
            return "boolean"
        if isinstance(instance, int):
            return "integer"
    return None


def schema_matches(instance: object, schema: dict[str, object], location: str) -> bool:
    try:
        validate_instance_against_schema(instance, schema, location)
    except SchemaValidationError:
        return False
    return True


def validate_conditional_keywords(instance: object, schema: dict[str, object], location: str) -> None:
    if_schema = schema.get("if")
    then_schema = schema.get("then")
    else_schema = schema.get("else")

    if if_schema is None:
        if then_schema is not None or else_schema is not None:
            fail_schema(f"{location} conditional schema must define 'if' before 'then' or 'else'")
        return

    if not isinstance(if_schema, dict):
        fail_schema(f"{location}.if must be an object")

    matched = schema_matches(instance, if_schema, f"{location}.if")
    branch_name = "then" if matched else "else"
    branch_schema = then_schema if matched else else_schema
    if branch_schema is None:
        return
    if not isinstance(branch_schema, dict):
        fail_schema(f"{location}.{branch_name} must be an object")
    validate_instance_against_schema(instance, branch_schema, f"{location}.{branch_name}")


def validate_instance_against_schema(instance: object, schema: dict[str, object], location: str) -> None:
    all_of = schema.get("allOf")
    if all_of is not None:
        if not isinstance(all_of, list):
            fail_schema(f"{location}.allOf must be a list")
        for index, item in enumerate(all_of):
            if not isinstance(item, dict):
                fail_schema(f"{location}.allOf[{index}] must be an object")
            validate_instance_against_schema(instance, item, f"{location}.allOf[{index}]")

    schema_type = infer_schema_type(instance, schema)

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
        validate_conditional_keywords(instance, schema, location)
        return

    if schema_type == "array":
        if not isinstance(instance, list):
            fail_schema(f"{location} must be an array")
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            fail_schema(f"{location} must contain at least {min_items} items")
        if schema.get("uniqueItems") is True:
            rendered = [json.dumps(item, sort_keys=True) for item in instance]
            if len(rendered) != len(set(rendered)):
                fail_schema(f"{location} must not contain duplicate items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                validate_instance_against_schema(item, item_schema, f"{location}[{index}]")
        validate_conditional_keywords(instance, schema, location)
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
            fail_schema(
                f"{location} must be one of: {', '.join(str(item) for item in enum_values)}",
                code="invalid_enum_value",
            )
        validate_conditional_keywords(instance, schema, location)
        return

    if schema_type == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            fail_schema(f"{location} must be an integer")
        minimum = schema.get("minimum")
        if isinstance(minimum, int) and instance < minimum:
            fail_schema(f"{location} must be >= {minimum}", code="below_minimum")
        validate_conditional_keywords(instance, schema, location)
        return

    if schema_type == "boolean":
        if not isinstance(instance, bool):
            fail_schema(f"{location} must be a boolean")
        validate_conditional_keywords(instance, schema, location)
        return

    if schema_type is None and any(key in schema for key in ("if", "then", "else")):
        validate_conditional_keywords(instance, schema, location)
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


def runtime_artifact_example_paths(artifact_name: str) -> list[Path]:
    paths = [RUNTIME_ARTIFACT_EXAMPLES_DIR / f"{artifact_name}.example.json"]
    pattern = SUPPLEMENTAL_RUNTIME_ARTIFACT_EXAMPLE_GLOBS.get(artifact_name)
    if pattern is not None:
        for path in sorted(RUNTIME_ARTIFACT_EXAMPLES_DIR.glob(pattern)):
            if path not in paths:
                paths.append(path)
    return paths


def validate_runtime_artifact_examples() -> None:
    for artifact_name, schema_path in RUNTIME_ARTIFACT_SCHEMA_PATHS.items():
        schema = read_json(schema_path)
        if not isinstance(schema, dict):
            fail(f"runtime artifact schema '{artifact_name}' must remain a JSON object")
        for example_path in runtime_artifact_example_paths(artifact_name):
            payload = read_json(example_path)
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


def validate_self_agent_checkpoint_example() -> dict[str, object]:
    schema = read_json(SELF_AGENT_CHECKPOINT_SCHEMA_PATH)
    payload = read_json(SELF_AGENT_CHECKPOINT_EXAMPLE_PATH)
    if not isinstance(schema, dict):
        fail("self-agent-checkpoint schema must remain a JSON object")
    if not isinstance(payload, dict):
        fail("self-agent checkpoint example must be a JSON object")
    validate_instance_against_schema(payload, schema, describe_path(SELF_AGENT_CHECKPOINT_EXAMPLE_PATH))
    return payload


def validate_negative_self_agent_checkpoint_examples() -> None:
    if not SELF_AGENT_CHECKPOINT_INVALID_DIR.is_dir():
        fail(f"missing required directory: {describe_path(SELF_AGENT_CHECKPOINT_INVALID_DIR)}")

    actual_files = {path.name for path in SELF_AGENT_CHECKPOINT_INVALID_DIR.glob("*.json")}
    expected_files = set(EXPECTED_SELF_AGENT_CHECKPOINT_INVALID_FIXTURES)
    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        extra = sorted(actual_files - expected_files)
        details: list[str] = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(extra)}")
        fail(f"self-agent checkpoint invalid fixtures drifted ({'; '.join(details)})")

    schema = read_json(SELF_AGENT_CHECKPOINT_SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("self-agent-checkpoint schema must remain a JSON object")

    for file_name, expected_code in EXPECTED_SELF_AGENT_CHECKPOINT_INVALID_FIXTURES.items():
        fixture_path = SELF_AGENT_CHECKPOINT_INVALID_DIR / file_name
        payload = read_json(fixture_path)
        try:
            validate_instance_against_schema(payload, schema, describe_path(fixture_path))
        except SchemaValidationError as exc:
            if exc.code != expected_code:
                fail(
                    f"{describe_path(fixture_path)} failed with unexpected error class "
                    f"'{exc.code}' instead of '{expected_code}'"
                )
        else:
            fail(f"{describe_path(fixture_path)} unexpectedly passed validation")


def validate_agent_profile_sources() -> list[dict[str, object]]:
    schema = read_json(PROFILE_SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("agent-profile schema must remain a JSON object")

    try:
        profiles = load_profiles()
    except BuildError as exc:
        fail(str(exc))

    if not profiles:
        fail("profiles/ must contain at least one '*.profile.json' file")

    expected_registry = build_agent_registry_payload(profiles)
    actual_registry = read_json(REGISTRY_PATH)
    if actual_registry != expected_registry:
        fail("generated/agent_registry.min.json drifted from profiles/*.profile.json")

    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    required_seed = {"architect", "coder", "reviewer", "evaluator", "memory-keeper"}
    for index, payload in enumerate(profiles):
        location = f"profiles[{index}]"
        validate_instance_against_schema(payload, schema, location)

        profile_id = payload.get("id")
        profile_name = payload.get("name")
        if not isinstance(profile_id, str) or not isinstance(profile_name, str):
            fail(f"{location} must expose string 'id' and 'name' fields")

        expected_profile_path = PROFILES_DIR / f"{profile_name}.profile.json"
        if not expected_profile_path.exists():
            fail(f"{location} expected source file is missing: {describe_path(expected_profile_path)}")

        if profile_id in seen_ids:
            fail(f"duplicate agent profile id in source layer: '{profile_id}'")
        seen_ids.add(profile_id)

        if profile_name in seen_names:
            fail(f"duplicate agent profile name in source layer: '{profile_name}'")
        seen_names.add(profile_name)

        owns = payload.get("owns")
        does_not_own = payload.get("does_not_own")
        if not isinstance(owns, list) or not isinstance(does_not_own, list):
            fail(f"{location} must expose list-valued owns and does_not_own fields")
        overlap = sorted(set(owns) & set(does_not_own))
        if overlap:
            fail(f"{location} owns/does_not_own overlap on: {', '.join(overlap)}")

        source_surfaces = payload.get("source_surfaces")
        if not isinstance(source_surfaces, list) or not source_surfaces:
            fail(f"{location} must expose a non-empty source_surfaces list")
        for ref in source_surfaces:
            if not isinstance(ref, str):
                fail(f"{location}.source_surfaces must contain only strings")
            resolve_aoa_agents_repo_ref(ref)

    missing_seed = sorted(required_seed - seen_names)
    if missing_seed:
        fail(f"source-authored agent profiles are missing required seed agents: {', '.join(missing_seed)}")

    return profiles


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


def validate_agent_profile_references(
    profiles: list[dict[str, object]],
    tiers_by_id: dict[str, dict[str, object]],
    cohort_patterns_by_id: dict[str, dict[str, object]],
) -> None:
    known_tier_ids = set(tiers_by_id)
    known_cohort_pattern_ids = set(cohort_patterns_by_id)

    for profile in profiles:
        profile_name = profile.get("name")
        location = f"agent profile '{profile_name}'"

        preferred_tier_ids = profile.get("preferred_tier_ids")
        if not isinstance(preferred_tier_ids, list) or not preferred_tier_ids:
            fail(f"{location} must expose a non-empty preferred_tier_ids list")
        for tier_id in preferred_tier_ids:
            if not isinstance(tier_id, str) or tier_id not in known_tier_ids:
                fail(f"{location}.preferred_tier_ids contains unknown tier '{tier_id}'")

        preferred_cohort_patterns = profile.get("preferred_cohort_patterns")
        if not isinstance(preferred_cohort_patterns, list) or not preferred_cohort_patterns:
            fail(f"{location} must expose a non-empty preferred_cohort_patterns list")
        for pattern_id in preferred_cohort_patterns:
            if not isinstance(pattern_id, str) or pattern_id not in known_cohort_pattern_ids:
                fail(f"{location}.preferred_cohort_patterns contains unknown pattern '{pattern_id}'")
            pattern = cohort_patterns_by_id[pattern_id]
            allowed_role_sets = pattern.get("allowed_role_sets")
            if not isinstance(allowed_role_sets, list):
                fail(f"cohort pattern '{pattern_id}' must expose allowed_role_sets")
            if not any(isinstance(role_set, list) and profile_name in role_set for role_set in allowed_role_sets):
                fail(
                    f"{location}.preferred_cohort_patterns contains '{pattern_id}', "
                    f"but the pattern never includes role '{profile_name}'"
                )

        source_surfaces = profile.get("source_surfaces")
        if not isinstance(source_surfaces, list) or not source_surfaces:
            fail(f"{location} must expose a non-empty source_surfaces list")
        for ref in source_surfaces:
            if not isinstance(ref, str):
                fail(f"{location}.source_surfaces must contain strings")
            resolve_aoa_agents_repo_ref(ref)


def validate_self_agent_checkpoint_example_coherence(
    payload: dict[str, object], profiles: list[dict[str, object]], agent_names: set[str]
) -> None:
    agent_id = payload.get("agent_id")
    role = payload.get("role")
    if not isinstance(agent_id, str) or not isinstance(role, str):
        fail("self-agent checkpoint example must expose string-valued 'agent_id' and 'role'")

    profiles_by_id = {
        profile["id"]: profile
        for profile in profiles
        if isinstance(profile, dict) and isinstance(profile.get("id"), str)
    }
    matched_profile = profiles_by_id.get(agent_id)
    if not isinstance(matched_profile, dict):
        fail(f"self-agent checkpoint example agent_id '{agent_id}' does not resolve in source-authored agent profiles")

    expected_role_name = matched_profile.get("name")
    if not isinstance(expected_role_name, str):
        fail(f"source-authored agent profile '{agent_id}' must expose a string 'name'")
    if role != expected_role_name:
        fail(
            "self-agent checkpoint example role must match the public role-facing agent name "
            f"for '{agent_id}': expected '{expected_role_name}', got '{role}'"
        )
    if role not in agent_names:
        fail(f"self-agent checkpoint example role '{role}' does not resolve in generated/agent_registry.min.json")


def validate_model_tier_sources() -> list[dict[str, object]]:
    schema = read_json(MODEL_TIER_ITEM_SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("model-tier item schema must remain a JSON object")

    try:
        tiers = load_model_tiers()
    except BuildError as exc:
        fail(str(exc))

    if not tiers:
        fail("model_tiers/ must contain at least one '*.tier.json' file")

    expected_registry = build_model_tier_registry_payload(tiers)
    actual_registry = read_json(MODEL_TIER_REGISTRY_PATH)
    if actual_registry != expected_registry:
        fail("generated/model_tier_registry.json drifted from model_tiers/*.tier.json")

    seen_ids: set[str] = set()
    for index, payload in enumerate(tiers):
        location = f"model_tiers[{index}]"
        validate_instance_against_schema(payload, schema, location)

        tier_id = payload.get("id")
        if not isinstance(tier_id, str):
            fail(f"{location} must expose string 'id'")

        expected_tier_path = MODEL_TIERS_DIR / f"{tier_id}.tier.json"
        if not expected_tier_path.exists():
            fail(f"{location} expected source file is missing: {describe_path(expected_tier_path)}")

        if tier_id in seen_ids:
            fail(f"duplicate model tier id in source layer: '{tier_id}'")
        seen_ids.add(tier_id)

    missing_tiers = sorted(REQUIRED_MODEL_TIERS - seen_ids)
    if missing_tiers:
        fail(f"source-authored model tiers are missing required ids: {', '.join(missing_tiers)}")

    return tiers


def validate_cohort_pattern_sources() -> list[dict[str, object]]:
    schema = read_json(COHORT_PATTERN_SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("cohort-pattern schema must remain a JSON object")

    try:
        patterns = load_cohort_patterns()
    except BuildError as exc:
        fail(str(exc))

    if not patterns:
        fail("cohort_patterns/ must contain at least one '*.pattern.json' file")

    expected_registry = build_cohort_registry_payload(patterns)
    actual_registry = read_json(COHORT_COMPOSITION_REGISTRY_PATH)
    if actual_registry != expected_registry:
        fail("generated/cohort_composition_registry.json drifted from cohort_patterns/*.pattern.json")

    seen_ids: set[str] = set()
    for index, payload in enumerate(patterns):
        location = f"cohort_patterns[{index}]"
        validate_instance_against_schema(payload, schema, location)

        pattern_id = payload.get("id")
        if not isinstance(pattern_id, str):
            fail(f"{location} must expose string 'id'")

        expected_pattern_path = COHORT_PATTERNS_DIR / f"{pattern_id}.pattern.json"
        if not expected_pattern_path.exists():
            fail(f"{location} expected source file is missing: {describe_path(expected_pattern_path)}")

        if pattern_id in seen_ids:
            fail(f"duplicate cohort pattern id in source layer: '{pattern_id}'")
        seen_ids.add(pattern_id)

    missing_patterns = sorted(REQUIRED_COHORT_PATTERNS - seen_ids)
    if missing_patterns:
        fail(f"source-authored cohort patterns are missing required ids: {', '.join(missing_patterns)}")

    return patterns


def validate_runtime_seam_binding_sources() -> list[dict[str, object]]:
    schema = read_json(RUNTIME_SEAM_BINDING_ITEM_SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("runtime-seam-binding schema must remain a JSON object")

    try:
        bindings = load_runtime_seam_bindings()
    except BuildError as exc:
        fail(str(exc))

    if not bindings:
        fail("runtime_seam/ must contain at least one '*.binding.json' file")

    expected_registry = build_runtime_seam_registry_payload(bindings)
    actual_registry = read_json(RUNTIME_SEAM_BINDINGS_PATH)
    if actual_registry != expected_registry:
        fail("generated/runtime_seam_bindings.json drifted from runtime_seam/*.binding.json")

    seen_phases: set[str] = set()
    for index, payload in enumerate(bindings):
        location = f"runtime_seam[{index}]"
        validate_instance_against_schema(payload, schema, location)

        phase = payload.get("phase")
        if not isinstance(phase, str):
            fail(f"{location} must expose string 'phase'")

        expected_binding_path = RUNTIME_SEAM_DIR / f"{phase}.binding.json"
        if not expected_binding_path.exists():
            fail(f"{location} expected source file is missing: {describe_path(expected_binding_path)}")

        if phase in seen_phases:
            fail(f"duplicate runtime seam phase in source layer: '{phase}'")
        seen_phases.add(phase)

    missing_phases = sorted(set(ALLOWED_RUNTIME_PHASES) - seen_phases)
    if missing_phases:
        fail(f"source-authored runtime seam bindings are missing phases: {', '.join(missing_phases)}")

    return bindings


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


def validate_cohort_composition_registry(
    agent_names: set[str], tiers_by_id: dict[str, dict[str, object]]
) -> dict[str, dict[str, object]]:
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
    patterns_by_id: dict[str, dict[str, object]] = {}
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
        patterns_by_id[pattern_id] = pattern

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

    return patterns_by_id


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
    agent_memory_posture = read_text(REPO_ROOT / "docs" / "AGENT_MEMORY_POSTURE.md")
    cohort_patterns = read_text(REPO_ROOT / "docs" / "AGENT_COHORT_PATTERNS.md")
    federation_consumer_seams = read_text(REPO_ROOT / "docs" / "FEDERATION_CONSUMER_SEAMS.md")
    agent_runtime_seam = read_text(REPO_ROOT / "docs" / "AGENT_RUNTIME_SEAM.md")
    model_tier_model = read_text(REPO_ROOT / "docs" / "MODEL_TIER_MODEL.md")
    recurrence_discipline = read_text(REPO_ROOT / "docs" / "RECURRENCE_DISCIPLINE.md")
    runtime_transitions = read_text(REPO_ROOT / "docs" / "RUNTIME_ARTIFACT_TRANSITIONS.md")
    self_agent_checkpoint = read_text(REPO_ROOT / "docs" / "SELF_AGENT_CHECKPOINT_STACK.md")

    for snippet in REQUIRED_AGENT_MEMORY_POSTURE_SNIPPETS:
        if snippet not in agent_memory_posture:
            fail(f"docs/AGENT_MEMORY_POSTURE.md is missing required memory posture guidance: {snippet}")

    if PUBLIC_LOOP not in agent_runtime_seam:
        fail("docs/AGENT_RUNTIME_SEAM.md must preserve the public loop string")
    if PUBLIC_LOOP not in model_tier_model:
        fail("docs/MODEL_TIER_MODEL.md must preserve the public loop string")
    if PUBLIC_LOOP not in runtime_transitions:
        fail("docs/RUNTIME_ARTIFACT_TRANSITIONS.md must preserve the public loop string")

    for line in EXPECTED_SEAM_BINDING_LINES:
        if line not in agent_runtime_seam:
            fail(f"docs/AGENT_RUNTIME_SEAM.md is missing runtime seam binding line: {line}")
    for snippet in REQUIRED_AGENT_RUNTIME_RECURRENCE_SNIPPETS:
        if snippet not in agent_runtime_seam:
            fail(f"docs/AGENT_RUNTIME_SEAM.md is missing recurrence guidance: {snippet}")

    for snippet in REQUIRED_COHORT_DOC_SNIPPETS:
        if snippet not in cohort_patterns:
            fail(f"docs/AGENT_COHORT_PATTERNS.md is missing required cohort guidance: {snippet}")
    for snippet in REQUIRED_FEDERATION_DOC_SNIPPETS:
        if snippet not in federation_consumer_seams:
            fail(f"docs/FEDERATION_CONSUMER_SEAMS.md is missing required federation guidance: {snippet}")
    for snippet in REQUIRED_RECURRENCE_DISCIPLINE_SNIPPETS:
        if snippet not in recurrence_discipline:
            fail(f"docs/RECURRENCE_DISCIPLINE.md is missing recurrence guidance: {snippet}")

    required_transition_snippets = (
        "`transition_decision` is a governance artifact between phases.",
        "`work_result` and `deep_synthesis_note` remain agent-layer artifacts",
        "`AOA-P-0008` and `AOA-P-0009` remain reference scenarios only.",
    )
    for snippet in required_transition_snippets:
        if snippet not in runtime_transitions:
            fail(f"docs/RUNTIME_ARTIFACT_TRANSITIONS.md is missing required transition guidance: {snippet}")
    for snippet in REQUIRED_TRANSITION_RECURRENCE_SNIPPETS:
        if snippet not in runtime_transitions:
            fail(f"docs/RUNTIME_ARTIFACT_TRANSITIONS.md is missing recurrence guidance: {snippet}")
    if REQUIRED_SELF_AGENT_COHORT_SNIPPET not in self_agent_checkpoint:
        fail("docs/SELF_AGENT_CHECKPOINT_STACK.md must map the portable route to `checkpoint_cohort`")
    for snippet in REQUIRED_SELF_AGENT_RETURN_SNIPPETS:
        if snippet not in self_agent_checkpoint:
            fail(f"docs/SELF_AGENT_CHECKPOINT_STACK.md is missing recurrence guidance: {snippet}")


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
            if not isinstance(item, str):
                fail(f"{location}.memory_rights.{array_name} must contain only strings")
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
        if not isinstance(item, str):
            fail(f"{location}.memory_rights.promotion_rights.allowed_transitions must contain only strings")
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


def find_mapping_by_key(items: object, *, key: str, expected_value: str) -> dict[str, object] | None:
    if not isinstance(items, list):
        return None
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get(key) == expected_value:
            return item
    return None


def resolve_aoa_agents_repo_ref(ref: str) -> Path:
    prefix = "repo:aoa-agents/"
    if not ref.startswith(prefix):
        fail(f"unsupported aoa-agents repo ref: {ref}")
    relative_path = ref.removeprefix(prefix).replace("\\", "/")
    if not relative_path:
        fail(f"aoa-agents repo ref must include a repo-relative path: {ref}")
    if re.match(r"^[A-Za-z]:/", relative_path) or relative_path.startswith(("/", "//")):
        fail(f"aoa-agents repo ref must stay inside this repository: {ref}")
    if ".." in Path(relative_path).parts:
        fail(f"aoa-agents repo ref must stay inside this repository: {ref}")
    target = (REPO_ROOT / relative_path).resolve()
    try:
        target.relative_to(REPO_ROOT.resolve())
    except ValueError:
        fail(f"aoa-agents repo ref must stay inside this repository: {ref}")
    if not target.exists():
        fail(f"aoa-agents repo ref does not resolve to an existing public surface: {ref}")
    return target


def validate_optional_memo_object_smoke_check(memo_root: Path) -> None:
    for surface_file in MEMO_OBJECT_SURFACE_PATHS:
        read_json(memo_root / surface_file, root=memo_root)

    for contract_file, expected_mode in MEMO_OBJECT_RECALL_CONTRACTS:
        payload = read_json(memo_root / contract_file, root=memo_root)
        if not isinstance(payload, dict):
            fail(f"aoa-memo {contract_file} must be a JSON object")
        mode = payload.get("mode")
        if mode != expected_mode:
            fail(f"aoa-memo {contract_file} must declare mode '{expected_mode}'")
        if payload.get("inspect_surface") != MEMO_OBJECT_INSPECT_SURFACE:
            fail(
                f"aoa-memo {contract_file} must point inspect_surface at {MEMO_OBJECT_INSPECT_SURFACE}"
            )
        if payload.get("expand_surface") != MEMO_OBJECT_EXPAND_SURFACE:
            fail(
                f"aoa-memo {contract_file} must point expand_surface at {MEMO_OBJECT_EXPAND_SURFACE}"
            )
        if expected_mode in MEMO_CAPSULE_REQUIRED_MODES and payload.get("capsule_surface") != MEMO_OBJECT_CAPSULE_SURFACE:
            fail(
                f"aoa-memo {contract_file} must point capsule_surface at {MEMO_OBJECT_CAPSULE_SURFACE}"
            )


def format_role_sets(role_sets: object) -> str:
    if not isinstance(role_sets, list):
        return "<invalid role set payload>"
    formatted: list[str] = []
    for role_set in role_sets:
        if isinstance(role_set, list):
            formatted.append("[" + ", ".join(str(item) for item in role_set) + "]")
        else:
            formatted.append(str(role_set))
    return "; ".join(formatted)


def validate_reference_playbook_cohort_compatibility(
    playbooks_root: Path, cohort_patterns_by_id: dict[str, dict[str, object]]
) -> None:
    payload = read_json(playbooks_root / "generated" / "playbook_registry.min.json", root=playbooks_root)
    if not isinstance(payload, dict) or not isinstance(payload.get("playbooks"), list):
        fail("aoa-playbooks generated/playbook_registry.min.json must expose a playbooks list")

    playbooks_by_id = {
        playbook.get("id"): playbook
        for playbook in payload["playbooks"]
        if isinstance(playbook, dict) and isinstance(playbook.get("id"), str)
    }

    checkpoint_playbook = playbooks_by_id.get("AOA-P-0006")
    if not isinstance(checkpoint_playbook, dict):
        fail("aoa-playbooks registry is missing playbook 'AOA-P-0006'")
    checkpoint_roles = checkpoint_playbook.get("participating_agents")
    checkpoint_pattern = cohort_patterns_by_id.get("checkpoint_cohort")
    if not isinstance(checkpoint_pattern, dict):
        fail("aoa-agents cohort registry is missing pattern 'checkpoint_cohort'")
    checkpoint_allowed_role_sets = checkpoint_pattern.get("allowed_role_sets")
    if (
        not isinstance(checkpoint_allowed_role_sets, list)
        or not checkpoint_allowed_role_sets
        or not isinstance(checkpoint_allowed_role_sets[0], list)
    ):
        fail("aoa-agents checkpoint_cohort pattern must expose at least one allowed_role_sets entry")
    expected_checkpoint_roles = checkpoint_allowed_role_sets[0]
    if checkpoint_roles != expected_checkpoint_roles:
        fail(
            "aoa-playbooks AOA-P-0006 participating_agents must match "
            f"checkpoint_cohort.allowed_role_sets[0]: expected {expected_checkpoint_roles}, got {checkpoint_roles}"
        )

    orchestrated_playbook = playbooks_by_id.get("AOA-P-0008")
    if not isinstance(orchestrated_playbook, dict):
        fail("aoa-playbooks registry is missing playbook 'AOA-P-0008'")
    orchestrated_roles = orchestrated_playbook.get("participating_agents")
    orchestrated_pattern = cohort_patterns_by_id.get("orchestrated_loop")
    if not isinstance(orchestrated_pattern, dict):
        fail("aoa-agents cohort registry is missing pattern 'orchestrated_loop'")
    orchestrated_allowed_role_sets = orchestrated_pattern.get("allowed_role_sets")
    if not isinstance(orchestrated_allowed_role_sets, list) or not orchestrated_allowed_role_sets:
        fail("aoa-agents orchestrated_loop pattern must expose at least one allowed_role_sets entry")
    if orchestrated_roles not in orchestrated_allowed_role_sets:
        fail(
            "aoa-playbooks AOA-P-0008 participating_agents must match one of "
            "orchestrated_loop.allowed_role_sets: "
            f"allowed {format_role_sets(orchestrated_allowed_role_sets)}, got {orchestrated_roles}"
        )


def validate_optional_routing_smoke_check(routing_root: Path, tiers_by_id: dict[str, dict[str, object]]) -> None:
    payload = read_json(routing_root / "generated" / "task_to_tier_hints.json", root=routing_root)
    if not isinstance(payload, dict):
        fail("aoa-routing generated/task_to_tier_hints.json must be a JSON object")

    source_of_truth = payload.get("source_of_truth")
    if not isinstance(source_of_truth, dict):
        fail("aoa-routing task_to_tier_hints.json must expose source_of_truth")
    if source_of_truth.get("tier_registry_repo") != "aoa-agents":
        fail("aoa-routing task_to_tier_hints.json must keep source_of_truth.tier_registry_repo = 'aoa-agents'")
    if source_of_truth.get("tier_registry_path") != "generated/model_tier_registry.json":
        fail(
            "aoa-routing task_to_tier_hints.json must keep "
            "source_of_truth.tier_registry_path = 'generated/model_tier_registry.json'"
        )

    hints = payload.get("hints")
    if not isinstance(hints, list) or not hints:
        fail("aoa-routing task_to_tier_hints.json must expose a non-empty hints list")

    for index, hint in enumerate(hints):
        location = f"aoa-routing task_to_tier_hints.json.hints[{index}]"
        if not isinstance(hint, dict):
            fail(f"{location} must be an object")
        preferred_tier = hint.get("preferred_tier")
        fallback_tier = hint.get("fallback_tier")
        output_artifact = hint.get("output_artifact")

        if not isinstance(preferred_tier, str) or preferred_tier not in tiers_by_id:
            fail(f"{location}.preferred_tier must resolve in aoa-agents model-tier registry")
        if fallback_tier is not None and (not isinstance(fallback_tier, str) or fallback_tier not in tiers_by_id):
            fail(f"{location}.fallback_tier must resolve in aoa-agents model-tier registry when present")

        expected_artifact = tiers_by_id[preferred_tier]["artifact_requirement"]
        if output_artifact != expected_artifact:
            fail(
                f"{location}.output_artifact must match artifact_requirement for tier '{preferred_tier}' "
                f"('{expected_artifact}')"
            )

    routing_hints = read_json(routing_root / ROUTING_TASK_TO_SURFACE_HINTS_PATH, root=routing_root)
    if not isinstance(routing_hints, dict):
        fail(f"aoa-routing {ROUTING_TASK_TO_SURFACE_HINTS_PATH} must be a JSON object")

    hint_entries = routing_hints.get("hints")
    memo_hint = find_mapping_by_key(hint_entries, key="kind", expected_value="memo")
    if memo_hint is None:
        fail("aoa-routing task_to_surface_hints.json must publish a memo hint")
    actions = memo_hint.get("actions")
    if not isinstance(actions, dict):
        fail("aoa-routing memo hint must expose actions")

    inspect = actions.get("inspect")
    if not isinstance(inspect, dict) or inspect.get("surface_file") != ROUTING_MEMO_DOCTRINE_INSPECT_SURFACE:
        fail(
            "aoa-routing memo hint must keep doctrine inspect_surface = "
            f"'{ROUTING_MEMO_DOCTRINE_INSPECT_SURFACE}'"
        )

    expand = actions.get("expand")
    if not isinstance(expand, dict) or expand.get("surface_file") != ROUTING_MEMO_DOCTRINE_EXPAND_SURFACE:
        fail(
            "aoa-routing memo hint must keep doctrine expand_surface = "
            f"'{ROUTING_MEMO_DOCTRINE_EXPAND_SURFACE}'"
        )

    recall = actions.get("recall")
    if not isinstance(recall, dict) or recall.get("enabled") is not True:
        fail("aoa-routing memo hint must expose enabled recall routing")

    doctrine_supported_modes = recall.get("supported_modes")
    if not isinstance(doctrine_supported_modes, list) or not doctrine_supported_modes:
        fail("aoa-routing memo recall hint must expose non-empty doctrine supported_modes")
    doctrine_supported_mode_set = set()
    for mode in doctrine_supported_modes:
        if not isinstance(mode, str) or not mode:
            fail("aoa-routing memo recall supported_modes must contain non-empty strings")
        doctrine_supported_mode_set.add(mode)

    doctrine_default_mode = recall.get("default_mode")
    if not isinstance(doctrine_default_mode, str) or doctrine_default_mode not in doctrine_supported_mode_set:
        fail("aoa-routing memo recall default_mode must resolve in doctrine supported_modes")

    doctrine_contracts_by_mode = recall.get("contracts_by_mode")
    if not isinstance(doctrine_contracts_by_mode, dict):
        fail("aoa-routing memo recall hint must expose doctrine contracts_by_mode")
    for mode in doctrine_supported_mode_set:
        if mode not in doctrine_contracts_by_mode:
            fail(
                "aoa-routing memo recall hint must publish a doctrine contract for mode "
                f"'{mode}'"
            )
    doctrine_capsule_surfaces_by_mode = recall.get("capsule_surfaces_by_mode")
    if not isinstance(doctrine_capsule_surfaces_by_mode, dict):
        fail("aoa-routing memo recall hint must expose doctrine capsule_surfaces_by_mode")
    for mode in MEMO_CAPSULE_REQUIRED_MODES:
        if mode not in doctrine_supported_mode_set:
            continue
        if doctrine_capsule_surfaces_by_mode.get(mode) != ROUTING_MEMO_DOCTRINE_CAPSULE_SURFACE:
            fail(
                "aoa-routing memo recall hint must publish doctrine capsule_surfaces_by_mode "
                f"for mode '{mode}' -> '{ROUTING_MEMO_DOCTRINE_CAPSULE_SURFACE}'"
            )

    parallel_families = recall.get("parallel_families")
    if not isinstance(parallel_families, dict):
        fail("aoa-routing memo recall hint must expose parallel_families")
    object_family = parallel_families.get(ROUTING_MEMO_OBJECT_RECALL_FAMILY)
    if not isinstance(object_family, dict):
        fail(
            "aoa-routing memo recall hint must publish the "
            f"'{ROUTING_MEMO_OBJECT_RECALL_FAMILY}' recall family"
        )
    if object_family.get("inspect_surface") != MEMO_OBJECT_INSPECT_SURFACE:
        fail(
            "aoa-routing memory_objects recall family must point inspect_surface at "
            f"'{MEMO_OBJECT_INSPECT_SURFACE}'"
        )
    if object_family.get("expand_surface") != MEMO_OBJECT_EXPAND_SURFACE:
        fail(
            "aoa-routing memory_objects recall family must point expand_surface at "
            f"'{MEMO_OBJECT_EXPAND_SURFACE}'"
        )

    object_supported_mode_set = {mode for _, mode in MEMO_OBJECT_RECALL_CONTRACTS}
    object_supported_modes = object_family.get("supported_modes")
    if not isinstance(object_supported_modes, list):
        fail("aoa-routing memory_objects recall family must expose supported_modes")
    actual_object_mode_set: set[str] = set()
    for mode in object_supported_modes:
        if not isinstance(mode, str) or not mode:
            fail("aoa-routing memory_objects supported_modes must contain non-empty strings")
        actual_object_mode_set.add(mode)
    if actual_object_mode_set != object_supported_mode_set:
        fail(
            "aoa-routing memory_objects supported_modes must match aoa-memo object recall modes: "
            f"expected {sorted(object_supported_mode_set)}, got {sorted(actual_object_mode_set)}"
        )
    if object_family.get("default_mode") != "working":
        fail("aoa-routing memory_objects recall family must keep default_mode = 'working'")

    object_contracts_by_mode = object_family.get("contracts_by_mode")
    if not isinstance(object_contracts_by_mode, dict):
        fail("aoa-routing memory_objects recall family must expose contracts_by_mode")
    for contract_file, mode in MEMO_OBJECT_RECALL_CONTRACTS:
        if object_contracts_by_mode.get(mode) != contract_file:
            fail(
                "aoa-routing memory_objects recall family must mirror aoa-memo object contract "
                f"'{contract_file}' for mode '{mode}'"
            )
    object_capsule_surfaces_by_mode = object_family.get("capsule_surfaces_by_mode")
    if not isinstance(object_capsule_surfaces_by_mode, dict):
        fail("aoa-routing memory_objects recall family must expose capsule_surfaces_by_mode")
    for mode in MEMO_CAPSULE_REQUIRED_MODES:
        if object_capsule_surfaces_by_mode.get(mode) != MEMO_OBJECT_CAPSULE_SURFACE:
            fail(
                "aoa-routing memory_objects recall family must publish capsule_surfaces_by_mode "
                f"for mode '{mode}' -> '{MEMO_OBJECT_CAPSULE_SURFACE}'"
            )

    tiny_payload = read_json(routing_root / ROUTING_TINY_MODEL_ENTRYPOINTS_PATH, root=routing_root)
    if not isinstance(tiny_payload, dict):
        fail(f"aoa-routing {ROUTING_TINY_MODEL_ENTRYPOINTS_PATH} must be a JSON object")

    queries = tiny_payload.get("queries")
    if not isinstance(queries, list) or not queries:
        fail("aoa-routing tiny_model_entrypoints.json must expose a non-empty queries list")
    starters = tiny_payload.get("starters")
    if not isinstance(starters, list) or not starters:
        fail("aoa-routing tiny_model_entrypoints.json must expose a non-empty starters list")

    doctrine_query_found = False
    object_query_found = False
    for query in queries:
        if not isinstance(query, dict):
            continue
        if query.get("verb") != "recall":
            continue
        if query.get("target_surface") != ROUTING_TASK_TO_SURFACE_HINTS_PATH:
            continue
        if query.get("match_key") != "kind" or query.get("allowed_kinds") != ["memo"]:
            continue
        recall_family = query.get("recall_family")
        if recall_family is None:
            doctrine_query_found = True
        elif recall_family == ROUTING_MEMO_OBJECT_RECALL_FAMILY:
            object_query_found = True

    if not doctrine_query_found:
        fail("aoa-routing tiny_model_entrypoints.json must publish a doctrine-default memo recall query")
    if not object_query_found:
        fail(
            "aoa-routing tiny_model_entrypoints.json must publish a memo recall query for "
            f"recall_family = '{ROUTING_MEMO_OBJECT_RECALL_FAMILY}'"
        )

    doctrine_starter_modes: set[str] = set()
    object_starter_modes: set[str] = set()
    for starter in starters:
        if not isinstance(starter, dict):
            continue
        if starter.get("verb") != "recall":
            continue
        if starter.get("target_surface") != ROUTING_TASK_TO_SURFACE_HINTS_PATH:
            continue
        if starter.get("match_key") != "kind":
            continue
        if starter.get("allowed_kinds") != ["memo"]:
            continue
        if starter.get("target_kind") != "memo" or starter.get("target_value") != "memo":
            fail("aoa-routing memo recall starters must keep target_kind/target_value = 'memo'")
        recall_mode = starter.get("recall_mode")
        if not isinstance(recall_mode, str) or not recall_mode:
            fail("aoa-routing memo recall starters must expose a non-empty recall_mode")
        recall_family = starter.get("recall_family")
        if recall_family is None:
            doctrine_starter_modes.add(recall_mode)
        elif recall_family == ROUTING_MEMO_OBJECT_RECALL_FAMILY:
            object_starter_modes.add(recall_mode)

    if doctrine_starter_modes != doctrine_supported_mode_set:
        fail(
            "aoa-routing doctrine recall starters must match doctrine supported_modes: "
            f"expected {sorted(doctrine_supported_mode_set)}, got {sorted(doctrine_starter_modes)}"
        )
    if object_starter_modes != object_supported_mode_set:
        fail(
            "aoa-routing memory_objects recall starters must match object family supported_modes: "
            f"expected {sorted(object_supported_mode_set)}, got {sorted(object_starter_modes)}"
        )


def validate_optional_consumer_smoke_checks(
    tiers_by_id: dict[str, dict[str, object]], cohort_patterns_by_id: dict[str, dict[str, object]]
) -> list[str]:
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
        validate_reference_playbook_cohort_compatibility(playbooks_root, cohort_patterns_by_id)
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
            if not ref.startswith("repo:aoa-agents/"):
                continue
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
        validate_optional_memo_object_smoke_check(memo_root)
        checked.append("aoa-memo")

    routing_root = env_repo_root("AOA_ROUTING_ROOT")
    if routing_root is not None:
        validate_optional_routing_smoke_check(routing_root, tiers_by_id)
        checked.append("aoa-routing")

    return checked


def main() -> int:
    try:
        validate_schema_surface()
        validate_model_tier_schema_surface()
        validate_model_tier_item_schema_surface()
        validate_agent_profile_schema_surface()
        validate_cohort_composition_schema_surface()
        validate_cohort_pattern_schema_surface()
        validate_runtime_seam_bindings_schema_surface()
        validate_runtime_seam_binding_item_schema_surface()
        validate_self_agent_checkpoint_schema_surface()
        validate_nested_agents_docs()
        validate_runtime_artifact_schema_surfaces()
        validate_runtime_artifact_examples()
        validate_negative_runtime_artifact_examples()
        self_agent_checkpoint_example = validate_self_agent_checkpoint_example()
        validate_negative_self_agent_checkpoint_examples()
        profiles = validate_agent_profile_sources()
        validate_model_tier_sources()
        validate_cohort_pattern_sources()
        validate_runtime_seam_binding_sources()
        agent_names = validate_registry()
        validate_self_agent_checkpoint_example_coherence(self_agent_checkpoint_example, profiles, agent_names)
        tiers_by_id = validate_model_tier_registry()
        cohort_patterns_by_id = validate_cohort_composition_registry(agent_names, tiers_by_id)
        validate_agent_profile_references(profiles, tiers_by_id, cohort_patterns_by_id)
        validate_runtime_seam_bindings(agent_names, tiers_by_id)
        validate_runtime_seam_doc_coherence()
        checked_roots = validate_optional_consumer_smoke_checks(tiers_by_id, cohort_patterns_by_id)
    except (NestedAgentsValidationError, ValidationError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[ok] validated agent registry schema surface")
    print("[ok] validated model-tier registry schema surface")
    print("[ok] validated model-tier item schema surface")
    print("[ok] validated agent profile schema surface")
    print("[ok] validated cohort composition schema surface")
    print("[ok] validated cohort-pattern schema surface")
    print("[ok] validated runtime seam bindings schema surface")
    print("[ok] validated runtime-seam-binding schema surface")
    print("[ok] validated self-agent-checkpoint schema surface")
    print("[ok] validated nested AGENTS.md guidance surfaces")
    print("[ok] validated source-authored agent profiles")
    print("[ok] validated source-authored model tiers")
    print("[ok] validated source-authored cohort patterns")
    print("[ok] validated source-authored runtime seam bindings")
    print("[ok] validated runtime artifact schema surfaces")
    print("[ok] validated runtime artifact examples")
    print("[ok] validated self-agent checkpoint examples")
    print("[ok] validated runtime seam bindings")
    print("[ok] validated generated/agent_registry.min.json")
    print("[ok] validated generated/model_tier_registry.json")
    print("[ok] validated generated/cohort_composition_registry.json")
    print("[ok] validated generated/runtime_seam_bindings.json")
    if checked_roots:
        print(f"[ok] validated optional consumer smoke checks against: {', '.join(checked_roots)}")
    else:
        print("[ok] optional consumer smoke checks skipped (env roots not set)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
