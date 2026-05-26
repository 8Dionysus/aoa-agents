#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
STRESS_PART_ROOT = Path("mechanics/antifragility/parts/stress-posture")

EXPECTED_EXAMPLE_SCHEMAS = {
    Path("mechanics/antifragility/parts/stress-posture/examples/agent-stress-posture.example.json"): Path(
        "mechanics/antifragility/parts/stress-posture/schemas/agent-stress-posture.schema.json"
    ),
    Path("mechanics/antifragility/parts/stress-posture/examples/stress-handoff-envelope.example.json"): Path(
        "mechanics/antifragility/parts/stress-posture/schemas/stress-handoff-envelope.schema.json"
    ),
}

FORMER_ROOT_PATHS = {
    Path("schemas") / ("agent" + "_stress_posture_v1.json"),
    Path("schemas") / ("stress" + "_handoff_envelope_v1.json"),
    Path("examples") / ("agent" + "_stress_posture.example.json"),
    Path("examples") / ("stress" + "_handoff_envelope.example.json"),
}


class AntifragilityStressValidationError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AntifragilityStressValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AntifragilityStressValidationError(f"invalid JSON in {path}: {exc}") from exc


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def active_schema_files(root: Path) -> list[Path]:
    return sorted((root / STRESS_PART_ROOT / "schemas").glob("*.schema.json"))


def active_example_files(root: Path) -> list[Path]:
    return sorted((root / STRESS_PART_ROOT / "examples").glob("*.json"))


def collect_antifragility_stress_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for former_path in sorted(FORMER_ROOT_PATHS):
        if (root / former_path).exists():
            errors.append(f"former root path is still active: {former_path.as_posix()}")

    actual_schemas = {path.relative_to(root) for path in active_schema_files(root)}
    expected_schemas = set(EXPECTED_EXAMPLE_SCHEMAS.values())
    if actual_schemas != expected_schemas:
        missing = sorted(expected_schemas - actual_schemas)
        extra = sorted(actual_schemas - expected_schemas)
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("antifragility stress schema file set drifted (" + "; ".join(details) + ")")

    actual_examples = {path.relative_to(root) for path in active_example_files(root)}
    expected_examples = set(EXPECTED_EXAMPLE_SCHEMAS)
    if actual_examples != expected_examples:
        missing = sorted(expected_examples - actual_examples)
        extra = sorted(actual_examples - expected_examples)
        details = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("antifragility stress example file set drifted (" + "; ".join(details) + ")")

    for relative_path in sorted(actual_schemas | actual_examples):
        if "_" in relative_path.name:
            errors.append(f"{relative_path.as_posix()}: active antifragility stress names must use part-local slug style")

    for example_relative_path, schema_relative_path in sorted(EXPECTED_EXAMPLE_SCHEMAS.items()):
        example_path = root / example_relative_path
        schema_path = root / schema_relative_path
        if not example_path.is_file():
            errors.append(f"missing antifragility stress example: {example_relative_path.as_posix()}")
            continue
        if not schema_path.is_file():
            errors.append(f"missing antifragility stress schema: {schema_relative_path.as_posix()}")
            continue
        try:
            schema = read_json(schema_path)
            payload = read_json(example_path)
            Draft202012Validator.check_schema(schema)
        except (AntifragilityStressValidationError, SchemaError) as exc:
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
            if "examples/" + "agent_stress_" in text or "examples/" + "stress_handoff_" in text:
                errors.append(
                    f"{example_relative_path.as_posix()}: active payload still references former root example namespace"
                )

        if example_relative_path.name == "agent-stress-posture.example.json" and isinstance(payload, dict):
            applies_to = payload.get("applies_to")
            if not isinstance(applies_to, dict):
                errors.append(f"{example_relative_path.as_posix()}: applies_to must be an object")
            else:
                agent_profile = applies_to.get("agent_profile")
                if not isinstance(agent_profile, str) or not (root / agent_profile).is_file():
                    errors.append(f"{example_relative_path.as_posix()}: applies_to.agent_profile must point to a file")

    return errors


def validate_antifragility_stress_payloads(root: Path = ROOT) -> None:
    errors = collect_antifragility_stress_errors(root)
    if errors:
        raise AntifragilityStressValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate antifragility stress part-local schemas and examples.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_antifragility_stress_payloads(root)
    except AntifragilityStressValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Antifragility stress validation passed. examples={len(EXPECTED_EXAMPLE_SCHEMAS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
