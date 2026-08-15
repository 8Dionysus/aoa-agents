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
RUNTIME_RESULT_SCHEMA_VERSION = "abyss_stack_external_codex_result_v2"
USAGE_PROJECTION_SCHEMA_VERSION = "aoa_actor_usage_observation_projection_v1"
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


def _compact_source_strings(value: Any, label: str) -> list[str]:
    """Project source string arrays into the receipt's compact form."""

    _require(isinstance(value, list), f"{label} must be an array")
    compacted: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        _require(isinstance(item, str), f"{label}[{index}] must be a string")
        if not item or item in seen:
            continue
        seen.add(item)
        compacted.append(item)
    return compacted


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


def _load_runtime_result(
    path: Path,
    *,
    runtime_result_ref: Mapping[str, Any],
    expected_digest: str | None,
    expected_task_id: str | None = None,
) -> dict[str, Any]:
    """Load the exact runtime bytes named by the accepted owner receipt."""

    location = path.resolve()
    _require(
        not path.is_symlink() and location.is_file(),
        f"runtime result must be a regular file: {path}",
    )
    try:
        raw = location.read_bytes()
        document = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ActorResponsibilityReceiptError("runtime result is not valid JSON") from exc
    _require(isinstance(document, dict), "runtime result must be a JSON object")
    runtime_digest = digest_bytes(raw)
    _require(
        runtime_digest == runtime_result_ref["digest"],
        "runtime result bytes do not match owner runtime_result_ref.digest",
    )
    if expected_digest is not None:
        _require_digest(expected_digest, "expected_runtime_result_digest")
        _require(
            expected_digest == runtime_digest,
            "runtime result digest does not match expected_runtime_result_digest",
        )
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
            "runtime actor input envelope shape is invalid",
        )
        _require(
            document.get("$schema") == "schemas/external-codex-actor-input-envelope.schema.json",
            "runtime actor input envelope schema ref is invalid",
        )
        _require(document.get("payload_kind") == "json", "runtime actor input envelope payload kind is invalid")
        _require_string(document.get("input_id"), "runtime actor input envelope input_id")
        _require_string(document.get("source_schema_ref"), "runtime actor input envelope source_schema_ref")
        _require(
            document.get("source_schema_version") == RUNTIME_RESULT_SCHEMA_VERSION,
            "runtime actor input envelope source schema version is invalid",
        )
        _require_digest(
            document.get("source_artifact_digest"),
            "runtime actor input envelope source_artifact_digest",
        )
        payload = document.get("payload")
        _require(isinstance(payload, dict), "runtime actor input envelope payload must be an object")
        document = payload
    _require(
        document.get("schema_version") == RUNTIME_RESULT_SCHEMA_VERSION,
        "runtime result schema version is not abyss_stack_external_codex_result_v2",
    )
    task_id = _require_string(document.get("task_id"), "runtime result task_id")
    if expected_task_id is not None:
        _require(
            task_id == expected_task_id,
            "runtime result task_id does not match owner runtime_a2a_return_ref.object_id",
        )
    result_id = document.get("result_id")
    if result_id is not None:
        _require_string(result_id, "runtime result result_id")
        _require(
            result_id == runtime_result_ref["object_id"],
            "runtime result result_id does not match owner runtime_result_ref.object_id",
        )
    else:
        _require(
            task_id == runtime_result_ref["object_id"],
            "runtime result task_id does not match owner runtime_result_ref.object_id",
        )
    return document


def _require_nonnegative_int(value: Any, label: str) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool), f"{label} must be a non-negative integer")
    _require(value >= 0, f"{label} must be a non-negative integer")
    return value


def _require_nonnegative_number(value: Any, label: str) -> int | float:
    _require(
        isinstance(value, (int, float)) and not isinstance(value, bool),
        f"{label} must be a non-negative number",
    )
    _require(value >= 0, f"{label} must be a non-negative number")
    return value


def _observed_int(
    value: Any,
    *,
    label: str,
    unknown_field: str,
    unknown_fields: list[str],
) -> int | None:
    if value is None:
        unknown_fields.append(unknown_field)
        return None
    return _require_nonnegative_int(value, label)


def _observed_number(
    value: Any,
    *,
    label: str,
    unknown_field: str,
    unknown_fields: list[str],
) -> int | float | None:
    if value is None:
        unknown_fields.append(unknown_field)
        return None
    return _require_nonnegative_number(value, label)


def _validate_runtime_usage_observation(value: Any) -> dict[str, Any]:
    _require(isinstance(value, Mapping), "runtime result usage_observation is absent")
    _require(
        set(value) == {"status", "gap_reasons"},
        "runtime result usage_observation shape is invalid",
    )
    status = value.get("status")
    _require(status in {"complete", "partial"}, "runtime result usage_observation.status is invalid")
    gaps = value.get("gap_reasons")
    _require(isinstance(gaps, list), "runtime result usage_observation.gap_reasons is invalid")
    projected_gaps: list[dict[str, Any]] = []
    for index, gap in enumerate(gaps):
        _require(isinstance(gap, Mapping), f"usage_observation.gap_reasons[{index}] must be an object")
        _require(
            set(gap) == {"attempt_id", "reason", "event_sequence"},
            f"usage_observation.gap_reasons[{index}] shape is invalid",
        )
        projected_gaps.append(
            {
                "attempt_id": _require_string(
                    gap.get("attempt_id"),
                    f"usage_observation.gap_reasons[{index}].attempt_id",
                ),
                "reason": _require_string(
                    gap.get("reason"),
                    f"usage_observation.gap_reasons[{index}].reason",
                ),
                "event_sequence": _require_nonnegative_int(
                    gap.get("event_sequence"),
                    f"usage_observation.gap_reasons[{index}].event_sequence",
                ),
            }
        )
        _require(
            projected_gaps[-1]["reason"] == "controlled_interruption_before_turn_usage",
            f"usage_observation.gap_reasons[{index}].reason is unsupported",
        )
    _require(
        (status == "complete" and not projected_gaps)
        or (status == "partial" and bool(projected_gaps)),
        "runtime result usage_observation status/gap law is invalid",
    )
    return {"status": status, "gap_reasons": projected_gaps}


def _project_runtime_usage(
    result: Mapping[str, Any],
    runtime_result_path: Path,
    expected_runtime_result_digest: str | None,
) -> dict[str, Any]:
    runtime_state = result["runtime_state"]
    runtime_result_ref = runtime_state.get("runtime_result_ref")
    usage_ref = runtime_state.get("usage_observation_ref")
    _require_ref(
        runtime_result_ref,
        label="runtime_state.runtime_result_ref",
        owner_repo="abyss-stack",
        schema_version="abyss_stack_external_codex_result_v2",
    )
    _require_ref(
        usage_ref,
        label="runtime_state.usage_observation_ref",
        owner_repo="abyss-stack",
        schema_version="abyss_stack_external_codex_usage_observation_v1",
    )
    runtime_a2a_return_ref = runtime_state.get("runtime_a2a_return_ref")
    expected_task_id: str | None = None
    if runtime_a2a_return_ref is not None:
        _require_ref(
            runtime_a2a_return_ref,
            label="runtime_state.runtime_a2a_return_ref",
            owner_repo="abyss-stack",
            schema_version="abyss_stack_external_codex_a2a_return_v1",
        )
        expected_task_id = runtime_a2a_return_ref["object_id"]
    runtime = _load_runtime_result(
        runtime_result_path,
        runtime_result_ref=runtime_result_ref,
        expected_digest=expected_runtime_result_digest,
        expected_task_id=expected_task_id,
    )
    usage_observation = _validate_runtime_usage_observation(runtime.get("usage_observation"))
    _require(
        usage_ref["object_id"] == f"{runtime_result_ref['object_id']}#/usage_observation",
        "usage_observation_ref.object_id is not the runtime /usage_observation pointer",
    )
    _require(
        digest_bytes(canonical_bytes(usage_observation)) == usage_ref["digest"],
        "runtime usage_observation bytes do not match owner usage_observation_ref.digest",
    )

    unknown_fields: list[str] = []
    model_value = runtime.get("model_slug")
    model_slug = (
        _require_string(model_value, "runtime result model_slug")
        if model_value is not None
        else None
    )
    reasoning_value = runtime.get("reasoning_effort")
    reasoning_effort = (
        _require_string(reasoning_value, "runtime result reasoning_effort")
        if reasoning_value is not None
        else None
    )
    if reasoning_effort is None:
        unknown_fields.append("reasoning_effort")
    else:
        _require(
            reasoning_effort in {"low", "medium", "high", "xhigh", "max"},
            "runtime result reasoning_effort is invalid",
        )
    if model_slug is None:
        unknown_fields.append("model_slug")
    status_value = runtime.get("status")
    runtime_status = (
        _require_string(status_value, "runtime result status")
        if status_value is not None
        else None
    )
    if runtime_status is None:
        unknown_fields.append("runtime_outcome.status")
    duration_seconds = _observed_number(
        runtime.get("duration_seconds"),
        label="runtime result duration_seconds",
        unknown_field="timing.duration_seconds",
        unknown_fields=unknown_fields,
    )
    active_wall_seconds = _observed_number(
        runtime.get("active_wall_seconds"),
        label="runtime result active_wall_seconds",
        unknown_field="timing.active_wall_seconds",
        unknown_fields=unknown_fields,
    )
    attempt_count = _observed_int(
        runtime.get("attempt_count"),
        label="runtime result attempt_count",
        unknown_field="activity.attempts",
        unknown_fields=unknown_fields,
    )
    turn_count = _observed_int(
        runtime.get("turn_count"),
        label="runtime result turn_count",
        unknown_field="activity.turns",
        unknown_fields=unknown_fields,
    )
    exit_code = runtime.get("exit_code")
    if exit_code is None:
        unknown_fields.append("runtime_outcome.exit_code")
    else:
        _require(
            isinstance(exit_code, int) and not isinstance(exit_code, bool),
            "runtime result exit_code must be an integer or null",
        )

    usage = runtime.get("usage")
    if usage is None:
        usage = {}
    _require(isinstance(usage, Mapping), "runtime result usage must be an object or null")
    input_tokens = _observed_int(
        usage.get("input_tokens"),
        label="runtime result usage.input_tokens",
        unknown_field="tokens.input",
        unknown_fields=unknown_fields,
    )
    cached_input_tokens = _observed_int(
        usage.get("cached_input_tokens"),
        label="runtime result usage.cached_input_tokens",
        unknown_field="tokens.cached_input",
        unknown_fields=unknown_fields,
    )
    output_tokens = _observed_int(
        usage.get("output_tokens"),
        label="runtime result usage.output_tokens",
        unknown_field="tokens.output",
        unknown_fields=unknown_fields,
    )
    metering_mode = usage.get("metering_mode")
    if metering_mode is None:
        unknown_fields.append("cost.metering_mode")
    else:
        _require(metering_mode == "observe_only", "runtime result usage.metering_mode is not observe_only")
    active_cost_regime = usage.get("active_cost_regime")
    if active_cost_regime is None:
        unknown_fields.append("cost.active_cost_regime")
    else:
        active_cost_regime = _require_string(
            active_cost_regime, "runtime result usage.active_cost_regime"
        )
    if "cost_usd" not in usage:
        cost_usd = None
        cost_status = "unknown"
        unknown_fields.append("cost.usd")
    else:
        cost_usd = usage.get("cost_usd")
        _require(
            cost_usd is None
            or (
                isinstance(cost_usd, (int, float))
                and not isinstance(cost_usd, bool)
                and cost_usd >= 0
            ),
            "runtime result usage.cost_usd must be a non-negative number or null",
        )
        cost_status = "not_reported" if cost_usd is None else "reported"

    invocations = runtime.get("codex_invocations")
    start_invocation_count: int | None = 0
    resume_invocation_count: int | None = 0
    if invocations is None:
        start_invocation_count = None
        resume_invocation_count = None
        unknown_fields.extend(("activity.start_invocations", "activity.resume_invocations"))
    else:
        _require(isinstance(invocations, list), "runtime result codex_invocations must be an array or null")
        for index, invocation in enumerate(invocations):
            _require(isinstance(invocation, Mapping), f"codex_invocations[{index}] must be an object")
            mode = invocation.get("mode")
            if mode == "start":
                start_invocation_count += 1
            elif mode == "resume":
                resume_invocation_count += 1
            else:
                start_invocation_count = None
                resume_invocation_count = None
                unknown_fields.extend(("activity.start_invocations", "activity.resume_invocations"))
                break
    commands = runtime.get("executed_commands")
    if commands is None:
        executed_command_count = None
        unknown_fields.append("activity.commands")
    else:
        _require(isinstance(commands, list), "runtime result executed_commands must be an array or null")
        executed_command_count = len(commands)

    return {
        "schema_version": USAGE_PROJECTION_SCHEMA_VERSION,
        "source_ref": dict(usage_ref),
        "runtime_result_ref": dict(runtime_result_ref),
        "observation_status": usage_observation["status"],
        "gap_reasons": usage_observation["gap_reasons"],
        "model_slug": model_slug,
        "reasoning_effort": reasoning_effort,
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "output_tokens": output_tokens,
        "active_wall_seconds": active_wall_seconds,
        "duration_seconds": duration_seconds,
        "turn_count": turn_count,
        "executed_command_count": executed_command_count,
        "attempt_count": attempt_count,
        "start_invocation_count": start_invocation_count,
        "resume_invocation_count": resume_invocation_count,
        "runtime_status": runtime_status,
        "exit_code": exit_code,
        "metering_mode": metering_mode,
        "active_cost_regime": active_cost_regime,
        "cost_usd": cost_usd,
        "cost_status": cost_status,
        "unknown_fields": sorted(set(unknown_fields)),
    }


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
        if state in {"launched", "running"}:
            _require(
                value is None,
                f"runtime_state.{field} must be absent for {state} receipts",
            )
        elif field in required_runtime_refs or value is not None:
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


def _copy_closeout_handoff(result: Mapping[str, Any]) -> dict[str, Any]:
    source = result["closeout_handoff"]
    return {
        field: source[field]
        for field in ("parent_owner", "residual_risk", "next_route")
    }


def _identity_digest(
    *,
    result_digest: str,
    observed_at: str,
    run_ref: str,
    session_ref: str,
    actor_ref: str,
    object_ref: Mapping[str, str],
    payload: Mapping[str, Any],
    supersedes: str | None = None,
) -> str:
    identity = {
        "result_digest": result_digest,
        "observed_at": observed_at,
        "run_ref": run_ref,
        "session_ref": session_ref,
        "actor_ref": actor_ref,
        "object_ref": dict(object_ref),
        "payload_digest": digest_bytes(canonical_bytes(payload)),
    }
    if supersedes is not None:
        identity["supersedes"] = supersedes
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
    result_artifact_ref: str,
    observed_at: str,
    run_ref: str,
    session_ref: str,
    actor_ref: str,
    object_ref: Mapping[str, str],
    event_id: str | None = None,
    expected_result_digest: str | None = None,
    runtime_result_path: Path | None = None,
    expected_runtime_result_digest: str | None = None,
    supersedes: str | None = None,
) -> dict[str, Any]:
    """Compile one deterministic actor responsibility receipt envelope."""

    _raw, result, result_digest = _load_result(summon_result_path)
    _validate_result(result)
    result_artifact_ref = _require_string(result_artifact_ref, "result_artifact_ref")
    _require(result_artifact_ref != result["request_ref"], "result_artifact_ref must not reuse request_ref")
    observed_at = _validate_observed_at(observed_at)
    run_ref = _require_string(run_ref, "run_ref")
    session_ref = _require_string(session_ref, "session_ref")
    actor_ref = _require_string(actor_ref, "actor_ref")
    object_ref = _validate_object_ref(object_ref)
    if expected_result_digest is not None:
        _require_digest(expected_result_digest, "expected_result_digest")
        _require(expected_result_digest == result_digest, "summon result digest does not match expected_result_digest")
    if expected_runtime_result_digest is not None:
        _require(runtime_result_path is not None, "expected_runtime_result_digest requires --runtime-result")
    if supersedes is not None:
        _require_string(supersedes, "supersedes")
        _require(
            supersedes.startswith(EVENT_ID_PREFIX),
            "supersedes must name an actor responsibility execution event",
        )

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
            "stop_line",
        )
    }
    execution.update(
        {
            "checkpoint_required": result.get("checkpoint_required", False),
            "progression_required": result.get("progression_required", False),
            "requested_posture": result.get("requested_posture"),
            "owner_publication_plan": result.get("owner_publication_plan", []),
        }
    )
    execution.update(
        {
            "runtime_state": result["runtime_state"]["state"],
            "actual_effects": result["actual_effects"],
            "blocked_actions": _compact_source_strings(
                result.get("blocked_actions", []), "blocked_actions"
            ),
            "reason_codes": _compact_source_strings(
                result.get("reason_codes", []), "reason_codes"
            ),
        }
    )
    payload: dict[str, Any] = {
        "schema_version": PAYLOAD_SCHEMA_VERSION,
        "source_result": {
            "owner_repo": "aoa-agents",
            "artifact_ref": result_artifact_ref,
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
            "closeout_handoff": _copy_closeout_handoff(result),
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
    if runtime_result_path is not None:
        payload["usage_observation"] = _project_runtime_usage(
            result,
            runtime_result_path,
            expected_runtime_result_digest,
        )
    _validate_document(payload, PAYLOAD_SCHEMA, "actor responsibility receipt payload")
    identity_digest = _identity_digest(
        result_digest=result_digest,
        observed_at=observed_at,
        run_ref=run_ref,
        session_ref=session_ref,
        actor_ref=actor_ref,
        object_ref=object_ref,
        payload=payload,
        supersedes=supersedes,
    )
    derived_event_id = EVENT_ID_PREFIX + identity_digest.removeprefix("sha256:")
    if event_id is not None:
        _require(event_id == derived_event_id, "event_id does not match deterministic owner evidence identity")
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
    if supersedes is not None:
        envelope["supersedes"] = supersedes
    validate_receipt(envelope)
    return envelope


def validate_receipt(envelope: Mapping[str, Any]) -> None:
    """Validate the local envelope shape and the owner payload contract."""

    _require(isinstance(envelope, Mapping), "receipt envelope must be an object")
    required_envelope_fields = {
        "event_kind",
        "event_id",
        "observed_at",
        "run_ref",
        "session_ref",
        "actor_ref",
        "object_ref",
        "evidence_refs",
        "payload",
    }
    _require(
        required_envelope_fields <= set(envelope) <= required_envelope_fields | {"supersedes"},
        "receipt envelope has unsupported or missing fields",
    )
    _require(envelope["event_kind"] == EVENT_KIND, "receipt event_kind is not actor_responsibility_execution_receipt")
    if "supersedes" in envelope:
        _require_string(envelope["supersedes"], "supersedes")
        _require(
            envelope["supersedes"].startswith(EVENT_ID_PREFIX),
            "supersedes must name an actor responsibility execution event",
        )
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
    _require(
        envelope["payload"]["execution"]["runtime_state"]
        == envelope["payload"]["owner_evidence"]["runtime_state"]["state"],
        "payload execution.runtime_state must match owner_evidence.runtime_state.state",
    )
    source_result = envelope["payload"]["source_result"]
    _require(
        source_result["artifact_ref"] != source_result["request_ref"],
        "source_result.artifact_ref must not reuse request_ref",
    )
    expected_event_id = EVENT_ID_PREFIX + _identity_digest(
        result_digest=source_result["artifact_digest"],
        observed_at=envelope["observed_at"],
        run_ref=envelope["run_ref"],
        session_ref=envelope["session_ref"],
        actor_ref=envelope["actor_ref"],
        object_ref=envelope["object_ref"],
        payload=envelope["payload"],
        supersedes=envelope.get("supersedes"),
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
    result.add_argument("--result-artifact-ref", required=True, help="Canonical ref for the exact summon-result-v4 input artifact")
    result.add_argument("--observed-at", required=True)
    result.add_argument("--run-ref", required=True)
    result.add_argument("--session-ref", required=True)
    result.add_argument("--actor-ref", required=True)
    result.add_argument("--object-ref", required=True, help="JSON object or path containing the explicit stats object_ref")
    result.add_argument("--event-id")
    result.add_argument("--expected-result-digest", "--result-digest")
    result.add_argument("--runtime-result", type=Path, help="Exact abyss-stack runtime-result-v2 bytes for an opt-in usage projection")
    result.add_argument("--expected-runtime-result-digest", help="Expected digest for the exact runtime-result-v2 bytes")
    result.add_argument("--supersedes", help="Prior actor responsibility event ID that this observation supersedes")
    result.add_argument("--output", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        receipt = compile_actor_responsibility_receipt(
            summon_result_path=args.summon_result_path,
            result_artifact_ref=args.result_artifact_ref,
            observed_at=args.observed_at,
            run_ref=args.run_ref,
            session_ref=args.session_ref,
            actor_ref=args.actor_ref,
            object_ref=_parse_object_ref(args.object_ref),
            event_id=args.event_id,
            expected_result_digest=args.expected_result_digest,
            runtime_result_path=args.runtime_result,
            expected_runtime_result_digest=args.expected_runtime_result_digest,
            supersedes=args.supersedes,
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
