#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[3]
TITAN_PARTS_ROOT = Path("mechanics/titan/parts")

EXPECTED_EXAMPLE_SCHEMAS = {
    Path("mechanics/titan/parts/role-bearing/examples/bearer-identity.v0.json"): Path(
        "mechanics/titan/parts/role-bearing/schemas/bearer-identity.schema.json"
    ),
    Path("mechanics/titan/parts/lineage-ledger/examples/lineage-ledger.v0.json"): Path(
        "mechanics/titan/parts/lineage-ledger/schemas/lineage-ledger.schema.json"
    ),
    Path("mechanics/titan/parts/incarnation-spine/examples/incarnation-identity.example.json"): Path(
        "mechanics/titan/parts/incarnation-spine/schemas/incarnation-identity.schema.json"
    ),
    Path("mechanics/titan/parts/incarnation-spine/examples/operator-console-roster.v0.json"): Path(
        "mechanics/titan/parts/incarnation-spine/schemas/operator-console-roster.schema.json"
    ),
    Path("mechanics/titan/parts/runtime-roster/examples/runtime-roster.v0.json"): Path(
        "mechanics/titan/parts/runtime-roster/schemas/runtime-roster.schema.json"
    ),
    Path("mechanics/titan/parts/runtime-roster/examples/appserver-bridge-boundary.v0.json"): Path(
        "mechanics/titan/parts/runtime-roster/schemas/appserver-bridge-boundary.schema.json"
    ),
    Path("mechanics/titan/parts/service-cohort/examples/memory-roster.v0.json"): Path(
        "mechanics/titan/parts/service-cohort/schemas/memory-roster.schema.json"
    ),
    Path("mechanics/titan/parts/service-cohort/examples/service-cohort.v0.json"): Path(
        "mechanics/titan/parts/service-cohort/schemas/service-cohort.schema.json"
    ),
    Path("mechanics/titan/parts/summon-boundary/examples/compact-review-task.example.json"): Path(
        "mechanics/titan/parts/summon-boundary/schemas/agent-role-assignment.schema.json"
    ),
    Path("mechanics/titan/parts/summon-boundary/examples/delta-residual-risk-task.example.json"): Path(
        "mechanics/titan/parts/summon-boundary/schemas/agent-role-assignment.schema.json"
    ),
}

LINEAGE_REF_EXPECTATIONS = {
    "role_classes_ref": "mechanics/titan/parts/role-bearing/config/role-classes.v0.json",
    "bearers_ref": "mechanics/titan/parts/role-bearing/config/bearers.v0.json",
}
FORMER_ROOT_EXAMPLE_PREFIX = "examples/" + "titan_"


class TitanExamplesValidationError(RuntimeError):
    pass


def describe(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TitanExamplesValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TitanExamplesValidationError(f"invalid JSON in {path}: {exc}") from exc


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def active_example_files(root: Path) -> list[Path]:
    return sorted((root / TITAN_PARTS_ROOT).glob("*/examples/*.json"))


def validate_active_example_path(relative_path: Path, errors: list[str]) -> None:
    parts = relative_path.parts
    if len(parts) != 6 or parts[:3] != ("mechanics", "titan", "parts") or parts[4] != "examples":
        errors.append(f"{relative_path.as_posix()}: Titan example must live under mechanics/titan/parts/*/examples/")
    if relative_path.name.startswith("titan_"):
        errors.append(f"{relative_path.as_posix()}: active Titan example names must not keep the old titan_ prefix")


def collect_titan_example_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    actual = {path.relative_to(root) for path in active_example_files(root)}
    expected = set(EXPECTED_EXAMPLE_SCHEMAS)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("Titan example file set drifted (" + "; ".join(details) + ")")

    for relative_path in sorted(actual):
        validate_active_example_path(relative_path, errors)

    for example_relative_path, schema_relative_path in sorted(EXPECTED_EXAMPLE_SCHEMAS.items()):
        example_path = root / example_relative_path
        schema_path = root / schema_relative_path
        if not example_path.is_file():
            errors.append(f"missing Titan example: {example_relative_path.as_posix()}")
            continue
        if not schema_path.is_file():
            errors.append(f"missing Titan example schema: {schema_relative_path.as_posix()}")
            continue
        try:
            schema = read_json(schema_path)
            payload = read_json(example_path)
            Draft202012Validator.check_schema(schema)
        except (TitanExamplesValidationError, SchemaError) as exc:
            errors.append(f"{example_relative_path.as_posix()}: {exc}")
            continue
        validation_errors = sorted(
            Draft202012Validator(schema).iter_errors(payload),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        if validation_errors:
            first = validation_errors[0]
            location = ".".join(str(part) for part in first.absolute_path)
            suffix = f" at {location}" if location else ""
            errors.append(f"{example_relative_path.as_posix()}: schema violation{suffix}: {first.message}")

        for text in iter_strings(payload):
            if FORMER_ROOT_EXAMPLE_PREFIX in text:
                errors.append(
                    f"{example_relative_path.as_posix()}: active payload still references former root examples namespace"
                )

        if example_relative_path.name == "lineage-ledger.v0.json" and isinstance(payload, dict):
            for field_name, expected_value in LINEAGE_REF_EXPECTATIONS.items():
                if payload.get(field_name) != expected_value:
                    errors.append(
                        f"{example_relative_path.as_posix()}: {field_name} must point to {expected_value}"
                    )

    return errors


def validate_titan_examples(root: Path = ROOT) -> None:
    errors = collect_titan_example_errors(root)
    if errors:
        raise TitanExamplesValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Titan part-local examples.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_titan_examples(root)
    except TitanExamplesValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Titan examples validation passed. examples={len(EXPECTED_EXAMPLE_SCHEMAS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
