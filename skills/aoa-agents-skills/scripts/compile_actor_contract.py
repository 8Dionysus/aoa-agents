#!/usr/bin/env python3
"""Compile semantically selected classification, obligation, and mandate packets.

The caller decides whether an obligation is independent, which role bears it,
and which model-fit task family describes it.  This compiler only validates
those decisions, binds exact inputs, and emits deterministic content-addressed
owner packets.  It never selects a role, model, runtime, or launch posture.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from jsonschema import Draft202012Validator


REFERENCES = Path(__file__).resolve().parents[1] / "references"
ZERO_DIGEST = "sha256:" + "0" * 64
OBLIGATION_SEMANTIC_FIELDS = {
    "obligation_id",
    "goal_ref",
    "phase",
    "duty",
    "domain_owner",
    "current_holder",
    "responsibility_boundary",
    "missed_consequence",
    "independence_findings",
    "trigger",
    "expected_outcomes",
    "return_owner",
    "lifecycle_posture",
    "stop_line",
    "evidence_refs",
    "uncertainty",
    "next_route",
}
CLASSIFICATION_SEMANTIC_FIELDS = {
    "classification_id",
    "goal_ref",
    "current_holder_ref",
    "reason",
    "stop_line",
    "evidence_refs",
}
MANDATE_SEMANTIC_FIELDS = {
    "mandate_id",
    "identity_posture",
    "domain_procedure_refs",
    "required_executor_properties",
    "model_fit_relation",
    "authority",
    "environment",
    "continuity",
    "named_outputs",
    "review_policy",
    "refusal_policy",
    "wake_policy",
    "review_after",
    "uncertainty",
}


class ActorContractError(ValueError):
    """A semantic packet or exact owner input is absent or contradictory."""


def _load_json(path: Path, *, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise ActorContractError(f"{label} is unavailable as a regular file: {path}")
    try:
        payload = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ActorContractError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ActorContractError(f"{label} must be a JSON object: {path}")
    return payload


def _schema(name: str) -> dict[str, Any]:
    return _load_json(REFERENCES / name, label=f"{name} schema")


def _validate(payload: dict[str, Any], schema_name: str, *, label: str) -> None:
    errors = sorted(
        Draft202012Validator(_schema(schema_name)).iter_errors(payload),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path)
        location = f" at {path}" if path else ""
        raise ActorContractError(
            f"{label} violates {schema_name}{location}: {errors[0].message}"
        )


def _canonical_digest(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def _assert_digest(payload: dict[str, Any], field: str, *, label: str) -> None:
    if field not in payload:
        raise ActorContractError(f"{label} has no {field}")
    expected = _canonical_digest(payload | {field: ZERO_DIGEST})
    if payload[field] != expected:
        raise ActorContractError(f"{label} digest mismatch: expected {expected}")


def _require_exact_fields(
    payload: dict[str, Any], expected: set[str], *, label: str
) -> None:
    present = set(payload)
    missing = sorted(expected - present)
    extra = sorted(present - expected)
    if missing or extra:
        raise ActorContractError(
            f"{label} fields differ: missing={missing or []}, extra={extra or []}"
        )


def _content_ref(
    *, object_id: str, owner_repo: str, schema_version: str, digest: str
) -> dict[str, str]:
    return {
        "object_id": object_id,
        "owner_repo": owner_repo,
        "schema_version": schema_version,
        "digest": digest,
    }


def compile_classification(semantic: dict[str, Any]) -> dict[str, Any]:
    """Bind one already-admitted ordinary-local classification."""

    _require_exact_fields(
        semantic,
        CLASSIFICATION_SEMANTIC_FIELDS,
        label="classification semantic input",
    )
    payload = {
        "schema_version": "responsibility-classification-v1",
        **semantic,
        "disposition": "not_independent",
        "next_route": "codex_local",
        "classification_digest": ZERO_DIGEST,
    }
    payload["classification_digest"] = _canonical_digest(payload)
    _validate(
        payload,
        "responsibility-classification-v1.schema.json",
        label="responsibility classification",
    )
    _assert_digest(
        payload,
        "classification_digest",
        label="responsibility classification",
    )
    return payload


def compile_obligation(semantic: dict[str, Any]) -> dict[str, Any]:
    """Bind one already-admitted semantic obligation without detecting it."""

    _require_exact_fields(
        semantic, OBLIGATION_SEMANTIC_FIELDS, label="obligation semantic input"
    )
    payload = {
        "schema_version": "agent-obligation-v1",
        **semantic,
        "obligation_digest": ZERO_DIGEST,
    }
    payload["obligation_digest"] = _canonical_digest(payload)
    _validate(payload, "agent-obligation-v1.schema.json", label="agent obligation")
    _assert_digest(payload, "obligation_digest", label="agent obligation")
    return payload


def _assert_unique_ids(items: object, *, field: str, identity: str, label: str) -> None:
    if not isinstance(items, list):
        return
    identities = [item.get(identity) for item in items if isinstance(item, dict)]
    if len(identities) != len(set(identities)):
        raise ActorContractError(f"{label} {field} identities must be unique")


def compile_mandate(
    obligation: dict[str, Any],
    role_resolution: dict[str, Any],
    semantic: dict[str, Any],
) -> dict[str, Any]:
    """Bind a chosen role and explicit duty-to-fit relation into one mandate."""

    _validate(obligation, "agent-obligation-v1.schema.json", label="agent obligation")
    _assert_digest(obligation, "obligation_digest", label="agent obligation")
    _validate(
        role_resolution,
        "role-resolution-v1.schema.json",
        label="role resolution",
    )
    _assert_digest(role_resolution, "resolution_digest", label="role resolution")
    _require_exact_fields(
        semantic, MANDATE_SEMANTIC_FIELDS, label="mandate semantic input"
    )

    if semantic["identity_posture"] != obligation["lifecycle_posture"]:
        raise ActorContractError(
            "mandate identity posture must preserve the obligation lifecycle posture"
        )
    continuity = semantic["continuity"]
    if (
        not isinstance(continuity, dict)
        or continuity.get("posture") != semantic["identity_posture"]
    ):
        raise ActorContractError(
            "continuity posture must match the mandate identity posture"
        )
    model_fit = semantic["model_fit_relation"]
    if (
        not isinstance(model_fit, dict)
        or model_fit.get("relation_authority_ref") != obligation["current_holder"]
    ):
        raise ActorContractError(
            "duty-to-model-fit relation must be authorized by the current obligation holder"
        )
    if semantic["authority"].get("stop_line") != obligation["stop_line"]:
        raise ActorContractError(
            "mandate stop line must preserve the admitted obligation stop line exactly"
        )
    _assert_unique_ids(
        semantic["required_executor_properties"],
        field="required_executor_properties",
        identity="property_id",
        label="mandate",
    )
    _assert_unique_ids(
        semantic["named_outputs"],
        field="named_outputs",
        identity="name",
        label="mandate",
    )

    payload: dict[str, Any] = {
        "schema_version": "actor-mandate-v1",
        "mandate_id": semantic["mandate_id"],
        "obligation_ref": _content_ref(
            object_id=obligation["obligation_id"],
            owner_repo="aoa-agents",
            schema_version="agent-obligation-v1",
            digest=obligation["obligation_digest"],
        ),
        "goal_ref": obligation["goal_ref"],
        "role_resolution_ref": _content_ref(
            object_id=role_resolution["resolution_id"],
            owner_repo="aoa-agents",
            schema_version="aoa_role_resolution_v1",
            digest=role_resolution["resolution_digest"],
        ),
        "role_binding": {
            "role_id": role_resolution["role_id"],
            "specialization_id": role_resolution["specialization_id"],
            "tier_id": role_resolution["tier_id"],
            "base_role_ref": role_resolution["base_role_ref"],
            "specialization_ref": role_resolution["specialization_ref"],
            "tier_ref": role_resolution["tier_ref"],
            "capability_pack_refs": role_resolution["capability_pack_refs"],
        },
        "identity_posture": semantic["identity_posture"],
        "domain_owner": obligation["domain_owner"],
        "domain_procedure_refs": semantic["domain_procedure_refs"],
        "required_executor_properties": semantic["required_executor_properties"],
        "model_fit_relation": model_fit,
        "authority": semantic["authority"],
        "environment": semantic["environment"],
        "continuity": continuity,
        "named_outputs": semantic["named_outputs"],
        "return_owner": obligation["return_owner"],
        "review_policy": semantic["review_policy"],
        "refusal_policy": semantic["refusal_policy"],
        "wake_policy": semantic["wake_policy"],
        "review_after": semantic["review_after"],
        "uncertainty": semantic["uncertainty"],
        "compiler_authority": {
            "obligation_detection_performed": False,
            "role_selection_performed": False,
            "model_selection_performed": False,
            "runtime_activation_performed": False,
        },
        "mandate_digest": ZERO_DIGEST,
    }
    payload["mandate_digest"] = _canonical_digest(payload)
    _validate(payload, "actor-mandate-v1.schema.json", label="actor mandate")
    _assert_digest(payload, "mandate_digest", label="actor mandate")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compile content-addressed aoa-agents obligation contracts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    classification_parser = subparsers.add_parser("classification")
    classification_parser.add_argument("--input", type=Path, required=True)
    obligation_parser = subparsers.add_parser("obligation")
    obligation_parser.add_argument("--input", type=Path, required=True)
    mandate_parser = subparsers.add_parser("mandate")
    mandate_parser.add_argument("--input", type=Path, required=True)
    mandate_parser.add_argument("--obligation", type=Path, required=True)
    mandate_parser.add_argument("--role-resolution", type=Path, required=True)
    args = parser.parse_args()

    try:
        semantic = _load_json(args.input, label=f"{args.command} semantic input")
        if args.command == "classification":
            result = compile_classification(semantic)
        elif args.command == "obligation":
            result = compile_obligation(semantic)
        else:
            result = compile_mandate(
                _load_json(args.obligation, label="agent obligation"),
                _load_json(args.role_resolution, label="role resolution"),
                semantic,
            )
    except (ActorContractError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
