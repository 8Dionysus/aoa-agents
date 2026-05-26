#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
TITAN_PARTS_ROOT = Path("mechanics/titan/parts")

EXPECTED_SCHEMA_PATHS = {
    Path("mechanics/titan/parts/role-bearing/schemas/role-class.schema.json"),
    Path("mechanics/titan/parts/role-bearing/schemas/bearer-identity.schema.json"),
    Path("mechanics/titan/parts/lineage-ledger/schemas/lineage-ledger.schema.json"),
    Path("mechanics/titan/parts/incarnation-spine/schemas/incarnation-identity.schema.json"),
    Path("mechanics/titan/parts/incarnation-spine/schemas/operator-console-roster.schema.json"),
    Path("mechanics/titan/parts/runtime-roster/schemas/agent-report.schema.json"),
    Path("mechanics/titan/parts/runtime-roster/schemas/runtime-roster.schema.json"),
    Path("mechanics/titan/parts/runtime-roster/schemas/appserver-bridge-boundary.schema.json"),
    Path("mechanics/titan/parts/service-cohort/schemas/memory-roster.schema.json"),
    Path("mechanics/titan/parts/service-cohort/schemas/service-cohort.schema.json"),
    Path("mechanics/titan/parts/summon-boundary/schemas/agent-role-assignment.schema.json"),
}


class TitanSchemasValidationError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TitanSchemasValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TitanSchemasValidationError(f"invalid JSON in {path}: {exc}") from exc


def active_schema_files(root: Path) -> list[Path]:
    return sorted((root / TITAN_PARTS_ROOT).glob("*/schemas/*.schema.json"))


def validate_active_schema_path(relative_path: Path, errors: list[str]) -> None:
    parts = relative_path.parts
    if len(parts) != 6 or parts[:3] != ("mechanics", "titan", "parts") or parts[4] != "schemas":
        errors.append(f"{relative_path.as_posix()}: Titan schema must live under mechanics/titan/parts/*/schemas/")
    if relative_path.name.startswith("titan_"):
        errors.append(f"{relative_path.as_posix()}: active Titan schema names must not keep the old titan_ prefix")
    if not relative_path.name.endswith(".schema.json"):
        errors.append(f"{relative_path.as_posix()}: Titan schema files must keep the .schema.json suffix")


def collect_titan_schema_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    root_titan_schemas = sorted(path.relative_to(root) for path in (root / "schemas").glob("titan*.json"))
    if root_titan_schemas:
        errors.append(
            "root schemas/ still contains Titan-specific schemas: "
            + ", ".join(path.as_posix() for path in root_titan_schemas)
        )

    actual = {path.relative_to(root) for path in active_schema_files(root)}
    expected = set(EXPECTED_SCHEMA_PATHS)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("Titan schema file set drifted (" + "; ".join(details) + ")")

    for relative_path in sorted(actual):
        validate_active_schema_path(relative_path, errors)
        try:
            payload = read_json(root / relative_path)
            Draft202012Validator.check_schema(payload)
        except (TitanSchemasValidationError, SchemaError) as exc:
            errors.append(f"{relative_path.as_posix()}: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{relative_path.as_posix()}: Titan schema must be a JSON object")

    return errors


def validate_titan_schemas(root: Path = ROOT) -> None:
    errors = collect_titan_schema_errors(root)
    if errors:
        raise TitanSchemasValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Titan part-local schemas.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_titan_schemas(root)
    except TitanSchemasValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Titan schema validation passed. schemas={len(EXPECTED_SCHEMA_PATHS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
