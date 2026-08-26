#!/usr/bin/env python3
"""Build the source-owned exact Goal participant relation reader."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = Path("mechanics/boundary-bridge/parts/participant-relations")
CONTRACT_PATH = PART_ROOT / "contract.json"
RELATION_SCHEMA_PATH = PART_ROOT / "schemas/goal-participant-relation.schema.json"
SOURCE_SCHEMA_PATH = PART_ROOT / "schemas/goal-participant-source.schema.json"
GRAPH_SCHEMA_PATH = PART_ROOT / "schemas/goal-participant-graph.schema.json"
PUBLICATION_SCHEMA_PATH = PART_ROOT / "schemas/goal-participant-publication.schema.json"
ADMISSION_SCHEMA_PATH = PART_ROOT / "schemas/goal-participant-admission.schema.json"
SOURCE_PATH = PART_ROOT / "records/goal-participant-relations.source.json"
GRAPH_PATH = PART_ROOT / "generated/goal-participant-graph.min.json"

RELATION_SCHEMA_VERSION = "aoa_agents_goal_participant_relation_v1"
SOURCE_SCHEMA_VERSION = "aoa_agents_goal_participant_relation_source_v1"
GRAPH_SCHEMA_VERSION = "aoa_agents_goal_participant_graph_v1"
CONTRACT_SCHEMA_VERSION = "aoa_agents_goal_participant_relation_contract_v1"
RELATION_KEY_SCHEMA_VERSION = "aoa_agents_goal_participant_relation_key_v1"
PUBLICATION_SCHEMA_VERSION = "aoa_agents_goal_participant_relation_publication_v1"
ADMISSION_SCHEMA_VERSION = "aoa_agents_goal_participant_relation_admission_v1"
RELATION_SCHEMA_ID = "https://aoa-agents.local/schemas/aoa_agents_goal_participant_relation_v1.json"
FALLBACK_LITERALS = {"participant n", "working agent", "master"}
FORBIDDEN_KEY_PARTS = {
    "luna",
    "display",
    "display_name",
    "role",
    "role_label",
    "model",
    "model_name",
    "model_version",
    "pid",
    "cwd",
    "path",
    "version",
    "holder",
    "goal",
    "goal_id",
    "master",
    "thread",
}
PRIVACY_OMISSION_FIELDS = (
    "human_display_name",
    "raw_prompt",
    "secrets",
    "cwd",
    "path",
    "pid",
    "terminal_title",
    "unreviewed_model_metadata",
)
REQUIRED_PRIVACY_OMISSIONS = frozenset(PRIVACY_OMISSION_FIELDS)
DIMENSION_NAMES = (
    "identity",
    "obligation_role",
    "task_assignment",
    "model_realization",
    "runtime_incarnation",
)
SCOPE_FIELDS = ("goal_ref", "goal_instance_ref", "master_thread_ref")
STABLE_REF_IDENTITY_FIELDS = ("owner_repo", "object_id", "source_ref", "schema_version")
RFC3339_DATE_TIME = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
FORMAT_CHECKER = FormatChecker()


@FORMAT_CHECKER.checks("date-time")
def _is_rfc3339_date_time(value: Any) -> bool:
    if not isinstance(value, str) or not RFC3339_DATE_TIME.fullmatch(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


class GoalParticipantGraphError(RuntimeError):
    """Raised when the relation surface cannot be admitted or built."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GoalParticipantGraphError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GoalParticipantGraphError(f"invalid JSON in {path}: {exc}") from exc


def compact_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_value(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_ref(ref: dict[str, Any]) -> str:
    return json.dumps(ref, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def is_ref(value: Any) -> bool:
    return isinstance(value, dict) and all(
        key in value
        for key in ("owner_repo", "object_id", "source_ref", "schema_version", "content_digest")
    )


def iter_refs(value: Any) -> Iterable[dict[str, Any]]:
    if is_ref(value):
        yield value
        return
    if isinstance(value, dict):
        for child in value.values():
            yield from iter_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_refs(child)


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_strings(child)


def _schema_registry(root: Path) -> Registry:
    relation_schema = read_json(root.resolve() / RELATION_SCHEMA_PATH)
    if relation_schema.get("$id") != RELATION_SCHEMA_ID:
        raise GoalParticipantGraphError("relation schema $id drifted from the admitted container reference")
    return Registry().with_resource(
        RELATION_SCHEMA_ID,
        Resource.from_contents(relation_schema),
    )


def validate_instance(
    payload: Any,
    schema: dict[str, Any],
    label: str,
    *,
    root: Path | None = None,
) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise GoalParticipantGraphError(f"{label}: invalid schema: {exc}") from exc
    validator = Draft202012Validator(
        schema,
        registry=_schema_registry(root or ROOT),
        format_checker=FORMAT_CHECKER,
    )
    errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path)
        suffix = f" at {location}" if location else ""
        raise GoalParticipantGraphError(f"{label}: schema violation{suffix}: {first.message}")


def ref_for_file(
    *,
    root: Path,
    path: Path,
    object_id: str,
    schema_version: str,
) -> dict[str, str]:
    relative = path.relative_to(root).as_posix()
    return {
        "owner_repo": "aoa-agents",
        "object_id": object_id,
        "source_ref": f"repo:aoa-agents/{relative}",
        "schema_version": schema_version,
        "content_digest": sha256_file(path),
    }


def current_contract_ref(root: Path) -> dict[str, str]:
    root = root.resolve()
    return ref_for_file(
        root=root,
        path=root / CONTRACT_PATH,
        object_id="contract:goal-participant-relations",
        schema_version=CONTRACT_SCHEMA_VERSION,
    )


def current_source_ref(root: Path) -> dict[str, str]:
    root = root.resolve()
    return ref_for_file(
        root=root,
        path=root / SOURCE_PATH,
        object_id="source:goal-participant-relations",
        schema_version=SOURCE_SCHEMA_VERSION,
    )


def current_privacy_policy_ref(root: Path) -> dict[str, str]:
    root = root.resolve()
    return ref_for_file(
        root=root,
        path=root / CONTRACT_PATH,
        object_id="privacy:goal-participant-relations-v1",
        schema_version=CONTRACT_SCHEMA_VERSION,
    )


def validate_privacy_omissions(
    privacy: dict[str, Any],
    *,
    label: str,
    expected_policy_ref: dict[str, Any] | None = None,
) -> None:
    if privacy["state"] != "applied":
        raise GoalParticipantGraphError(f"{label}: privacy policy must be applied")
    if set(privacy["omitted_fields"]) != REQUIRED_PRIVACY_OMISSIONS:
        raise GoalParticipantGraphError(f"{label}: privacy omissions do not match the canonical policy")
    if expected_policy_ref is not None and privacy["policy_ref"] != expected_policy_ref:
        raise GoalParticipantGraphError(f"{label}: privacy policy ref is not the exact current policy reference")


def relation_endpoint_refs(record: dict[str, Any]) -> set[str]:
    endpoints: set[str] = set()
    endpoints.update(canonical_ref(ref) for ref in iter_refs(record["scope"]))
    for dimension in record["dimensions"].values():
        if dimension["state"] == "present":
            endpoints.update(canonical_ref(ref) for ref in iter_refs(dimension["value"]))
    return endpoints


def relation_key_digest(relation_key: dict[str, Any]) -> str:
    material = {key: value for key, value in relation_key.items() if key != "content_digest"}
    return digest_value(material)


def publication_payload_digest(records: list[dict[str, Any]]) -> str:
    return digest_value(records)


def _declared_dimension_owner_repos(root: Path, dimension_name: str) -> frozenset[str]:
    contract = read_json(root.resolve() / CONTRACT_PATH)
    dimensions = contract.get("dimensions")
    dimension = dimensions.get(dimension_name) if isinstance(dimensions, dict) else None
    allowed = dimension.get("allowed_owner_repos") if isinstance(dimension, dict) else None
    if (
        not isinstance(allowed, list)
        or not allowed
        or any(not isinstance(owner_repo, str) or not owner_repo for owner_repo in allowed)
    ):
        raise GoalParticipantGraphError(
            f"contract dimensions.{dimension_name}.allowed_owner_repos is missing or invalid"
        )
    return frozenset(allowed)


def _declared_scope_owner_repos(root: Path, scope_field: str) -> frozenset[str]:
    contract = read_json(root.resolve() / CONTRACT_PATH)
    scope_owners = contract.get("scope_owner_repos")
    allowed = scope_owners.get(scope_field) if isinstance(scope_owners, dict) else None
    if (
        not isinstance(allowed, list)
        or not allowed
        or any(not isinstance(owner_repo, str) or not owner_repo for owner_repo in allowed)
    ):
        raise GoalParticipantGraphError(
            f"contract scope_owner_repos.{scope_field} is missing or invalid"
        )
    return frozenset(allowed)


def _validate_ref_source_owner(ref: dict[str, Any], *, label: str) -> None:
    encoded = ref["source_ref"][len("repo:") :]
    source_owner, separator, source_path = encoded.partition("/")
    if source_owner != ref["owner_repo"]:
        raise GoalParticipantGraphError(
            f"{label}: source_ref repository {source_owner!r} contradicts owner_repo {ref['owner_repo']!r}"
        )
    path_parts = source_path.split("/") if separator else []
    if (
        not separator
        or not source_path
        or source_path.startswith("/")
        or source_path.endswith("/")
        or any(part in {"", ".", ".."} for part in path_parts)
    ):
        raise GoalParticipantGraphError(
            f"{label}: source_ref must include a normalized non-empty path after the owner repository"
        )


def _validate_ref_owner(
    ref: dict[str, Any],
    *,
    allowed_owner_repos: frozenset[str],
    label: str,
) -> None:
    _validate_ref_source_owner(ref, label=label)
    if ref["owner_repo"] not in allowed_owner_repos:
        expected = ", ".join(sorted(allowed_owner_repos))
        raise GoalParticipantGraphError(
            f"{label}: owner_repo {ref['owner_repo']!r} is not declared; expected one of {expected}"
        )


def _validate_dimension_ref_owners(
    root: Path,
    dimension_name: str,
    dimension: dict[str, Any],
    *,
    label: str,
) -> None:
    allowed_owner_repos = _declared_dimension_owner_repos(root, dimension_name)
    owner_ref = dimension.get("owner_ref")
    if owner_ref is not None:
        _validate_ref_owner(
            owner_ref,
            allowed_owner_repos=allowed_owner_repos,
            label=f"{label}.owner_ref",
        )
    for index, evidence_ref in enumerate(dimension.get("evidence_refs", [])):
        _validate_ref_owner(
            evidence_ref,
            allowed_owner_repos=allowed_owner_repos,
            label=f"{label}.evidence_refs[{index}]",
        )

    value = dimension.get("value")
    if value is None:
        return
    if dimension_name == "task_assignment":
        _validate_ref_owner(
            value["assignment_ref"],
            allowed_owner_repos=allowed_owner_repos,
            label=f"{label}.value.assignment_ref",
        )
        if value.get("task_ref") is not None:
            _validate_ref_owner(
                value["task_ref"],
                allowed_owner_repos=allowed_owner_repos,
                label=f"{label}.value.task_ref",
            )
        for scope_field in SCOPE_FIELDS:
            _validate_ref_owner(
                value[scope_field],
                allowed_owner_repos=_declared_scope_owner_repos(root, scope_field),
                label=f"{label}.value.{scope_field}",
            )
        return

    for index, value_ref in enumerate(iter_refs(value)):
        _validate_ref_owner(
            value_ref,
            allowed_owner_repos=allowed_owner_repos,
            label=f"{label}.value.ref[{index}]",
        )


RECEIPT_IDENTITY_FIELDS = (
    "schema_version",
    "kind",
    "admission_state",
    "publisher_ref",
    "producer_ref",
    "publication_ref",
    "publication_schema_version",
    "payload_digest",
    "scope",
    "relation_ids",
    "currentness",
    "pagination",
    "privacy_omissions",
    "claim_limit",
)


def admission_receipt_identity_material(receipt: dict[str, Any]) -> dict[str, Any]:
    return {field: receipt[field] for field in RECEIPT_IDENTITY_FIELDS}


def admission_receipt_id(receipt: dict[str, Any]) -> str:
    return "receipt:" + hashlib.sha256(
        canonical_json(admission_receipt_identity_material(receipt)).encode("utf-8")
    ).hexdigest()


def _key_parts(key_id: str) -> set[str]:
    return {
        part
        for token in re.split(r"[._:-]+", key_id.lower())
        for part in re.findall(r"[a-z]+|[0-9]+", token)
        if part
    }


OPAQUE_RELATION_KEY_SUFFIX = re.compile(r"^[a-z0-9]+(?:[._:-][a-z0-9]+)+$")


CLAIM_LIMIT_POSITIVE_VERBS = re.compile(
    r"\b(?:assert(?:s|ed)?|claim(?:s|ed)?|confirm(?:s|ed)?|demonstrat(?:e|es|ed)|"
    r"establish(?:es|ed)?|ensur(?:e|es|ed)|guarante(?:e|es|d)|pro(?:ve|ves|ved)|"
    r"show(?:s|ed)?|validat(?:e|es|ed)|verif(?:y|ies|ied))\b"
)
CLAIM_LIMIT_UNBOUNDED_TERMS = re.compile(
    r"\b(?:live(?:ness)?|activation|wake|accept(?:s|ed|ance|ing)?|completion)\b|"
    r"\b(?:runtime\s+(?:activation|health|presence)|owner\s+truth|"
    r"goal\s+completion|semantic\s+goal\s+acceptance|live\s+participant\s+presence)\b"
)
CLAIM_LIMIT_NEGATION = re.compile(
    r"\b(?:cannot|can't|does\s+not|doesn't|do\s+not|don't|never|no|not|without)\b"
)
CLAIM_LIMIT_NEGATION_BOUNDARY = re.compile(r"\b(?:and|although|but|however|yet)\b")


def _claim_limit_is_negated(clause: str, start: int) -> bool:
    prefix = clause[:start]
    negations = list(CLAIM_LIMIT_NEGATION.finditer(prefix))
    if not negations:
        return False
    negation = negations[-1]
    governed = clause[negation.end() : start]
    return not CLAIM_LIMIT_NEGATION_BOUNDARY.search(governed)


def validate_claim_limit(claim_limit: str, *, label: str) -> None:
    for clause in re.split(r"[.!?;:]+", claim_limit.lower()):
        if not clause.strip():
            continue
        for pattern in (CLAIM_LIMIT_POSITIVE_VERBS, CLAIM_LIMIT_UNBOUNDED_TERMS):
            if any(not _claim_limit_is_negated(clause, match.start()) for match in pattern.finditer(clause)):
                raise GoalParticipantGraphError(
                    f"{label}: claim_limit widens beyond structural relation admission"
                )


def _validate_currentness_provenance(currentness: dict[str, Any], *, label: str) -> None:
    watermark = currentness.get("source_watermark_ref")
    if watermark is not None:
        _validate_ref_source_owner(watermark, label=f"{label}.source_watermark_ref")


def validate_relation(
    record: dict[str, Any],
    *,
    relation_schema: dict[str, Any],
    label: str,
    root: Path | None = None,
    publisher_ref: dict[str, Any] | None = None,
    require_key_digest: bool = False,
    expected_privacy_policy_ref: dict[str, Any] | None = None,
) -> None:
    repo_root = (root or ROOT).resolve()
    validate_instance(record, relation_schema, label, root=repo_root)
    validate_claim_limit(record["claim_limit"], label=f"{label}.claim_limit")
    for dimension_name, dimension in record["dimensions"].items():
        validate_claim_limit(
            dimension["claim_limit"],
            label=f"{label}.dimensions.{dimension_name}.claim_limit",
        )
    validate_privacy_omissions(
        record["privacy_omissions"],
        label=f"{label}.privacy_omissions",
        expected_policy_ref=expected_privacy_policy_ref,
    )
    if record["relation_key"]["schema_version"] != RELATION_KEY_SCHEMA_VERSION:
        raise GoalParticipantGraphError(f"{label}: relation key schema version is not admitted")
    key_id = record["relation_key"]["key_id"]
    key_suffix = key_id[len("rel:") :]
    if not OPAQUE_RELATION_KEY_SUFFIX.fullmatch(key_suffix):
        raise GoalParticipantGraphError(
            f"{label}: relation key must use an opaque segmented suffix; concatenated heuristic keys are not admissible"
        )
    key_parts = _key_parts(key_id)
    forbidden_parts = sorted(key_parts & FORBIDDEN_KEY_PARTS)
    if forbidden_parts:
        raise GoalParticipantGraphError(
            f"{label}: relation key must not contain heuristic join parts: {', '.join(forbidden_parts)}"
        )
    if publisher_ref is not None and record["relation_key"]["publisher_ref"] != publisher_ref:
        raise GoalParticipantGraphError(f"{label}: relation key publisher_ref does not match source publisher")
    if require_key_digest and record["relation_key"]["content_digest"] != relation_key_digest(record["relation_key"]):
        raise GoalParticipantGraphError(f"{label}: relation key content_digest does not match its canonical key material")

    expected_endpoints = relation_endpoint_refs(record)
    actual_endpoints = {
        canonical_ref(ref) for ref in record["relation_key"]["endpoint_refs"]
    }
    if actual_endpoints != expected_endpoints:
        raise GoalParticipantGraphError(
            f"{label}: publisher endpoint references do not exactly cover the relation scope and present dimensions"
        )

    scope_identities = [
        tuple(record["scope"][scope_field][field] for field in STABLE_REF_IDENTITY_FIELDS)
        for scope_field in SCOPE_FIELDS
    ]
    if len(set(scope_identities)) != len(scope_identities):
        raise GoalParticipantGraphError(
            f"{label}: goal, Goal-instance, and master-thread scope references must be distinct stable endpoints"
        )
    for scope_field in SCOPE_FIELDS:
        _validate_ref_owner(
            record["scope"][scope_field],
            allowed_owner_repos=_declared_scope_owner_repos(repo_root, scope_field),
            label=f"{label}.scope.{scope_field}",
        )

    for dimension_name in DIMENSION_NAMES:
        dimension = record["dimensions"][dimension_name]
        _validate_dimension_ref_owners(
            repo_root,
            dimension_name,
            dimension,
            label=f"{label}.dimensions.{dimension_name}",
        )
        if dimension["state"] != "present":
            continue
        owner_ref = canonical_ref(dimension["owner_ref"])
        value_refs = {canonical_ref(ref) for ref in iter_refs(dimension["value"])}
        if owner_ref not in value_refs:
            raise GoalParticipantGraphError(
                f"{label}: {dimension_name}.owner_ref must exactly identify one populated dimension endpoint"
            )

    assignment = record["dimensions"]["task_assignment"]
    if assignment["state"] == "present":
        assignment_value = assignment["value"]
        for scope_field in SCOPE_FIELDS:
            if assignment_value[scope_field] != record["scope"][scope_field]:
                raise GoalParticipantGraphError(
                    f"{label}: task_assignment.{scope_field} must exactly match the relation scope"
                )

    for text in iter_strings(record):
        if text.lower() in FALLBACK_LITERALS:
            raise GoalParticipantGraphError(f"{label}: fallback literal is not admissible: {text!r}")


def _currentness_and_pagination_errors(source: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    pagination = source["pagination"]
    currentness = source["currentness"]
    has_more = pagination["has_more"]
    next_cursor = pagination["next_cursor_ref"]
    if pagination["page_index"] != 0:
        errors.append(
            f"{label}: only page_index=0 may be admitted as one complete publication"
        )
    if has_more and next_cursor is None:
        errors.append(f"{label}: has_more=true requires an exact next_cursor_ref")
    if not has_more and next_cursor is not None:
        errors.append(f"{label}: has_more=false cannot carry a next_cursor_ref")
    if next_cursor is not None:
        try:
            _validate_ref_source_owner(next_cursor, label=f"{label}.pagination.next_cursor_ref")
        except GoalParticipantGraphError as exc:
            errors.append(str(exc))
    if has_more and currentness["state"] != "deferred":
        errors.append(f"{label}: a paginated continuation must remain currentness=deferred")
    if source["evidence_class"] == "empty_deferred":
        if source["records"]:
            errors.append(f"{label}: empty_deferred source cannot publish relation records")
        if currentness["state"] != "deferred":
            errors.append(f"{label}: empty_deferred source must remain currentness=deferred")
    return errors


def validate_admission_receipt(
    root: Path,
    receipt: dict[str, Any],
    *,
    publication: dict[str, Any] | None = None,
    source: dict[str, Any] | None = None,
) -> None:
    admission_schema = read_json(root / ADMISSION_SCHEMA_PATH)
    validate_instance(receipt, admission_schema, "admission receipt", root=root)
    if receipt["receipt_id"] != admission_receipt_id(receipt):
        raise GoalParticipantGraphError("admission receipt receipt_id does not match its canonical identity")
    expected_contract_ref = current_contract_ref(root)
    if receipt["publisher_ref"] != expected_contract_ref:
        raise GoalParticipantGraphError("admission receipt publisher_ref is not the exact current contract reference")
    if receipt["currentness"]["state"] != "current":
        raise GoalParticipantGraphError("admission receipt must preserve currentness=current")
    if not receipt["currentness"].get("observed_at"):
        raise GoalParticipantGraphError("admission receipt currentness requires observed_at")
    if receipt["pagination"]["has_more"] or receipt["pagination"]["next_cursor_ref"] is not None:
        raise GoalParticipantGraphError("admission receipt cannot admit an incomplete paginated publication")
    if receipt["pagination"]["page_index"] != 0:
        raise GoalParticipantGraphError("admission receipt must represent the initial complete publication page")
    if set(receipt["privacy_omissions"]) != REQUIRED_PRIVACY_OMISSIONS:
        raise GoalParticipantGraphError("admission receipt privacy omissions drifted from the contract baseline")
    validate_claim_limit(receipt["claim_limit"], label="admission receipt.claim_limit")
    _validate_currentness_provenance(receipt["currentness"], label="admission receipt.currentness")
    for field in ("publisher_ref", "producer_ref", "publication_ref"):
        _validate_ref_source_owner(receipt[field], label=f"admission receipt.{field}")
    for scope_field in SCOPE_FIELDS:
        _validate_ref_owner(
            receipt["scope"][scope_field],
            allowed_owner_repos=_declared_scope_owner_repos(root, scope_field),
            label=f"admission receipt.scope.{scope_field}",
        )
    if receipt["producer_ref"] == receipt["publication_ref"]:
        raise GoalParticipantGraphError("admission receipt producer_ref and publication_ref must remain distinct")
    if receipt["producer_ref"]["owner_repo"] != receipt["publication_ref"]["owner_repo"]:
        raise GoalParticipantGraphError("admission receipt producer_ref and publication_ref must name one producer owner")
    if publication is not None:
        expected_ids = [record["relation_id"] for record in publication["records"]]
        if receipt["producer_ref"] != publication["producer_ref"]:
            raise GoalParticipantGraphError("admission receipt producer_ref does not match publication")
        if receipt["publication_ref"] != publication["publication_ref"]:
            raise GoalParticipantGraphError("admission receipt publication_ref does not match publication")
        if receipt["payload_digest"] != publication["payload_digest"]:
            raise GoalParticipantGraphError("admission receipt payload_digest does not match publication")
        if receipt["scope"] != publication["scope"]:
            raise GoalParticipantGraphError("admission receipt scope does not match publication")
        if receipt["relation_ids"] != expected_ids:
            raise GoalParticipantGraphError("admission receipt relation_ids do not preserve publication order")
        if receipt["currentness"] != publication["currentness"]:
            raise GoalParticipantGraphError("admission receipt currentness does not match publication")
        if receipt["pagination"] != publication["pagination"]:
            raise GoalParticipantGraphError("admission receipt pagination does not match publication")
        if receipt["privacy_omissions"] != publication["privacy_omissions"]:
            raise GoalParticipantGraphError("admission receipt privacy omissions do not match publication")
    if source is not None:
        source_records = source["records"]
        if receipt["relation_ids"] != [record["relation_id"] for record in source_records]:
            raise GoalParticipantGraphError("admission receipt relation_ids do not match source records")
        if receipt["payload_digest"] != publication_payload_digest(source_records):
            raise GoalParticipantGraphError("admission receipt payload_digest does not match source records")
        if receipt["currentness"] != source["currentness"]:
            raise GoalParticipantGraphError("admission receipt currentness does not match source")
        if receipt["pagination"] != source["pagination"]:
            raise GoalParticipantGraphError("admission receipt pagination does not match source")
        if receipt["privacy_omissions"] != source["privacy_omissions"]:
            raise GoalParticipantGraphError("admission receipt privacy omissions do not match source")
        scopes = {canonical_json(record["scope"]) for record in source_records}
        if len(scopes) != 1 or canonical_json(receipt["scope"]) not in scopes:
            raise GoalParticipantGraphError("admission receipt scope does not cover exactly the source relation scope")


def validate_source_payload(root: Path, source: dict[str, Any]) -> None:
    source_schema = read_json(root / SOURCE_SCHEMA_PATH)
    relation_schema = read_json(root / RELATION_SCHEMA_PATH)
    validate_instance(source, source_schema, SOURCE_PATH.as_posix(), root=root)
    _validate_currentness_provenance(source["currentness"], label=f"{SOURCE_PATH.as_posix()}.currentness")
    contract_path = root / CONTRACT_PATH
    contract = read_json(contract_path)
    if contract.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        raise GoalParticipantGraphError("participant relation contract has an unexpected schema_version")
    expected_contract_ref = current_contract_ref(root)
    expected_privacy_ref = current_privacy_policy_ref(root)
    if source["publisher_ref"] != expected_contract_ref:
        raise GoalParticipantGraphError("source publisher_ref is not the exact current contract reference")
    if source["relation_contract_ref"] != expected_contract_ref:
        raise GoalParticipantGraphError("source relation_contract_ref is not the exact current contract reference")
    if source["privacy_policy_ref"] != expected_privacy_ref:
        raise GoalParticipantGraphError("source privacy_policy_ref is not the exact current privacy-policy reference")
    if set(source["privacy_omissions"]) != REQUIRED_PRIVACY_OMISSIONS:
        raise GoalParticipantGraphError("source privacy omissions drifted from the contract baseline")
    pagination_errors = _currentness_and_pagination_errors(source, SOURCE_PATH.as_posix())
    if pagination_errors:
        raise GoalParticipantGraphError("; ".join(pagination_errors))
    admission_receipt = source["admission_receipt"]
    if source["evidence_class"] == "empty_deferred":
        if admission_receipt is not None:
            raise GoalParticipantGraphError("empty_deferred source cannot carry an admission receipt")
    else:
        if not source["records"]:
            raise GoalParticipantGraphError("owner_published source must contain at least one relation record")
        if admission_receipt is None:
            raise GoalParticipantGraphError("owner_published source requires an admission receipt")
        if any(record["evidence_class"] != "owner_published" for record in source["records"]):
            raise GoalParticipantGraphError("owner_published source cannot contain synthetic relation records")
        validate_admission_receipt(root, admission_receipt, source=source)
    relation_ids: set[str] = set()
    relation_keys: set[str] = set()
    for index, record in enumerate(source["records"]):
        label = f"{SOURCE_PATH.as_posix()}.records[{index}]"
        validate_relation(
            record,
            relation_schema=relation_schema,
            label=label,
            publisher_ref=source["publisher_ref"],
            root=root,
            require_key_digest=source["evidence_class"] == "owner_published",
            expected_privacy_policy_ref=expected_privacy_ref,
        )
        if set(record["privacy_omissions"]["omitted_fields"]) != set(source["privacy_omissions"]):
            raise GoalParticipantGraphError(f"{label}: relation privacy omissions do not match source policy")
        relation_id = record["relation_id"]
        if relation_id in relation_ids:
            raise GoalParticipantGraphError(f"{label}: duplicate relation_id {relation_id!r}")
        relation_ids.add(relation_id)
        if source["evidence_class"] == "owner_published":
            key_id = record["relation_key"]["key_id"]
            if key_id in relation_keys:
                raise GoalParticipantGraphError(f"{label}: duplicate publisher relation key")
            relation_keys.add(key_id)


def build_graph_payload(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    source = read_json(root / SOURCE_PATH)
    validate_source_payload(root, source)
    contract_ref = current_contract_ref(root)
    source_ref = current_source_ref(root)
    graph = {
        "schema_version": GRAPH_SCHEMA_VERSION,
        "kind": "aoa_agents_goal_participant_graph",
        "owner_repo": "aoa-agents",
        "source": {
            "source_ref": source_ref,
            "contract_ref": contract_ref,
            "admission_receipt": source["admission_receipt"],
        },
        "currentness": source["currentness"],
        "pagination": source["pagination"],
        "privacy_omissions": {
            "state": "applied",
            "omitted_fields": source["privacy_omissions"],
            "policy_ref": source["privacy_policy_ref"],
        },
        "fallback_policy": {
            "state": "disabled",
            "reason": "No display, participant, role, model, runtime, or evidence fallback is emitted.",
        },
        "records": source["records"],
        "claim_limit": (
            "This is an exact source-owned relation projection. Empty records or deferred currentness do not "
            "establish a live participant graph."
        ),
    }
    validate_graph_payload(root, graph)
    return graph


def validate_graph_payload(root: Path, graph: dict[str, Any]) -> None:
    root = root.resolve()
    graph_schema = read_json(root / GRAPH_SCHEMA_PATH)
    relation_schema = read_json(root / RELATION_SCHEMA_PATH)
    validate_instance(graph, graph_schema, GRAPH_PATH.as_posix(), root=root)
    validate_claim_limit(graph["claim_limit"], label="generated graph.claim_limit")
    _validate_currentness_provenance(graph["currentness"], label="generated graph.currentness")
    expected_contract = current_contract_ref(root)
    expected_source = current_source_ref(root)
    expected_privacy = current_privacy_policy_ref(root)
    if graph["source"]["contract_ref"] != expected_contract:
        raise GoalParticipantGraphError("generated graph contract_ref is not the exact current contract reference")
    if graph["source"]["source_ref"] != expected_source:
        raise GoalParticipantGraphError("generated graph source_ref is not the exact current source reference")
    validate_privacy_omissions(
        graph["privacy_omissions"],
        label="generated graph privacy_omissions",
        expected_policy_ref=expected_privacy,
    )

    records = graph["records"]
    receipt = graph["source"]["admission_receipt"]
    if not records:
        if receipt is not None:
            raise GoalParticipantGraphError("empty generated graph cannot carry an admission receipt")
        if graph["currentness"]["state"] != "deferred":
            raise GoalParticipantGraphError("empty generated graph without a receipt must remain deferred")
    else:
        if receipt is None:
            raise GoalParticipantGraphError("non-empty generated graph requires its admission receipt")
        if any(record["evidence_class"] != "owner_published" for record in records):
            raise GoalParticipantGraphError("non-empty generated graph cannot contain synthetic relation records")
        validate_admission_receipt(root, receipt)
        if receipt["publisher_ref"] != graph["source"]["contract_ref"]:
            raise GoalParticipantGraphError("graph admission receipt is not bound to graph contract_ref")
        if receipt["relation_ids"] != [record["relation_id"] for record in records]:
            raise GoalParticipantGraphError("graph admission receipt relation_ids do not match graph records")
        if receipt["payload_digest"] != publication_payload_digest(records):
            raise GoalParticipantGraphError("graph admission receipt payload_digest does not match graph records")
        if receipt["currentness"] != graph["currentness"]:
            raise GoalParticipantGraphError("graph admission receipt currentness does not match graph")
        if receipt["pagination"] != graph["pagination"]:
            raise GoalParticipantGraphError("graph admission receipt pagination does not match graph")
        if set(receipt["privacy_omissions"]) != set(graph["privacy_omissions"]["omitted_fields"]):
            raise GoalParticipantGraphError("graph admission receipt privacy omissions do not match graph policy")
        scopes = {canonical_json(record["scope"]) for record in records}
        if len(scopes) != 1 or canonical_json(receipt["scope"]) not in scopes:
            raise GoalParticipantGraphError("graph admission receipt scope does not cover exactly one graph scope")

    relation_ids: set[str] = set()
    relation_keys: set[str] = set()
    for index, record in enumerate(records):
        label = f"{GRAPH_PATH.as_posix()}.records[{index}]"
        validate_relation(
            record,
            relation_schema=relation_schema,
            label=label,
            publisher_ref=expected_contract,
            root=root,
            require_key_digest=record["evidence_class"] == "owner_published",
            expected_privacy_policy_ref=expected_privacy,
        )
        if set(record["privacy_omissions"]["omitted_fields"]) != set(graph["privacy_omissions"]["omitted_fields"]):
            raise GoalParticipantGraphError(f"{label}: relation privacy omissions do not match graph policy")
        relation_id = record["relation_id"]
        if relation_id in relation_ids:
            raise GoalParticipantGraphError(f"{label}: duplicate relation_id {relation_id!r}")
        relation_ids.add(relation_id)
        if record["evidence_class"] == "owner_published":
            key_id = record["relation_key"]["key_id"]
            if key_id in relation_keys:
                raise GoalParticipantGraphError(f"{label}: duplicate publisher relation key")
            relation_keys.add(key_id)


def check_generated(root: Path, output: Path) -> None:
    expected = compact_json(build_graph_payload(root))
    try:
        actual = output.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise GoalParticipantGraphError(f"missing generated reader: {output}") from exc
    if actual != expected:
        try:
            display_path = output.relative_to(root).as_posix()
        except ValueError:
            display_path = output.as_posix()
        raise GoalParticipantGraphError(f"generated reader is stale: {display_path}")


def display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the aoa-agents Goal participant graph reader.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.out if args.out is not None else root / GRAPH_PATH
    if not output.is_absolute():
        output = root / output
    try:
        if args.check:
            check_generated(root, output)
            print(f"Goal participant graph is current: {display_path(root, output)}")
        else:
            payload = build_graph_payload(root)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(compact_json(payload), encoding="utf-8")
            print(
                "Wrote Goal participant graph: "
                f"{display_path(root, output)} records={len(payload['records'])}"
            )
    except GoalParticipantGraphError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
