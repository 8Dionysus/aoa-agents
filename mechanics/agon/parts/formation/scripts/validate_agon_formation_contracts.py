#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = Path(__file__).resolve().parent
FORMATION_PART = Path("mechanics/agon/parts/formation")
ARENA_PART = Path("mechanics/agon/parts/arena-rank-school")
FORMATION_SCHEMA_DIR = FORMATION_PART / "schemas"
FORMATION_EXAMPLE_DIR = FORMATION_PART / "examples"
ARENA_SCHEMA_DIR = ARENA_PART / "schemas"

EXPECTED_FORMATION_SCHEMAS = {
    "agent-kind.schema.json",
    "formation-trial.schema.json",
    "office-overlay.schema.json",
    "resistance-revision.schema.json",
    "subjectivity.schema.json",
}
EXPECTED_FORMATION_EXAMPLES = {
    "agent-agonic-formation.example.json",
    "formation-trial.example.json",
}
EXPECTED_ARENA_FORMATION_SCHEMAS = {"arena-eligibility.schema.json"}


class AgonFormationContractsValidationError(RuntimeError):
    pass


def _load_repo_python_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AgonFormationContractsValidationError(f"cannot load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_agent_agonic_formation = _load_repo_python_module(
    "validate_agent_agonic_formation",
    SCRIPT_DIR / "validate_agent_agonic_formation.py",
)
validate_agent_formation_trial = _load_repo_python_module(
    "validate_agent_formation_trial",
    SCRIPT_DIR / "validate_agent_formation_trial.py",
)
validate_assistant_civil_formation = _load_repo_python_module(
    "validate_assistant_civil_formation",
    ROOT / "scripts" / "validate_assistant_civil_formation.py",
)


FORMER_SCHEMA_NAMES = (
    "agent" + "_kind_v1.json",
    "agent" + "_subjectivity_v1.json",
    "agent" + "_office_overlay_v1.json",
    "agent" + "_arena_eligibility_v1.json",
    "agent" + "_resistance_revision_v1.json",
    "agent" + "_formation_trial_v1.json",
)
FORMER_EXAMPLE_NAMES = (
    "agent" + "_agonic_formation.example.json",
    "agent" + "_formation_trial.example.json",
)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AgonFormationContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AgonFormationContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


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


def _validate_schema(path: Path, errors: list[str]) -> None:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        errors.append(f"{path} must contain a JSON object schema")
        return
    try:
        Draft202012Validator.check_schema(payload)
    except Exception as exc:
        errors.append(f"{path} is not a valid draft 2020-12 schema: {exc}")
        return
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{path} must use draft 2020-12")
    if payload.get("additionalProperties") is not False:
        errors.append(f"{path} must be closed by default")


def _validate_examples(root: Path, errors: list[str]) -> None:
    agonic = _read_json(root / FORMATION_EXAMPLE_DIR / "agent-agonic-formation.example.json")
    if agonic.get("actor") != "reviewer":
        errors.append("agent-agonic-formation.example.json should keep reviewer as the reader-path example")
    read_order = agonic.get("read_order")
    if not isinstance(read_order, list) or "generated/agent_agonic_formation_index.min.json" not in read_order:
        errors.append("agent-agonic-formation.example.json must route through the generated formation index")

    trial = _read_json(root / FORMATION_EXAMPLE_DIR / "formation-trial.example.json")
    if trial.get("verdict") != "survive_with_split_forms":
        errors.append("formation-trial.example.json must preserve the split-form survivor verdict")
    if trial.get("assistant_form", {}).get("variant_id") != "reviewer.assistant":
        errors.append("formation-trial.example.json must preserve the reviewer assistant split-form reference")


def _collect_dependency_errors(root: Path) -> list[str]:
    errors: list[str] = []
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
        try:
            if validate_agent_agonic_formation.main() != 0:
                errors.append("validate_agent_agonic_formation.py failed")
        except SystemExit as exc:
            errors.append(f"validate_agent_agonic_formation.py exited with {exc.code}")
        try:
            if validate_assistant_civil_formation.main(["--root", str(root)]) != 0:
                errors.append("validate_assistant_civil_formation.py failed")
        except SystemExit as exc:
            errors.append(f"validate_assistant_civil_formation.py exited with {exc.code}")
        try:
            if validate_agent_formation_trial.main(["--root", str(root)]) != 0:
                errors.append("validate_agent_formation_trial.py failed")
        except SystemExit as exc:
            errors.append(f"validate_agent_formation_trial.py exited with {exc.code}")
    return errors


def collect_agon_formation_contract_errors(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for file_name in FORMER_SCHEMA_NAMES:
        former_path = root / "schemas" / file_name
        if former_path.exists():
            errors.append(f"former root Agon formation schema is still active: {former_path.relative_to(root).as_posix()}")

    for file_name in FORMER_EXAMPLE_NAMES:
        former_path = root / "examples" / file_name
        if former_path.exists():
            errors.append(f"former root Agon formation example is still active: {former_path.relative_to(root).as_posix()}")

    for relative_path in (
        "scripts/build_agent_agonic_formation_index.py",
        "scripts/validate_agent_agonic_formation.py",
        "scripts/build_agent_formation_trial.py",
        "scripts/validate_agent_formation_trial.py",
        "scripts/validate_agon_formation_contracts.py",
        "tests/test_agent_agonic_formation.py",
        "tests/test_agent_formation_trial.py",
        "tests/test_agon_formation_contracts.py",
    ):
        former_path = root / relative_path
        if former_path.exists():
            errors.append(f"former root Agon formation check is still active: {relative_path}")

    _check_file_set(root, FORMATION_SCHEMA_DIR, EXPECTED_FORMATION_SCHEMAS, label="formation schema", errors=errors)
    _check_file_set(root, FORMATION_EXAMPLE_DIR, EXPECTED_FORMATION_EXAMPLES, label="formation example", errors=errors)
    for schema_name in EXPECTED_ARENA_FORMATION_SCHEMAS:
        if not (root / ARENA_SCHEMA_DIR / schema_name).is_file():
            errors.append(f"missing arena formation schema: {(ARENA_SCHEMA_DIR / schema_name).as_posix()}")

    for schema_name in sorted(EXPECTED_FORMATION_SCHEMAS):
        _validate_schema(root / FORMATION_SCHEMA_DIR / schema_name, errors)
    for schema_name in sorted(EXPECTED_ARENA_FORMATION_SCHEMAS):
        _validate_schema(root / ARENA_SCHEMA_DIR / schema_name, errors)

    try:
        _validate_examples(root, errors)
    except AgonFormationContractsValidationError as exc:
        errors.append(str(exc))

    errors.extend(_collect_dependency_errors(root))
    return errors


def validate_agon_formation_contracts(root: Path = ROOT) -> None:
    errors = collect_agon_formation_contract_errors(root)
    if errors:
        raise AgonFormationContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agon formation part-local contracts.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_agon_formation_contracts(args.root.resolve())
    except AgonFormationContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Agon formation contract validation passed. schemas=6 examples=2 dependent_waves=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
