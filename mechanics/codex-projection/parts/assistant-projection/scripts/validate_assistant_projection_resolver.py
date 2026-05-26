#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[5]
ASSISTANT_PART_ROOT = Path("mechanics/codex-projection/parts/assistant-projection")
PUBLIC_SCHEMA_PATH = ASSISTANT_PART_ROOT / "schemas" / "assistant-projection-resolver.schema.json"
LOCAL_V1_SCHEMA_PATH = ASSISTANT_PART_ROOT / "schemas" / "assistant-projection-resolver-v1.schema.json"
EXAMPLE_PATH = ASSISTANT_PART_ROOT / "examples" / "assistant-projection-resolver.example.json"
DOC_PATH = Path("mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md")
FORMER_ROOT_PATHS = {
    Path("schemas") / "assistant-projection-resolver.schema.json",
    Path("schemas") / ("assistant" + "_projection_resolver_v1.json"),
    Path("examples") / ("assistant" + "_projection_resolver.example.json"),
    Path("scripts") / "validate_assistant_projection_resolver.py",
}


class AssistantProjectionResolverValidationError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AssistantProjectionResolverValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AssistantProjectionResolverValidationError(f"invalid JSON in {path}: {exc}") from exc


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AssistantProjectionResolverValidationError(f"missing text file: {path}") from exc


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def collect_assistant_projection_resolver_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for former_path in sorted(FORMER_ROOT_PATHS):
        if (root / former_path).exists():
            errors.append(f"former root path is still active: {former_path.as_posix()}")

    active_schemas = {path.relative_to(root) for path in (root / ASSISTANT_PART_ROOT / "schemas").glob("*.json")}
    expected_schemas = {PUBLIC_SCHEMA_PATH, LOCAL_V1_SCHEMA_PATH}
    if active_schemas != expected_schemas:
        missing = sorted(expected_schemas - active_schemas)
        extra = sorted(active_schemas - expected_schemas)
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("assistant projection schema file set drifted (" + "; ".join(details) + ")")

    active_examples = {path.relative_to(root) for path in (root / ASSISTANT_PART_ROOT / "examples").glob("*.json")}
    if active_examples != {EXAMPLE_PATH}:
        missing = sorted({EXAMPLE_PATH} - active_examples)
        extra = sorted(active_examples - {EXAMPLE_PATH})
        details = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("assistant projection example file set drifted (" + "; ".join(details) + ")")

    for relative_path in expected_schemas | {EXAMPLE_PATH}:
        if "_" in relative_path.name:
            errors.append(f"{relative_path.as_posix()}: active assistant projection names must use part-local slug style")

    try:
        public_schema = read_json(root / PUBLIC_SCHEMA_PATH)
        local_v1_schema = read_json(root / LOCAL_V1_SCHEMA_PATH)
        example = read_json(root / EXAMPLE_PATH)
        doc = read_text(root / DOC_PATH)
        Draft202012Validator.check_schema(public_schema)
        Draft202012Validator.check_schema(local_v1_schema)
    except (AssistantProjectionResolverValidationError, SchemaError) as exc:
        errors.append(str(exc))
        return errors

    validation_errors = sorted(
        Draft202012Validator(public_schema).iter_errors(example),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if validation_errors:
        first = validation_errors[0]
        location = ".".join(str(part) for part in first.absolute_path)
        suffix = f" at {location}" if location else ""
        errors.append(f"{EXAMPLE_PATH.as_posix()}: schema violation{suffix}: {first.message}")

    for token in (
        PUBLIC_SCHEMA_PATH.as_posix(),
        EXAMPLE_PATH.as_posix(),
        "source profile",
        "projection wiring",
        "no-self-rewrite",
    ):
        if token not in doc:
            errors.append(f"{DOC_PATH.as_posix()} is missing required projection guidance: {token}")

    for text in iter_strings(example):
        if "examples/" + "assistant_projection_resolver" in text or "schemas/" + "assistant_projection_resolver" in text:
            errors.append(f"{EXAMPLE_PATH.as_posix()}: active payload still references former root projection namespace")

    if example.get("contract_id") != "aoa-agents.assistant-projection-resolver.v1":
        errors.append(f"{EXAMPLE_PATH.as_posix()} must keep contract_id aoa-agents.assistant-projection-resolver.v1")
    if example.get("owner_repo") != "aoa-agents":
        errors.append(f"{EXAMPLE_PATH.as_posix()} must keep owner_repo aoa-agents")
    if example.get("no_self_rewrite_posture", {}).get("allowed") is not False:
        errors.append(f"{EXAMPLE_PATH.as_posix()} must keep no_self_rewrite_posture.allowed false")

    return errors


def validate_assistant_projection_resolver(root: Path = ROOT) -> None:
    errors = collect_assistant_projection_resolver_errors(root)
    if errors:
        raise AssistantProjectionResolverValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate assistant projection resolver part-local payloads.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_assistant_projection_resolver(root)
    except AssistantProjectionResolverValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Assistant projection resolver validation passed. examples=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
