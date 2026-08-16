#!/usr/bin/env python3
"""Validate one summon-request-v4 and resolve its local classification.

This is a passive owner-local admission check.  It does not select a lane,
inspect a runtime, or launch a child.  A Codex-local request must carry the
exact classification artifact that produced its content reference; the
artifact is loaded, schema-checked, digest-checked, and bound to the request's
goal, child duty, and return holder before a local lane is considered.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Mapping

from jsonschema import Draft202012Validator


SUMMON_ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = SUMMON_ROOT / "references" / "summon-request-v4.schema.json"
CLASSIFICATION_SCHEMA = (
    SUMMON_ROOT.parent
    / "aoa-agents-skills"
    / "references"
    / "responsibility-classification-v1.schema.json"
)
ZERO_DIGEST = "sha256:" + "0" * 64


class SummonRequestError(ValueError):
    """The request or one required owner artifact is not admissible."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def semantic_digest(payload: Mapping[str, Any], field: str) -> str:
    return digest_bytes(canonical_bytes(dict(payload) | {field: ZERO_DIGEST}))


def request_digest(payload: Mapping[str, Any]) -> str:
    candidate = dict(payload)
    candidate.pop("request_digest", None)
    return digest_bytes(canonical_bytes(candidate))


def child_scope_digest(request: Mapping[str, Any]) -> str:
    """Digest the complete local-child duty subject carried by the request."""

    summon = request.get("summon_request")
    if not isinstance(summon, Mapping):
        raise SummonRequestError("summon_request is missing")
    subject = {
        "desired_role": summon.get("desired_role"),
        "expected_outputs": request.get("expected_outputs"),
        "intent": request.get("intent"),
        "child_scope": request.get("child_scope"),
        "child_stop_line": request.get("child_stop_line"),
        "child_inputs": request.get("child_inputs"),
    }
    return digest_bytes(canonical_bytes(subject))


def _load_exact(path: Path, *, label: str) -> tuple[bytes, dict[str, Any]]:
    location = path.resolve()
    if path.is_symlink() or not location.is_file():
        raise SummonRequestError(
            f"{label} must be an exact regular non-symlink file: {path}"
        )
    try:
        raw = location.read_bytes()
        payload = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SummonRequestError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise SummonRequestError(f"{label} must be a JSON object: {path}")
    return raw, payload


def _validate_schema(
    payload: Mapping[str, Any], schema_path: Path, *, label: str
) -> None:
    try:
        schema = json.loads(schema_path.resolve(strict=True).read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SummonRequestError(f"{label} schema is unavailable") from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path)
        where = f" at {path}" if path else ""
        raise SummonRequestError(
            f"{label} violates {schema_path.name}{where}: {errors[0].message}"
        )


def _classification_path(request_path: Path, value: str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = request_path.parent / candidate
    return candidate


def _validate_local_classification(
    request_path: Path, request: Mapping[str, Any]
) -> dict[str, Any]:
    envelope = request.get("responsibility_classification")
    if not isinstance(envelope, Mapping):
        raise SummonRequestError(
            "codex_local request is missing responsibility_classification"
        )
    artifact_path = envelope.get("artifact_path")
    if not isinstance(artifact_path, str) or not artifact_path:
        raise SummonRequestError(
            "responsibility classification artifact_path is missing"
        )
    raw, classification = _load_exact(
        _classification_path(request_path, artifact_path),
        label="responsibility classification",
    )
    _validate_schema(
        classification,
        CLASSIFICATION_SCHEMA,
        label="responsibility classification",
    )
    expected_digest = semantic_digest(classification, "classification_digest")
    if classification["classification_digest"] != expected_digest:
        raise SummonRequestError(
            "responsibility classification semantic digest mismatch"
        )

    result_ref = envelope.get("result_ref")
    if not isinstance(result_ref, Mapping):
        raise SummonRequestError("responsibility classification result_ref is missing")
    expected_ref = {
        "object_id": classification["classification_id"],
        "owner_repo": "aoa-agents",
        "schema_version": "responsibility-classification-v1",
        "digest": classification["classification_digest"],
    }
    if dict(result_ref) != expected_ref:
        raise SummonRequestError(
            "responsibility classification result_ref does not bind the exact artifact"
        )
    if envelope.get("disposition") != classification["disposition"]:
        raise SummonRequestError(
            "responsibility classification disposition differs from the artifact"
        )
    for field in ("goal_ref", "current_holder_ref", "child_scope_digest"):
        if envelope.get(field) != classification[field]:
            raise SummonRequestError(
                f"responsibility classification {field} differs from the artifact"
            )

    summon = request.get("summon_request")
    if not isinstance(summon, Mapping):
        raise SummonRequestError("summon_request is missing")
    passport = request.get("quest_passport")
    if not isinstance(passport, Mapping):
        raise SummonRequestError("quest_passport is missing")
    if passport.get("route_anchor") != classification["goal_ref"]["object_id"]:
        raise SummonRequestError(
            "responsibility classification goal is not bound to quest_passport.route_anchor"
        )
    if summon.get("parent_task_id") != classification["goal_ref"]["object_id"]:
        raise SummonRequestError(
            "responsibility classification goal is not bound to parent_task_id"
        )
    if request.get("return_owner") != classification["current_holder_ref"]["object_id"]:
        raise SummonRequestError(
            "responsibility classification holder is not bound to return_owner"
        )
    expected_child_scope_digest = child_scope_digest(request)
    if classification["child_scope_digest"] != expected_child_scope_digest:
        raise SummonRequestError(
            "responsibility classification child_scope_digest is not bound to the request"
        )
    return {
        "artifact_path": str(_classification_path(request_path, artifact_path).resolve()),
        "artifact_digest": digest_bytes(raw),
        "classification_ref": expected_ref,
        "child_scope_digest": expected_child_scope_digest,
    }


def validate_request(request_path: Path) -> dict[str, Any]:
    raw, request = _load_exact(request_path, label="summon request")
    _validate_schema(request, REQUEST_SCHEMA, label="summon request")
    expected_request_digest = request_digest(request)
    if request.get("request_digest") != expected_request_digest:
        raise SummonRequestError("summon request digest mismatch")
    transport = request["summon_request"]["transport_preference"]
    if transport == "codex_local":
        classification = _validate_local_classification(request_path, request)
    elif transport == "external_cli":
        if "responsibility_classification" in request:
            raise SummonRequestError(
                "external_cli request must not carry a local responsibility classification"
            )
        classification = None
    else:  # The v4 schema should already reject this; keep the guard explicit.
        raise SummonRequestError(
            "unresolved SDK transport cannot enter aoa-summon; resolve it first"
        )
    return {
        "request_digest": expected_request_digest,
        "request_artifact_digest": digest_bytes(raw),
        "transport_preference": transport,
        "classification": classification,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate_request(args.request)
    except (OSError, SummonRequestError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
