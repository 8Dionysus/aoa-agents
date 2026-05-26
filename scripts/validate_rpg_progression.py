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
PROGRESSION_PART_ROOT = Path("mechanics/rpg/parts/progression-model")
SCHEMA_PATH = PROGRESSION_PART_ROOT / "schemas" / "agent-progression.schema.json"
EXAMPLE_PATH = PROGRESSION_PART_ROOT / "examples" / "agent-progression.example.json"
FORMER_ROOT_PATHS = {
    Path("schemas") / ("agent" + "_progression.schema.json"),
    Path("examples") / ("agent" + "_progression.example.json"),
}


class RPGProgressionValidationError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RPGProgressionValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RPGProgressionValidationError(f"invalid JSON in {path}: {exc}") from exc


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def collect_rpg_progression_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for former_path in sorted(FORMER_ROOT_PATHS):
        if (root / former_path).exists():
            errors.append(f"former root path is still active: {former_path.as_posix()}")

    active_schemas = {path.relative_to(root) for path in (root / PROGRESSION_PART_ROOT / "schemas").glob("*.json")}
    if active_schemas != {SCHEMA_PATH}:
        missing = sorted({SCHEMA_PATH} - active_schemas)
        extra = sorted(active_schemas - {SCHEMA_PATH})
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("RPG progression schema file set drifted (" + "; ".join(details) + ")")

    active_examples = {path.relative_to(root) for path in (root / PROGRESSION_PART_ROOT / "examples").glob("*.json")}
    if active_examples != {EXAMPLE_PATH}:
        missing = sorted({EXAMPLE_PATH} - active_examples)
        extra = sorted(active_examples - {EXAMPLE_PATH})
        details = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("RPG progression example file set drifted (" + "; ".join(details) + ")")

    try:
        schema = read_json(root / SCHEMA_PATH)
        payload = read_json(root / EXAMPLE_PATH)
        Draft202012Validator.check_schema(schema)
    except (RPGProgressionValidationError, SchemaError) as exc:
        errors.append(str(exc))
        return errors

    validation_errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if validation_errors:
        first = validation_errors[0]
        location = ".".join(str(part) for part in first.absolute_path)
        suffix = f" at {location}" if location else ""
        errors.append(f"{EXAMPLE_PATH.as_posix()}: schema violation{suffix}: {first.message}")

    for relative_path in (SCHEMA_PATH, EXAMPLE_PATH):
        if "_" in relative_path.name:
            errors.append(f"{relative_path.as_posix()}: active RPG progression names must use part-local slug style")

    for text in iter_strings(payload):
        if "examples/" + "agent_progression" in text or "schemas/" + "agent_progression" in text:
            errors.append(f"{EXAMPLE_PATH.as_posix()}: active payload still references former root progression namespace")

    return errors


def validate_rpg_progression(root: Path = ROOT) -> None:
    errors = collect_rpg_progression_errors(root)
    if errors:
        raise RPGProgressionValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate RPG progression part-local schema and example.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_rpg_progression(root)
    except RPGProgressionValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("RPG progression validation passed. examples=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
