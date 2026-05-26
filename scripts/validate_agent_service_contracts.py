#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]

EXPERIENCE_ADOPTION_PART = Path("mechanics/experience/parts/adoption-and-regression")
EXPERIENCE_ARENA_PART = Path("mechanics/experience/parts/arena-exclusion")
EXPERIENCE_CIVIL_PART = Path("mechanics/experience/parts/assistant-civil-service")
EXPERIENCE_OFFICE_PART = Path("mechanics/experience/parts/office-operations")
EXPERIENCE_RELEASE_PART = Path("mechanics/experience/parts/runtime-release-holds")
EXPERIENCE_WATCH_PART = Path("mechanics/experience/parts/watch-and-rollback")
RUNTIME_AUTHORITY_PART = Path("mechanics/runtime-seam/parts/artifact-contracts")
RELEASE_HOLD_PART = Path("mechanics/release-support/parts/runtime-release-hold")

ESCAPE_VALUE = "__agent_service_contract_escape__"


class AgentServiceContractsValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class AgentServiceContract:
    part: Path
    active_stem: str
    former_schema_tokens: tuple[str, ...]
    former_example_tokens: tuple[str, ...] | None = None
    former_example_has_v1: bool = False

    @property
    def schema_rel(self) -> Path:
        return self.part / "schemas" / f"{self.active_stem}.schema.json"

    @property
    def example_rel(self) -> Path:
        return self.part / "examples" / f"{self.active_stem}.example.json"

    @property
    def former_schema_name(self) -> str:
        return f"{_former_stem(*self.former_schema_tokens)}_v1.json"

    @property
    def former_example_name(self) -> str:
        tokens = self.former_example_tokens or self.former_schema_tokens
        suffix = "_v1" if self.former_example_has_v1 else ""
        return f"{_former_stem(*tokens)}{suffix}.example.json"


def _former_stem(*parts: str) -> str:
    return "_".join(parts)


def _contract(
    part: Path,
    active_stem: str,
    *former_schema_tokens: str,
    example_tokens: tuple[str, ...] | None = None,
    example_v1: bool = False,
) -> AgentServiceContract:
    return AgentServiceContract(
        part=part,
        active_stem=active_stem,
        former_schema_tokens=former_schema_tokens,
        former_example_tokens=example_tokens,
        former_example_has_v1=example_v1,
    )


CONTRACTS = (
    _contract(EXPERIENCE_ADOPTION_PART, "assistant-behavior-contract-delta", "assistant", "behavior", "contract", "delta"),
    _contract(EXPERIENCE_ADOPTION_PART, "assistant-canary-probe-matrix", "assistant", "canary", "probe", "matrix"),
    _contract(EXPERIENCE_ADOPTION_PART, "assistant-regression-result", "assistant", "regression", "result"),
    _contract(EXPERIENCE_ARENA_PART, "agent-kind-conflict-case", "agent", "kind", "conflict", "case"),
    _contract(EXPERIENCE_ARENA_PART, "assistant-recharter-request", "assistant", "recharter", "request"),
    _contract(EXPERIENCE_CIVIL_PART, "agent-governance-posture", "agent", "governance", "posture"),
    _contract(EXPERIENCE_OFFICE_PART, "agent-office-charter-change", "agent", "office", "charter", "change"),
    _contract(
        EXPERIENCE_OFFICE_PART,
        "assistant-multi-office-release-result",
        "assistant",
        "multi",
        "office",
        "release",
        "result",
        example_v1=True,
    ),
    _contract(
        EXPERIENCE_OFFICE_PART,
        "assistant-office-install-profile",
        "assistant",
        "office",
        "install",
        "profile",
        example_v1=True,
    ),
    _contract(
        EXPERIENCE_OFFICE_PART,
        "assistant-office-live-profile",
        "assistant",
        "office",
        "live",
        "profile",
        example_v1=True,
    ),
    _contract(EXPERIENCE_OFFICE_PART, "assistant-office-pairing", "assistant", "office", "pairing", example_v1=True),
    _contract(
        EXPERIENCE_OFFICE_PART,
        "assistant-office-revision-ledger-entry",
        "assistant",
        "office",
        "revision",
        "ledger",
        "entry",
        example_v1=True,
    ),
    _contract(
        EXPERIENCE_OFFICE_PART,
        "assistant-office-service-contract",
        "assistant",
        "office",
        "service",
        "contract",
        example_v1=True,
    ),
    _contract(
        EXPERIENCE_OFFICE_PART,
        "assistant-train-release-participant",
        "assistant",
        "train",
        "release",
        "participant",
        example_v1=True,
    ),
    _contract(
        EXPERIENCE_RELEASE_PART,
        "agent-install-compatibility",
        "agent",
        "install",
        "compatibility",
        example_v1=True,
    ),
    _contract(
        EXPERIENCE_RELEASE_PART,
        "assistant-office-live-contract",
        "assistant",
        "office",
        "live",
        "contract",
        example_v1=True,
    ),
    _contract(EXPERIENCE_RELEASE_PART, "assistant-release-activation", "assistant", "release", "activation"),
    _contract(EXPERIENCE_RELEASE_PART, "assistant-release-approval", "assistant", "release", "approval"),
    _contract(EXPERIENCE_RELEASE_PART, "assistant-release-candidate", "assistant", "release", "candidate"),
    _contract(EXPERIENCE_RELEASE_PART, "assistant-runtime-hold", "assistant", "runtime", "hold", example_v1=True),
    _contract(
        EXPERIENCE_RELEASE_PART,
        "assistant-service-release",
        "assistant",
        "service",
        "release",
        example_v1=True,
    ),
    _contract(EXPERIENCE_RELEASE_PART, "assistant-service-version", "assistant", "service", "version"),
    _contract(EXPERIENCE_WATCH_PART, "assistant-deployment-instance", "assistant", "deployment", "instance"),
    _contract(EXPERIENCE_WATCH_PART, "assistant-live-incident", "assistant", "live", "incident", example_v1=True),
    _contract(EXPERIENCE_WATCH_PART, "assistant-office-incident", "assistant", "office", "incident", example_v1=True),
    _contract(
        EXPERIENCE_WATCH_PART,
        "assistant-office-post-release-watch",
        "assistant",
        "office",
        "post",
        "release",
        "watch",
        example_v1=True,
    ),
    _contract(
        EXPERIENCE_WATCH_PART,
        "assistant-post-release-certification-watch",
        "assistant",
        "post",
        "release",
        "certification",
        "watch",
    ),
    _contract(EXPERIENCE_WATCH_PART, "assistant-post-release-watch", "assistant", "post", "release", "watch"),
    _contract(
        EXPERIENCE_WATCH_PART,
        "assistant-release-watch-config",
        "assistant",
        "release",
        "watch",
        "config",
        example_v1=True,
    ),
    _contract(EXPERIENCE_WATCH_PART, "assistant-ring-state", "assistant", "ring", "state"),
    _contract(EXPERIENCE_WATCH_PART, "assistant-rollback-execution", "assistant", "rollback", "execution"),
    _contract(EXPERIENCE_WATCH_PART, "assistant-rollback-policy", "assistant", "rollback", "policy"),
    _contract(
        EXPERIENCE_WATCH_PART,
        "assistant-runtime-behavior-snapshot",
        "assistant",
        "runtime",
        "behavior",
        "snapshot",
    ),
    _contract(EXPERIENCE_WATCH_PART, "assistant-watchtower-alarm", "assistant", "watchtower", "alarm"),
    _contract(
        RUNTIME_AUTHORITY_PART,
        "agent-authority-claim",
        "agent",
        "authority",
        "claim",
        example_v1=True,
    ),
    _contract(RELEASE_HOLD_PART, "agent-release-hold", "agent", "release", "hold"),
)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AgentServiceContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AgentServiceContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


def _schema(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise AgentServiceContractsValidationError(f"{path} must contain a JSON object schema")
    try:
        Draft202012Validator.check_schema(payload)
    except SchemaError as exc:
        raise AgentServiceContractsValidationError(
            f"{path} is not a valid draft 2020-12 schema: {exc}"
        ) from exc
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise AgentServiceContractsValidationError(f"{path} must use draft 2020-12")
    return payload


def validation_errors(schema: dict[str, Any], value: object) -> list[object]:
    return sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda error: (list(error.path), error.message),
    )


def effective_schema(schema: object, value: object) -> object:
    if not isinstance(schema, dict):
        return schema
    variants = schema.get("oneOf")
    if isinstance(variants, list):
        for variant in variants:
            if isinstance(variant, dict) and not validation_errors(variant, value):
                return variant
    return schema


def schema_properties(schema: object, value: object | None = None) -> dict[str, object]:
    if value is not None:
        schema = effective_schema(schema, value)
    if not isinstance(schema, dict):
        return {}
    properties = schema.get("properties")
    return properties if isinstance(properties, dict) else {}


def child_schema(schema: object, value: object, key: object) -> object:
    schema = effective_schema(schema, value)
    if isinstance(key, str) and isinstance(value, dict):
        return schema_properties(schema, value).get(key, {})
    if isinstance(key, int) and isinstance(value, list) and isinstance(schema, dict):
        return effective_schema(schema.get("items", {}), value[key])
    return {}


def schema_for_path(schema: object, example: object, path: tuple[object, ...]) -> object:
    cursor_schema = schema
    cursor_value = example
    for part in path:
        cursor_schema = child_schema(cursor_schema, cursor_value, part)
        if isinstance(part, int):
            assert isinstance(cursor_value, list)
            cursor_value = cursor_value[part]
        else:
            assert isinstance(cursor_value, dict)
            cursor_value = cursor_value[part]
    return effective_schema(cursor_schema, cursor_value)


def wrong_type_value(value: object) -> object:
    if isinstance(value, bool):
        return "not-a-boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "not-an-integer"
    if isinstance(value, float):
        return "not-a-number"
    if isinstance(value, str):
        return 12345
    if isinstance(value, list):
        return {"not": "an array"}
    if isinstance(value, dict):
        return "not-an-object"
    return "not-null"


def escape_value(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int) and not isinstance(value, bool):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return f"{value}{ESCAPE_VALUE}"
    return ESCAPE_VALUE


def get_path(value: object, path: tuple[object, ...]) -> object:
    cursor = value
    for part in path:
        if isinstance(part, int):
            assert isinstance(cursor, list)
            cursor = cursor[part]
        else:
            assert isinstance(cursor, dict)
            cursor = cursor[part]
    return cursor


def set_path(value: object, path: tuple[object, ...], replacement: object) -> None:
    cursor = value
    for part in path[:-1]:
        if isinstance(part, int):
            assert isinstance(cursor, list)
            cursor = cursor[part]
        else:
            assert isinstance(cursor, dict)
            cursor = cursor[part]
    last = path[-1]
    if isinstance(last, int):
        assert isinstance(cursor, list)
        cursor[last] = replacement
    else:
        assert isinstance(cursor, dict)
        cursor[last] = replacement


def delete_path(value: object, path: tuple[object, ...]) -> None:
    cursor = value
    for part in path[:-1]:
        if isinstance(part, int):
            assert isinstance(cursor, list)
            cursor = cursor[part]
        else:
            assert isinstance(cursor, dict)
            cursor = cursor[part]
    last = path[-1]
    if isinstance(last, int):
        assert isinstance(cursor, list)
        del cursor[last]
    else:
        assert isinstance(cursor, dict)
        del cursor[last]


def walk_values(value: object, path: tuple[object, ...] = ()) -> list[tuple[tuple[object, ...], object]]:
    found: list[tuple[tuple[object, ...], object]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = (*path, key)
            found.append((child_path, child))
            found.extend(walk_values(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = (*path, index)
            found.append((child_path, child))
            found.extend(walk_values(child, child_path))
    return found


def object_paths(value: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    found: list[tuple[object, ...]] = []
    if isinstance(value, dict):
        found.append(path)
        for key, child in value.items():
            found.extend(object_paths(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(object_paths(child, (*path, index)))
    return found


def array_paths(value: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    found: list[tuple[object, ...]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found.extend(array_paths(child, (*path, key)))
    elif isinstance(value, list):
        found.append(path)
        for index, child in enumerate(value):
            found.extend(array_paths(child, (*path, index)))
    return found


def string_paths(value: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    found: list[tuple[object, ...]] = []
    if isinstance(value, str):
        found.append(path)
    elif isinstance(value, dict):
        for key, child in value.items():
            found.extend(string_paths(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(string_paths(child, (*path, index)))
    return found


def required_paths(schema: object, example: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    schema = effective_schema(schema, example)
    found: list[tuple[object, ...]] = []
    if isinstance(schema, dict) and schema.get("type") == "object" and isinstance(example, dict):
        required = schema.get("required")
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key in example:
                    found.append((*path, key))
        for key, prop in schema_properties(schema, example).items():
            if key in example:
                found.extend(required_paths(prop, example[key], (*path, key)))
    if isinstance(schema, dict) and schema.get("type") == "array" and isinstance(example, list) and example:
        found.extend(required_paths(schema.get("items"), example[0], (*path, 0)))
    return found


def constrained_paths(
    schema: object,
    example: object,
    keyword: str,
    path: tuple[object, ...] = (),
) -> list[tuple[tuple[object, ...], object]]:
    schema = effective_schema(schema, example)
    found: list[tuple[tuple[object, ...], object]] = []
    if not isinstance(schema, dict):
        return found
    if keyword in schema:
        found.append((path, schema[keyword]))
    if schema.get("type") == "object" and isinstance(example, dict):
        for key, prop in schema_properties(schema, example).items():
            if key in example:
                found.extend(constrained_paths(prop, example[key], keyword, (*path, key)))
    if schema.get("type") == "array" and isinstance(example, list) and example:
        found.extend(constrained_paths(schema.get("items"), example[0], keyword, (*path, 0)))
    return found


def should_check_wrong_type(schema: object) -> bool:
    return isinstance(schema, dict) and any(key in schema for key in ("type", "enum", "const", "oneOf"))


def should_check_array_items(schema: object) -> bool:
    return isinstance(schema, dict) and schema.get("type") == "array" and "items" in schema


def should_check_empty_string(schema: object) -> bool:
    return isinstance(schema, dict) and schema.get("type") == "string" and schema.get("minLength", 0) > 0


def assert_invalid(errors: list[str], schema: dict[str, Any], value: object, label: str) -> None:
    validation = validation_errors(schema, value)
    if not validation:
        errors.append(f"{label} unexpectedly validated")


def collect_agent_service_contract_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    if not CONTRACTS:
        errors.append("no agent service contracts configured")

    for contract in CONTRACTS:
        former_schema = root / "schemas" / contract.former_schema_name
        former_example = root / "examples" / contract.former_example_name
        if former_schema.exists():
            errors.append(f"former root schema is still active: {former_schema.relative_to(root).as_posix()}")
        if former_example.exists():
            errors.append(f"former root example is still active: {former_example.relative_to(root).as_posix()}")

        schema_path = root / contract.schema_rel
        example_path = root / contract.example_rel
        try:
            schema = _schema(schema_path)
            example = _read_json(example_path)
        except AgentServiceContractsValidationError as exc:
            errors.append(str(exc))
            continue

        example_errors = validation_errors(schema, example)
        if example_errors:
            errors.append(f"{contract.example_rel.as_posix()}: {example_errors[0].message}")
            continue

        for path in object_paths(example):
            field_schema = schema_for_path(schema, example, path)
            if not (isinstance(field_schema, dict) and field_schema.get("additionalProperties") is False):
                continue
            mutated = copy.deepcopy(example)
            target = get_path(mutated, path) if path else mutated
            if not isinstance(target, dict):
                continue
            target["contract_escape"] = "loose-field"
            label = f"{contract.active_stem} unknown field at {'.'.join(str(part) for part in path) or 'top'}"
            assert_invalid(errors, schema, mutated, label)

        for path, value in walk_values(example):
            field_schema = schema_for_path(schema, example, path)
            if not should_check_wrong_type(field_schema):
                continue
            mutated = copy.deepcopy(example)
            set_path(mutated, path, wrong_type_value(value))
            label = f"{contract.active_stem} wrong type at {'.'.join(str(part) for part in path)}"
            assert_invalid(errors, schema, mutated, label)

        for path in required_paths(schema, example):
            mutated = copy.deepcopy(example)
            delete_path(mutated, path)
            label = f"{contract.active_stem} missing required field at {'.'.join(str(part) for part in path)}"
            assert_invalid(errors, schema, mutated, label)

        for path in array_paths(example):
            field_schema = schema_for_path(schema, example, path)
            if not should_check_array_items(field_schema):
                continue
            mutated = copy.deepcopy(example)
            array_value = get_path(mutated, path)
            if not isinstance(array_value, list):
                continue
            if array_value:
                array_value[0] = wrong_type_value(array_value[0])
            else:
                array_value.append({"not": "a valid array item"})
            label = f"{contract.active_stem} bad array item at {'.'.join(str(part) for part in path)}"
            assert_invalid(errors, schema, mutated, label)

        for path in string_paths(example):
            field_schema = schema_for_path(schema, example, path)
            if not should_check_empty_string(field_schema):
                continue
            mutated = copy.deepcopy(example)
            set_path(mutated, path, "")
            label = f"{contract.active_stem} empty string at {'.'.join(str(part) for part in path)}"
            assert_invalid(errors, schema, mutated, label)

        for path, _constraint in constrained_paths(schema, example, "const"):
            if not path:
                continue
            mutated = copy.deepcopy(example)
            set_path(mutated, path, escape_value(get_path(example, path)))
            label = f"{contract.active_stem} const escape at {'.'.join(str(part) for part in path)}"
            assert_invalid(errors, schema, mutated, label)

        for path, _constraint in constrained_paths(schema, example, "enum"):
            if not path:
                continue
            mutated = copy.deepcopy(example)
            set_path(mutated, path, escape_value(get_path(example, path)))
            label = f"{contract.active_stem} enum escape at {'.'.join(str(part) for part in path)}"
            assert_invalid(errors, schema, mutated, label)

        for path, value in walk_values(example):
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                continue
            field_schema = schema_for_path(schema, example, path)
            if not isinstance(field_schema, dict):
                continue
            if "minimum" in field_schema:
                mutated = copy.deepcopy(example)
                set_path(mutated, path, field_schema["minimum"] - 1)
                label = f"{contract.active_stem} below minimum at {'.'.join(str(part) for part in path)}"
                assert_invalid(errors, schema, mutated, label)
            if "maximum" in field_schema:
                mutated = copy.deepcopy(example)
                set_path(mutated, path, field_schema["maximum"] + 1)
                label = f"{contract.active_stem} above maximum at {'.'.join(str(part) for part in path)}"
                assert_invalid(errors, schema, mutated, label)

    return errors


def validate_agent_service_contracts(root: Path = ROOT) -> None:
    errors = collect_agent_service_contract_errors(root)
    if errors:
        raise AgentServiceContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate part-local agent service contract payloads.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_agent_service_contracts(root)
    except AgentServiceContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Agent service contract validation passed. contracts={len(CONTRACTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
