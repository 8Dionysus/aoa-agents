#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import copy
import importlib.util
import io
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ARENA_PART = Path("mechanics/agon/parts/arena-rank-school")
EPISTEMIC_PART = Path("mechanics/agon/parts/epistemic-actor")
ARENA_SCHEMA_DIR = ARENA_PART / "schemas"
ARENA_EXAMPLE_DIR = ARENA_PART / "examples"
EPISTEMIC_SCHEMA_DIR = EPISTEMIC_PART / "schemas"
EPISTEMIC_EXAMPLE_DIR = EPISTEMIC_PART / "examples"

EXPECTED_ARENA_SCHEMAS = {
    "rank-jurisdiction.schema.json",
    "rank-jurisdiction-registry.schema.json",
    "school-campaign-posture.schema.json",
    "school-campaign-posture-registry.schema.json",
}
EXPECTED_ARENA_EXAMPLES = {
    "rank-surface.example.json",
    "school-campaign-posture.example.json",
}
EXPECTED_EPISTEMIC_SCHEMAS = {
    "epistemic-actor-posture.schema.json",
    "epistemic-actor-posture-registry.schema.json",
}
EXPECTED_EPISTEMIC_EXAMPLES = {"epistemic-actor-posture.example.json"}


class AgonRankEpistemicContractsValidationError(RuntimeError):
    pass


def _former_schema_name(stem: str) -> str:
    return "agon-" + stem + ".schema.json"


FORMER_SCHEMA_NAMES = (
    _former_schema_name("agent-rank-jurisdiction"),
    _former_schema_name("agent-rank-jurisdiction-registry"),
    _former_schema_name("agent-school-campaign-posture"),
    _former_schema_name("agent-school-campaign-posture-registry"),
    _former_schema_name("epistemic-actor-posture"),
    _former_schema_name("epistemic-actor-posture-registry"),
)
FORMER_EXAMPLE_NAMES = (
    "agon" + "_agent_rank_surface.example.json",
    "agon" + "_agent_school_campaign_posture.example.json",
    "agon" + "_epistemic_actor_posture.example.json",
)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AgonRankEpistemicContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AgonRankEpistemicContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


def _schema(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise AgonRankEpistemicContractsValidationError(f"{path} must contain a JSON object schema")
    Draft202012Validator.check_schema(payload)
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


def _load_script(name: str):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise AgonRankEpistemicContractsValidationError(f"cannot load validator: {path}")
    spec.loader.exec_module(module)
    return module


def _collect_script_result_errors() -> list[str]:
    errors: list[str] = []
    rank_validator = _load_script("validate_agon_agent_rank_jurisdiction.py")
    school_validator = _load_script("validate_agon_agent_school_campaign_posture_registry.py")
    epistemic_validator = _load_script("validate_agon_epistemic_actor_posture.py")

    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
        if rank_validator.main() != 0:
            errors.append("validate_agon_agent_rank_jurisdiction.py failed")
        if school_validator.validate() != 0:
            errors.append("validate_agon_agent_school_campaign_posture_registry.py failed")
        if epistemic_validator.validate() != 0:
            errors.append("validate_agon_epistemic_actor_posture.py failed")
    return errors


def collect_agon_rank_epistemic_contract_errors(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for file_name in FORMER_SCHEMA_NAMES:
        former_path = root / "schemas" / file_name
        if former_path.exists():
            errors.append(f"former root Agon schema is still active: {former_path.relative_to(root).as_posix()}")

    for file_name in FORMER_EXAMPLE_NAMES:
        former_path = root / "examples" / file_name
        if former_path.exists():
            errors.append(f"former root Agon example is still active: {former_path.relative_to(root).as_posix()}")

    _check_file_set(root, ARENA_SCHEMA_DIR, EXPECTED_ARENA_SCHEMAS, label="arena-rank-school schema", errors=errors)
    _check_file_set(root, ARENA_EXAMPLE_DIR, EXPECTED_ARENA_EXAMPLES, label="arena-rank-school example", errors=errors)
    _check_file_set(root, EPISTEMIC_SCHEMA_DIR, EXPECTED_EPISTEMIC_SCHEMAS, label="epistemic-actor schema", errors=errors)
    _check_file_set(root, EPISTEMIC_EXAMPLE_DIR, EXPECTED_EPISTEMIC_EXAMPLES, label="epistemic-actor example", errors=errors)

    try:
        rank_schema = _schema(root / ARENA_SCHEMA_DIR / "rank-jurisdiction.schema.json")
        rank_registry_schema = _schema(root / ARENA_SCHEMA_DIR / "rank-jurisdiction-registry.schema.json")
        school_schema = _schema(root / ARENA_SCHEMA_DIR / "school-campaign-posture.schema.json")
        school_registry_schema = _schema(root / ARENA_SCHEMA_DIR / "school-campaign-posture-registry.schema.json")
        epistemic_schema = _schema(root / EPISTEMIC_SCHEMA_DIR / "epistemic-actor-posture.schema.json")
        epistemic_registry_schema = _schema(root / EPISTEMIC_SCHEMA_DIR / "epistemic-actor-posture-registry.schema.json")
    except Exception as exc:
        errors.append(str(exc))
        return errors

    rank_example = _read_json(root / ARENA_EXAMPLE_DIR / "rank-surface.example.json")
    school_example = _read_json(root / ARENA_EXAMPLE_DIR / "school-campaign-posture.example.json")
    epistemic_example = _read_json(root / EPISTEMIC_EXAMPLE_DIR / "epistemic-actor-posture.example.json")
    rank_registry = _read_json(root / "generated" / "agon_agent_rank_jurisdiction_registry.min.json")
    school_registry = _read_json(root / "generated" / "agon_agent_school_campaign_posture_registry.min.json")
    epistemic_registry = _read_json(root / "generated" / "agon_epistemic_actor_posture_registry.min.json")

    inlined_epistemic_registry_schema = copy.deepcopy(epistemic_registry_schema)
    inlined_epistemic_registry_schema["properties"]["postures"]["items"] = epistemic_schema

    _validate_payload(rank_schema, rank_example, location="rank-surface.example.json", errors=errors)
    _validate_payload(rank_registry_schema, rank_registry, location="generated/agon_agent_rank_jurisdiction_registry.min.json", errors=errors)
    _validate_payload(school_schema, school_example, location="school-campaign-posture.example.json", errors=errors)
    _validate_payload(school_registry_schema, school_registry, location="generated/agon_agent_school_campaign_posture_registry.min.json", errors=errors)
    _validate_payload(epistemic_schema, epistemic_example, location="epistemic-actor-posture.example.json", errors=errors)
    _validate_payload(inlined_epistemic_registry_schema, epistemic_registry, location="generated/agon_epistemic_actor_posture_registry.min.json", errors=errors)

    try:
        errors.extend(_collect_script_result_errors())
    except AgonRankEpistemicContractsValidationError as exc:
        errors.append(str(exc))

    return errors


def validate_agon_rank_epistemic_contracts(root: Path = ROOT) -> None:
    errors = collect_agon_rank_epistemic_contract_errors(root)
    if errors:
        raise AgonRankEpistemicContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agon rank/school/epistemic part-local contracts.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_agon_rank_epistemic_contracts(args.root.resolve())
    except AgonRankEpistemicContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Agon rank/epistemic contract validation passed. schemas=6 examples=3 generated=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
