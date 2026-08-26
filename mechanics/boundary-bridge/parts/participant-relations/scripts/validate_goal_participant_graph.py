#!/usr/bin/env python3
"""Validate the complete participant-relation part and its generated reader."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_goal_participant_graph import (
    CONTRACT_PATH,
    CONTRACT_SCHEMA_VERSION,
    ADMISSION_SCHEMA_PATH,
    GRAPH_PATH,
    GRAPH_SCHEMA_PATH,
    PART_ROOT,
    RELATION_SCHEMA_ID,
    RELATION_SCHEMA_PATH,
    PUBLICATION_SCHEMA_PATH,
    ROOT,
    SOURCE_PATH,
    SOURCE_SCHEMA_PATH,
    FALLBACK_LITERALS,
    GoalParticipantGraphError,
    PRIVACY_OMISSION_FIELDS,
    build_graph_payload,
    check_generated,
    read_json,
    validate_instance,
    validate_relation,
    validate_source_payload,
)
from admit_goal_participant_publication import validate_publication
from read_goal_participant_graph import read_goal_participant_graph


DOC_PATH = PART_ROOT / "docs/goal-participant-relations.md"
README_PATH = PART_ROOT / "README.md"
EXAMPLE_PATH = PART_ROOT / "examples/goal-participant-relation.example.json"
INVALID_EXAMPLE_PATHS = {
    PART_ROOT / "examples/invalid/missing-producer-ref.json",
    PART_ROOT / "examples/invalid/current-publication-with-more.json",
}
AGENTS_PATH = PART_ROOT / "AGENTS.md"
EXPECTED_SCHEMA_FILES = {
    "goal-participant-admission.schema.json",
    "goal-participant-publication.schema.json",
    "goal-participant-relation.schema.json",
    "goal-participant-source.schema.json",
    "goal-participant-graph.schema.json",
}


class GoalParticipantGraphValidationError(GoalParticipantGraphError):
    """Raised when the complete participant-relation part is inconsistent."""


def _require_text(root: Path, relative: Path) -> str:
    path = root / relative
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise GoalParticipantGraphValidationError(f"missing required text surface: {relative.as_posix()}") from exc


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise GoalParticipantGraphValidationError(message)


def validate_goal_participant_graph(root: Path = ROOT) -> None:
    root = root.resolve()
    part_root = root / PART_ROOT
    contract = read_json(root / CONTRACT_PATH)
    _assert(contract.get("schema_version") == CONTRACT_SCHEMA_VERSION, "contract schema_version drifted")
    _assert(contract.get("owner_repo") == "aoa-agents", "contract owner_repo must remain aoa-agents")
    _assert(
        set(contract.get("dimensions", {}))
        == {"identity", "obligation_role", "task_assignment", "model_realization", "runtime_incarnation"},
        "contract dimensions drifted",
    )
    _assert(contract.get("admission", {}).get("relation_key", {}).get("publisher_owned") is True,
            "relation key must remain publisher-owned")
    _assert("bare_goal_id" in contract.get("forbidden_join_inputs", []),
            "contract must forbid bare Goal joins")

    schema_files = {
        path.name for path in (part_root / "schemas").glob("*.json") if path.is_file()
    }
    _assert(schema_files == EXPECTED_SCHEMA_FILES, "participant relation schema file set drifted")
    relation_schema = read_json(root / RELATION_SCHEMA_PATH)
    source_schema = read_json(root / SOURCE_SCHEMA_PATH)
    graph_schema = read_json(root / GRAPH_SCHEMA_PATH)
    publication_schema = read_json(root / PUBLICATION_SCHEMA_PATH)
    admission_schema = read_json(root / ADMISSION_SCHEMA_PATH)
    _assert(relation_schema.get("$id") == RELATION_SCHEMA_ID, "relation schema $id drifted")
    for schema, label in (
        (source_schema, "source"),
        (publication_schema, "publication"),
        (graph_schema, "graph"),
    ):
        _assert(
            schema["properties"]["records"]["items"] == {"$ref": RELATION_SCHEMA_ID},
            f"{label} records must reference the exact relation schema",
        )
    _assert(
        relation_schema["$defs"]["privacy_omissions"]["properties"]["omitted_fields"]["const"]
        == list(PRIVACY_OMISSION_FIELDS),
        "relation privacy omission schema drifted",
    )
    for schema, label in (
        (relation_schema, RELATION_SCHEMA_PATH.as_posix()),
        (source_schema, SOURCE_SCHEMA_PATH.as_posix()),
        (graph_schema, GRAPH_SCHEMA_PATH.as_posix()),
        (publication_schema, PUBLICATION_SCHEMA_PATH.as_posix()),
        (admission_schema, ADMISSION_SCHEMA_PATH.as_posix()),
    ):
        try:
            from jsonschema import Draft202012Validator

            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # jsonschema exposes several schema error types.
            raise GoalParticipantGraphValidationError(f"{label}: invalid JSON schema: {exc}") from exc

    example = read_json(root / EXAMPLE_PATH)
    _assert(example.get("evidence_class") == "synthetic_public_example",
            "public example must remain explicitly synthetic")
    validate_relation(example, relation_schema=relation_schema, label=EXAMPLE_PATH.as_posix())

    for invalid_path in INVALID_EXAMPLE_PATHS:
        invalid = read_json(root / invalid_path)
        try:
            validate_publication(root, invalid)
        except GoalParticipantGraphError:
            continue
        raise GoalParticipantGraphValidationError(
            f"negative publication fixture was accepted: {invalid_path.as_posix()}"
        )

    source = read_json(root / SOURCE_PATH)
    validate_source_payload(root, source)
    _assert(source.get("evidence_class") == "empty_deferred",
            "checked-in source must remain an empty deferred capture until owner evidence is admitted")
    _assert(source.get("records") == [], "checked-in source must not fabricate live relation records")
    _assert(source.get("currentness", {}).get("state") == "deferred",
            "checked-in source must preserve deferred currentness")
    _assert(source.get("admission_receipt") is None,
            "checked-in empty source must not carry an admission receipt")

    expected = build_graph_payload(root)
    check_generated(root, root / GRAPH_PATH)
    graph = read_goal_participant_graph(root)
    _assert(graph == expected, "generated reader does not equal the source-owned builder output")
    _assert(graph.get("records") == [], "generated reader must not fabricate participant rows")
    _assert(graph.get("currentness", {}).get("state") == "deferred",
            "generated reader must preserve deferred currentness")
    _assert(graph.get("source", {}).get("admission_receipt") is None,
            "generated empty reader must not carry an admission receipt")
    _assert(graph.get("fallback_policy", {}).get("state") == "disabled",
            "generated reader must disable fallback enrichment")
    for value in graph.get("records", []):
        for text in _iter_strings(value):
            _assert(text.lower() not in FALLBACK_LITERALS, "generated reader contains a forbidden fallback literal")

    for relative, required in (
        (DOC_PATH, ("relation_key", "currentness", "pagination", "privacy", "no live", "admission receipt")),
        (README_PATH, ("source feed", "generated reader", "synthetic", "publication", "admission")),
        (AGENTS_PATH, ("exact owner reference", "publisher-owned", "deferred", "typed publication", "receipt")),
    ):
        text = _require_text(root, relative).lower()
        for snippet in required:
            _assert(snippet.lower() in text, f"{relative.as_posix()} is missing required guidance: {snippet}")


def _iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_strings(child)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the aoa-agents Goal participant relation part.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_goal_participant_graph(args.root)
    except GoalParticipantGraphError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Goal participant relation part is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
