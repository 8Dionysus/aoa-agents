#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import validate_agents


ROOT = Path(__file__).resolve().parents[1]
SELF_AGENT_PART = Path("mechanics/checkpoint/parts/self-agent-checkpoint")
CONTINUITY_PART = Path("mechanics/checkpoint/parts/continuity-lane")
FORMER_EXAMPLES_DIR = Path("examples") / ("self" + "_agent" + "_checkpoint")
FORMER_SCHEMA_NAMES = (
    "self-agent-checkpoint.schema.json",
    "self-agency-continuity-window.schema.json",
)


class CheckpointContractsValidationError(RuntimeError):
    pass


def collect_checkpoint_contract_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    for file_name in FORMER_SCHEMA_NAMES:
        former_path = root / "schemas" / file_name
        if former_path.exists():
            errors.append(f"former root checkpoint schema is still active: {former_path.relative_to(root).as_posix()}")

    if (root / FORMER_EXAMPLES_DIR).exists():
        errors.append(f"former root checkpoint example directory is still active: {FORMER_EXAMPLES_DIR.as_posix()}")

    expected_self_agent_schemas = {SELF_AGENT_PART / "schemas" / "self-agent-checkpoint.schema.json"}
    actual_self_agent_schemas = {
        path.relative_to(root)
        for path in (root / SELF_AGENT_PART / "schemas").glob("*.json")
    }
    if actual_self_agent_schemas != expected_self_agent_schemas:
        errors.append("self-agent-checkpoint schema file set drifted")

    expected_continuity_schemas = {CONTINUITY_PART / "schemas" / "self-agency-continuity-window.schema.json"}
    actual_continuity_schemas = {
        path.relative_to(root)
        for path in (root / CONTINUITY_PART / "schemas").glob("*.json")
    }
    if actual_continuity_schemas != expected_continuity_schemas:
        errors.append("continuity-lane schema file set drifted")

    expected_self_agent_examples = {"self-agent-checkpoint.example.json"}
    actual_self_agent_examples = {
        path.name
        for path in (root / SELF_AGENT_PART / "examples").glob("*.example.json")
    }
    if actual_self_agent_examples != expected_self_agent_examples:
        errors.append("self-agent-checkpoint example file set drifted")

    expected_continuity_examples = {"self-agency-continuity-window.example.json"}
    actual_continuity_examples = {
        path.name
        for path in (root / CONTINUITY_PART / "examples").glob("*.example.json")
    }
    if actual_continuity_examples != expected_continuity_examples:
        errors.append("continuity-lane example file set drifted")

    try:
        validate_agents.validate_self_agent_checkpoint_schema_surface()
        validate_agents.validate_self_agency_continuity_window_schema_surface()
        validate_agents.validate_self_agent_checkpoint_example()
        validate_agents.validate_self_agency_continuity_window_example()
        validate_agents.validate_negative_self_agent_checkpoint_examples()
    except (validate_agents.AgentsValidationError, validate_agents.SchemaValidationError) as exc:
        errors.append(str(exc))

    return errors


def validate_checkpoint_contracts(root: Path = ROOT) -> None:
    errors = collect_checkpoint_contract_errors(root)
    if errors:
        raise CheckpointContractsValidationError("\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate checkpoint part-local contract payloads.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        validate_checkpoint_contracts(root)
    except CheckpointContractsValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Checkpoint contract validation passed. schemas=2 examples=2 invalid=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
