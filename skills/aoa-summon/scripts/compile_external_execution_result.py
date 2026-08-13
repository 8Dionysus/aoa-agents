#!/usr/bin/env python3
"""Compile one reviewed external execution chain into summon-result-v4.

This is a passive owner-local closeout compiler.  It validates already-created
aoa-sdk, abyss-stack, and review evidence, preserves those objects as exact
references, and emits no runtime, A2A, usage, or acceptance artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


SUMMON_ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = SUMMON_ROOT / "references" / "summon-request-v4.schema.json"
RESULT_SCHEMA = SUMMON_ROOT / "references" / "summon-result-v4.schema.json"
MANDATE_SCHEMA = (
    SUMMON_ROOT.parent
    / "aoa-agents-skills"
    / "references"
    / "actor-mandate-v1.schema.json"
)
OBLIGATION_SCHEMA = (
    SUMMON_ROOT.parent
    / "aoa-agents-skills"
    / "references"
    / "agent-obligation-v1.schema.json"
)
ZERO_DIGEST = "sha256:" + "0" * 64
SUMMON_REQUEST_SCHEMA_VERSION = "summon-request-v4"
INCARNATION_BINDING_SCHEMA_VERSION = "aoa_agent_incarnation_binding_v2"
MANDATE_SCHEMA_VERSION = "actor-mandate-v1"
OBLIGATION_SCHEMA_VERSION = "agent-obligation-v1"
SDK_SUMMON_REQUEST_SCHEMA_VERSION = "urn:aoa-sdk:a2a:summon-request:v4"
SDK_SUMMON_DECISION_SCHEMA_VERSION = "urn:aoa-sdk:a2a:summon-result:v4"
RUNTIME_RESULT_SCHEMA_VERSION = "abyss_stack_external_codex_result_v2"
TERMINAL_RUNTIME_STATUSES = {
    "completed",
    "failed",
    "review_required",
    "authority_blocked",
}
SUCCESS_REVIEW_OUTCOMES = {"proceed"}
A2A_RETURN_SCHEMA_VERSION = "abyss_stack_external_codex_a2a_return_v1"
RUNTIME_PROFILE_SCHEMA_VERSION = "abyss_stack_external_codex_runtime_profile_v2"
USAGE_OBSERVATION_SCHEMA_VERSION = "abyss_stack_external_codex_usage_observation_v1"
VALIDATED_EVENT_KIND = "result.validated"
VALIDATED_CONDITION_ID = "validated-completion"


class ExternalExecutionResultError(ValueError):
    """A supplied owner artifact or relationship is not admissible."""


def canonical_bytes(value: Any) -> bytes:
    """Return the stable JSON representation used by owner content refs."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def semantic_request_digest(request: Mapping[str, Any]) -> str:
    candidate = dict(request)
    candidate.pop("request_digest", None)
    return digest_bytes(canonical_bytes(candidate))


def semantic_self_digest(value: Mapping[str, Any], field: str) -> str:
    return digest_bytes(canonical_bytes(dict(value) | {field: ZERO_DIGEST}))


def semantic_excluding_digest(value: Mapping[str, Any], field: str) -> str:
    candidate = dict(value)
    candidate.pop(field, None)
    return digest_bytes(canonical_bytes(candidate))


def _json_pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ExternalExecutionResultError(
            "usage pointer must be an RFC 6901 JSON pointer"
        )
    current = value
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, Mapping):
            if part not in current:
                raise ExternalExecutionResultError(
                    f"usage pointer does not resolve: {pointer}"
                )
            current = current[part]
        elif isinstance(current, list):
            try:
                index = int(part)
            except ValueError as exc:
                raise ExternalExecutionResultError(
                    f"usage pointer does not resolve: {pointer}"
                ) from exc
            if index < 0 or index >= len(current):
                raise ExternalExecutionResultError(
                    f"usage pointer does not resolve: {pointer}"
                )
            current = current[index]
        else:
            raise ExternalExecutionResultError(
                f"usage pointer does not resolve: {pointer}"
            )
    return current


def _load_with_metadata(
    path: Path,
    *,
    label: str,
) -> tuple[bytes, dict[str, Any], str, dict[str, Any]]:
    """Load a raw JSON artifact or an immutable actor input envelope.

    An actor envelope is a runtime-created safe derivative.  Its embedded
    ``source_artifact_digest`` is useful provenance, but the envelope alone
    cannot authenticate that stronger-owner digest.  Address the exact
    envelope bytes unless a separate trusted attestation is supplied by a
    future contract.
    """

    location = path.resolve()
    if path.is_symlink() or not location.is_file():
        raise ExternalExecutionResultError(
            f"{label} must be an exact regular non-symlink file: {path}"
        )
    try:
        raw = location.read_bytes()
        loaded = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalExecutionResultError(f"{label} is not valid JSON") from exc
    if not isinstance(loaded, dict):
        raise ExternalExecutionResultError(f"{label} must be a JSON object")
    if (
        loaded.get("schema_version")
        == "abyss_stack_external_codex_actor_input_envelope_v1"
    ):
        _require(
            set(loaded)
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
            f"{label} actor envelope shape is invalid",
        )
        _require(
            loaded.get("$schema")
            == "schemas/external-codex-actor-input-envelope.schema.json",
            f"{label} actor envelope schema ref is invalid",
        )
        _require(
            loaded.get("payload_kind") == "json",
            f"{label} actor envelope must contain a JSON payload",
        )
        payload = loaded.get("payload")
        if not isinstance(payload, dict):
            raise ExternalExecutionResultError(
                f"{label} actor envelope must contain a JSON payload"
            )
        artifact_digest = loaded.get("source_artifact_digest")
        if (
            not isinstance(artifact_digest, str)
            or re.fullmatch(r"sha256:[0-9a-f]{64}", artifact_digest) is None
        ):
            raise ExternalExecutionResultError(
                f"{label} actor envelope has no source artifact digest"
            )
        _require(
            isinstance(loaded.get("source_schema_ref"), str)
            and bool(loaded["source_schema_ref"]),
            f"{label} actor envelope has no source schema ref",
        )
        _require(
            isinstance(loaded.get("source_schema_version"), str)
            and bool(loaded["source_schema_version"]),
            f"{label} actor envelope has no source schema version",
        )
        payload_schema_version = payload.get("schema_version")
        if payload_schema_version is not None:
            _require(
                loaded.get("source_schema_version") == payload_schema_version,
                f"{label} actor envelope provenance schema differs from payload schema",
            )
        return (
            raw,
            payload,
            digest_bytes(raw),
            {
                "actor_envelope": True,
                "source_schema_ref": loaded.get("source_schema_ref"),
                "source_schema_version": loaded.get("source_schema_version"),
                "unattested_source_artifact_digest": artifact_digest,
            },
        )
    return (
        raw,
        loaded,
        digest_bytes(raw),
        {
            "actor_envelope": False,
            "source_schema_ref": loaded.get("$schema"),
            "source_schema_version": loaded.get("schema_version"),
        },
    )


def _load(
    path: Path,
    *,
    label: str,
    expected_envelope_schema_version: str | None = None,
) -> tuple[bytes, dict[str, Any], str]:
    raw, payload, artifact_digest, metadata = _load_with_metadata(path, label=label)
    if metadata["actor_envelope"]:
        expected_schema_version = (
            payload.get("schema_version") or expected_envelope_schema_version
        )
        _require(
            isinstance(expected_schema_version, str) and bool(expected_schema_version),
            f"{label} actor envelope has no expected owner schema",
        )
        _require(
            metadata.get("source_schema_version") == expected_schema_version,
            f"{label} actor envelope provenance schema differs from the expected owner schema",
        )
    return raw, payload, artifact_digest


def _validate_document(
    document: Mapping[str, Any],
    *,
    schema_path: Path,
    label: str,
) -> None:
    try:
        schema = json.loads(schema_path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalExecutionResultError(
            f"{label} schema is unavailable: {schema_path}"
        ) from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path)
        where = f" at {path}" if path else ""
        raise ExternalExecutionResultError(
            f"{label} schema validation failed{where}: {errors[0].message}"
        )


def _validate_request_schema(request: Mapping[str, Any]) -> None:
    _validate_document(
        request,
        schema_path=REQUEST_SCHEMA,
        label="summon-request-v4",
    )


def _validate_result(result: Mapping[str, Any]) -> None:
    _validate_document(
        result,
        schema_path=RESULT_SCHEMA,
        label="compiled summon-result-v4",
    )


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ExternalExecutionResultError(message)


def _require_string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{label} is absent")
    return value


def _require_shape(
    value: Any,
    *,
    label: str,
    required: set[str],
    allowed: set[str] | None = None,
) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} is absent")
    keys = set(value)
    allowed_keys = required if allowed is None else allowed
    _require(required <= keys, f"{label} required fields are absent")
    _require(keys <= allowed_keys, f"{label} has unsupported fields")
    return value


def _require_provenance(value: Any, *, label: str) -> dict[str, Any]:
    provenance = _require_shape(
        value,
        label=label,
        required={
            "owner_repo",
            "artifact_ref",
            "source_ref",
            "artifact_digest",
            "schema_ref",
            "schema_version",
        },
    )
    for field in (
        "owner_repo",
        "artifact_ref",
        "source_ref",
        "schema_ref",
        "schema_version",
    ):
        _require_string(provenance.get(field), f"{label}.{field}")
    digest = provenance.get("artifact_digest")
    _require(
        isinstance(digest, str)
        and re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is not None,
        f"{label}.artifact_digest is invalid",
    )
    return dict(provenance)


def _require_string_list(
    value: Any,
    *,
    label: str,
    nonempty: bool = False,
    unique: bool = False,
) -> list[str]:
    _require(
        isinstance(value, list) and (bool(value) or not nonempty),
        f"{label} is invalid",
    )
    _require(
        all(isinstance(item, str) and bool(item) for item in value),
        f"{label} entries are invalid",
    )
    if unique:
        _require(len(value) == len(set(value)), f"{label} entries are duplicated")
    return value


def _require_ref(
    value: Any,
    *,
    label: str,
    owner_repo: str,
    schema_version: str,
) -> dict[str, Any]:
    _require(isinstance(value, Mapping), f"{label} is absent")
    result = {
        "object_id": value.get("object_id"),
        "owner_repo": value.get("owner_repo"),
        "schema_version": value.get("schema_version"),
        "digest": value.get("digest"),
    }
    _require_string(result.get("object_id"), f"{label}.object_id")
    _require(result.get("owner_repo") == owner_repo, f"{label} owner drift")
    _require(
        result.get("schema_version") == schema_version,
        f"{label} schema drift",
    )
    digest = result.get("digest")
    _require(
        isinstance(digest, str)
        and re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is not None,
        f"{label} digest is invalid",
    )
    return result


def _content_ref_from_artifact(
    artifact_digest: str,
    payload: Mapping[str, Any],
    *,
    label: str,
    owner_repo: str,
    schema_version: str,
    object_keys: Sequence[str],
) -> dict[str, str]:
    object_id = next(
        (payload.get(key) for key in object_keys if isinstance(payload.get(key), str)),
        None,
    )
    _require_string(object_id, f"{label} object identity")
    return {
        "object_id": object_id,
        "owner_repo": owner_repo,
        "schema_version": schema_version,
        "digest": artifact_digest,
    }


def _runtime_profile_ref(
    *,
    runtime_profile_ref: Mapping[str, Any] | None,
    runtime_profile_path: Path | None,
) -> dict[str, Any]:
    _require(
        (runtime_profile_ref is None) != (runtime_profile_path is None),
        "provide exactly one runtime profile ref or runtime profile artifact",
    )
    if runtime_profile_ref is not None:
        return _require_ref(
            runtime_profile_ref,
            label="runtime profile ref",
            owner_repo="abyss-stack",
            schema_version=RUNTIME_PROFILE_SCHEMA_VERSION,
        )
    assert runtime_profile_path is not None
    raw, payload, artifact_digest = _load(
        runtime_profile_path,
        label="runtime profile",
        expected_envelope_schema_version=RUNTIME_PROFILE_SCHEMA_VERSION,
    )
    del raw
    _require(
        payload.get("schema_version") == RUNTIME_PROFILE_SCHEMA_VERSION,
        "runtime profile artifact schema is invalid",
    )
    return _content_ref_from_artifact(
        artifact_digest,
        payload,
        label="runtime profile",
        owner_repo="abyss-stack",
        schema_version=RUNTIME_PROFILE_SCHEMA_VERSION,
        object_keys=("profile_id", "runtime_profile_id", "id"),
    )


def _ref_from_provenance(
    value: Any,
    *,
    label: str,
    owner_repo: str,
    schema_version: str,
) -> dict[str, Any]:
    provenance = _require_provenance(value, label=label)
    return _require_ref(
        {
            "object_id": provenance.get("artifact_ref"),
            "owner_repo": provenance.get("owner_repo"),
            "schema_version": provenance.get("schema_version"),
            "digest": provenance.get("artifact_digest"),
        },
        label=label,
        owner_repo=owner_repo,
        schema_version=schema_version,
    )


def _untyped_ref(value: Any, *, label: str) -> dict[str, Any]:
    _require(isinstance(value, Mapping), f"{label} is absent")
    result = {
        "object_id": value.get("object_id"),
        "owner_repo": value.get("owner_repo"),
        "schema_version": value.get("schema_version"),
        "digest": value.get("digest"),
    }
    for field in ("object_id", "owner_repo", "schema_version"):
        _require_string(result.get(field), f"{label}.{field}")
    _require(
        isinstance(result.get("digest"), str)
        and re.fullmatch(r"sha256:[0-9a-f]{64}", result["digest"]) is not None,
        f"{label} digest is invalid",
    )
    return result


def _untyped_ref_from_provenance(value: Any, *, label: str) -> dict[str, Any]:
    provenance = _require_provenance(value, label=label)
    return _untyped_ref(
        {
            "object_id": provenance.get("artifact_ref"),
            "owner_repo": provenance.get("owner_repo"),
            "schema_version": provenance.get("schema_version"),
            "digest": provenance.get("artifact_digest"),
        },
        label=label,
    )


def _require_one_ref(
    refs: Sequence[Mapping[str, Any]],
    expected: Mapping[str, Any],
    *,
    label: str,
) -> None:
    identity = tuple(
        expected[field] for field in ("object_id", "owner_repo", "schema_version")
    )
    same_identity = [
        candidate
        for candidate in refs
        if tuple(
            candidate[field] for field in ("object_id", "owner_repo", "schema_version")
        )
        == identity
    ]
    _require(
        same_identity == [expected],
        f"incarnation continuation does not preserve the exact {label}",
    )


def _validate_incarnation_binding(
    binding: Mapping[str, Any],
    *,
    binding_digest: str,
    request: Mapping[str, Any],
    incarnation: Mapping[str, Any],
    runtime: Mapping[str, Any],
    runtime_profile_ref: Mapping[str, Any],
    mandate_ref: Mapping[str, Any],
    mandate_artifact_digest: str,
) -> None:
    _require_shape(
        binding,
        label="incarnation binding",
        required={
            "schema_version",
            "binding_id",
            "incarnation_id",
            "correlation_id",
            "causation_id",
            "trace_id",
            "run_plan_ref",
            "task_request_ref",
            "role_id",
            "role_contract_ref",
            "model_realization_ref",
            "runtime_profile_ref",
            "workspace_source_ref",
            "permission_posture",
            "tool_profile",
            "usage_metering",
            "stop_conditions",
            "expected_result_schema_ref",
            "continuation",
            "wake_policy",
            "binding_digest",
            "provenance",
            "agent_obligation_ref",
            "actor_mandate_ref",
            "role_resolution_ref",
            "model_fit_query_result_ref",
            "model_fit_projection_ref",
        },
    )
    _require(
        binding.get("schema_version") == "aoa_agent_incarnation_binding_v2",
        "incarnation binding schema is invalid",
    )
    for field in (
        "binding_id",
        "incarnation_id",
        "correlation_id",
        "causation_id",
        "trace_id",
        "role_id",
    ):
        _require_string(binding.get(field), f"incarnation binding {field}")
    _require(
        binding.get("binding_digest")
        == semantic_excluding_digest(binding, "binding_digest"),
        "incarnation binding semantic digest mismatch",
    )
    for field in (
        "run_plan_ref",
        "agent_obligation_ref",
        "actor_mandate_ref",
        "role_resolution_ref",
        "model_fit_query_result_ref",
    ):
        _require_shape(
            binding.get(field),
            label=f"incarnation binding {field}",
            required={"object_id", "owner_repo", "schema_version", "digest"},
        )
    bound_run_plan_ref = _require_ref(
        binding.get("run_plan_ref"),
        label="incarnation binding run plan ref",
        owner_repo="aoa-sdk",
        schema_version="aoa_control_plane_v1",
    )
    model_realization = _require_provenance(
        binding.get("model_realization_ref"),
        label="incarnation binding model realization ref",
    )
    _require(
        model_realization["owner_repo"] == "aoa-models"
        and model_realization["schema_version"] == "aoa_model_realization_v1",
        "incarnation binding model realization ownership is invalid",
    )
    _require(
        model_realization["schema_ref"] == "schemas/model-realization.schema.json",
        "incarnation binding model realization schema ref is invalid",
    )
    bound_model_realization_ref = _require_ref(
        {
            "object_id": model_realization["artifact_ref"],
            "owner_repo": model_realization["owner_repo"],
            "schema_version": model_realization["schema_version"],
            "digest": model_realization["artifact_digest"],
        },
        label="incarnation binding model realization ref",
        owner_repo="aoa-models",
        schema_version="aoa_model_realization_v1",
    )
    for field in (
        "task_request_ref",
        "role_contract_ref",
        "runtime_profile_ref",
        "workspace_source_ref",
        "expected_result_schema_ref",
        "model_fit_projection_ref",
        "provenance",
    ):
        _require_provenance(
            binding.get(field),
            label=f"incarnation binding {field}",
        )
    _require(
        binding["model_fit_projection_ref"]["owner_repo"] == "aoa-models"
        and binding["model_fit_projection_ref"]["schema_version"]
        == "aoa_model_fit_projection_v1"
        and binding["model_fit_projection_ref"]["schema_ref"]
        == "schemas/model-fit-projection.schema.json",
        "incarnation binding model-fit projection provenance is invalid",
    )
    _require(
        binding["provenance"]["owner_repo"] == "aoa-sdk",
        "incarnation binding provenance owner is invalid",
    )
    permission = _require_shape(
        binding.get("permission_posture"),
        label="incarnation binding permission posture",
        required={
            "sandbox_mode",
            "approval_policy",
            "allowed_effect_classes",
            "network_access",
        },
        allowed={
            "sandbox_mode",
            "approval_policy",
            "allowed_effect_classes",
            "network_access",
            "external_effects",
            "secret_access",
        },
    )
    _require(
        permission.get("sandbox_mode")
        in {"read_only", "workspace_write", "danger_full_access"},
        "incarnation binding sandbox mode is invalid",
    )
    _require(
        permission.get("approval_policy")
        in {"never", "on_request", "on_failure", "untrusted"},
        "incarnation binding approval policy is invalid",
    )
    _require(
        permission.get("network_access") in {"disabled", "allowlisted", "enabled"},
        "incarnation binding network access is invalid",
    )
    effect_classes = _require_string_list(
        permission.get("allowed_effect_classes"),
        label="incarnation binding allowed effect classes",
        nonempty=True,
        unique=True,
    )
    _require(
        set(effect_classes)
        <= {"read_only", "repo_mutation", "runtime_mutation", "external"},
        "incarnation binding effect class is invalid",
    )
    for field in ("external_effects", "secret_access"):
        if field in permission:
            _require(
                isinstance(permission[field], bool),
                f"incarnation binding {field} is invalid",
            )
    external_effects = permission.get("external_effects", False)
    secret_access = permission.get("secret_access", False)
    _require(
        external_effects is ("external" in effect_classes),
        "incarnation binding external-effects flag differs from its effect ceiling",
    )
    _require(
        permission.get("sandbox_mode") != "read_only"
        or set(effect_classes) == {"read_only"},
        "incarnation binding read-only sandbox admits non-read-only effects",
    )
    _require(
        not secret_access or permission.get("approval_policy") != "never",
        "incarnation binding secret access cannot use approval_policy=never",
    )
    tool_profile = _require_shape(
        binding.get("tool_profile"),
        label="incarnation binding tool profile",
        required={"profile_id", "profile_ref", "required_tool_ids"},
        allowed={
            "profile_id",
            "profile_ref",
            "required_tool_ids",
            "required_mcp_server_ids",
            "inherit_user_configuration",
        },
    )
    _require_string(
        tool_profile.get("profile_id"), "incarnation binding tool profile id"
    )
    _require_provenance(
        tool_profile.get("profile_ref"),
        label="incarnation binding tool profile ref",
    )
    _require_string_list(
        tool_profile.get("required_tool_ids"),
        label="incarnation binding required tool ids",
        nonempty=True,
        unique=True,
    )
    if "required_mcp_server_ids" in tool_profile:
        _require_string_list(
            tool_profile.get("required_mcp_server_ids"),
            label="incarnation binding required MCP server ids",
            unique=True,
        )
    if "inherit_user_configuration" in tool_profile:
        _require(
            tool_profile["inherit_user_configuration"] is False,
            "incarnation binding cannot inherit user configuration",
        )
    metering = _require_shape(
        binding.get("usage_metering"),
        label="incarnation binding usage metering",
        required={"metering_regime", "dimensions"},
        allowed={
            "metering_regime",
            "dimensions",
            "cost_interpretation",
            "execution_limit_policy",
            "mode",
        },
    )
    _require_string(
        metering.get("metering_regime"), "incarnation binding metering regime"
    )
    dimensions = _require_string_list(
        metering.get("dimensions"),
        label="incarnation binding metering dimensions",
        nonempty=True,
        unique=True,
    )
    _require(
        set(dimensions)
        == {
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "active_wall_seconds",
            "turn_count",
            "output_bytes",
            "executed_commands",
        },
        "incarnation binding metering dimensions are incomplete",
    )
    for field, expected in (
        ("cost_interpretation", "measurement_owner"),
        ("execution_limit_policy", "none"),
        ("mode", "observe_only"),
    ):
        if field in metering:
            _require(
                metering[field] == expected,
                f"incarnation binding usage {field} is invalid",
            )
    stop_conditions = binding.get("stop_conditions")
    _require(
        isinstance(stop_conditions, list) and bool(stop_conditions),
        "incarnation binding stop conditions are absent",
    )
    stop_ids: list[str] = []
    for index, value in enumerate(stop_conditions):
        condition = _require_shape(
            value,
            label=f"incarnation binding stop condition {index}",
            required={"condition_id", "kind", "description"},
            allowed={"condition_id", "kind", "description", "terminal"},
        )
        stop_ids.append(
            _require_string(
                condition.get("condition_id"),
                f"incarnation binding stop condition {index}.condition_id",
            )
        )
        _require_string(
            condition.get("kind"), f"incarnation binding stop condition {index}.kind"
        )
        _require(
            condition.get("kind")
            in {
                "authority_boundary",
                "scope_boundary",
                "validation_failure",
                "ambiguity",
                "external_effect_required",
                "runtime_failure",
                "custom",
            },
            f"incarnation binding stop condition {index}.kind is invalid",
        )
        _require_string(
            condition.get("description"),
            f"incarnation binding stop condition {index}.description",
        )
        if "terminal" in condition:
            _require(
                isinstance(condition["terminal"], bool),
                f"incarnation binding stop condition {index}.terminal is invalid",
            )
    _require(
        len(stop_ids) == len(set(stop_ids)),
        "incarnation binding stop condition ids are duplicated",
    )
    wake_policy = _require_shape(
        binding.get("wake_policy"),
        label="incarnation binding wake policy",
        required={"default_action", "conditions", "escalation_conditions"},
        allowed={"mode", "default_action", "conditions", "escalation_conditions"},
    )
    wake_actions = {
        "continue_without_parent",
        "activate_review_role",
        "wake_parent",
        "stop",
    }
    _require(
        wake_policy.get("default_action") in wake_actions,
        "incarnation binding wake default action is invalid",
    )
    if "mode" in wake_policy:
        _require(
            wake_policy["mode"] == "event_filtered_reentry",
            "incarnation binding wake mode is invalid",
        )
    _require_string_list(
        wake_policy.get("escalation_conditions"),
        label="incarnation binding wake escalation conditions",
        nonempty=True,
        unique=True,
    )
    _require(
        isinstance(wake_policy.get("conditions"), list)
        and bool(wake_policy["conditions"]),
        "incarnation binding wake conditions are absent",
    )
    wake_ids: list[str] = []
    for index, value in enumerate(wake_policy["conditions"]):
        condition = _require_shape(
            value,
            label=f"incarnation binding wake condition {index}",
            required={"condition_id", "event_kind", "action", "description"},
        )
        wake_ids.append(
            _require_string(
                condition.get("condition_id"),
                f"incarnation binding wake condition {index}.condition_id",
            )
        )
        for field in ("event_kind", "action", "description"):
            _require_string(
                condition.get(field),
                f"incarnation binding wake condition {index}.{field}",
            )
        _require(
            condition.get("action") in wake_actions,
            f"incarnation binding wake condition {index}.action is invalid",
        )
    _require(
        len(wake_ids) == len(set(wake_ids)),
        "incarnation binding wake condition ids are duplicated",
    )
    _require(
        incarnation["incarnation_binding_ref"]["digest"] == binding_digest,
        "incarnation binding artifact differs from the request ref",
    )
    binding_provenance = binding.get("provenance")
    _require(
        isinstance(binding_provenance, Mapping),
        "incarnation binding provenance is absent",
    )
    _require(
        binding_provenance.get("owner_repo") == "aoa-sdk"
        and binding_provenance.get("artifact_ref")
        == incarnation["incarnation_binding_ref"]["object_id"],
        "incarnation binding provenance differs from the request ref",
    )
    expected_incarnation_id = request.get("summon_request", {}).get("child_agent_id")
    _require(
        binding.get("incarnation_id")
        == expected_incarnation_id
        == runtime.get("incarnation_id"),
        "incarnation binding identity differs from request or runtime",
    )
    request_run_plan_ref = _require_ref(
        incarnation.get("run_plan_ref"),
        label="request incarnation run plan ref",
        owner_repo="aoa-sdk",
        schema_version="aoa_control_plane_v1",
    )
    _require(
        bound_run_plan_ref == request_run_plan_ref,
        "incarnation binding run_plan_ref differs from the request",
    )
    request_model_realization_ref = _require_ref(
        incarnation.get("model_realization_ref"),
        label="request incarnation model realization ref",
        owner_repo="aoa-models",
        schema_version="aoa_model_realization_v1",
    )
    _require(
        bound_model_realization_ref == request_model_realization_ref,
        "incarnation binding model_realization_ref differs from the request",
    )
    for binding_field, incarnation_field, owner_repo, schema_version in (
        ("agent_obligation_ref", "obligation_ref", "aoa-agents", "agent-obligation-v1"),
        ("actor_mandate_ref", "actor_mandate_ref", "aoa-agents", "actor-mandate-v1"),
        (
            "role_resolution_ref",
            "role_resolution_ref",
            "aoa-agents",
            "aoa_role_resolution_v1",
        ),
        (
            "model_fit_query_result_ref",
            "model_fit_query_result_ref",
            "aoa-models",
            "aoa_model_fit_query_result_v2",
        ),
    ):
        bound_ref = _require_ref(
            binding.get(binding_field),
            label=f"incarnation binding {binding_field}",
            owner_repo=owner_repo,
            schema_version=schema_version,
        )
        request_ref = _require_ref(
            incarnation.get(incarnation_field),
            label=f"request incarnation {incarnation_field}",
            owner_repo=owner_repo,
            schema_version=schema_version,
        )
        _require(
            bound_ref == request_ref,
            f"incarnation binding {binding_field} differs from the request",
        )
    bound_projection_ref = _ref_from_provenance(
        binding.get("model_fit_projection_ref"),
        label="incarnation binding model-fit projection ref",
        owner_repo="aoa-models",
        schema_version="aoa_model_fit_projection_v1",
    )
    request_projection_ref = _require_ref(
        incarnation.get("model_fit_projection_ref"),
        label="request incarnation model-fit projection ref",
        owner_repo="aoa-models",
        schema_version="aoa_model_fit_projection_v1",
    )
    _require(
        bound_projection_ref == request_projection_ref,
        "incarnation binding model_fit_projection_ref differs from the request",
    )
    _require(
        binding["model_fit_projection_ref"].get("source_ref")
        == model_realization.get("source_ref"),
        "incarnation binding model realization differs from the fit projection source",
    )
    bound_task_request_ref = _ref_from_provenance(
        binding.get("task_request_ref"),
        label="incarnation binding task request ref",
        owner_repo="aoa-sdk",
        schema_version="urn:aoa-sdk:a2a:summon-request:v4",
    )
    request_task_ref = _require_ref(
        incarnation.get("sdk_summon_request_ref"),
        label="request incarnation SDK summon request ref",
        owner_repo="aoa-sdk",
        schema_version="urn:aoa-sdk:a2a:summon-request:v4",
    )
    _require(
        bound_task_request_ref == request_task_ref,
        "incarnation binding task_request_ref differs from the request",
    )
    role_contract_ref = _ref_from_provenance(
        binding.get("role_contract_ref"),
        label="incarnation binding role contract ref",
        owner_repo="aoa-agents",
        schema_version="actor-mandate-v1",
    )
    request_mandate_ref = _require_ref(
        incarnation.get("actor_mandate_ref"),
        label="request incarnation actor mandate ref",
        owner_repo="aoa-agents",
        schema_version="actor-mandate-v1",
    )
    _require(
        request_mandate_ref == mandate_ref,
        "actor mandate artifact differs from the request ref",
    )
    _require(
        role_contract_ref == {**mandate_ref, "digest": mandate_artifact_digest},
        "incarnation binding role_contract_ref differs from the exact mandate artifact",
    )
    continuation = binding.get("continuation")
    continuation = _require_shape(
        continuation,
        label="incarnation continuation",
        required={
            "continuation_id",
            "parent_objective_ref",
            "established_decision_refs",
            "delegated_obligation",
            "delegation_reason",
            "exact_child_identity",
            "owner_scope",
            "immutable_input_refs",
            "expected_output",
            "validation_refs",
            "deferred_parent_decisions",
            "invariants",
            "stop_condition_ids",
            "wake_condition_ids",
            "return_owner",
            "rollback_reentry_anchor",
        },
    )
    for field in (
        "continuation_id",
        "delegated_obligation",
        "delegation_reason",
        "exact_child_identity",
        "expected_output",
    ):
        _require_string(continuation.get(field), f"incarnation continuation {field}")
    for field in (
        "owner_scope",
        "invariants",
        "stop_condition_ids",
        "wake_condition_ids",
    ):
        _require_string_list(
            continuation.get(field),
            label=f"incarnation continuation {field}",
            nonempty=True,
            unique=True,
        )
    _require_string_list(
        continuation.get("deferred_parent_decisions"),
        label="incarnation continuation deferred parent decisions",
        unique=True,
    )
    for field in ("immutable_input_refs", "validation_refs"):
        _require(
            isinstance(continuation.get(field), list) and bool(continuation[field]),
            f"incarnation continuation {field} is absent",
        )
    _require(
        set(continuation["stop_condition_ids"]) == set(stop_ids),
        "incarnation continuation stop conditions differ from the binding",
    )
    _require(
        set(continuation["wake_condition_ids"]) == set(wake_ids),
        "incarnation continuation wake conditions differ from the binding",
    )
    for field in ("return_owner", "rollback_reentry_anchor"):
        _require_provenance(
            continuation.get(field),
            label=f"incarnation continuation {field}",
        )
    validation_values = continuation.get("validation_refs")
    assert isinstance(validation_values, list)
    for index, value in enumerate(validation_values):
        _require_provenance(
            value,
            label=f"incarnation continuation validation ref {index}",
        )
    parent_objective_value = continuation.get("parent_objective_ref")
    _require_provenance(
        parent_objective_value,
        label="incarnation continuation parent objective ref",
    )
    continuity_ref = incarnation["continuity_ref"]
    _require(
        continuity_ref["digest"] == binding_digest
        and continuation.get("continuation_id") == continuity_ref["object_id"],
        "incarnation continuation differs from the request ref",
    )
    _require(
        continuation.get("exact_child_identity") == expected_incarnation_id,
        "incarnation continuation child identity differs from the request",
    )
    parent_objective_ref = _ref_from_provenance(
        continuation.get("parent_objective_ref"),
        label="incarnation continuation parent objective ref",
        owner_repo="aoa-skills",
        schema_version="aoa-task-local-dag-v2",
    )
    request_dag_ref = _require_ref(
        incarnation.get("task_local_dag_ref"),
        label="request incarnation task-local DAG ref",
        owner_repo="aoa-skills",
        schema_version="aoa-task-local-dag-v2",
    )
    _require(
        parent_objective_ref == request_dag_ref,
        "incarnation continuation parent objective differs from the request DAG",
    )
    established_values = continuation.get("established_decision_refs")
    _require(
        isinstance(established_values, list),
        "incarnation continuation established decisions are absent",
    )
    established_refs = [
        _untyped_ref_from_provenance(
            value,
            label=f"incarnation continuation established decision {index}",
        )
        for index, value in enumerate(established_values)
    ]
    request_decision_ref = _require_ref(
        incarnation.get("sdk_summon_decision_ref"),
        label="request incarnation SDK summon decision ref",
        owner_repo="aoa-sdk",
        schema_version="urn:aoa-sdk:a2a:summon-result:v4",
    )
    _require_one_ref(
        established_refs, request_decision_ref, label="SDK summon decision"
    )
    immutable_values = continuation.get("immutable_input_refs")
    _require(
        isinstance(immutable_values, list),
        "incarnation continuation immutable inputs are absent",
    )
    immutable_refs = [
        _untyped_ref_from_provenance(
            value,
            label=f"incarnation continuation immutable input {index}",
        )
        for index, value in enumerate(immutable_values)
    ]
    _require_one_ref(immutable_refs, request_task_ref, label="SDK summon request")
    _require_one_ref(
        immutable_refs, request_projection_ref, label="model-fit projection"
    )
    _require_one_ref(immutable_refs, request_dag_ref, label="task-local DAG")
    transfer_ref = _require_ref(
        incarnation.get("responsibility_transfer_ref"),
        label="request incarnation responsibility transfer ref",
        owner_repo="aoa-agents",
        schema_version="responsibility-transfer-v1",
    )
    _require_one_ref(immutable_refs, transfer_ref, label="responsibility transfer")
    procedure_values = incarnation.get("domain_procedure_refs")
    _require(
        isinstance(procedure_values, list) and bool(procedure_values),
        "request incarnation domain procedure refs are absent",
    )
    for index, value in enumerate(procedure_values):
        procedure_ref = _untyped_ref(
            value,
            label=f"request incarnation domain procedure ref {index}",
        )
        _require_one_ref(
            immutable_refs, procedure_ref, label=f"domain procedure {index}"
        )
    permission = binding.get("permission_posture")
    _require(
        isinstance(permission, Mapping), "incarnation permission posture is absent"
    )
    _require(
        permission.get("allowed_effect_classes")
        == request.get("child_scope", {}).get("allowed_effects"),
        "incarnation effect posture differs from the request",
    )
    tool_profile = binding.get("tool_profile")
    _require(isinstance(tool_profile, Mapping), "incarnation tool profile is absent")
    request_tools = _require_string_list(
        request.get("child_scope", {}).get("allowed_tools"),
        label="request child tool scope",
        nonempty=True,
        unique=True,
    )
    binding_tools = _require_string_list(
        tool_profile.get("required_tool_ids"),
        label="incarnation required tools",
        nonempty=True,
        unique=True,
    )
    _require(
        set(request_tools) == set(binding_tools),
        "incarnation tool ceiling differs from the request",
    )
    bound_runtime_profile_ref = _ref_from_provenance(
        binding.get("runtime_profile_ref"),
        label="incarnation runtime profile ref",
        owner_repo="abyss-stack",
        schema_version=RUNTIME_PROFILE_SCHEMA_VERSION,
    )
    bound_profile_ref = _ref_from_provenance(
        tool_profile.get("profile_ref"),
        label="incarnation tool profile ref",
        owner_repo="abyss-stack",
        schema_version=RUNTIME_PROFILE_SCHEMA_VERSION,
    )
    _require(
        bound_runtime_profile_ref == bound_profile_ref == runtime_profile_ref,
        "runtime profile differs from the incarnation binding",
    )


def _validate_mandate_chain(
    obligation: Mapping[str, Any],
    mandate: Mapping[str, Any],
    *,
    binding: Mapping[str, Any],
    request: Mapping[str, Any],
    incarnation: Mapping[str, Any],
) -> None:
    obligation_ref = _require_ref(
        {
            "object_id": obligation.get("obligation_id"),
            "owner_repo": "aoa-agents",
            "schema_version": obligation.get("schema_version"),
            "digest": obligation.get("obligation_digest"),
        },
        label="agent obligation ref",
        owner_repo="aoa-agents",
        schema_version="agent-obligation-v1",
    )
    mandate_obligation_ref = _require_ref(
        mandate.get("obligation_ref"),
        label="actor mandate obligation ref",
        owner_repo="aoa-agents",
        schema_version="agent-obligation-v1",
    )
    request_obligation_ref = _require_ref(
        incarnation.get("obligation_ref"),
        label="request incarnation obligation ref",
        owner_repo="aoa-agents",
        schema_version="agent-obligation-v1",
    )
    _require(
        obligation_ref == mandate_obligation_ref == request_obligation_ref,
        "actor mandate obligation differs from the request incarnation",
    )
    mandate_role_resolution_ref = _require_ref(
        mandate.get("role_resolution_ref"),
        label="actor mandate role resolution ref",
        owner_repo="aoa-agents",
        schema_version="aoa_role_resolution_v1",
    )
    request_role_resolution_ref = _require_ref(
        incarnation.get("role_resolution_ref"),
        label="request incarnation role resolution ref",
        owner_repo="aoa-agents",
        schema_version="aoa_role_resolution_v1",
    )
    _require(
        mandate_role_resolution_ref == request_role_resolution_ref,
        "actor mandate role resolution differs from the request incarnation",
    )
    role_binding = mandate.get("role_binding")
    _require(isinstance(role_binding, Mapping), "actor mandate role binding is absent")
    selected_role = request.get("summon_request", {}).get("desired_role")
    _require(
        role_binding.get("role_id") == binding.get("role_id") == selected_role,
        "actor mandate role binding differs from the selected incarnation role",
    )
    mandate_procedure_values = mandate.get("domain_procedure_refs")
    request_procedure_values = incarnation.get("domain_procedure_refs")
    _require(
        isinstance(mandate_procedure_values, list)
        and bool(mandate_procedure_values)
        and isinstance(request_procedure_values, list)
        and bool(request_procedure_values),
        "actor mandate domain procedure refs are absent",
    )
    mandate_procedure_refs = [
        _untyped_ref(value, label=f"actor mandate domain procedure ref {index}")
        for index, value in enumerate(mandate_procedure_values)
    ]
    request_procedure_refs = [
        _untyped_ref(value, label=f"request incarnation domain procedure ref {index}")
        for index, value in enumerate(request_procedure_values)
    ]
    _require(
        mandate_procedure_refs == request_procedure_refs,
        "actor mandate domain procedures differ from the request incarnation",
    )
    environment = mandate.get("environment")
    _require(isinstance(environment, Mapping), "actor mandate environment is absent")
    tool_profile = binding.get("tool_profile")
    _require(isinstance(tool_profile, Mapping), "incarnation tool profile is absent")
    request_tools = _require_string_list(
        request.get("child_scope", {}).get("allowed_tools"),
        label="request child tool scope",
        nonempty=True,
        unique=True,
    )
    mandate_tools = _require_string_list(
        environment.get("required_tools"),
        label="actor mandate required tools",
        nonempty=True,
        unique=True,
    )
    binding_tools = _require_string_list(
        tool_profile.get("required_tool_ids"),
        label="incarnation required tools",
        nonempty=True,
        unique=True,
    )
    _require(
        set(mandate_tools) == set(binding_tools) == set(request_tools),
        "actor mandate tool ceiling differs from the incarnation request",
    )
    mandate_mcp = _require_string_list(
        environment.get("required_mcp_servers"),
        label="actor mandate required MCP servers",
        unique=True,
    )
    binding_mcp = _require_string_list(
        tool_profile.get("required_mcp_server_ids"),
        label="incarnation required MCP servers",
        unique=True,
    )
    _require(
        set(mandate_mcp) == set(binding_mcp),
        "actor mandate MCP ceiling differs from the incarnation binding",
    )
    permission = binding.get("permission_posture")
    _require(
        isinstance(permission, Mapping), "incarnation permission posture is absent"
    )
    mandate_effects = _require_string_list(
        mandate.get("authority", {}).get("allowed_effects"),
        label="actor mandate allowed effects",
        nonempty=True,
        unique=True,
    )
    binding_effects = _require_string_list(
        permission.get("allowed_effect_classes"),
        label="incarnation allowed effects",
        nonempty=True,
        unique=True,
    )
    request_effects = _require_string_list(
        request.get("child_scope", {}).get("allowed_effects"),
        label="request child effect scope",
        nonempty=True,
        unique=True,
    )
    _require(
        set(mandate_effects) == set(binding_effects) == set(request_effects),
        "actor mandate effect ceiling differs from the incarnation request",
    )
    mandate_sandbox = environment.get("sandbox_mode")
    _require_string(mandate_sandbox, "actor mandate sandbox mode")
    _require(
        mandate_sandbox.replace("-", "_") == permission.get("sandbox_mode"),
        "actor mandate sandbox differs from the incarnation binding",
    )

    mandate_return_owner = _untyped_ref(
        mandate.get("return_owner"),
        label="actor mandate return owner",
    )
    request_return_owner = request.get("return_owner")
    _require_string(request_return_owner, "request return owner")
    _require(
        mandate_return_owner["object_id"] == request_return_owner,
        "actor mandate return owner differs from the request",
    )
    obligation_return_owner = _untyped_ref(
        obligation.get("return_owner"),
        label="agent obligation return owner",
    )
    obligation_current_holder = _untyped_ref(
        obligation.get("current_holder"),
        label="agent obligation current holder",
    )
    _require(
        obligation_return_owner == mandate_return_owner
        and obligation_current_holder == obligation_return_owner,
        "agent obligation holder chain differs from the actor mandate return owner",
    )
    _require(
        request.get("child_scope", {}).get("authority_limit")
        == obligation.get("responsibility_boundary"),
        "request authority limit differs from the exact agent obligation",
    )
    _require(
        request.get("child_stop_line") == mandate.get("authority", {}).get("stop_line"),
        "request stop line differs from the exact actor mandate",
    )
    transfer = incarnation.get("responsibility_transfer_ref")
    _require(
        isinstance(transfer, Mapping),
        "request incarnation responsibility transfer ref is absent",
    )
    transfer_holders = _require_string_list(
        transfer.get("holder_ids"),
        label="responsibility transfer holders",
        nonempty=True,
        unique=True,
    )
    _require(
        len(transfer_holders) == 2 and transfer_holders[0] == request_return_owner,
        "responsibility transfer does not return to the request owner",
    )
    mandate_continuity = mandate.get("continuity")
    _require(
        isinstance(mandate_continuity, Mapping),
        "actor mandate continuity is absent",
    )
    _require(
        transfer_holders[1] == mandate_continuity.get("identity_key"),
        "responsibility transfer current holder differs from the actor mandate identity",
    )
    continuation = binding.get("continuation")
    _require(isinstance(continuation, Mapping), "incarnation continuation is absent")
    continuation_return_owner = _require_provenance(
        continuation.get("return_owner"),
        label="incarnation continuation return owner",
    )
    _require(
        continuation_return_owner["owner_repo"] == mandate_return_owner["owner_repo"],
        "incarnation continuation return owner differs from the mandate owner",
    )


def _usage_ref(
    runtime: Mapping[str, Any],
    runtime_ref: Mapping[str, Any],
    *,
    usage_pointer: str,
    usage_observation_ref: Mapping[str, Any] | None,
) -> dict[str, Any]:
    _require(
        usage_pointer == "/usage_observation",
        "usage pointer must be the canonical /usage_observation locator",
    )
    usage_value = _json_pointer(runtime, usage_pointer)
    _validate_usage_observation(usage_value, label="embedded usage observation")
    canonical_ref = {
        "object_id": f"{runtime_ref['object_id']}#{usage_pointer}",
        "owner_repo": "abyss-stack",
        "schema_version": USAGE_OBSERVATION_SCHEMA_VERSION,
        "digest": digest_bytes(canonical_bytes(usage_value)),
    }
    if usage_observation_ref is not None:
        asserted_ref = _require_ref(
            usage_observation_ref,
            label="usage observation ref",
            owner_repo="abyss-stack",
            schema_version=USAGE_OBSERVATION_SCHEMA_VERSION,
        )
        _require(
            asserted_ref == canonical_ref,
            "usage observation ref differs from the exact runtime observation",
        )
    return canonical_ref


def _validate_usage_observation(value: Any, *, label: str) -> None:
    _require(isinstance(value, Mapping), f"{label} shape is invalid")
    _require(set(value) == {"status", "gap_reasons"}, f"{label} shape is invalid")
    _require(
        value.get("status") in {"complete", "partial"},
        f"{label} status is invalid",
    )
    gaps = value.get("gap_reasons")
    _require(isinstance(gaps, list), f"{label} gaps are invalid")
    for gap in gaps:
        _require(isinstance(gap, Mapping), f"{label} gap shape is invalid")
        _require(
            set(gap) == {"attempt_id", "reason", "event_sequence"},
            f"{label} gap shape is invalid",
        )
        _require_string(gap.get("attempt_id"), f"{label} gap attempt id")
        _require(
            gap.get("reason") == "controlled_interruption_before_turn_usage",
            f"{label} gap reason is invalid",
        )
        _require(
            isinstance(gap.get("event_sequence"), int)
            and not isinstance(gap.get("event_sequence"), bool)
            and gap["event_sequence"] >= 0,
            f"{label} gap event sequence is invalid",
        )
    _require(
        (value["status"] == "complete" and not gaps)
        or (value["status"] == "partial" and bool(gaps)),
        f"{label} status and gaps contradict each other",
    )


def _validate_external_request(request: Mapping[str, Any]) -> dict[str, Any]:
    _validate_request_schema(request)
    _require(request.get("intent") == "execute", "request intent must be execute")
    _require(request.get("request_ref"), "request ref is absent")
    expected_digest = semantic_request_digest(request)
    _require(
        request.get("request_digest") == expected_digest,
        "request digest mismatch",
    )
    expected_outputs = request.get("expected_outputs")
    _require(
        isinstance(expected_outputs, list)
        and bool(expected_outputs)
        and all(isinstance(item, str) and item for item in expected_outputs)
        and len(set(expected_outputs)) == len(expected_outputs),
        "request expected outputs are incomplete or duplicated",
    )
    scope = request.get("child_scope")
    _require(isinstance(scope, Mapping), "request child scope is absent")
    effects = scope.get("allowed_effects")
    _require(
        isinstance(effects, list)
        and len(effects) == 1
        and effects[0] in {"read_only", "repo_mutation"},
        "request effect ceiling is outside the admitted external effect classes",
    )
    summon_request = request.get("summon_request")
    _require(isinstance(summon_request, Mapping), "summon request body is absent")
    incarnation = request.get("external_incarnation")
    _require(isinstance(incarnation, Mapping), "external incarnation is absent")
    _require(
        summon_request.get("transport_preference")
        in {"external_cli", "a2a_remote", "either"},
        "request does not authorize the external CLI lane",
    )
    for field, owner, schema in (
        ("obligation_ref", "aoa-agents", "agent-obligation-v1"),
        ("actor_mandate_ref", "aoa-agents", "actor-mandate-v1"),
        ("role_resolution_ref", "aoa-agents", "aoa_role_resolution_v1"),
        ("model_fit_query_result_ref", "aoa-models", "aoa_model_fit_query_result_v2"),
        ("model_fit_projection_ref", "aoa-models", "aoa_model_fit_projection_v1"),
        ("task_local_dag_ref", "aoa-skills", "aoa-task-local-dag-v2"),
        ("incarnation_binding_ref", "aoa-sdk", "aoa_agent_incarnation_binding_v2"),
        ("sdk_summon_request_ref", "aoa-sdk", "urn:aoa-sdk:a2a:summon-request:v4"),
        ("sdk_summon_decision_ref", "aoa-sdk", "urn:aoa-sdk:a2a:summon-result:v4"),
        ("runtime_launch_ref", "abyss-stack", "abyss_stack_external_codex_launch_v1"),
        ("responsibility_transfer_ref", "aoa-agents", "responsibility-transfer-v1"),
        ("continuity_ref", "aoa-sdk", "continuation-obligation-v1"),
        (
            "return_event_schema_ref",
            "abyss-stack",
            "abyss_stack_external_codex_event_v1",
        ),
    ):
        _require_ref(
            incarnation.get(field),
            label=f"external incarnation {field}",
            owner_repo=owner,
            schema_version=schema,
        )
    procedures = incarnation.get("domain_procedure_refs")
    _require(
        isinstance(procedures, list)
        and bool(procedures)
        and all(isinstance(item, Mapping) for item in procedures),
        "domain procedure refs are absent",
    )
    for index, procedure in enumerate(procedures, start=1):
        _require_string(
            procedure.get("object_id"), f"domain procedure {index} object identity"
        )
        _require_string(procedure.get("owner_repo"), f"domain procedure {index} owner")
        _require_string(
            procedure.get("schema_version"), f"domain procedure {index} schema"
        )
        _require(
            isinstance(procedure.get("digest"), str)
            and re.fullmatch(r"sha256:[0-9a-f]{64}", procedure["digest"]) is not None,
            f"domain procedure {index} digest is invalid",
        )
    _require(incarnation.get("runtime_interface"), "runtime interface is absent")
    _require(
        incarnation.get("launches_separate_os_process") is True,
        "separate process was not bound",
    )
    _require(
        incarnation.get("separate_cli_session") is True,
        "separate CLI session was not bound",
    )
    _require(
        incarnation.get("uses_builtin_codex_subagents") is False,
        "built-in subagents are enabled",
    )
    _require(
        incarnation.get("usage_metering") == "observe_only_no_budget",
        "usage metering is not observe-only",
    )
    transfer = incarnation["responsibility_transfer_ref"]
    _require(
        transfer.get("admitted_state") in {"accepted", "launched", "narrowed"},
        "responsibility transfer is not admitted",
    )
    holders = transfer.get("holder_ids")
    _require(
        isinstance(holders, list) and len(holders) == 2 and len(set(holders)) == 2,
        "responsibility holders are not distinct",
    )
    return dict(incarnation)


def _validate_sdk_chain(
    request: Mapping[str, Any],
    incarnation: Mapping[str, Any],
    sdk_request: Mapping[str, Any],
    sdk_request_digest: str,
    sdk_decision: Mapping[str, Any],
    sdk_decision_digest: str,
) -> str:
    _require(
        sdk_request.get("schema_version")
        in {
            None,
            "urn:aoa-sdk:a2a:summon-request:v4",
            "summon-request-v4",
        },
        "SDK summon request schema is invalid",
    )
    sdk_summon = sdk_request.get("summon_request")
    _require(isinstance(sdk_summon, Mapping), "SDK summon request body is absent")
    _require(
        sdk_summon.get("transport_preference") in {"a2a_remote", "either"},
        "SDK summon request does not authorize the external A2A transport",
    )
    expected_owner_summon = dict(sdk_summon)
    expected_owner_summon.pop("expected_outputs", None)
    expected_owner_summon["transport_preference"] = "external_cli"
    _require(
        request.get("summon_request") == expected_owner_summon,
        "owner summon request differs from the SDK summon body",
    )
    _require(
        request.get("quest_passport") == sdk_request.get("quest_passport"),
        "owner quest passport differs from the SDK summon request",
    )
    sdk_outputs = sdk_request.get("expected_outputs")
    requested_outputs = request.get("expected_outputs")
    _require(
        isinstance(sdk_outputs, list) and sdk_outputs == requested_outputs,
        "SDK and owner request output keys differ",
    )
    _require(
        sdk_decision.get("schema_version") == "urn:aoa-sdk:a2a:summon-result:v4",
        "SDK summon decision schema is invalid",
    )
    _require(sdk_decision.get("allowed") is True, "SDK summon decision is not allowed")
    _require(
        sdk_decision.get("capability_execution_claimed") is False,
        "SDK decision claims runtime execution",
    )
    _require(
        sdk_decision.get("request_artifact_digest") == sdk_request_digest,
        "SDK summon decision names another summon request",
    )
    _require(
        incarnation["sdk_summon_request_ref"]["digest"] == sdk_request_digest,
        "SDK summon request digest differs from the incarnation ref",
    )
    _require(
        incarnation["sdk_summon_decision_ref"]["digest"] == sdk_decision_digest,
        "SDK summon decision digest differs from the incarnation ref",
    )
    return _require_string(
        sdk_decision.get("cohort_pattern"),
        "SDK summon decision cohort pattern",
    )


def _validate_sdk_a2a_request_ref(
    value: Any,
    *,
    expected_ref: Mapping[str, Any],
    expected_digest: str,
) -> None:
    """Bind a runtime A2A provenance ref to the exact SDK request bytes.

    Historical synthetic fixtures used the owner-local compact content-ref
    shape.  The real abyss-stack A2A return carries an aoa-sdk provenance ref.
    Both representations must name the same artifact, schema, and digest.
    """

    if isinstance(value, Mapping) and "artifact_ref" in value:
        provenance = _require_provenance(value, label="reviewed A2A summon request ref")
        _require(
            provenance["owner_repo"] == "aoa-sdk",
            "reviewed A2A summon request ref owner drift",
        )
        _require(
            provenance["schema_version"] == SDK_SUMMON_REQUEST_SCHEMA_VERSION,
            "reviewed A2A summon request ref schema drift",
        )
        _require(
            provenance["artifact_ref"] == expected_ref.get("object_id"),
            "reviewed A2A return names another summon request ref",
        )
        _require(
            provenance["artifact_digest"] == expected_digest,
            "reviewed A2A return names another summon request digest",
        )
        return
    compact = _require_ref(
        value,
        label="reviewed A2A summon request ref",
        owner_repo="aoa-sdk",
        schema_version=SDK_SUMMON_REQUEST_SCHEMA_VERSION,
    )
    _require(
        compact == expected_ref and compact["digest"] == expected_digest,
        "reviewed A2A return names another summon request ref",
    )


def _validate_review_request(
    review_request: Mapping[str, Any],
    *,
    review_request_digest: str,
    reviewed_return: Mapping[str, Any],
    runtime: Mapping[str, Any],
    runtime_ref: Mapping[str, Any],
) -> None:
    """Authenticate the independent-review request and its writer relation."""

    _require(
        review_request.get("schema_version")
        in {None, SDK_SUMMON_REQUEST_SCHEMA_VERSION, "summon-request-v4"},
        "review summon request schema is invalid",
    )
    review_ref = _require_provenance(
        reviewed_return.get("review_summon_request_ref"),
        label="reviewed A2A review request ref",
    )
    _require(
        review_ref["owner_repo"] == "abyss-stack",
        "reviewed A2A review request ref owner drift",
    )
    _require(
        review_ref["schema_version"] == SDK_SUMMON_REQUEST_SCHEMA_VERSION,
        "reviewed A2A review request ref schema drift",
    )
    _require(
        review_ref["artifact_digest"] == review_request_digest,
        "reviewed A2A review request digest differs from the supplied artifact",
    )
    _require(
        review_ref["source_ref"] == runtime_ref["digest"],
        "reviewed A2A review request is not sourced from the terminal runtime result",
    )
    evidence_digests = reviewed_return.get("evidence_digests")
    _require(isinstance(evidence_digests, Mapping), "A2A evidence digests are absent")
    _require(
        evidence_digests.get("review_summon_request") == review_request_digest,
        "A2A evidence names another review summon request",
    )

    summon = review_request.get("summon_request")
    _require(isinstance(summon, Mapping), "review summon request body is absent")
    reviewed_path = _require_string(
        reviewed_return.get("reviewed_artifact_path"),
        "reviewed A2A artifact path",
    )
    _require(
        review_request.get("reviewed_artifact_path") == reviewed_path
        and summon.get("reviewed_artifact_path") == reviewed_path,
        "review summon request names another reviewed artifact",
    )
    _require(
        summon.get("parent_task_id") == runtime.get("task_id"),
        "review summon request names another writer task",
    )
    _require(
        summon.get("desired_role") == "reviewer",
        "review summon request does not select a reviewer",
    )
    _require(
        summon.get("transport_preference") == "codex_local",
        "review summon request does not use the admitted review transport",
    )
    _require(
        summon.get("review_required") is False,
        "review summon request recursively requires another review",
    )
    reviewer_id = _require_string(
        summon.get("child_agent_id"), "review summon request child agent"
    )
    _require(
        reviewer_id != runtime.get("incarnation_id"),
        "review summon request reuses the writer incarnation",
    )
    _require_string(summon.get("session_ref"), "review summon request session ref")

    passport = review_request.get("quest_passport")
    _require(isinstance(passport, Mapping), "review quest passport is absent")
    _require(
        passport.get("route_anchor") == runtime_ref["digest"],
        "review summon request route anchor differs from the terminal runtime result",
    )
    _require(
        passport.get("delegate_tier") == "verifier"
        and passport.get("risk") == "r0_readonly",
        "review summon request is not an independent read-only verifier route",
    )
    expected_outputs = _require_string_list(
        review_request.get("expected_outputs"),
        label="review summon request expected outputs",
        nonempty=True,
        unique=True,
    )
    passport_outputs = _require_string_list(
        passport.get("expected_artifacts"),
        label="review quest passport expected artifacts",
        nonempty=True,
        unique=True,
    )
    _require(
        passport_outputs == expected_outputs,
        "review quest passport output closure is inconsistent",
    )
    _require(
        summon.get("expected_outputs") == expected_outputs,
        "review summon request output closure is inconsistent",
    )
    audit_refs = _require_string_list(
        review_request.get("audit_refs"),
        label="review summon request audit refs",
        nonempty=True,
        unique=True,
    )
    _require(
        summon.get("audit_refs") == audit_refs,
        "review summon request audit closure is inconsistent",
    )
    exact_writer_ref = f"abyss-stack:{reviewed_path}@{runtime_ref['digest']}"
    _require(
        exact_writer_ref in audit_refs,
        "review summon request does not audit the exact terminal runtime result",
    )


def _process_handle(runtime: Mapping[str, Any]) -> str:
    invocations = runtime.get("codex_invocations")
    _require(
        isinstance(invocations, list) and bool(invocations),
        "runtime process evidence is absent",
    )
    invocation = invocations[-1]
    _require(isinstance(invocation, Mapping), "runtime process evidence is invalid")
    process_ref = invocation.get("process_identity_ref")
    _require(isinstance(process_ref, Mapping), "runtime process identity ref is absent")
    return _require_string(process_ref.get("artifact_ref"), "runtime process handle")


def _validate_runtime(
    runtime: Mapping[str, Any],
    request: Mapping[str, Any],
    request_artifact_digest: str,
) -> tuple[dict[str, str], dict[str, str]]:
    _require(
        runtime.get("schema_version") == "abyss_stack_external_codex_result_v2",
        "runtime result schema is invalid",
    )
    _require(
        runtime.get("status") in TERMINAL_RUNTIME_STATUSES,
        "runtime result is nonterminal",
    )
    _require(
        runtime.get("status") in {"completed", "review_required"},
        "runtime result cannot support an accepted closeout",
    )
    _require(
        runtime.get("execution_posture") in {"bounded_execution", "closeout"},
        "runtime execution posture exceeds the mandate",
    )
    _require(
        runtime.get("admission_class") == "owner_contour",
        "runtime admission class is not owner-contour",
    )
    _require_string(runtime.get("task_id"), "runtime task id")
    _require_string(runtime.get("incarnation_id"), "runtime incarnation id")
    _require_string(runtime.get("session_id"), "runtime session id")
    runtime_thread_id = _require_string(
        runtime.get("thread_id"), "runtime continuation id"
    )
    usage = runtime.get("usage_observation")
    _validate_usage_observation(usage, label="runtime usage observation")
    invocations = runtime.get("codex_invocations")
    _require(
        isinstance(invocations, list) and bool(invocations),
        "runtime invocation evidence is absent",
    )
    for invocation in invocations:
        _require(
            isinstance(invocation, Mapping), "runtime invocation evidence is invalid"
        )
        argv = invocation.get("argv")
        _require(isinstance(argv, list), "runtime invocation argv is absent")
        _require(
            not bool(invocation.get("uses_builtin_codex_subagents", False)),
            "runtime invocation claims built-in subagent use",
        )
        _require(
            any(
                argv[index : index + 2] == ["--disable", "multi_agent"]
                for index in range(max(0, len(argv) - 1))
            ),
            "runtime invocation does not disable built-in subagents",
        )
        _require(
            invocation.get("thread_id") == runtime_thread_id,
            "runtime continuation differs from physical invocation evidence",
        )
    runtime_ref = _content_ref_from_artifact(
        runtime.get("artifact_digest", digest_bytes(canonical_bytes(runtime))),
        runtime,
        label="runtime result",
        owner_repo="abyss-stack",
        schema_version="abyss_stack_external_codex_result_v2",
        object_keys=("result_id", "task_id"),
    )
    actor_handle = _require_string(runtime.get("incarnation_id"), "actor handle")
    process_handle = _process_handle(runtime)
    session_handle = _require_string(runtime.get("session_id"), "session handle")
    continuation_handle = runtime_thread_id
    handles = {
        "actor_handle": actor_handle,
        "process_handle": process_handle,
        "session_handle": session_handle,
        "continuation_handle": continuation_handle,
    }
    if runtime.get("exit_code") is not None and runtime.get("status") != "failed":
        _require(
            runtime.get("exit_code") == 0,
            "successful runtime result has a nonzero exit code",
        )
    _require(
        runtime.get("incarnation_id")
        == request.get("summon_request", {}).get("child_agent_id"),
        "runtime incarnation differs from the summon request",
    )
    owner_admission_ref = runtime.get("owner_admission_ref")
    _require(
        isinstance(owner_admission_ref, Mapping),
        "runtime owner admission ref is absent",
    )
    _require_string(
        owner_admission_ref.get("artifact_ref"),
        "runtime owner admission artifact ref",
    )
    _require(
        owner_admission_ref.get("artifact_ref") == request.get("request_ref")
        and owner_admission_ref.get("owner_repo") == "aoa-agents"
        and owner_admission_ref.get("artifact_digest") == request_artifact_digest,
        "runtime result differs from the selected owner request and launch",
    )
    return runtime_ref, handles


def _validate_reviewed_return(
    reviewed_return: Mapping[str, Any],
    request: Mapping[str, Any],
    runtime: Mapping[str, Any],
    runtime_ref: Mapping[str, Any],
    *,
    sdk_request_digest: str,
    reviewed_return_digest: str,
    reviewed_return_metadata: Mapping[str, Any],
) -> dict[str, str]:
    _require(
        reviewed_return.get("schema_version") == A2A_RETURN_SCHEMA_VERSION,
        "A2A return payload schema/version is invalid",
    )
    _require(
        reviewed_return_metadata.get("source_schema_version")
        == A2A_RETURN_SCHEMA_VERSION,
        "A2A return schema/version is invalid",
    )
    source_schema_ref = reviewed_return_metadata.get("source_schema_ref")
    if source_schema_ref is not None:
        _require(
            source_schema_ref
            == "runtime/schemas/external-codex-a2a-return.schema.json",
            "A2A return schema ref is invalid",
        )
    _require(reviewed_return.get("reviewed") is True, "A2A return is not reviewed")
    _require(
        reviewed_return.get("review_status") == "reviewed",
        "A2A review status is not reviewed",
    )
    _require(
        reviewed_return.get("reviewer_status") == "completed",
        "A2A reviewer is not terminal",
    )
    _require(
        reviewed_return.get("reviewer_decision") in SUCCESS_REVIEW_OUTCOMES,
        "A2A reviewer disposition is not accepting",
    )
    _require(
        reviewed_return.get("review_outcome") in SUCCESS_REVIEW_OUTCOMES,
        "A2A review outcome is not accepting",
    )
    remote_task = reviewed_return.get("remote_task")
    _require(isinstance(remote_task, Mapping), "A2A remote task is absent")
    _require(remote_task.get("state") == "completed", "A2A remote task is nonterminal")
    _require_string(remote_task.get("task_id"), "A2A remote task id")
    _require_string(remote_task.get("agent_id"), "A2A remote task agent id")
    _require(
        remote_task.get("task_id") == runtime.get("task_id"),
        "A2A remote task id differs from the terminal runtime task id",
    )
    _require(
        remote_task.get("agent_id") == runtime.get("incarnation_id"),
        "A2A remote task agent id differs from the terminal runtime incarnation id",
    )
    _require_string(remote_task.get("context_id"), "A2A remote task context id")
    _require(
        remote_task.get("parent_task_id")
        == request.get("summon_request", {}).get("parent_task_id"),
        "A2A remote task parent identity differs from the summon request",
    )
    artifact_refs = remote_task.get("artifact_refs")
    _require(
        isinstance(artifact_refs, list)
        and all(isinstance(item, str) and item for item in artifact_refs),
        "A2A remote task artifact refs are absent",
    )
    reviewed_artifact_path = reviewed_return.get("reviewed_artifact_path")
    _require_string(reviewed_artifact_path, "reviewed A2A artifact path")
    _require(
        reviewed_artifact_path in artifact_refs,
        "reviewed A2A artifact path is not bound to the remote task",
    )
    evidence_digests = reviewed_return.get("evidence_digests")
    _require(isinstance(evidence_digests, Mapping), "A2A evidence digests are absent")
    _require(
        evidence_digests.get("writer_result") == runtime_ref["digest"],
        "A2A reviewed writer result differs from the terminal runtime result",
    )
    _require(
        runtime.get("status") == "completed",
        "reviewed A2A return requires a completed terminal runtime result",
    )
    wake = runtime.get("wake_evaluation")
    _require(isinstance(wake, Mapping), "runtime validation event is absent")
    _require(
        wake.get("event_kind") == VALIDATED_EVENT_KIND,
        "runtime validation event is not result.validated",
    )
    _require(
        wake.get("condition_id") == VALIDATED_CONDITION_ID,
        "runtime validation condition is not validated-completion",
    )
    _require(
        wake.get("wake_parent") is True,
        "runtime validation event does not wake the parent",
    )
    expected_ref = request["external_incarnation"]["sdk_summon_request_ref"]
    _validate_sdk_a2a_request_ref(
        reviewed_return.get("summon_request_ref"),
        expected_ref=expected_ref,
        expected_digest=sdk_request_digest,
    )
    _require(
        evidence_digests.get("summon_request") == sdk_request_digest,
        "A2A evidence names another SDK summon request",
    )
    return {
        "object_id": str(remote_task["task_id"]),
        "owner_repo": "abyss-stack",
        "schema_version": "abyss_stack_external_codex_a2a_return_v1",
        "digest": reviewed_return_digest,
    }


def _output_checks(
    expected_outputs: Sequence[str],
    reviewed_return: Mapping[str, Any],
    runtime_ref: Mapping[str, Any],
    explicit_artifact_refs: Mapping[str, str] | None,
) -> dict[str, dict[str, Any]]:
    def returned_output_names(value: Any) -> dict[str, str]:
        _require(isinstance(value, list), "A2A returned artifacts are absent")
        artifacts_by_name: dict[str, str] = {}
        for artifact in value:
            if not isinstance(artifact, str) or not artifact:
                raise ExternalExecutionResultError(
                    "A2A returned artifact identity is invalid"
                )
            if artifact not in expected_outputs:
                raise ExternalExecutionResultError(
                    f"A2A returned artifact is outside the requested output keys/closure: {artifact}"
                )
            if artifact in artifacts_by_name:
                raise ExternalExecutionResultError(
                    f"A2A returned duplicate output: {artifact}"
                )
            artifacts_by_name[artifact] = artifact
        _require(
            set(artifacts_by_name) == set(expected_outputs),
            "A2A returned output keys do not match the request",
        )
        return artifacts_by_name

    if explicit_artifact_refs is not None:
        _require(
            set(explicit_artifact_refs) == set(expected_outputs),
            "explicit output refs do not match request output keys",
        )
        artifacts = dict(explicit_artifact_refs)
        returned = reviewed_return["remote_task"].get("returned_artifacts")
        returned_output_names(returned)
        allowed = set(returned)
        allowed.add(str(runtime_ref["object_id"]))
        _require(
            all(value in allowed for value in artifacts.values()),
            "explicit output refs are not linked to the reviewed A2A return",
        )
    else:
        remote_task = reviewed_return["remote_task"]
        returned = remote_task.get("returned_artifacts")
        artifacts = returned_output_names(returned)
    return {
        output: {
            "received": True,
            "artifact_ref": _require_string(
                artifacts[output], f"output {output} artifact ref"
            ),
            "accepted": True,
        }
        for output in expected_outputs
    }


def compile_external_execution_result(
    *,
    request_path: Path,
    incarnation_binding_path: Path,
    obligation_path: Path,
    mandate_path: Path,
    sdk_summon_request_path: Path,
    sdk_summon_decision_path: Path,
    runtime_result_path: Path,
    reviewed_a2a_return_path: Path,
    review_summon_request_path: Path,
    runtime_profile_ref: Mapping[str, Any] | None = None,
    runtime_profile_path: Path | None = None,
    usage_pointer: str = "/usage_observation",
    usage_observation_ref: Mapping[str, Any] | None = None,
    output_artifact_refs: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Compile one exact terminal, reviewed external execution chain."""

    _request_raw, request, request_artifact_digest = _load(
        request_path,
        label="summon request",
        expected_envelope_schema_version=SUMMON_REQUEST_SCHEMA_VERSION,
    )
    _binding_raw, incarnation_binding, incarnation_binding_digest = _load(
        incarnation_binding_path,
        label="incarnation binding",
        expected_envelope_schema_version=INCARNATION_BINDING_SCHEMA_VERSION,
    )
    _obligation_raw, obligation, _obligation_artifact_digest = _load(
        obligation_path,
        label="agent obligation",
        expected_envelope_schema_version=OBLIGATION_SCHEMA_VERSION,
    )
    _validate_document(
        obligation,
        schema_path=OBLIGATION_SCHEMA,
        label="agent obligation",
    )
    _require(
        obligation.get("obligation_digest")
        == semantic_self_digest(obligation, "obligation_digest"),
        "agent obligation semantic digest mismatch",
    )
    mandate_raw, mandate, mandate_artifact_digest = _load(
        mandate_path,
        label="actor mandate",
        expected_envelope_schema_version=MANDATE_SCHEMA_VERSION,
    )
    del mandate_raw
    _validate_document(mandate, schema_path=MANDATE_SCHEMA, label="actor mandate")
    _require(
        mandate.get("mandate_digest")
        == semantic_self_digest(mandate, "mandate_digest"),
        "actor mandate semantic digest mismatch",
    )
    mandate_ref = _require_ref(
        {
            "object_id": mandate.get("mandate_id"),
            "owner_repo": "aoa-agents",
            "schema_version": mandate.get("schema_version"),
            "digest": mandate.get("mandate_digest"),
        },
        label="actor mandate ref",
        owner_repo="aoa-agents",
        schema_version="actor-mandate-v1",
    )
    _sdk_request_raw, sdk_request, sdk_request_digest = _load(
        sdk_summon_request_path,
        label="SDK summon request",
        expected_envelope_schema_version=SDK_SUMMON_REQUEST_SCHEMA_VERSION,
    )
    _sdk_decision_raw, sdk_decision, sdk_decision_digest = _load(
        sdk_summon_decision_path,
        label="SDK summon decision",
        expected_envelope_schema_version=SDK_SUMMON_DECISION_SCHEMA_VERSION,
    )
    _runtime_raw, runtime, runtime_artifact_digest = _load(
        runtime_result_path,
        label="runtime result",
        expected_envelope_schema_version=RUNTIME_RESULT_SCHEMA_VERSION,
    )
    _a2a_raw, reviewed_return, reviewed_return_digest, reviewed_return_metadata = (
        _load_with_metadata(reviewed_a2a_return_path, label="reviewed A2A return")
    )
    _review_request_raw, review_request, review_request_digest = _load(
        review_summon_request_path,
        label="review summon request",
        expected_envelope_schema_version=SDK_SUMMON_REQUEST_SCHEMA_VERSION,
    )
    incarnation = _validate_external_request(request)
    cohort_pattern = _validate_sdk_chain(
        request,
        incarnation,
        sdk_request,
        sdk_request_digest,
        sdk_decision,
        sdk_decision_digest,
    )
    runtime["artifact_digest"] = runtime_artifact_digest
    runtime_ref, handles = _validate_runtime(
        runtime,
        request,
        request_artifact_digest,
    )
    usage_ref = _usage_ref(
        runtime,
        runtime_ref,
        usage_pointer=usage_pointer,
        usage_observation_ref=usage_observation_ref,
    )
    a2a_ref = _validate_reviewed_return(
        reviewed_return,
        request,
        runtime,
        runtime_ref,
        sdk_request_digest=sdk_request_digest,
        reviewed_return_digest=reviewed_return_digest,
        reviewed_return_metadata=reviewed_return_metadata,
    )
    _validate_review_request(
        review_request,
        review_request_digest=review_request_digest,
        reviewed_return=reviewed_return,
        runtime=runtime,
        runtime_ref=runtime_ref,
    )
    profile_ref = _runtime_profile_ref(
        runtime_profile_ref=runtime_profile_ref,
        runtime_profile_path=runtime_profile_path,
    )
    _validate_incarnation_binding(
        incarnation_binding,
        binding_digest=incarnation_binding_digest,
        request=request,
        incarnation=incarnation,
        runtime=runtime,
        runtime_profile_ref=profile_ref,
        mandate_ref=mandate_ref,
        mandate_artifact_digest=mandate_artifact_digest,
    )
    _validate_mandate_chain(
        obligation,
        mandate,
        binding=incarnation_binding,
        request=request,
        incarnation=incarnation,
    )
    output_checks = _output_checks(
        request["expected_outputs"],
        reviewed_return,
        runtime_ref,
        output_artifact_refs,
    )
    result: dict[str, Any] = {
        "allowed": True,
        "lane": "external_cli_reviewed",
        "execution_surface": incarnation["runtime_interface"],
        "cohort_pattern": cohort_pattern,
        "closeout_required": True,
        "decision_state": "allowed",
        "binding": {
            "interface": incarnation["runtime_interface"],
            "inspected": True,
            "available": True,
            "reason": None,
            "binding_kind": "external_cli_incarnation",
            "runtime_owner": "abyss-stack",
            "role_resolution_ref": _require_ref(
                incarnation["role_resolution_ref"],
                label="role resolution ref",
                owner_repo="aoa-agents",
                schema_version="aoa_role_resolution_v1",
            ),
            "model_fit_query_result_ref": _require_ref(
                incarnation["model_fit_query_result_ref"],
                label="model-fit query ref",
                owner_repo="aoa-models",
                schema_version="aoa_model_fit_query_result_v2",
            ),
            "model_fit_projection_ref": _require_ref(
                incarnation["model_fit_projection_ref"],
                label="model-fit projection ref",
                owner_repo="aoa-models",
                schema_version="aoa_model_fit_projection_v1",
            ),
            "model_realization_ref": _require_ref(
                incarnation["model_realization_ref"],
                label="model realization ref",
                owner_repo="aoa-models",
                schema_version="aoa_model_realization_v1",
            ),
            "run_plan_ref": _require_ref(
                incarnation["run_plan_ref"],
                label="run plan ref",
                owner_repo="aoa-sdk",
                schema_version="aoa_control_plane_v1",
            ),
            "incarnation_binding_ref": _require_ref(
                incarnation["incarnation_binding_ref"],
                label="incarnation binding ref",
                owner_repo="aoa-sdk",
                schema_version="aoa_agent_incarnation_binding_v2",
            ),
            "sdk_summon_request_ref": _require_ref(
                incarnation["sdk_summon_request_ref"],
                label="SDK summon request ref",
                owner_repo="aoa-sdk",
                schema_version="urn:aoa-sdk:a2a:summon-request:v4",
            ),
            "sdk_summon_decision_ref": _require_ref(
                incarnation["sdk_summon_decision_ref"],
                label="SDK summon decision ref",
                owner_repo="aoa-sdk",
                schema_version="urn:aoa-sdk:a2a:summon-result:v4",
            ),
            "runtime_profile_ref": profile_ref,
            "uses_builtin_codex_subagents": False,
        },
        "runtime_state": {
            "state": "accepted",
            "child_handle": None,
            **handles,
            "runtime_result_ref": runtime_ref,
            "runtime_a2a_return_ref": a2a_ref,
            "usage_observation_ref": usage_ref,
        },
        "return_validation": {
            "output_checks": output_checks,
            "accepted": True,
        },
        "closeout_handoff": {
            "parent_owner": _require_string(
                request.get("return_owner"), "request return owner"
            ),
            "residual_risk": "Owner acceptance, publication, and stronger-owner artifact meaning remain outside aoa-summon.",
            "next_route": "aoa-agents:review-and-owner-acceptance",
        },
        "actual_effects": ["external-actor-runtime"],
        "stop_line": _require_string(
            request.get("child_stop_line"), "request stop line"
        ),
        "request_ref": request["request_ref"],
        "request_digest": request["request_digest"],
        "request_intent": request["intent"],
        "reason_codes": [
            "terminal_runtime_result",
            "reviewed_a2a_return",
            "usage_observation_located",
            "named_outputs_validated",
        ],
        "checkpoint_required": False,
        "progression_required": False,
        "requested_posture": None,
        "blocked_actions": [],
        "codex_local_target": None,
        "return_plan": None,
        "checkpoint_bridge_plan": None,
        "return_receipt_plan": None,
        "memo_export_plan": None,
        "owner_publication_plan": [],
    }
    _validate_result(result)
    return result


def _write(path: Path, payload: Mapping[str, Any]) -> None:
    location = path.resolve()
    _require(not path.is_symlink(), "output must not be a symlink")
    _require(location.parent.is_dir(), "output parent directory is absent")
    _require(not location.exists(), "output must be a new file")
    with location.open("xb") as output:
        output.write(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode(
                "utf-8"
            )
            + b"\n"
        )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--request", dest="request_path", type=Path, required=True)
    result.add_argument("--incarnation-binding", type=Path, required=True)
    result.add_argument("--obligation", dest="obligation_path", type=Path, required=True)
    result.add_argument("--mandate", dest="mandate_path", type=Path, required=True)
    result.add_argument("--sdk-summon-request", type=Path, required=True)
    result.add_argument("--sdk-summon-decision", type=Path, required=True)
    result.add_argument("--runtime-result", type=Path, required=True)
    result.add_argument("--reviewed-a2a-return", type=Path, required=True)
    result.add_argument("--review-summon-request", type=Path, required=True)
    profile = result.add_mutually_exclusive_group(required=True)
    profile.add_argument("--runtime-profile", dest="runtime_profile_path", type=Path)
    profile.add_argument(
        "--runtime-profile-ref", dest="runtime_profile_ref_path", type=Path
    )
    result.add_argument("--usage-pointer", default="/usage_observation")
    result.add_argument("--usage-observation-ref", type=Path)
    result.add_argument("--output", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        profile_ref = None
        if args.runtime_profile_ref_path is not None:
            _raw, profile_ref, _digest = _load(
                args.runtime_profile_ref_path, label="runtime profile ref"
            )
        usage_ref = None
        if args.usage_observation_ref is not None:
            _raw, usage_ref, _digest = _load(
                args.usage_observation_ref, label="usage observation ref"
            )
        result = compile_external_execution_result(
            request_path=args.request_path,
            incarnation_binding_path=args.incarnation_binding,
            obligation_path=args.obligation_path,
            mandate_path=args.mandate_path,
            sdk_summon_request_path=args.sdk_summon_request,
            sdk_summon_decision_path=args.sdk_summon_decision,
            runtime_result_path=args.runtime_result,
            reviewed_a2a_return_path=args.reviewed_a2a_return,
            review_summon_request_path=args.review_summon_request,
            runtime_profile_ref=profile_ref,
            runtime_profile_path=args.runtime_profile_path,
            usage_pointer=args.usage_pointer,
            usage_observation_ref=usage_ref,
        )
        _write(args.output, result)
    except (ExternalExecutionResultError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(
        json.dumps(
            {
                "ok": True,
                "output": str(args.output.resolve()),
                "request_ref": result["request_ref"],
                "request_digest": result["request_digest"],
                "started": False,
                "runtime_state": result["runtime_state"]["state"],
                "next_route": result["closeout_handoff"]["next_route"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
