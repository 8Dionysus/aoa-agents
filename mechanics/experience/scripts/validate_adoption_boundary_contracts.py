#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[3]
EXPERIENCE_ADOPTION_PART = Path("mechanics/experience/parts/adoption-and-regression")
EXPERIENCE_OFFICE_PART = Path("mechanics/experience/parts/office-operations")
AGON_ADOPTION_PART = Path("mechanics/agon/parts/adoption-retention")
BOUNDARY_HANDOFF_PART = Path("mechanics/boundary-bridge/parts/consumer-handoff")
BOUNDARY_FEDERATION_PART = Path("mechanics/boundary-bridge/parts/federation-consumer-seams")

GUARDRAIL_BOOLEAN_FIELDS = {
    "authority_required",
    "derived_only",
    "direct_tos_write",
    "direct_write",
    "direct_write_allowed",
    "direct_write_blocked",
    "dossier_allowed",
    "drill_required",
    "kag_may_force_uptake",
    "kag_may_propose",
    "lineage_indexed",
    "meaning_authority",
    "release_required",
    "required_trial",
    "requires_eval_verdict",
    "requires_owner_consent",
    "rollback_required",
    "scar_required",
    "source_theft",
    "submit_only",
}
RATIO_FIELD_HINTS = ("rate", "threshold")
ENUM_ESCAPE_VALUE = "__adoption_boundary_not_allowed__"


class AdoptionBoundaryContractsValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class AdoptionBoundaryContract:
    part: Path
    active_stem: str
    former_stem: str

    @property
    def schema_rel(self) -> Path:
        return self.part / "schemas" / f"{self.active_stem}.schema.json"

    @property
    def example_rel(self) -> Path:
        return self.part / "examples" / f"{self.active_stem}.example.json"

    @property
    def former_schema_name(self) -> str:
        return f"{self.former_stem}_v1.json"

    @property
    def former_example_name(self) -> str:
        return f"{self.former_stem}.example.json"


def _former_stem(*parts: str) -> str:
    return "_".join(parts)


def _contract(part: Path, active_stem: str, *former_parts: str) -> AdoptionBoundaryContract:
    return AdoptionBoundaryContract(
        part=part,
        active_stem=active_stem,
        former_stem=_former_stem(*former_parts),
    )


CONTRACTS = (
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "agent-adoption-participation-record",
        "agent",
        "adoption",
        "participation",
        "record",
    ),
    _contract(EXPERIENCE_ADOPTION_PART, "agent-adoption-posture-contract", "agent", "adoption", "posture", "contract"),
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "assistant-adoption-certification-delta",
        "assistant",
        "adoption",
        "certification",
        "delta",
    ),
    _contract(EXPERIENCE_ADOPTION_PART, "assistant-adoption-guard", "assistant", "adoption", "guard"),
    _contract(EXPERIENCE_ADOPTION_PART, "assistant-adoption-projection", "assistant", "adoption", "projection"),
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "assistant-adoption-regression-matrix",
        "assistant",
        "adoption",
        "regression",
        "matrix",
    ),
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "assistant-adoption-release-candidate",
        "assistant",
        "adoption",
        "release",
        "candidate",
    ),
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "assistant-adoption-rollback-marker",
        "assistant",
        "adoption",
        "rollback",
        "marker",
    ),
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "assistant-pattern-adoption-request",
        "assistant",
        "pattern",
        "adoption",
        "request",
    ),
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "assistant-pattern-release-delta",
        "assistant",
        "pattern",
        "release",
        "delta",
    ),
    _contract(
        EXPERIENCE_ADOPTION_PART,
        "assistant-shared-pattern-adoption",
        "assistant",
        "shared",
        "pattern",
        "adoption",
    ),
    _contract(EXPERIENCE_OFFICE_PART, "office-adoption-posture", "office", "adoption", "posture"),
    _contract(EXPERIENCE_OFFICE_PART, "office-pair-adoption-policy", "office", "pair", "adoption", "policy"),
    _contract(EXPERIENCE_OFFICE_PART, "office-pattern-compatibility", "office", "pattern", "compatibility"),
    _contract(AGON_ADOPTION_PART, "agent-kind-adoption-boundary", "agent", "kind", "adoption", "boundary"),
    _contract(AGON_ADOPTION_PART, "agonic-adoption-scar-candidate", "agonic", "adoption", "scar", "candidate"),
    _contract(AGON_ADOPTION_PART, "agonic-pattern-adoption-trial", "agonic", "pattern", "adoption", "trial"),
    _contract(
        AGON_ADOPTION_PART,
        "agonic-pattern-retention-obligation",
        "agonic",
        "pattern",
        "retention",
        "obligation",
    ),
    _contract(AGON_ADOPTION_PART, "agonic-shared-scar-harvest", "agonic", "shared", "scar", "harvest"),
    _contract(
        BOUNDARY_HANDOFF_PART,
        "cross-repo-adoption-readiness",
        "cross",
        "repo",
        "adoption",
        "readiness",
    ),
    _contract(
        BOUNDARY_FEDERATION_PART,
        "federation-projection-boundary",
        "federation",
        "projection",
        "boundary",
    ),
)

AGENT_SERVICE_CONTRACT_STEMS_BY_PART = {
    EXPERIENCE_ADOPTION_PART: {
        "assistant-behavior-contract-delta",
        "assistant-canary-probe-matrix",
        "assistant-regression-result",
    },
    EXPERIENCE_OFFICE_PART: {
        "agent-office-charter-change",
        "assistant-multi-office-release-result",
        "assistant-office-install-profile",
        "assistant-office-live-profile",
        "assistant-office-pairing",
        "assistant-office-revision-ledger-entry",
        "assistant-office-service-contract",
        "assistant-train-release-participant",
    },
}

FORMER_CHECK_PATHS = (
    Path("scripts/validate_adoption_boundary_contracts.py"),
    Path("tests/test_experience_wave3_seed_contracts.py"),
)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AdoptionBoundaryContractsValidationError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AdoptionBoundaryContractsValidationError(f"invalid JSON in {path}: {exc}") from exc


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
        raise AdoptionBoundaryContractsValidationError(f"{path} must contain a JSON object schema")
    try:
        Draft202012Validator.check_schema(payload)
    except SchemaError as exc:
        raise AdoptionBoundaryContractsValidationError(
            f"{path} is not a valid draft 2020-12 schema: {exc}"
        ) from exc
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise AdoptionBoundaryContractsValidationError(f"{path} must use draft 2020-12")
    if payload.get("additionalProperties") is not False:
        raise AdoptionBoundaryContractsValidationError(f"{path} must be closed by default")
    return payload


def validation_errors(schema: dict[str, Any], value: dict[str, Any]) -> list[object]:
    return sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda error: (list(error.path), error.message),
    )


def wrong_type_value(value: object) -> object:
    if isinstance(value, bool):
        return "not-a-boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "not-an-integer"
    if isinstance(value, float):
        return "not-a-number"
    if isinstance(value, str):
        return 12345
    if isinstance(value, list):
        return {"not": "an array"}
    if isinstance(value, dict):
        return "not-an-object"
    return "not-null"


def payload_schema_properties(schema: dict[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return {}
    payload = properties.get("payload")
    if not isinstance(payload, dict):
        return {}
    payload_properties = payload.get("properties")
    if not isinstance(payload_properties, dict):
        return {}
    return payload_properties


def array_field_targets(example: dict[str, Any]) -> list[tuple[str, str]]:
    targets: list[tuple[str, str]] = []
    for key, value in example.items():
        if isinstance(value, list):
            targets.append(("top", key))
    refs = example.get("refs")
    if isinstance(refs, dict):
        for key, value in refs.items():
            if isinstance(value, list):
                targets.append(("refs", key))
    payload = example.get("payload")
    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(value, list):
                targets.append(("payload", key))
    return targets


def set_section_value(value: dict[str, Any], section: str, key: str, replacement: object) -> None:
    if section == "top":
        value[key] = replacement
        return
    nested = value[section]
    if not isinstance(nested, dict):
        raise AdoptionBoundaryContractsValidationError(f"{section} is not an object")
    nested[key] = replacement


def _expect_invalid(schema: dict[str, Any], value: dict[str, Any], *, label: str, errors: list[str]) -> None:
    if not validation_errors(schema, value):
        errors.append(f"{label} unexpectedly validated")


def _validate_schema_example_pair(
    root: Path,
    contract: AdoptionBoundaryContract,
    *,
    errors: list[str],
) -> int:
    schema_path = root / contract.schema_rel
    example_path = root / contract.example_rel
    try:
        schema = _schema(schema_path)
        example = _read_json(example_path)
    except AdoptionBoundaryContractsValidationError as exc:
        errors.append(str(exc))
        return 0

    if not isinstance(example, dict):
        errors.append(f"{contract.example_rel.as_posix()} must contain a JSON object")
        return 0

    schema_errors = validation_errors(schema, example)
    if schema_errors:
        first = schema_errors[0]
        location = ".".join(str(part) for part in first.absolute_path)
        suffix = f" at {location}" if location else ""
        errors.append(f"{contract.example_rel.as_posix()} schema violation{suffix}: {first.message}")
        return 0

    with_unknown_top = copy.deepcopy(example)
    with_unknown_top["contract_escape"] = True
    _expect_invalid(
        schema,
        with_unknown_top,
        label=f"{contract.active_stem} unknown top-level field",
        errors=errors,
    )

    refs = example.get("refs")
    if isinstance(refs, dict):
        with_unknown_ref = copy.deepcopy(example)
        with_unknown_ref["refs"]["contract_escape"] = "loose-ref"
        _expect_invalid(
            schema,
            with_unknown_ref,
            label=f"{contract.active_stem} unknown refs field",
            errors=errors,
        )

    payload = example.get("payload")
    if isinstance(payload, dict):
        with_unknown_payload = copy.deepcopy(example)
        with_unknown_payload["payload"]["contract_escape"] = "loose-payload"
        _expect_invalid(
            schema,
            with_unknown_payload,
            label=f"{contract.active_stem} unknown payload field",
            errors=errors,
        )

        for key, value in payload.items():
            with_wrong_payload_type = copy.deepcopy(example)
            with_wrong_payload_type["payload"][key] = wrong_type_value(value)
            _expect_invalid(
                schema,
                with_wrong_payload_type,
                label=f"{contract.active_stem} wrong {key} type",
                errors=errors,
            )

            if key in GUARDRAIL_BOOLEAN_FIELDS and isinstance(value, bool):
                with_inverted_boolean = copy.deepcopy(example)
                with_inverted_boolean["payload"][key] = not value
                _expect_invalid(
                    schema,
                    with_inverted_boolean,
                    label=f"{contract.active_stem} inverted {key}",
                    errors=errors,
                )

            if isinstance(value, (int, float)) and not isinstance(value, bool):
                with_negative_number = copy.deepcopy(example)
                with_negative_number["payload"][key] = -1
                _expect_invalid(
                    schema,
                    with_negative_number,
                    label=f"{contract.active_stem} negative {key}",
                    errors=errors,
                )

                if key == "retention_cycles":
                    with_zero_cycles = copy.deepcopy(example)
                    with_zero_cycles["payload"][key] = 0
                    _expect_invalid(
                        schema,
                        with_zero_cycles,
                        label=f"{contract.active_stem} zero {key}",
                        errors=errors,
                    )

                if key == "value" or any(hint in key for hint in RATIO_FIELD_HINTS):
                    with_above_one = copy.deepcopy(example)
                    with_above_one["payload"][key] = 1.5
                    _expect_invalid(
                        schema,
                        with_above_one,
                        label=f"{contract.active_stem} out-of-range {key}",
                        errors=errors,
                    )

        for key, prop in payload_schema_properties(schema).items():
            if not isinstance(prop, dict) or "enum" not in prop or key not in payload:
                continue
            with_enum_escape = copy.deepcopy(example)
            with_enum_escape["payload"][key] = ENUM_ESCAPE_VALUE
            _expect_invalid(
                schema,
                with_enum_escape,
                label=f"{contract.active_stem} enum escape {key}",
                errors=errors,
            )

    exercised_arrays = 0
    for section, key in array_field_targets(example):
        exercised_arrays += 1

        with_non_string_item = copy.deepcopy(example)
        set_section_value(with_non_string_item, section, key, [12345])
        _expect_invalid(
            schema,
            with_non_string_item,
            label=f"{contract.active_stem} non-string {section}.{key} item",
            errors=errors,
        )

        with_empty_string_item = copy.deepcopy(example)
        set_section_value(with_empty_string_item, section, key, [""])
        _expect_invalid(
            schema,
            with_empty_string_item,
            label=f"{contract.active_stem} empty {section}.{key} item",
            errors=errors,
        )

    return exercised_arrays


def collect_adoption_boundary_contract_errors(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for former_path in FORMER_CHECK_PATHS:
        if (root / former_path).exists():
            errors.append(f"former root adoption/boundary check is still active: {former_path.as_posix()}")

    for contract in CONTRACTS:
        former_schema_path = root / "schemas" / contract.former_schema_name
        if former_schema_path.exists():
            errors.append(
                "former root adoption/boundary schema is still active: "
                f"{former_schema_path.relative_to(root).as_posix()}"
            )
        former_example_path = root / "examples" / contract.former_example_name
        if former_example_path.exists():
            errors.append(
                "former root adoption/boundary example is still active: "
                f"{former_example_path.relative_to(root).as_posix()}"
            )

    for part in sorted({contract.part for contract in CONTRACTS}, key=lambda path: path.as_posix()):
        part_contracts = [contract for contract in CONTRACTS if contract.part == part]
        allowed_agent_service_stems = AGENT_SERVICE_CONTRACT_STEMS_BY_PART.get(part, set())
        expected_schemas = {contract.schema_rel.name for contract in part_contracts} | {
            f"{stem}.schema.json" for stem in allowed_agent_service_stems
        }
        expected_examples = {contract.example_rel.name for contract in part_contracts} | {
            f"{stem}.example.json" for stem in allowed_agent_service_stems
        }
        _check_file_set(root, part / "schemas", expected_schemas, label=f"{part.as_posix()} schema", errors=errors)
        _check_file_set(root, part / "examples", expected_examples, label=f"{part.as_posix()} example", errors=errors)

    exercised_arrays = 0
    for contract in CONTRACTS:
        exercised_arrays += _validate_schema_example_pair(root, contract, errors=errors)

    if exercised_arrays == 0:
        errors.append("no adoption/boundary array fields were exercised")

    return errors


def validate_adoption_boundary_contracts(root: Path = ROOT) -> None:
    errors = collect_adoption_boundary_contract_errors(root)
    if errors:
        raise AdoptionBoundaryContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate adoption and boundary part-local contracts.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_adoption_boundary_contracts(args.root.resolve())
    except AdoptionBoundaryContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Adoption/boundary contract validation passed. schemas=21 examples=21")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
