#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError


ROOT = Path(__file__).resolve().parents[3]
SELF_AGENT_PART = Path("mechanics/checkpoint/parts/self-agent-checkpoint")
CONTINUITY_PART = Path("mechanics/checkpoint/parts/continuity-lane")
FORMER_EXAMPLES_DIR = Path("examples") / ("self" + "_agent" + "_checkpoint")
FORMER_SCHEMA_NAMES = (
    "self-agent-checkpoint.schema.json",
    "self-agency-continuity-window.schema.json",
)
SELF_AGENT_SCHEMA = SELF_AGENT_PART / "schemas" / "self-agent-checkpoint.schema.json"
SELF_AGENT_EXAMPLE = SELF_AGENT_PART / "examples" / "self-agent-checkpoint.example.json"
SELF_AGENT_INVALID_DIR = SELF_AGENT_PART / "examples" / "invalid"
CONTINUITY_SCHEMA = CONTINUITY_PART / "schemas" / "self-agency-continuity-window.schema.json"
CONTINUITY_EXAMPLE = CONTINUITY_PART / "examples" / "self-agency-continuity-window.example.json"
EXPECTED_INVALID_FIXTURES = {
    "self-agent-checkpoint.missing-required-field.json": "required",
    "self-agent-checkpoint.invalid-approval-mode.json": "enum",
    "self-agent-checkpoint.max-iterations-below-minimum.json": "minimum",
}


class CheckpointContractsValidationError(RuntimeError):
    pass


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CheckpointContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CheckpointContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


def _schema(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise CheckpointContractsValidationError(f"{path} must contain a JSON object schema")
    try:
        Draft202012Validator.check_schema(payload)
    except SchemaError as exc:
        raise CheckpointContractsValidationError(
            f"{path} is not a valid draft 2020-12 schema: {exc.message}"
        ) from exc
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise CheckpointContractsValidationError(f"{path} must use draft 2020-12")
    return payload


def _validation_errors(schema: dict[str, Any], value: object) -> list[ValidationError]:
    return sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda error: (list(error.path), error.message),
    )


def _validate_payload(schema_path: Path, payload_path: Path) -> None:
    schema = _schema(schema_path)
    payload = _read_json(payload_path)
    errors = _validation_errors(schema, payload)
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise CheckpointContractsValidationError(
            f"{payload_path} does not match {schema_path}: {location}: {first.message}"
        )


def collect_checkpoint_contract_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    for file_name in FORMER_SCHEMA_NAMES:
        former_path = root / "schemas" / file_name
        if former_path.exists():
            errors.append(f"former root checkpoint schema is still active: {former_path.relative_to(root).as_posix()}")

    if (root / FORMER_EXAMPLES_DIR).exists():
        errors.append(f"former root checkpoint example directory is still active: {FORMER_EXAMPLES_DIR.as_posix()}")

    expected_self_agent_schemas = {SELF_AGENT_SCHEMA}
    actual_self_agent_schemas = {
        path.relative_to(root)
        for path in (root / SELF_AGENT_PART / "schemas").glob("*.json")
    }
    if actual_self_agent_schemas != expected_self_agent_schemas:
        errors.append("self-agent-checkpoint schema file set drifted")

    expected_continuity_schemas = {CONTINUITY_SCHEMA}
    actual_continuity_schemas = {
        path.relative_to(root)
        for path in (root / CONTINUITY_PART / "schemas").glob("*.json")
    }
    if actual_continuity_schemas != expected_continuity_schemas:
        errors.append("continuity-lane schema file set drifted")

    expected_self_agent_examples = {"self-agent-checkpoint.example.json"}
    actual_self_agent_examples = {
        path.name
        for path in (root / SELF_AGENT_PART / "examples").glob("*.example.json")
    }
    if actual_self_agent_examples != expected_self_agent_examples:
        errors.append("self-agent-checkpoint example file set drifted")

    expected_continuity_examples = {"self-agency-continuity-window.example.json"}
    actual_continuity_examples = {
        path.name
        for path in (root / CONTINUITY_PART / "examples").glob("*.example.json")
    }
    if actual_continuity_examples != expected_continuity_examples:
        errors.append("continuity-lane example file set drifted")

    invalid_dir = root / SELF_AGENT_INVALID_DIR
    if not invalid_dir.is_dir():
        errors.append(f"missing required directory: {SELF_AGENT_INVALID_DIR.as_posix()}")
    else:
        actual_invalids = {path.name for path in invalid_dir.glob("*.json")}
        expected_invalids = set(EXPECTED_INVALID_FIXTURES)
        if actual_invalids != expected_invalids:
            missing = sorted(expected_invalids - actual_invalids)
            extra = sorted(actual_invalids - expected_invalids)
            details: list[str] = []
            if missing:
                details.append("missing: " + ", ".join(missing))
            if extra:
                details.append("unexpected: " + ", ".join(extra))
            errors.append("self-agent checkpoint invalid fixtures drifted (" + "; ".join(details) + ")")

    try:
        _validate_payload(root / SELF_AGENT_SCHEMA, root / SELF_AGENT_EXAMPLE)
        _validate_payload(root / CONTINUITY_SCHEMA, root / CONTINUITY_EXAMPLE)
    except CheckpointContractsValidationError as exc:
        errors.append(str(exc))

    for file_name, expected_validator in EXPECTED_INVALID_FIXTURES.items():
        fixture_path = root / SELF_AGENT_INVALID_DIR / file_name
        if not fixture_path.exists():
            continue
        try:
            schema = _schema(root / SELF_AGENT_SCHEMA)
            payload = _read_json(fixture_path)
            validation_errors = _validation_errors(schema, payload)
        except CheckpointContractsValidationError as exc:
            errors.append(str(exc))
            continue
        if not validation_errors:
            errors.append(f"{fixture_path} unexpectedly passed validation")
            continue
        if not any(error.validator == expected_validator for error in validation_errors):
            validators = ", ".join(sorted({str(error.validator) for error in validation_errors}))
            errors.append(
                f"{fixture_path} failed with unexpected validator set '{validators}' "
                f"instead of '{expected_validator}'"
            )

    return errors


def validate_checkpoint_contracts(root: Path = ROOT) -> None:
    errors = collect_checkpoint_contract_errors(root)
    if errors:
        raise CheckpointContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate checkpoint part-local contract payloads.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_checkpoint_contracts(root)
    except CheckpointContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Checkpoint contract validation passed. schemas=2 examples=2 invalid=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
