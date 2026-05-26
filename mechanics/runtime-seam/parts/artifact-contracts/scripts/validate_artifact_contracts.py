#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError


ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = Path("mechanics/runtime-seam/parts/artifact-contracts")
SCHEMAS_DIR = PART_ROOT / "schemas"
EXAMPLES_DIR = PART_ROOT / "examples"
INVALID_DIR = EXAMPLES_DIR / "invalid"
FORMER_ROOT_EXAMPLES_DIR = Path("examples") / ("runtime" + "_artifacts")
RUNTIME_ARTIFACT_NAMES = (
    "route_decision",
    "bounded_plan",
    "work_result",
    "verification_result",
    "transition_decision",
    "deep_synthesis_note",
    "distillation_pack",
)
SUPPLEMENTAL_EXAMPLE_GLOBS = {
    "transition_decision": "transition_decision.*.example.json",
}
EXPECTED_INVALID_FIXTURES = {
    "route_decision.wrong_artifact_type.json": ("route_decision", "const"),
    "bounded_plan.missing_required_field.json": ("bounded_plan", "required"),
    "verification_result.forbidden_extra_property.json": ("verification_result", "additionalProperties"),
    "transition_decision.return.invalid.missing_anchor.json": ("transition_decision", "required"),
}


class RuntimeArtifactContractsValidationError(RuntimeError):
    pass


def _artifact_schema_name(artifact_name: str) -> str:
    return f"artifact.{artifact_name}.schema.json"


def _expected_schema_paths() -> set[Path]:
    paths = {
        SCHEMAS_DIR / _artifact_schema_name(artifact_name)
        for artifact_name in RUNTIME_ARTIFACT_NAMES
    }
    paths.add(SCHEMAS_DIR / "agent-authority-claim.schema.json")
    return paths


def _expected_example_names() -> set[str]:
    names = {f"{artifact_name}.example.json" for artifact_name in RUNTIME_ARTIFACT_NAMES}
    names.add("transition_decision.return.example.json")
    names.add("agent-authority-claim.example.json")
    return names


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeArtifactContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeArtifactContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


def _schema(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise RuntimeArtifactContractsValidationError(f"{path} must contain a JSON object schema")
    try:
        Draft202012Validator.check_schema(payload)
    except SchemaError as exc:
        raise RuntimeArtifactContractsValidationError(
            f"{path} is not a valid draft 2020-12 schema: {exc.message}"
        ) from exc
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise RuntimeArtifactContractsValidationError(f"{path} must use draft 2020-12")
    return payload


def _schema_path(root: Path, artifact_name: str) -> Path:
    return root / SCHEMAS_DIR / _artifact_schema_name(artifact_name)


def _example_paths(root: Path, artifact_name: str) -> list[Path]:
    examples_dir = root / EXAMPLES_DIR
    paths = [examples_dir / f"{artifact_name}.example.json"]
    pattern = SUPPLEMENTAL_EXAMPLE_GLOBS.get(artifact_name)
    if pattern is not None:
        for path in sorted(examples_dir.glob(pattern)):
            if path not in paths:
                paths.append(path)
    return paths


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
        raise RuntimeArtifactContractsValidationError(
            f"{payload_path} does not match {schema_path}: {location}: {first.message}"
        )


def _validate_artifact_schema_surface(root: Path, artifact_name: str) -> None:
    schema_path = _schema_path(root, artifact_name)
    schema = _schema(schema_path)
    if schema.get("type") != "object":
        raise RuntimeArtifactContractsValidationError(
            f"runtime artifact schema '{artifact_name}' must declare type 'object'"
        )
    properties = schema.get("properties")
    if not isinstance(properties, dict) or "artifact_type" not in properties:
        raise RuntimeArtifactContractsValidationError(
            f"runtime artifact schema '{artifact_name}' must expose an artifact_type property"
        )
    artifact_type = properties["artifact_type"]
    if not isinstance(artifact_type, dict) or artifact_type.get("const") != artifact_name:
        raise RuntimeArtifactContractsValidationError(
            f"runtime artifact schema '{artifact_name}' must pin artifact_type.const to '{artifact_name}'"
        )


def collect_runtime_artifact_contract_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    former_schema_dir = root / "schemas"
    for artifact_name in RUNTIME_ARTIFACT_NAMES:
        former_path = former_schema_dir / _artifact_schema_name(artifact_name)
        if former_path.exists():
            errors.append(f"former root artifact schema is still active: {former_path.relative_to(root).as_posix()}")

    if (root / FORMER_ROOT_EXAMPLES_DIR).exists():
        errors.append(f"former root runtime artifact examples directory is still active: {FORMER_ROOT_EXAMPLES_DIR.as_posix()}")

    schema_dir = root / SCHEMAS_DIR
    active_schemas = {path.relative_to(root) for path in schema_dir.glob("*.json")}
    expected_schemas = _expected_schema_paths()
    if active_schemas != expected_schemas:
        missing = sorted(expected_schemas - active_schemas)
        extra = sorted(active_schemas - expected_schemas)
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("runtime artifact schema file set drifted (" + "; ".join(details) + ")")

    examples_dir = root / EXAMPLES_DIR
    active_examples = {path.name for path in examples_dir.glob("*.example.json")}
    expected_examples = _expected_example_names()
    if active_examples != expected_examples:
        missing = sorted(expected_examples - active_examples)
        extra = sorted(active_examples - expected_examples)
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("unexpected: " + ", ".join(extra))
        errors.append("runtime artifact example file set drifted (" + "; ".join(details) + ")")

    if not (root / INVALID_DIR).is_dir():
        errors.append(f"missing required directory: {INVALID_DIR.as_posix()}")
    else:
        active_invalids = {path.name for path in (root / INVALID_DIR).glob("*.json")}
        expected_invalids = set(EXPECTED_INVALID_FIXTURES)
        if active_invalids != expected_invalids:
            missing = sorted(expected_invalids - active_invalids)
            extra = sorted(active_invalids - expected_invalids)
            details = []
            if missing:
                details.append("missing: " + ", ".join(missing))
            if extra:
                details.append("unexpected: " + ", ".join(extra))
            errors.append("runtime artifact invalid fixtures drifted (" + "; ".join(details) + ")")

    for artifact_name in RUNTIME_ARTIFACT_NAMES:
        try:
            _validate_artifact_schema_surface(root, artifact_name)
            for example_path in _example_paths(root, artifact_name):
                _validate_payload(_schema_path(root, artifact_name), example_path)
        except RuntimeArtifactContractsValidationError as exc:
            errors.append(str(exc))

    try:
        _validate_payload(
            root / SCHEMAS_DIR / "agent-authority-claim.schema.json",
            root / EXAMPLES_DIR / "agent-authority-claim.example.json",
        )
    except RuntimeArtifactContractsValidationError as exc:
        errors.append(str(exc))

    for file_name, (artifact_name, expected_validator) in EXPECTED_INVALID_FIXTURES.items():
        fixture_path = root / INVALID_DIR / file_name
        if not fixture_path.exists():
            continue
        try:
            schema = _schema(_schema_path(root, artifact_name))
            payload = _read_json(fixture_path)
            validation_errors = _validation_errors(schema, payload)
        except RuntimeArtifactContractsValidationError as exc:
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


def validate_runtime_artifact_contracts(root: Path = ROOT) -> None:
    errors = collect_runtime_artifact_contract_errors(root)
    if errors:
        raise RuntimeArtifactContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runtime-seam artifact-contract part payloads.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_runtime_artifact_contracts(root)
    except RuntimeArtifactContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Runtime artifact contract validation passed. schemas=8 examples=9 invalid=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
