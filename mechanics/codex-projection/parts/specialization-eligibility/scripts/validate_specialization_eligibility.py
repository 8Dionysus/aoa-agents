#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = Path("mechanics/codex-projection/parts/specialization-eligibility")
SCHEMA_PATH = PART_ROOT / "schemas" / "specialization-eligibility.schema.json"
EXAMPLE_PATH = PART_ROOT / "examples" / "specialization-eligibility.example.json"
DOC_PATH = PART_ROOT / "docs" / "specialization-eligibility.md"
README_PATH = PART_ROOT / "README.md"
PROJECTION_MANIFEST_PATH = Path("generated/codex_agents/projection_manifest.json")
FORMER_ROOT_PATHS = {
    Path("schemas") / "codex_specialization_eligibility_v1.json",
    Path("examples") / "codex_specialization_eligibility.example.json",
    Path("scripts") / "validate_specialization_eligibility.py",
}


class SpecializationEligibilityValidationError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SpecializationEligibilityValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SpecializationEligibilityValidationError(f"invalid JSON in {path}: {exc}") from exc


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SpecializationEligibilityValidationError(f"missing text file: {path}") from exc


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def collect_specialization_eligibility_errors(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for former_path in sorted(FORMER_ROOT_PATHS):
        if (root / former_path).exists():
            errors.append(f"former root eligibility path is still active: {former_path.as_posix()}")

    actual_schemas = {path.relative_to(root) for path in (root / PART_ROOT / "schemas").glob("*.json")}
    if actual_schemas != {SCHEMA_PATH}:
        missing = sorted({SCHEMA_PATH} - actual_schemas)
        extra = sorted(actual_schemas - {SCHEMA_PATH})
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("specialization eligibility schema file set drifted (" + "; ".join(details) + ")")

    actual_examples = {path.relative_to(root) for path in (root / PART_ROOT / "examples").glob("*.json")}
    if actual_examples != {EXAMPLE_PATH}:
        missing = sorted({EXAMPLE_PATH} - actual_examples)
        extra = sorted(actual_examples - {EXAMPLE_PATH})
        details = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("specialization eligibility example file set drifted (" + "; ".join(details) + ")")

    try:
        schema = read_json(root / SCHEMA_PATH)
        example = read_json(root / EXAMPLE_PATH)
        doc = read_text(root / DOC_PATH)
        readme = read_text(root / README_PATH)
        manifest = read_json(root / PROJECTION_MANIFEST_PATH)
        Draft202012Validator.check_schema(schema)
    except (SpecializationEligibilityValidationError, SchemaError) as exc:
        errors.append(str(exc))
        return errors

    validation_errors = sorted(
        Draft202012Validator(schema).iter_errors(example),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if validation_errors:
        first = validation_errors[0]
        location = ".".join(str(part) for part in first.absolute_path)
        suffix = f" at {location}" if location else ""
        errors.append(f"{EXAMPLE_PATH.as_posix()}: schema violation{suffix}: {first.message}")

    specialization_ref = example.get("specialization_ref")
    if isinstance(specialization_ref, str):
        try:
            specialization = read_json(root / specialization_ref)
        except SpecializationEligibilityValidationError as exc:
            errors.append(str(exc))
            specialization = {}
        if isinstance(specialization, dict):
            if specialization.get("id") != example.get("specialization_id"):
                errors.append(f"{EXAMPLE_PATH.as_posix()}: specialization_id must match source specialization id")
            if specialization.get("role_id") != example.get("base_role_id"):
                errors.append(f"{EXAMPLE_PATH.as_posix()}: base_role_id must match source specialization role_id")
            if specialization.get("capability_pack_ref") != example.get("capability_pack_ref"):
                errors.append(
                    f"{EXAMPLE_PATH.as_posix()}: capability_pack_ref must match source specialization"
                )

    capability_pack_ref = example.get("capability_pack_ref")
    if isinstance(capability_pack_ref, str) and not (root / capability_pack_ref).is_file():
        errors.append(f"{EXAMPLE_PATH.as_posix()}: missing capability pack ref: {capability_pack_ref}")

    if manifest.get("projection_scope") != "base_role_profiles_only":
        errors.append(f"{PROJECTION_MANIFEST_PATH.as_posix()} must stay base_role_profiles_only")

    proposed_agent_name = (example.get("codex_install") or {}).get("proposed_agent_name")
    generated_names = {
        entry.get("name")
        for entry in manifest.get("generated_agents", [])
        if isinstance(entry, dict)
    }
    if proposed_agent_name in generated_names:
        errors.append(f"{EXAMPLE_PATH.as_posix()}: proposed agent is already generated: {proposed_agent_name}")

    expected_candidate_posture = {
        ("decision", "status"): "candidate_only",
        ("codex_install", "install_state"): "not_projected",
        ("codex_install", "generated_surface_policy"): "no_generated_change",
        ("codex_install", "workspace_install_policy"): "no_workspace_install",
    }
    for path, expected in expected_candidate_posture.items():
        cursor: Any = example
        for key in path:
            cursor = cursor.get(key) if isinstance(cursor, dict) else None
        if cursor != expected:
            errors.append(f"{EXAMPLE_PATH.as_posix()}: {'.'.join(path)} must stay {expected!r}")

    for key in (
        "no_generated_agent_change",
        "no_workspace_install",
        "no_runtime_activation",
        "requires_reviewed_intake",
    ):
        if (example.get("guardrails") or {}).get(key) is not True:
            errors.append(f"{EXAMPLE_PATH.as_posix()}: guardrails.{key} must stay true")

    for token in (
        SCHEMA_PATH.as_posix(),
        EXAMPLE_PATH.as_posix(),
        "owner consent",
        "not projection itself",
        "base_role_profiles_only",
    ):
        if token not in doc and token not in readme:
            errors.append(f"{PART_ROOT.as_posix()} docs are missing required guidance: {token}")

    for text in iter_strings(example):
        if "generated/codex_agents/agents/" in text or ".codex/agents/" in text:
            errors.append(f"{EXAMPLE_PATH.as_posix()}: candidate-only example must not point at install paths")

    return errors


def validate_specialization_eligibility(root: Path = ROOT) -> None:
    errors = collect_specialization_eligibility_errors(root)
    if errors:
        raise SpecializationEligibilityValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex specialization eligibility part.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_specialization_eligibility(args.root.resolve())
    except SpecializationEligibilityValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Codex specialization eligibility validation passed. examples=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
