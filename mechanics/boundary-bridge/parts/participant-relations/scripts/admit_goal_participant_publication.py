#!/usr/bin/env python3
"""Admit an explicit typed Goal participant publication without enrichment.

This module is a reusable fail-closed intake boundary.  It validates one
owner-published publication and returns a structural admission receipt.  It
does not discover Goal data, infer a participant, or publish the checked-in
source unless a caller explicitly supplies an output path.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_goal_participant_graph import (  # noqa: E402
    ADMISSION_SCHEMA_VERSION,
    PUBLICATION_SCHEMA_PATH,
    PUBLICATION_SCHEMA_VERSION,
    RELATION_SCHEMA_PATH,
    PRIVACY_OMISSION_FIELDS,
    ROOT,
    SOURCE_SCHEMA_VERSION,
    GoalParticipantGraphError,
    admission_receipt_id,
    canonical_json,
    compact_json,
    current_contract_ref,
    current_privacy_policy_ref,
    publication_payload_digest,
    read_json,
    validate_admission_receipt,
    validate_instance,
    validate_relation,
    validate_source_payload,
)


class GoalParticipantPublicationError(GoalParticipantGraphError):
    """Raised when an owner publication cannot be admitted."""


def validate_publication(root: Path, publication: dict[str, Any]) -> None:
    publication_schema = read_json(root / PUBLICATION_SCHEMA_PATH)
    relation_schema = read_json(root / RELATION_SCHEMA_PATH)
    validate_instance(publication, publication_schema, "Goal participant publication", root=root)
    expected_contract_ref = current_contract_ref(root)
    expected_privacy_ref = current_privacy_policy_ref(root)
    if publication["publisher_ref"] != expected_contract_ref:
        raise GoalParticipantPublicationError(
            "publication publisher_ref is not the exact current aoa-agents contract reference"
        )
    if publication["relation_contract_ref"] != expected_contract_ref:
        raise GoalParticipantPublicationError(
            "publication relation_contract_ref is not the exact current aoa-agents contract reference"
        )
    if publication["producer_ref"] == publication["publication_ref"]:
        raise GoalParticipantPublicationError("producer_ref and publication_ref must remain distinct")
    if publication["producer_ref"]["owner_repo"] != publication["publication_ref"]["owner_repo"]:
        raise GoalParticipantPublicationError("producer_ref and publication_ref must name one producer owner")
    if publication["currentness"]["state"] != "current":
        raise GoalParticipantPublicationError("only current owner publications can receive an admission receipt")
    if not publication["currentness"].get("observed_at"):
        raise GoalParticipantPublicationError("current publication requires currentness.observed_at")
    pagination = publication["pagination"]
    if pagination["has_more"] or pagination["next_cursor_ref"] is not None:
        raise GoalParticipantPublicationError(
            "an incomplete paginated publication remains deferred and cannot be admitted as current"
        )
    if set(publication["privacy_omissions"]) != set(PRIVACY_OMISSION_FIELDS):
        raise GoalParticipantPublicationError("publication privacy omissions drifted from the contract baseline")
    if publication["payload_digest"] != publication_payload_digest(publication["records"]):
        raise GoalParticipantPublicationError("publication payload_digest does not match canonical relation records")

    relation_ids: set[str] = set()
    relation_keys: set[str] = set()
    expected_scope = canonical_json(publication["scope"])
    for index, record in enumerate(publication["records"]):
        label = f"publication.records[{index}]"
        if record.get("evidence_class") != "owner_published":
            raise GoalParticipantPublicationError(f"{label}: synthetic or unknown evidence cannot be admitted")
        validate_relation(
            record,
            relation_schema=relation_schema,
            label=label,
            publisher_ref=expected_contract_ref,
            require_key_digest=True,
            expected_privacy_policy_ref=expected_privacy_ref,
        )
        if set(record["privacy_omissions"]["omitted_fields"]) != set(publication["privacy_omissions"]):
            raise GoalParticipantPublicationError(f"{label}: relation privacy omissions do not match publication policy")
        if canonical_json(record["scope"]) != expected_scope:
            raise GoalParticipantPublicationError(f"{label}: record scope does not match the one publication scope")
        if record["relation_id"] in relation_ids:
            raise GoalParticipantPublicationError(f"{label}: duplicate relation_id")
        relation_ids.add(record["relation_id"])
        key_id = record["relation_key"]["key_id"]
        if key_id in relation_keys:
            raise GoalParticipantPublicationError(f"{label}: duplicate publisher relation key")
        relation_keys.add(key_id)


def build_admission_receipt(root: Path, publication: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    validate_publication(root, publication)
    receipt = {
        "schema_version": ADMISSION_SCHEMA_VERSION,
        "kind": "aoa_agents_goal_participant_relation_admission",
        "admission_state": "admitted",
        "publisher_ref": publication["publisher_ref"],
        "producer_ref": publication["producer_ref"],
        "publication_ref": publication["publication_ref"],
        "publication_schema_version": PUBLICATION_SCHEMA_VERSION,
        "payload_digest": publication["payload_digest"],
        "scope": publication["scope"],
        "relation_ids": [record["relation_id"] for record in publication["records"]],
        "currentness": publication["currentness"],
        "pagination": publication["pagination"],
        "privacy_omissions": publication["privacy_omissions"],
        "claim_limit": (
            "Structural admission of one exact owner publication. This receipt does not prove owner truth, "
            "live presence, runtime health, wake, acceptance, or Goal completion."
        ),
    }
    receipt["receipt_id"] = admission_receipt_id(receipt)
    validate_admission_receipt(root, receipt, publication=publication)
    return receipt


def build_source_payload(root: Path, publication: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    receipt = build_admission_receipt(root, publication)
    contract_ref = current_contract_ref(root)
    source = {
        "schema_version": SOURCE_SCHEMA_VERSION,
        "kind": "aoa_agents_goal_participant_relation_source",
        "owner_repo": "aoa-agents",
        "evidence_class": "owner_published",
        "publisher_ref": contract_ref,
        "relation_contract_ref": contract_ref,
        "currentness": publication["currentness"],
        "pagination": publication["pagination"],
        "privacy_policy_ref": current_privacy_policy_ref(root),
        "privacy_omissions": publication["privacy_omissions"],
        "admission_receipt": receipt,
        "records": publication["records"],
    }
    validate_source_payload(root, source)
    return source


def _load_publication(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise GoalParticipantPublicationError("publication input must be a regular non-symlink file")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GoalParticipantPublicationError("publication input is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise GoalParticipantPublicationError("publication input must be a JSON object")
    return payload


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    if path.exists() and path.is_symlink():
        raise GoalParticipantPublicationError("publication output must not be a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(compact_json(payload))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--out-source",
        type=Path,
        default=None,
        help="optional explicit source output; omitted means validate and emit only the receipt",
    )
    args = parser.parse_args()
    try:
        publication = _load_publication(args.input)
        receipt = build_admission_receipt(args.root, publication)
        if args.out_source is not None:
            _atomic_write(args.out_source, build_source_payload(args.root, publication))
        print(compact_json(receipt), end="")
    except GoalParticipantGraphError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
