#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

import validate_assistant_civil_formation


ROOT = Path(__file__).resolve().parents[1]
ASSISTANT_PART = Path("mechanics/experience/parts/assistant-civil-service")
ARENA_PART = Path("mechanics/experience/parts/arena-exclusion")
ASSISTANT_SCHEMA_DIR = ASSISTANT_PART / "schemas"
ASSISTANT_EXAMPLE_DIR = ASSISTANT_PART / "examples"
ARENA_SCHEMA_DIR = ARENA_PART / "schemas"

EXPECTED_ASSISTANT_SCHEMAS = {
    "assistant-variant.schema.json",
    "civil-formation.schema.json",
    "service-certification.schema.json",
    "service-contract.schema.json",
    "service-governance.schema.json",
    "service-identity.schema.json",
}
EXPECTED_ASSISTANT_EXAMPLES = {"civil-formation.example.json"}
EXPECTED_ARENA_SCHEMAS = {"arena-exclusion.schema.json"}

ADJUNCT_SCHEMA_ROUTES = {
    "assistant-variant.schema.json": ("assistant_variant", "*.assistant.variant.json"),
    "service-identity.schema.json": ("assistant_service_identity", "*.assistant.identity.json"),
    "service-contract.schema.json": ("assistant_service_contract", "*.assistant.contract.json"),
    "service-governance.schema.json": ("assistant_service_governance", "*.assistant.governance.json"),
    "service-certification.schema.json": ("assistant_service_certification", "*.assistant.certification.json"),
}
ARENA_ADJUNCT_ROUTE = ("assistant_arena_exclusion", "*.assistant.arena_exclusion.json")


class ExperienceAssistantCivilContractsValidationError(RuntimeError):
    pass


FORMER_SCHEMA_NAMES = (
    "assistant" + "_variant_v1.json",
    "assistant" + "_service_identity_v1.json",
    "assistant" + "_service_contract_v1.json",
    "assistant" + "_service_governance_v1.json",
    "assistant" + "_service_certification_v1.json",
    "assistant" + "_civil_formation_v1.json",
    "assistant" + "_arena_exclusion_v1.json",
)
FORMER_EXAMPLE_NAMES = ("assistant" + "_civil_formation.example.json",)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ExperienceAssistantCivilContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ExperienceAssistantCivilContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


def _check_file_set(
    root: Path,
    directory: Path,
    expected: set[str],
    *,
    label: str,
    errors: list[str],
) -> None:
    actual = {path.name for path in (root / directory).glob("*.json")}
    if actual == expected:
        return
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    details: list[str] = []
    if missing:
        details.append("missing: " + ", ".join(missing))
    if extra:
        details.append("unexpected: " + ", ".join(extra))
    errors.append(f"{label} file set drifted (" + "; ".join(details) + ")")


def _schema(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ExperienceAssistantCivilContractsValidationError(f"{path} must contain a JSON object schema")
    try:
        Draft202012Validator.check_schema(payload)
    except SchemaError as exc:
        raise ExperienceAssistantCivilContractsValidationError(
            f"{path} is not a valid draft 2020-12 schema: {exc}"
        ) from exc
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ExperienceAssistantCivilContractsValidationError(f"{path} must use draft 2020-12")
    if payload.get("additionalProperties") is not False:
        raise ExperienceAssistantCivilContractsValidationError(f"{path} must be closed by default")
    return payload


def _validate_payload(
    schema: dict[str, Any],
    payload: Any,
    *,
    location: str,
    errors: list[str],
) -> None:
    validator = Draft202012Validator(schema)
    schema_errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if schema_errors:
        first = schema_errors[0]
        path = ".".join(str(part) for part in first.absolute_path)
        suffix = f" at {path}" if path else ""
        errors.append(f"{location} schema violation{suffix}: {first.message}")


def _validate_adjunct_family(
    root: Path,
    schema: dict[str, Any],
    *,
    family: str,
    pattern: str,
    errors: list[str],
) -> None:
    family_dir = root / "agents" / "profiles" / "adjuncts" / family
    files = sorted(family_dir.glob(pattern))
    if not files:
        errors.append(f"missing adjunct payloads for {family}: {family_dir}")
        return
    for path in files:
        _validate_payload(schema, _read_json(path), location=path.relative_to(root).as_posix(), errors=errors)


def _validate_examples(root: Path, civil_schema: dict[str, Any], errors: list[str]) -> None:
    example_path = root / ASSISTANT_EXAMPLE_DIR / "civil-formation.example.json"
    example = _read_json(example_path)
    _validate_payload(civil_schema, example, location=example_path.relative_to(root).as_posix(), errors=errors)

    if example.get("variant_id") != "reviewer.assistant":
        errors.append("civil-formation.example.json should keep reviewer.assistant as the reader-path example")
    civil_reading = example.get("civil_reading", {})
    if civil_reading.get("kind") != "assistant":
        errors.append("civil-formation.example.json must preserve assistant kind")
    if civil_reading.get("not_a_contestant") is not True:
        errors.append("civil-formation.example.json must preserve not_a_contestant=true")
    if "issue_verdict" not in civil_reading.get("must_not", []):
        errors.append("civil-formation.example.json must preserve issue_verdict prohibition")


def _collect_dependency_errors(root: Path) -> list[str]:
    errors: list[str] = []
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
        try:
            if validate_assistant_civil_formation.main(["--root", str(root)]) != 0:
                errors.append("validate_assistant_civil_formation.py failed")
        except SystemExit as exc:
            errors.append(f"validate_assistant_civil_formation.py exited with {exc.code}")
    return errors


def collect_experience_assistant_civil_contract_errors(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for file_name in FORMER_SCHEMA_NAMES:
        former_path = root / "schemas" / file_name
        if former_path.exists():
            errors.append(
                "former root experience assistant civil schema is still active: "
                f"{former_path.relative_to(root).as_posix()}"
            )

    for file_name in FORMER_EXAMPLE_NAMES:
        former_path = root / "examples" / file_name
        if former_path.exists():
            errors.append(
                "former root experience assistant civil example is still active: "
                f"{former_path.relative_to(root).as_posix()}"
            )

    _check_file_set(root, ASSISTANT_SCHEMA_DIR, EXPECTED_ASSISTANT_SCHEMAS, label="assistant civil schema", errors=errors)
    _check_file_set(root, ASSISTANT_EXAMPLE_DIR, EXPECTED_ASSISTANT_EXAMPLES, label="assistant civil example", errors=errors)
    _check_file_set(root, ARENA_SCHEMA_DIR, EXPECTED_ARENA_SCHEMAS, label="arena exclusion schema", errors=errors)

    try:
        assistant_schemas = {
            name: _schema(root / ASSISTANT_SCHEMA_DIR / name)
            for name in sorted(EXPECTED_ASSISTANT_SCHEMAS)
        }
        arena_schema = _schema(root / ARENA_SCHEMA_DIR / "arena-exclusion.schema.json")
    except ExperienceAssistantCivilContractsValidationError as exc:
        errors.append(str(exc))
        return errors

    for schema_name, (family, pattern) in ADJUNCT_SCHEMA_ROUTES.items():
        _validate_adjunct_family(root, assistant_schemas[schema_name], family=family, pattern=pattern, errors=errors)

    arena_family, arena_pattern = ARENA_ADJUNCT_ROUTE
    _validate_adjunct_family(root, arena_schema, family=arena_family, pattern=arena_pattern, errors=errors)
    _validate_examples(root, assistant_schemas["civil-formation.schema.json"], errors)
    errors.extend(_collect_dependency_errors(root))
    return errors


def validate_experience_assistant_civil_contracts(root: Path = ROOT) -> None:
    errors = collect_experience_assistant_civil_contract_errors(root)
    if errors:
        raise ExperienceAssistantCivilContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Experience assistant civil part-local contracts.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_experience_assistant_civil_contracts(args.root.resolve())
    except ExperienceAssistantCivilContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Experience assistant civil contract validation passed. schemas=7 examples=1 adjunct_families=6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
