#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _recursor_common import build_boundary_report, build_readiness_index, stable_hash


ROOT = Path(__file__).resolve().parents[3]
RECURRENCE_PARTS = Path("mechanics/recurrence/parts")
RECURSOR_READINESS_PART = RECURRENCE_PARTS / "recursor-readiness"
RECURSOR_PROJECTION_PART = RECURRENCE_PARTS / "codex-recursor-projection"
RECURSOR_BOUNDARY_PART = RECURRENCE_PARTS / "agon-recursor-boundary"
RECURSOR_READINESS_GENERATED = RECURSOR_READINESS_PART / "generated"
RECURSOR_PROJECTION_GENERATED = RECURSOR_PROJECTION_PART / "generated"
RECURSOR_BOUNDARY_GENERATED = RECURSOR_BOUNDARY_PART / "generated"

EXPECTED_READINESS_SCHEMAS = {
    "handoff-ledger.schema.json",
    "pair-contract.schema.json",
    "readiness-index.schema.json",
    "role-contract.schema.json",
    "session-intent.schema.json",
}
EXPECTED_READINESS_EXAMPLES = {
    "executor-receipt.example.json",
    "session-intent.example.json",
    "witness-handoff.example.json",
}
EXPECTED_PROJECTION_SCHEMAS = {"projection-candidate.schema.json"}
EXPECTED_BOUNDARY_SCHEMAS = {"boundary-report.schema.json"}
EXPECTED_BOUNDARY_EXAMPLES = {"boundary-report.example.json"}
EXPECTED_READINESS_GENERATED = {"role-readiness.min.json", "pair-contract.min.json"}
EXPECTED_PROJECTION_GENERATED = {"projection-candidates.min.json"}
EXPECTED_BOUNDARY_GENERATED = {"boundary-report.min.json"}


def _former_schema_name(stem: str) -> str:
    return "recursor-" + stem + ".v1.schema.json"


def _former_example_name(stem: str) -> str:
    return "recursor" + "_" + stem + ".example.json"


FORMER_SCHEMA_NAMES = (
    _former_schema_name("role-contract"),
    _former_schema_name("pair-contract"),
    _former_schema_name("readiness-index"),
    _former_schema_name("handoff-ledger"),
    _former_schema_name("session-intent"),
    _former_schema_name("projection-candidate"),
    _former_schema_name("boundary-report"),
)
FORMER_EXAMPLE_NAMES = (
    _former_example_name("session_intent"),
    _former_example_name("witness_handoff"),
    _former_example_name("executor_receipt"),
    _former_example_name("boundary_report"),
)
FORMER_GENERATED_NAMES = (
    "recursor" + "_role_readiness.min.json",
    "recursor" + "_pair_contract.min.json",
    "recursor" + "_projection_candidates.min.json",
    "recursor" + "_agon_boundary_report.min.json",
)


class RecursorContractsValidationError(RuntimeError):
    pass


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RecursorContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RecursorContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


def _schema_validator(path: Path) -> Draft202012Validator:
    schema = _read_json(path)
    if not isinstance(schema, dict):
        raise RecursorContractsValidationError(f"{path} must contain a JSON object schema")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _validate_payload(
    validator: Draft202012Validator,
    payload: Any,
    *,
    location: str,
    errors: list[str],
) -> None:
    schema_errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if schema_errors:
        first = schema_errors[0]
        path = ".".join(str(part) for part in first.absolute_path)
        suffix = f" at {path}" if path else ""
        errors.append(f"{location} schema violation{suffix}: {first.message}")


def _relative_file_names(root: Path, directory: Path, glob: str) -> set[str]:
    return {path.name for path in (root / directory).glob(glob)}


def _check_file_set(
    root: Path,
    directory: Path,
    expected: set[str],
    *,
    label: str,
    errors: list[str],
) -> None:
    actual = _relative_file_names(root, directory, "*.json")
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


def collect_recursor_contract_errors(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for file_name in FORMER_SCHEMA_NAMES:
        former_path = root / "schemas" / file_name
        if former_path.exists():
            errors.append(f"former root recursor schema is still active: {former_path.relative_to(root).as_posix()}")

    for file_name in FORMER_EXAMPLE_NAMES:
        former_path = root / "examples" / file_name
        if former_path.exists():
            errors.append(f"former root recursor example is still active: {former_path.relative_to(root).as_posix()}")

    for file_name in FORMER_GENERATED_NAMES:
        former_path = root / "generated" / file_name
        if former_path.exists():
            errors.append(f"former root recursor generated reader is still active: {former_path.relative_to(root).as_posix()}")

    readiness_schema_dir = RECURSOR_READINESS_PART / "schemas"
    readiness_examples_dir = RECURSOR_READINESS_PART / "examples"
    projection_schema_dir = RECURSOR_PROJECTION_PART / "schemas"
    boundary_schema_dir = RECURSOR_BOUNDARY_PART / "schemas"
    boundary_examples_dir = RECURSOR_BOUNDARY_PART / "examples"

    _check_file_set(
        root,
        readiness_schema_dir,
        EXPECTED_READINESS_SCHEMAS,
        label="recursor-readiness schema",
        errors=errors,
    )
    _check_file_set(
        root,
        readiness_examples_dir,
        EXPECTED_READINESS_EXAMPLES,
        label="recursor-readiness example",
        errors=errors,
    )
    _check_file_set(
        root,
        projection_schema_dir,
        EXPECTED_PROJECTION_SCHEMAS,
        label="codex-recursor-projection schema",
        errors=errors,
    )
    _check_file_set(
        root,
        boundary_schema_dir,
        EXPECTED_BOUNDARY_SCHEMAS,
        label="agon-recursor-boundary schema",
        errors=errors,
    )
    _check_file_set(
        root,
        boundary_examples_dir,
        EXPECTED_BOUNDARY_EXAMPLES,
        label="agon-recursor-boundary example",
        errors=errors,
    )
    _check_file_set(
        root,
        RECURSOR_READINESS_GENERATED,
        EXPECTED_READINESS_GENERATED,
        label="recursor-readiness generated",
        errors=errors,
    )
    _check_file_set(
        root,
        RECURSOR_PROJECTION_GENERATED,
        EXPECTED_PROJECTION_GENERATED,
        label="codex-recursor-projection generated",
        errors=errors,
    )
    _check_file_set(
        root,
        RECURSOR_BOUNDARY_GENERATED,
        EXPECTED_BOUNDARY_GENERATED,
        label="agon-recursor-boundary generated",
        errors=errors,
    )

    try:
        role_validator = _schema_validator(root / readiness_schema_dir / "role-contract.schema.json")
        pair_validator = _schema_validator(root / readiness_schema_dir / "pair-contract.schema.json")
        readiness_validator = _schema_validator(root / readiness_schema_dir / "readiness-index.schema.json")
        handoff_validator = _schema_validator(root / readiness_schema_dir / "handoff-ledger.schema.json")
        session_intent_validator = _schema_validator(root / readiness_schema_dir / "session-intent.schema.json")
        projection_validator = _schema_validator(root / projection_schema_dir / "projection-candidate.schema.json")
        boundary_validator = _schema_validator(root / boundary_schema_dir / "boundary-report.schema.json")
    except RecursorContractsValidationError as exc:
        errors.append(str(exc))
        return errors
    except Exception as exc:  # jsonschema raises several schema-check exceptions.
        errors.append(f"invalid recursor schema surface: {exc}")
        return errors

    roles = _read_json(root / RECURSOR_READINESS_PART / "config" / "roles.seed.json")
    pair = _read_json(root / RECURSOR_READINESS_PART / "config" / "pair.seed.json")
    projection = _read_json(root / RECURSOR_PROJECTION_PART / "config" / "projection-candidate.json")
    session_intent = _read_json(root / readiness_examples_dir / "session-intent.example.json")
    witness_handoff = _read_json(root / readiness_examples_dir / "witness-handoff.example.json")
    executor_handoff = _read_json(root / readiness_examples_dir / "executor-receipt.example.json")
    boundary_example = _read_json(root / boundary_examples_dir / "boundary-report.example.json")
    generated_readiness = _read_json(root / RECURSOR_READINESS_GENERATED / "role-readiness.min.json")
    generated_pair = _read_json(root / RECURSOR_READINESS_GENERATED / "pair-contract.min.json")
    generated_projection = _read_json(root / RECURSOR_PROJECTION_GENERATED / "projection-candidates.min.json")
    generated_boundary = _read_json(root / RECURSOR_BOUNDARY_GENERATED / "boundary-report.min.json")

    if not isinstance(roles, dict) or not isinstance(roles.get("roles"), list):
        errors.append("recursor-readiness roles seed must contain a roles array")
    else:
        for index, role in enumerate(roles["roles"]):
            _validate_payload(role_validator, role, location=f"roles.seed.json roles[{index}]", errors=errors)

    _validate_payload(pair_validator, pair, location="pair.seed.json", errors=errors)
    _validate_payload(pair_validator, generated_pair, location="recursor-readiness/generated/pair-contract.min.json", errors=errors)
    _validate_payload(projection_validator, projection, location="projection-candidate.json", errors=errors)
    _validate_payload(session_intent_validator, session_intent, location="session-intent.example.json", errors=errors)
    _validate_payload(handoff_validator, witness_handoff, location="witness-handoff.example.json", errors=errors)
    _validate_payload(handoff_validator, executor_handoff, location="executor-receipt.example.json", errors=errors)
    _validate_payload(boundary_validator, boundary_example, location="boundary-report.example.json", errors=errors)
    _validate_payload(boundary_validator, generated_boundary, location="agon-recursor-boundary/generated/boundary-report.min.json", errors=errors)
    _validate_payload(readiness_validator, generated_readiness, location="recursor-readiness/generated/role-readiness.min.json", errors=errors)
    _validate_payload(readiness_validator, build_readiness_index(root), location="built recursor readiness index", errors=errors)
    _validate_payload(boundary_validator, build_boundary_report(root), location="built recursor boundary report", errors=errors)

    if not isinstance(generated_projection, dict):
        errors.append("codex-recursor-projection generated reader must be an object")
    else:
        if generated_projection.get("schema_version") != "recursor-projection-candidates-index/v1":
            errors.append("codex-recursor-projection generated reader has wrong schema_version")
        if generated_projection.get("boundary", {}).get("status") != "pass":
            errors.append("codex-recursor-projection generated reader boundary must pass")
        if generated_projection.get("source_hash") != stable_hash(projection):
            errors.append("codex-recursor-projection generated reader source_hash is stale")

    return errors


def validate_recursor_contracts(root: Path = ROOT) -> None:
    errors = collect_recursor_contract_errors(root)
    if errors:
        raise RecursorContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate recurrence recursor part-local contract payloads.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_recursor_contracts(args.root.resolve())
    except RecursorContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Recursor contract validation passed. schemas=7 examples=4 generated=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
