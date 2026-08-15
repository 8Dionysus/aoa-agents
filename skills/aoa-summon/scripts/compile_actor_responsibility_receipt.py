#!/usr/bin/env python3
"""Compile one owner-valid summon-result-v4 into a stats receipt envelope.

This is a passive aoa-agents adapter.  It consumes one exact result artifact
and explicit observation coordinates, validates the owner result and the local
payload contract, and emits no runtime, stats, proof, or acceptance artifact.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from jsonschema import Draft202012Validator


SUMMON_ROOT = Path(__file__).resolve().parents[1]
RESULT_SCHEMA = SUMMON_ROOT / "references" / "summon-result-v4.schema.json"
PAYLOAD_SCHEMA = (
    SUMMON_ROOT / "references" / "actor-responsibility-execution-receipt.schema.json"
)
ACTOR_ENVELOPE_SCHEMA_VERSION = "abyss_stack_external_codex_actor_input_envelope_v1"
RESULT_SCHEMA_VERSION = "urn:aoa-agents:aoa-summon:result:v4"
PAYLOAD_SCHEMA_VERSION = "aoa_actor_responsibility_execution_receipt_v1"
EVENT_KIND = "actor_responsibility_execution_receipt"
EVENT_ID_PREFIX = "actor-responsibility-execution:"
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)

REF_SPECS = {
    "role_resolution_ref": ("aoa-agents", "aoa_role_resolution_v1"),
    "model_fit_query_result_ref": (
        "aoa-models",
        "aoa_model_fit_query_result_v2",
    ),
    "model_fit_projection_ref": ("aoa-models", "aoa_model_fit_projection_v1"),
    "model_realization_ref": ("aoa-models", "aoa_model_realization_v1"),
    "run_plan_ref": ("aoa-sdk", "aoa_control_plane_v1"),
    "incarnation_binding_ref": ("aoa-sdk", "aoa_agent_incarnation_binding_v2"),
    "sdk_summon_request_ref": (
        "aoa-sdk",
        "urn:aoa-sdk:a2a:summon-request:v4",
    ),
    "sdk_summon_decision_ref": (
        "aoa-sdk",
        "urn:aoa-sdk:a2a:summon-result:v4",
    ),
    "runtime_profile_ref": (
        "abyss-stack",
        "abyss_stack_external_codex_runtime_profile_v2",
    ),
    "runtime_result_ref": (
        "abyss-stack",
        "abyss_stack_external_codex_result_v2",
    ),
    "runtime_a2a_return_ref": (
        "abyss-stack",
        "abyss_stack_external_codex_a2a_return_v1",
    ),
    "usage_observation_ref": (
        "abyss-stack",
        "abyss_stack_external_codex_usage_observation_v1",
    ),
}


class ActorResponsibilityReceiptError(ValueError):
    """A supplied owner result or observation input is not admissible."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ActorResponsibilityReceiptError(message)


def _require_string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{label} must be non-empty")
    return value


def _require_digest(value: Any, label: str) -> str:
    _require(isinstance(value, str) and DIGEST_RE.fullmatch(value) is not None, f"{label} is invalid")
    return value


def _require_ref(
    value: Any,
    *,
    label: str,
    owner_repo: str,
    schema_version: str,
) -> dict[str, str]:
    _require(isinstance(value, Mapping), f"{label} is absent")
    _require(set(value) == {"object_id", "owner_repo", "schema_version", "digest"}, f"{label} shape is invalid")
    result = {field: value[field] for field in ("object_id", "owner_repo", "schema_version", "digest")}
    _require_string(result["object_id"], f"{label}.object_id")
    _require(result["owner_repo"] == owner_repo, f"{label}.owner_repo is not {owner_repo!r}")
    _require(result["schema_version"] == schema_version, f"{label}.schema_version is not {schema_version!r}")
    _require_digest(result["digest"], f"{label}.digest")
    return result


def _validate_document(document: Mapping[str, Any], schema_path: Path, label: str) -> None:
    try:
        schema = json.loads(schema_path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ActorResponsibilityReceiptError(f"{label} schema is unavailable") from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message),
    )
    if errors:
        error = errors[0]
        path = ".".join(str(part) for part in error.absolute_path)
        where = f" at {path}" if path else ""
        raise ActorResponsibilityReceiptError(f"{label} schema violation{where}: {error.message}")


def _load_result(path: Path) -> tuple[bytes, dict[str, Any], str]:
    location = path.resolve()
    _require(not path.is_symlink() and location.is_file(), f"summon result must be a regular file: {path}")
    try:
        raw = location.read_bytes()
        document = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ActorResponsibilityReceiptError("summon result is not valid JSON") from exc
    _require(isinstance(document, dict), "summon result must be a JSON object")
    if document.get("schema_version") == ACTOR_ENVELOPE_SCHEMA_VERSION:
        _require(
            set(document)
            == {
                "$schema",
                "schema_version",
                "input_id",
                "payload_kind",
                "source_artifact_digest",
                "source_schema_ref",
                "source_schema_version",
                "payload",
            },
            "actor input envelope shape is invalid",
        )
        _require(
            document.get("$schema") == "schemas/external-codex-actor-input-envelope.schema.json",
            "actor input envelope schema ref is invalid",
        )
        _require(document.get("payload_kind") == "json", "actor input envelope payload kind is invalid")
        _require_string(document.get("input_id"), "actor input envelope input_id")
        _require_string(document.get("source_schema_ref"), "actor input envelope source_schema_ref")
        _require(document.get("source_schema_version") == RESULT_SCHEMA_VERSION, "actor input envelope source schema version is invalid")
        _require_digest(document.get("source_artifact_digest"), "actor input envelope source_artifact_digest")
        payload = document.get("payload")
        _require(isinstance(payload, dict), "actor input envelope payload must be an object")
        _require(payload.get("schema_version") == RESULT_SCHEMA_VERSION, "actor input envelope payload schema version is invalid")
        return raw, payload, digest_bytes(raw)
    _require(document.get("schema_version") == RESULT_SCHEMA_VERSION, "summon result schema version is invalid")
    return raw, document, digest_bytes(raw)


def _validate_observed_at(value: Any) -> str:
    observed_at = _require_string(value, "observed_at")
    _require(RFC3339_RE.fullmatch(observed_at) is not None, "observed_at must be RFC3339 with an explicit UTC offset")
    normalized = observed_at[:-1] + "+00:00" if observed_at[-1:].lower() == "z" else observed_at
    normalized = normalized.replace("t", "T", 1)
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ActorResponsibilityReceiptError("observed_at is not a valid date-time") from exc
    _require(parsed.tzinfo is not None and parsed.utcoffset() is not None, "observed_at must include a UTC offset")
    return observed_at


def _validate_object_ref(value: Any) -> dict[str, str]:
    _require(isinstance(value, Mapping), "object_ref is absent")
    _require(set(value) <= {"repo", "kind", "id", "version"}, "object_ref has unsupported fields")
    for field in ("repo", "kind", "id"):
        _require_string(value.get(field), f"object_ref.{field}")
    result = {field: value[field] for field in ("repo", "kind", "id")}
    if "version" in value:
        result["version"] = _require_string(value["version"], "object_ref.version")
    return result


def _validate_result(result: Mapping[str, Any]) -> None:
    _validate_document(result, RESULT_SCHEMA, "summon-result-v4")
    required = {
        "allowed",
        "lane",
        "execution_surface",
        "cohort_pattern",
        "closeout_required",
        "decision_state",
        "binding",
        "runtime_state",
        "return_validation",
        "closeout_handoff",
        "actual_effects",
        "stop_line",
        "request_ref",
        "request_digest",
        "request_intent",
    }
    _require(required <= set(result), "summon-result-v4 is missing required owner fields")
    _require(result["lane"] == "external_cli_reviewed", "only external_cli_reviewed results are admissible")
    _require(result["request_intent"] == "execute", "a decision-only summon result is not an execution receipt")
    _require(result["runtime_state"].get("state") in {"launched", "running", "returned", "accepted", "failed"}, "summon result has no executable runtime state")
    _require(isinstance(result["actual_effects"], list), "summon result actual_effects is invalid")
    _require("external-actor-runtime" in result["actual_effects"], "summon result does not carry external-actor-runtime")
    _require(result["binding"].get("inspected") is True, "summon result binding was not inspected")
    _require(result["binding"].get("available") is True, "summon result binding is not available")
    _require(result["binding"].get("uses_builtin_codex_subagents") is False, "summon result uses built-in Codex subagents")
    _require(result["binding"].get("binding_kind") == "external_cli_incarnation", "summon result binding kind is not external_cli_incarnation")
    for field, (owner_repo, schema_version) in REF_SPECS.items():
        if field in {"model_realization_ref", "run_plan_ref"} and field not in result["binding"]:
            continue
        if field in {"runtime_result_ref", "runtime_a2a_return_ref", "usage_observation_ref"}:
            continue
        _require_ref(result["binding"].get(field), label=f"binding.{field}", owner_repo=owner_repo, schema_version=schema_version)
    runtime_state = result["runtime_state"]
    state = runtime_state["state"]
    required_runtime_refs = {
        "returned": {"runtime_result_ref", "runtime_a2a_return_ref", "usage_observation_ref"},
        "accepted": {"runtime_result_ref", "runtime_a2a_return_ref", "usage_observation_ref"},
        "failed": {"runtime_result_ref", "usage_observation_ref"},
    }.get(state, set())
    for field in ("actor_handle", "process_handle", "session_handle", "continuation_handle"):
        _require_string(runtime_state.get(field), f"runtime_state.{field}")
    for field in ("runtime_result_ref", "runtime_a2a_return_ref", "usage_observation_ref"):
        owner_repo, schema_version = REF_SPECS[field]
        value = runtime_state.get(field)
        if field in required_runtime_refs or value is not None:
            _require_ref(value, label=f"runtime_state.{field}", owner_repo=owner_repo, schema_version=schema_version)
    _require_string(result["request_ref"], "request_ref")
    _require_digest(result["request_digest"], "request_digest")
    _require(isinstance(result["return_validation"], Mapping), "return_validation is invalid")
    _require(isinstance(result["return_validation"].get("output_checks"), Mapping), "return_validation.output_checks is invalid")
    _require(isinstance(result["closeout_handoff"], Mapping), "closeout_handoff is invalid")
    for field in ("parent_owner", "residual_risk", "next_route"):
        _require(field in result["closeout_handoff"], f"closeout_handoff.{field} is absent")
    _require_string(result["stop_line"], "stop_line")


def _copy_binding(result: Mapping[str, Any]) -> dict[str, Any]:
    source = result["binding"]
    fields = (
        "interface",
        "inspected",
        "available",
        "reason",
        "binding_kind",
        "runtime_owner",
        "role_resolution_ref",
        "model_fit_query_result_ref",
        "model_fit_projection_ref",
        "model_realization_ref",
        "run_plan_ref",
        "incarnation_binding_ref",
        "sdk_summon_request_ref",
        "sdk_summon_decision_ref",
        "runtime_profile_ref",
        "uses_builtin_codex_subagents",
    )
    return {field: source[field] for field in fields if field in source}


def _copy_runtime_state(result: Mapping[str, Any]) -> dict[str, Any]:
    source = result["runtime_state"]
    return {
        field: source[field]
        for field in (
            "state",
            "actor_handle",
            "process_handle",
            "session_handle",
            "continuation_handle",
            "runtime_result_ref",
            "runtime_a2a_return_ref",
            "usage_observation_ref",
        )
        if field in source and source[field] is not None
    }


def _identity_digest(
    *,
    result_digest: str,
    observed_at: str,
    run_ref: str,
    session_ref: str,
    actor_ref: str,
    object_ref: Mapping[str, str],
) -> str:
    identity = {
        "result_digest": result_digest,
        "observed_at": observed_at,
        "run_ref": run_ref,
        "session_ref": session_ref,
        "actor_ref": actor_ref,
        "object_ref": dict(object_ref),
    }
    return digest_bytes(canonical_bytes(identity))


def _evidence_refs(payload: Mapping[str, Any]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = [
        {"kind": "aoa-summon-result-v4", "ref": payload["source_result"]["artifact_ref"], "role": "source-result"}
    ]
    binding = payload["owner_evidence"]["binding"]
    for field, role in (
        ("role_resolution_ref", "role-resolution"),
        ("model_fit_query_result_ref", "model-fit-query"),
        ("model_fit_projection_ref", "model-fit-projection"),
        ("model_realization_ref", "model-realization"),
        ("run_plan_ref", "run-plan"),
        ("incarnation_binding_ref", "incarnation-binding"),
        ("sdk_summon_request_ref", "sdk-summon-request"),
        ("sdk_summon_decision_ref", "sdk-summon-decision"),
        ("runtime_profile_ref", "runtime-profile"),
    ):
        if field in binding:
            result.append({"kind": field, "ref": binding[field]["object_id"], "role": role})
    runtime_state = payload["owner_evidence"]["runtime_state"]
    for field, role in (
        ("runtime_result_ref", "runtime-result"),
        ("runtime_a2a_return_ref", "runtime-a2a-return"),
        ("usage_observation_ref", "usage-observation"),
    ):
        if field in runtime_state:
            result.append({"kind": field, "ref": runtime_state[field]["object_id"], "role": role})
    return result


def compile_actor_responsibility_receipt(
    *,
    summon_result_path: Path,
    observed_at: str,
    run_ref: str,
    session_ref: str,
    actor_ref: str,
    object_ref: Mapping[str, str],
    event_id: str | None = None,
    expected_result_digest: str | None = None,
) -> dict[str, Any]:
    """Compile one deterministic actor responsibility receipt envelope."""

    _raw, result, result_digest = _load_result(summon_result_path)
    _validate_result(result)
    observed_at = _validate_observed_at(observed_at)
    run_ref = _require_string(run_ref, "run_ref")
    session_ref = _require_string(session_ref, "session_ref")
    actor_ref = _require_string(actor_ref, "actor_ref")
    object_ref = _validate_object_ref(object_ref)
    if expected_result_digest is not None:
        _require_digest(expected_result_digest, "expected_result_digest")
        _require(expected_result_digest == result_digest, "summon result digest does not match expected_result_digest")

    identity_digest = _identity_digest(
        result_digest=result_digest,
        observed_at=observed_at,
        run_ref=run_ref,
        session_ref=session_ref,
        actor_ref=actor_ref,
        object_ref=object_ref,
    )
    derived_event_id = EVENT_ID_PREFIX + identity_digest.removeprefix("sha256:")
    if event_id is not None:
        _require(event_id == derived_event_id, "event_id does not match deterministic owner evidence identity")

    execution = {
        field: result[field]
        for field in (
            "allowed",
            "lane",
            "execution_surface",
            "cohort_pattern",
            "decision_state",
            "request_intent",
            "closeout_required",
            "checkpoint_required",
            "progression_required",
            "requested_posture",
            "owner_publication_plan",
            "stop_line",
        )
    }
    execution.update(
        {
            "runtime_state": result["runtime_state"]["state"],
            "actual_effects": result["actual_effects"],
            "blocked_actions": result.get("blocked_actions", []),
            "reason_codes": result.get("reason_codes", []),
        }
    )
    payload: dict[str, Any] = {
        "schema_version": PAYLOAD_SCHEMA_VERSION,
        "source_result": {
            "owner_repo": "aoa-agents",
            "artifact_ref": result["request_ref"],
            "artifact_digest": result_digest,
            "schema_version": RESULT_SCHEMA_VERSION,
            "request_ref": result["request_ref"],
            "request_digest": result["request_digest"],
        },
        "execution": execution,
        "owner_evidence": {
            "binding": _copy_binding(result),
            "runtime_state": _copy_runtime_state(result),
            "return_validation": result["return_validation"],
            "closeout_handoff": result["closeout_handoff"],
        },
        "authority_posture": {
            "benefit": "not_inferred",
            "model_fit": "not_inferred",
            "task_success": "not_inferred",
            "proof": "not_inferred",
            "review_approval": "not_inferred",
            "owner_acceptance": "not_claimed",
            "publication": "not_claimed",
        },
    }
    _validate_document(payload, PAYLOAD_SCHEMA, "actor responsibility receipt payload")
    envelope = {
        "event_kind": EVENT_KIND,
        "event_id": derived_event_id,
        "observed_at": observed_at,
        "run_ref": run_ref,
        "session_ref": session_ref,
        "actor_ref": actor_ref,
        "object_ref": object_ref,
        "evidence_refs": _evidence_refs(payload),
        "payload": payload,
    }
    validate_receipt(envelope)
    return envelope


def validate_receipt(envelope: Mapping[str, Any]) -> None:
    """Validate the local envelope shape and the owner payload contract."""

    _require(isinstance(envelope, Mapping), "receipt envelope must be an object")
    _require(
        set(envelope) == {
            "event_kind",
            "event_id",
            "observed_at",
            "run_ref",
            "session_ref",
            "actor_ref",
            "object_ref",
            "evidence_refs",
            "payload",
        },
        "receipt envelope has unsupported or missing fields",
    )
    _require(envelope["event_kind"] == EVENT_KIND, "receipt event_kind is not actor_responsibility_execution_receipt")
    _require_string(envelope["event_id"], "event_id")
    _validate_observed_at(envelope["observed_at"])
    for field in ("run_ref", "session_ref", "actor_ref"):
        _require_string(envelope[field], field)
    _validate_object_ref(envelope["object_ref"])
    _require(isinstance(envelope["evidence_refs"], list) and bool(envelope["evidence_refs"]), "evidence_refs must be non-empty")
    for index, evidence in enumerate(envelope["evidence_refs"]):
        _require(isinstance(evidence, Mapping), f"evidence_refs[{index}] must be an object")
        _require(set(evidence) <= {"kind", "ref", "role"}, f"evidence_refs[{index}] has unsupported fields")
        _require_string(evidence.get("kind"), f"evidence_refs[{index}].kind")
        _require_string(evidence.get("ref"), f"evidence_refs[{index}].ref")
        if "role" in evidence:
            _require_string(evidence["role"], f"evidence_refs[{index}].role")
    _require(isinstance(envelope["payload"], Mapping), "receipt payload must be an object")
    _validate_document(envelope["payload"], PAYLOAD_SCHEMA, "actor responsibility receipt payload")
    _require(
        envelope["evidence_refs"] == _evidence_refs(envelope["payload"]),
        "evidence_refs do not match the owner evidence carried by the payload",
    )
    source_result = envelope["payload"]["source_result"]
    expected_event_id = EVENT_ID_PREFIX + _identity_digest(
        result_digest=source_result["artifact_digest"],
        observed_at=envelope["observed_at"],
        run_ref=envelope["run_ref"],
        session_ref=envelope["session_ref"],
        actor_ref=envelope["actor_ref"],
        object_ref=envelope["object_ref"],
    ).removeprefix("sha256:")
    _require(envelope["event_id"] == expected_event_id, "event_id does not match deterministic owner evidence identity")


def _parse_object_ref(raw: str) -> dict[str, str]:
    candidate: Any
    possible_path = Path(raw)
    if possible_path.is_file():
        try:
            candidate = json.loads(possible_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ActorResponsibilityReceiptError("object_ref file is not valid JSON") from exc
    else:
        try:
            candidate = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ActorResponsibilityReceiptError("object_ref must be JSON or a JSON file path") from exc
    return _validate_object_ref(candidate)


def _write_new(path: Path, payload: Mapping[str, Any]) -> None:
    location = path.resolve()
    _require(not path.is_symlink(), "output must not be a symlink")
    _require(not location.exists(), "output must be a new file")
    _require(location.parent.is_dir(), "output parent directory is absent")
    with location.open("xb") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--summon-result", "--result", "--input", dest="summon_result_path", type=Path, required=True)
    result.add_argument("--observed-at", required=True)
    result.add_argument("--run-ref", required=True)
    result.add_argument("--session-ref", required=True)
    result.add_argument("--actor-ref", required=True)
    result.add_argument("--object-ref", required=True, help="JSON object or path containing the explicit stats object_ref")
    result.add_argument("--event-id")
    result.add_argument("--expected-result-digest", "--result-digest")
    result.add_argument("--output", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        receipt = compile_actor_responsibility_receipt(
            summon_result_path=args.summon_result_path,
            observed_at=args.observed_at,
            run_ref=args.run_ref,
            session_ref=args.session_ref,
            actor_ref=args.actor_ref,
            object_ref=_parse_object_ref(args.object_ref),
            event_id=args.event_id,
            expected_result_digest=args.expected_result_digest,
        )
        _write_new(args.output, receipt)
    except (ActorResponsibilityReceiptError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(
        json.dumps(
            {
                "ok": True,
                "event_id": receipt["event_id"],
                "output": str(args.output.resolve()),
                "published": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
