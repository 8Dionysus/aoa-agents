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
RECORDS_DIR = PART_ROOT / "records"
READINESS_PATH = PART_ROOT / "generated" / "specialization-eligibility-readiness.min.json"
DOC_PATH = PART_ROOT / "docs" / "specialization-eligibility.md"
README_PATH = PART_ROOT / "README.md"
PROJECTION_MANIFEST_PATH = Path("generated/codex_agents/projection_manifest.json")
FORMER_ROOT_PATHS = {
    Path("schemas") / "codex_specialization_eligibility_v1.json",
    Path("examples") / "codex_specialization_eligibility.example.json",
    Path("scripts") / "validate_specialization_eligibility.py",
}

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_specialization_eligibility_readiness import build_readiness_payload  # noqa: E402


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

    records_root = root / RECORDS_DIR
    if not records_root.is_dir():
        errors.append(f"missing eligibility records directory: {RECORDS_DIR.as_posix()}")
        return errors

    unexpected_record_json = sorted(
        path.relative_to(root)
        for path in records_root.glob("*.json")
        if not path.name.endswith(".eligibility.json")
    )
    if unexpected_record_json:
        errors.append(
            "unexpected specialization eligibility record JSON: "
            + ", ".join(path.as_posix() for path in unexpected_record_json)
        )

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

    if manifest.get("projection_scope") != "base_role_profiles_only":
        errors.append(f"{PROJECTION_MANIFEST_PATH.as_posix()} must stay base_role_profiles_only")

    generated_names = {
        entry.get("name")
        for entry in manifest.get("generated_agents", [])
        if isinstance(entry, dict)
    }

    def validate_payload(path: Path, payload: dict[str, Any]) -> None:
        validation_errors = sorted(
            Draft202012Validator(schema).iter_errors(payload),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        if validation_errors:
            first = validation_errors[0]
            location = ".".join(str(part) for part in first.absolute_path)
            suffix = f" at {location}" if location else ""
            errors.append(f"{path.as_posix()}: schema violation{suffix}: {first.message}")

        specialization_ref = payload.get("specialization_ref")
        if isinstance(specialization_ref, str):
            try:
                specialization = read_json(root / specialization_ref)
            except SpecializationEligibilityValidationError as exc:
                errors.append(str(exc))
                specialization = {}
            if isinstance(specialization, dict):
                if specialization.get("id") != payload.get("specialization_id"):
                    errors.append(f"{path.as_posix()}: specialization_id must match source specialization id")
                if specialization.get("role_id") != payload.get("base_role_id"):
                    errors.append(f"{path.as_posix()}: base_role_id must match source specialization role_id")
                if specialization.get("capability_pack_ref") != payload.get("capability_pack_ref"):
                    errors.append(f"{path.as_posix()}: capability_pack_ref must match source specialization")

        capability_pack_ref = payload.get("capability_pack_ref")
        if isinstance(capability_pack_ref, str) and not (root / capability_pack_ref).is_file():
            errors.append(f"{path.as_posix()}: missing capability pack ref: {capability_pack_ref}")

        proposed_agent_name = (payload.get("codex_install") or {}).get("proposed_agent_name")
        if proposed_agent_name in generated_names:
            errors.append(f"{path.as_posix()}: proposed agent is already generated: {proposed_agent_name}")

        decision_status = (payload.get("decision") or {}).get("status")
        install_state = (payload.get("codex_install") or {}).get("install_state")
        if decision_status == "candidate_only" and install_state != "not_projected":
            errors.append(f"{path.as_posix()}: candidate_only records must stay not_projected")
        if decision_status == "eligible" and install_state != "eligible_not_projected":
            errors.append(f"{path.as_posix()}: eligible records must stay eligible_not_projected")
        if decision_status == "rejected" and install_state != "rejected":
            errors.append(f"{path.as_posix()}: rejected records must use rejected install_state")

        expected_candidate_posture = {
            ("codex_install", "generated_surface_policy"): "no_generated_change",
            ("codex_install", "workspace_install_policy"): "no_workspace_install",
        }
        for key_path, expected in expected_candidate_posture.items():
            cursor: Any = payload
            for key in key_path:
                cursor = cursor.get(key) if isinstance(cursor, dict) else None
            if cursor != expected:
                errors.append(f"{path.as_posix()}: {'.'.join(key_path)} must stay {expected!r}")

        for key in (
            "no_generated_agent_change",
            "no_workspace_install",
            "no_runtime_activation",
            "requires_reviewed_intake",
        ):
            if (payload.get("guardrails") or {}).get(key) is not True:
                errors.append(f"{path.as_posix()}: guardrails.{key} must stay true")

        for text in iter_strings(payload):
            if "generated/codex_agents/agents/" in text or ".codex/agents/" in text:
                errors.append(f"{path.as_posix()}: eligibility payload must not point at install paths")

    validate_payload(EXAMPLE_PATH, example)

    record_payloads: dict[str, tuple[Path, dict[str, Any]]] = {}
    for record_path in sorted(records_root.glob("*.eligibility.json")):
        relative = record_path.relative_to(root)
        try:
            record = read_json(record_path)
        except SpecializationEligibilityValidationError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(record, dict):
            errors.append(f"{relative.as_posix()}: eligibility record must be a JSON object")
            continue
        validate_payload(relative, record)
        specialization_id = record.get("specialization_id")
        if isinstance(specialization_id, str):
            if specialization_id in record_payloads:
                previous = record_payloads[specialization_id][0]
                errors.append(
                    f"{relative.as_posix()}: duplicate eligibility record for {specialization_id}; "
                    f"already declared in {previous.as_posix()}"
                )
            record_payloads[specialization_id] = (relative, record)

    specialization_sources: dict[str, Path] = {}
    for source_path in sorted((root / "agents" / "roles").glob("*/specializations/*/specialization.json")):
        try:
            specialization = read_json(source_path)
        except SpecializationEligibilityValidationError as exc:
            errors.append(str(exc))
            continue
        specialization_id = specialization.get("id")
        if isinstance(specialization_id, str):
            specialization_sources[specialization_id] = source_path.relative_to(root)

    missing_records = sorted(set(specialization_sources) - set(record_payloads))
    extra_records = sorted(set(record_payloads) - set(specialization_sources))
    if missing_records:
        errors.append("missing eligibility records for specializations: " + ", ".join(missing_records))
    if extra_records:
        errors.append("eligibility records without source specialization: " + ", ".join(extra_records))

    for specialization_id, source_path in specialization_sources.items():
        record_entry = record_payloads.get(specialization_id)
        if not record_entry:
            continue
        record_path, record = record_entry
        if record.get("specialization_ref") != source_path.as_posix():
            errors.append(
                f"{record_path.as_posix()}: specialization_ref must be {source_path.as_posix()}"
            )

    try:
        readiness = read_json(root / READINESS_PATH)
        expected_readiness = build_readiness_payload(root)
    except SpecializationEligibilityValidationError as exc:
        errors.append(str(exc))
    else:
        if readiness != expected_readiness:
            errors.append(
                f"{READINESS_PATH.as_posix()} is stale; run "
                "python mechanics/codex-projection/parts/specialization-eligibility/scripts/"
                "build_specialization_eligibility_readiness.py"
            )

    for token in (
        SCHEMA_PATH.as_posix(),
        EXAMPLE_PATH.as_posix(),
        RECORDS_DIR.as_posix(),
        READINESS_PATH.as_posix(),
        "owner consent",
        "not projection itself",
        "base_role_profiles_only",
    ):
        if token not in doc and token not in readme:
            errors.append(f"{PART_ROOT.as_posix()} docs are missing required guidance: {token}")

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
    record_count = len(list((args.root.resolve() / RECORDS_DIR).glob("*.eligibility.json")))
    print(f"Codex specialization eligibility validation passed. examples=1 records={record_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
