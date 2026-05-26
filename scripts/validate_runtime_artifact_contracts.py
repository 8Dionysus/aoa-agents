#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import validate_agents


ROOT = Path(__file__).resolve().parents[1]
PART_ROOT = Path("mechanics/runtime-seam/parts/artifact-contracts")
SCHEMAS_DIR = PART_ROOT / "schemas"
EXAMPLES_DIR = PART_ROOT / "examples"
FORMER_ROOT_EXAMPLES_DIR = Path("examples") / ("runtime" + "_artifacts")


class RuntimeArtifactContractsValidationError(RuntimeError):
    pass


def _artifact_schema_name(artifact_name: str) -> str:
    return f"artifact.{artifact_name}.schema.json"


def _expected_schema_paths() -> set[Path]:
    return {
        SCHEMAS_DIR / _artifact_schema_name(artifact_name)
        for artifact_name in validate_agents.RUNTIME_ARTIFACT_SCHEMA_PATHS
    }


def _expected_example_names() -> set[str]:
    names = {
        f"{artifact_name}.example.json"
        for artifact_name in validate_agents.RUNTIME_ARTIFACT_SCHEMA_PATHS
    }
    names.add("transition_decision.return.example.json")
    return names


def collect_runtime_artifact_contract_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    former_schema_dir = root / "schemas"
    for artifact_name in validate_agents.RUNTIME_ARTIFACT_SCHEMA_PATHS:
        former_path = former_schema_dir / _artifact_schema_name(artifact_name)
        if former_path.exists():
            errors.append(f"former root artifact schema is still active: {former_path.relative_to(root).as_posix()}")

    if (root / FORMER_ROOT_EXAMPLES_DIR).exists():
        errors.append(f"former root runtime artifact examples directory is still active: {FORMER_ROOT_EXAMPLES_DIR.as_posix()}")

    schema_dir = root / SCHEMAS_DIR
    active_schemas = {path.relative_to(root) for path in schema_dir.glob("*.json")}
    expected_schemas = _expected_schema_paths()
    if active_schemas != expected_schemas:
        missing = sorted(expected_schemas - active_schemas)
        extra = sorted(active_schemas - expected_schemas)
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if extra:
            details.append("unexpected: " + ", ".join(path.as_posix() for path in extra))
        errors.append("runtime artifact schema file set drifted (" + "; ".join(details) + ")")

    examples_dir = root / EXAMPLES_DIR
    active_examples = {path.name for path in examples_dir.glob("*.example.json")}
    expected_examples = _expected_example_names()
    if active_examples != expected_examples:
        missing = sorted(expected_examples - active_examples)
        extra = sorted(active_examples - expected_examples)
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("unexpected: " + ", ".join(extra))
        errors.append("runtime artifact example file set drifted (" + "; ".join(details) + ")")

    try:
        validate_agents.validate_runtime_artifact_schema_surfaces()
        validate_agents.validate_runtime_artifact_examples()
        validate_agents.validate_negative_runtime_artifact_examples()
    except (validate_agents.AgentsValidationError, validate_agents.SchemaValidationError) as exc:
        errors.append(str(exc))

    return errors


def validate_runtime_artifact_contracts(root: Path = ROOT) -> None:
    errors = collect_runtime_artifact_contract_errors(root)
    if errors:
        raise RuntimeArtifactContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runtime-seam artifact-contract part payloads.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_runtime_artifact_contracts(root)
    except RuntimeArtifactContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Runtime artifact contract validation passed. schemas=7 examples=8 invalid=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
