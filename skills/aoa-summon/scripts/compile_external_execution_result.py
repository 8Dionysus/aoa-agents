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
RESULT_SCHEMA = SUMMON_ROOT / "references" / "summon-result-v4.schema.json"
ZERO_DIGEST = "sha256:" + "0" * 64
TERMINAL_RUNTIME_STATUSES = {"completed", "failed", "review_required", "authority_blocked"}
SUCCESS_REVIEW_OUTCOMES = {"proceed"}


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


def _load(path: Path, *, label: str) -> tuple[bytes, dict[str, Any], str]:
    """Load a raw JSON artifact or an immutable actor input envelope.

    Envelopes carry the original owner digest in ``source_artifact_digest``;
    using it preserves the source artifact identity rather than addressing the
    runtime's safe derivative wrapper.
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
    if loaded.get("schema_version") == "abyss_stack_external_codex_actor_input_envelope_v1":
        payload = loaded.get("payload")
        if not isinstance(payload, dict):
            raise ExternalExecutionResultError(
                f"{label} actor envelope must contain a JSON payload"
            )
        artifact_digest = loaded.get("source_artifact_digest")
        if not isinstance(artifact_digest, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", artifact_digest) is None:
            raise ExternalExecutionResultError(
                f"{label} actor envelope has no source artifact digest"
            )
        return raw, payload, artifact_digest
    return raw, loaded, digest_bytes(raw)


def _validate_result(result: Mapping[str, Any]) -> None:
    try:
        schema = json.loads(RESULT_SCHEMA.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalExecutionResultError(
            f"summon-result-v4 schema is unavailable: {RESULT_SCHEMA}"
        ) from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(result),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path)
        where = f" at {path}" if path else ""
        raise ExternalExecutionResultError(
            f"compiled summon-result-v4 is invalid{where}: {errors[0].message}"
        )


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ExternalExecutionResultError(message)


def _require_string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{label} is absent")
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
            schema_version="abyss_stack_external_codex_runtime_profile_v2",
        )
    assert runtime_profile_path is not None
    raw, payload, artifact_digest = _load(runtime_profile_path, label="runtime profile")
    del raw
    return _content_ref_from_artifact(
        artifact_digest,
        payload,
        label="runtime profile",
        owner_repo="abyss-stack",
        schema_version="abyss_stack_external_codex_runtime_profile_v2",
        object_keys=("profile_id", "runtime_profile_id", "id"),
    )


def _usage_ref(
    runtime: Mapping[str, Any],
    runtime_ref: Mapping[str, Any],
    *,
    usage_pointer: str,
    usage_observation_ref: Mapping[str, Any] | None,
    usage_observation_path: Path | None,
) -> dict[str, Any]:
    _require(
        not (usage_observation_ref is not None and usage_observation_path is not None),
        "provide one standalone usage ref or usage artifact, not both",
    )
    if usage_observation_ref is not None:
        return _require_ref(
            usage_observation_ref,
            label="usage observation ref",
            owner_repo="abyss-stack",
            schema_version="abyss_stack_external_codex_usage_observation_v1",
        )
    if usage_observation_path is not None:
        _raw, payload, artifact_digest = _load(
            usage_observation_path, label="usage observation artifact"
        )
        return _content_ref_from_artifact(
            artifact_digest,
            payload,
            label="usage observation artifact",
            owner_repo="abyss-stack",
            schema_version="abyss_stack_external_codex_usage_observation_v1",
            object_keys=("usage_observation_id", "observation_id", "id", "object_id"),
        )
    usage_value = _json_pointer(runtime, usage_pointer)
    return {
        "object_id": f"{runtime_ref['object_id']}#{usage_pointer}",
        "owner_repo": "abyss-stack",
        "schema_version": "abyss_stack_external_codex_usage_observation_v1",
        "digest": digest_bytes(canonical_bytes(usage_value)),
    }


def _validate_external_request(request: Mapping[str, Any]) -> dict[str, Any]:
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
        and effects[0] == "repo_mutation",
        "request effect ceiling is not the admitted repo mutation scope",
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
        ("return_event_schema_ref", "abyss-stack", "abyss_stack_external_codex_event_v1"),
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
        _require_string(procedure.get("object_id"), f"domain procedure {index} object identity")
        _require_string(procedure.get("owner_repo"), f"domain procedure {index} owner")
        _require_string(procedure.get("schema_version"), f"domain procedure {index} schema")
        _require(
            isinstance(procedure.get("digest"), str)
            and re.fullmatch(r"sha256:[0-9a-f]{64}", procedure["digest"]) is not None,
            f"domain procedure {index} digest is invalid",
        )
    _require(incarnation.get("runtime_interface"), "runtime interface is absent")
    _require(incarnation.get("launches_separate_os_process") is True, "separate process was not bound")
    _require(incarnation.get("separate_cli_session") is True, "separate CLI session was not bound")
    _require(incarnation.get("uses_builtin_codex_subagents") is False, "built-in subagents are enabled")
    _require(
        incarnation.get("usage_metering") == "observe_only_no_budget",
        "usage metering is not observe-only",
    )
    transfer = incarnation["responsibility_transfer_ref"]
    _require(transfer.get("admitted_state") in {"accepted", "launched", "narrowed"}, "responsibility transfer is not admitted")
    holders = transfer.get("holder_ids")
    _require(isinstance(holders, list) and len(holders) == 2 and len(set(holders)) == 2, "responsibility holders are not distinct")
    return dict(incarnation)


def _validate_sdk_chain(
    request: Mapping[str, Any],
    incarnation: Mapping[str, Any],
    sdk_request: Mapping[str, Any],
    sdk_request_digest: str,
    sdk_decision: Mapping[str, Any],
    sdk_decision_digest: str,
) -> None:
    _require(
        sdk_request.get("schema_version") in {
            None,
            "urn:aoa-sdk:a2a:summon-request:v4",
            "summon-request-v4",
        },
        "SDK summon request schema is invalid",
    )
    sdk_summon = sdk_request.get("summon_request")
    _require(isinstance(sdk_summon, Mapping), "SDK summon request body is absent")
    _require(
        sdk_summon.get("transport_preference") in {"a2a_remote", "either", "external_cli"},
        "SDK summon request does not authorize an external transport",
    )
    sdk_outputs = sdk_request.get("expected_outputs")
    requested_outputs = request.get("expected_outputs")
    _require(
        isinstance(sdk_outputs, list)
        and set(sdk_outputs) == set(requested_outputs),
        "SDK and owner request output keys differ",
    )
    _require(sdk_decision.get("schema_version") == "urn:aoa-sdk:a2a:summon-result:v4", "SDK summon decision schema is invalid")
    _require(sdk_decision.get("allowed") is True, "SDK summon decision is not allowed")
    _require(sdk_decision.get("capability_execution_claimed") is False, "SDK decision claims runtime execution")
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


def _process_handle(runtime: Mapping[str, Any]) -> str:
    invocations = runtime.get("codex_invocations")
    _require(isinstance(invocations, list) and bool(invocations), "runtime process evidence is absent")
    invocation = invocations[-1]
    _require(isinstance(invocation, Mapping), "runtime process evidence is invalid")
    process_ref = invocation.get("process_identity_ref")
    _require(isinstance(process_ref, Mapping), "runtime process identity ref is absent")
    return _require_string(process_ref.get("artifact_ref"), "runtime process handle")


def _validate_runtime(
    runtime: Mapping[str, Any],
    request: Mapping[str, Any],
) -> tuple[dict[str, str], dict[str, str]]:
    _require(runtime.get("schema_version") == "abyss_stack_external_codex_result_v2", "runtime result schema is invalid")
    _require(runtime.get("status") in TERMINAL_RUNTIME_STATUSES, "runtime result is nonterminal")
    _require(
        runtime.get("status") in {"completed", "review_required"},
        "runtime result cannot support an accepted closeout",
    )
    _require(runtime.get("execution_posture") in {"bounded_execution", "closeout"}, "runtime execution posture exceeds the mandate")
    _require(runtime.get("admission_class") == "owner_contour", "runtime admission class is not owner-contour")
    _require_string(runtime.get("task_id"), "runtime task id")
    _require_string(runtime.get("incarnation_id"), "runtime incarnation id")
    _require_string(runtime.get("session_id"), "runtime session id")
    _require_string(runtime.get("thread_id"), "runtime continuation id")
    usage = runtime.get("usage_observation")
    _require(isinstance(usage, Mapping), "runtime usage observation is absent")
    _require(usage.get("status") in {"complete", "partial"}, "runtime usage observation status is invalid")
    _require(isinstance(usage.get("gap_reasons"), list), "runtime usage gaps are invalid")
    invocations = runtime.get("codex_invocations")
    _require(isinstance(invocations, list) and bool(invocations), "runtime invocation evidence is absent")
    for invocation in invocations:
        _require(isinstance(invocation, Mapping), "runtime invocation evidence is invalid")
        argv = invocation.get("argv")
        _require(isinstance(argv, list), "runtime invocation argv is absent")
        _require(
            not bool(invocation.get("uses_builtin_codex_subagents", False)),
            "runtime invocation claims built-in subagent use",
        )
        _require(
            any(argv[index:index + 2] == ["--disable", "multi_agent"] for index in range(max(0, len(argv) - 1))),
            "runtime invocation does not disable built-in subagents",
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
    continuation_handle = _require_string(runtime.get("thread_id"), "continuation handle")
    handles = {
        "actor_handle": actor_handle,
        "process_handle": process_handle,
        "session_handle": session_handle,
        "continuation_handle": continuation_handle,
    }
    if runtime.get("exit_code") is not None and runtime.get("status") != "failed":
        _require(runtime.get("exit_code") == 0, "successful runtime result has a nonzero exit code")
    _require(
        runtime.get("incarnation_id") == request.get("summon_request", {}).get("child_agent_id"),
        "runtime incarnation differs from the summon request",
    )
    return runtime_ref, handles


def _validate_reviewed_return(
    reviewed_return: Mapping[str, Any],
    request: Mapping[str, Any],
    runtime: Mapping[str, Any],
    *,
    reviewed_return_digest: str,
) -> dict[str, str]:
    _require(reviewed_return.get("reviewed") is True, "A2A return is not reviewed")
    _require(reviewed_return.get("review_status") == "reviewed", "A2A review status is not reviewed")
    _require(reviewed_return.get("reviewer_status") == "completed", "A2A reviewer is not terminal")
    _require(reviewed_return.get("reviewer_decision") in SUCCESS_REVIEW_OUTCOMES, "A2A reviewer disposition is not accepting")
    _require(reviewed_return.get("review_outcome") in SUCCESS_REVIEW_OUTCOMES, "A2A review outcome is not accepting")
    remote_task = reviewed_return.get("remote_task")
    _require(isinstance(remote_task, Mapping), "A2A remote task is absent")
    _require(remote_task.get("state") == "completed", "A2A remote task is nonterminal")
    _require_string(remote_task.get("task_id"), "A2A remote task id")
    original_ref = reviewed_return.get("summon_request_ref")
    expected_ref = request["external_incarnation"]["sdk_summon_request_ref"]
    original_ref = _require_ref(
        original_ref,
        label="reviewed A2A summon request ref",
        owner_repo="aoa-sdk",
        schema_version="urn:aoa-sdk:a2a:summon-request:v4",
    )
    _require(
        original_ref["digest"] == expected_ref.get("digest"),
        "reviewed A2A return names another summon request",
    )
    _require_ref(
        reviewed_return.get("review_summon_request_ref"),
        label="reviewed A2A review request ref",
        owner_repo="aoa-sdk",
        schema_version="urn:aoa-sdk:a2a:summon-request:v4",
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
    if explicit_artifact_refs is not None:
        _require(
            set(explicit_artifact_refs) == set(expected_outputs),
            "explicit output refs do not match request output keys",
        )
        artifacts = dict(explicit_artifact_refs)
        returned = reviewed_return["remote_task"].get("returned_artifacts")
        _require(isinstance(returned, list), "A2A returned artifacts are absent")
        allowed = {item for item in returned if isinstance(item, str)}
        allowed.add(str(runtime_ref["object_id"]))
        _require(
            all(value in allowed for value in artifacts.values()),
            "explicit output refs are not linked to the reviewed A2A return",
        )
    else:
        remote_task = reviewed_return["remote_task"]
        returned = remote_task.get("returned_artifacts")
        _require(isinstance(returned, list), "A2A returned artifacts are absent")
        artifacts_by_name: dict[str, str] = {}
        for artifact in returned:
            if not isinstance(artifact, str) or not artifact:
                raise ExternalExecutionResultError("A2A returned artifact identity is invalid")
            name = Path(artifact).name
            candidates = {artifact, name}
            for output in expected_outputs:
                if output in candidates or artifact.endswith("/" + output):
                    if output in artifacts_by_name and artifacts_by_name[output] != artifact:
                        raise ExternalExecutionResultError(f"A2A returned duplicate output: {output}")
                    artifacts_by_name[output] = artifact
        artifacts = dict(artifacts_by_name)
        if "external_codex_agent_result" in expected_outputs and "external_codex_agent_result" not in artifacts:
            artifacts["external_codex_agent_result"] = str(runtime_ref["object_id"])
    _require(set(artifacts) == set(expected_outputs), "A2A returned output keys do not match the request")
    return {
        output: {
            "received": True,
            "artifact_ref": _require_string(artifacts[output], f"output {output} artifact ref"),
            "accepted": True,
        }
        for output in expected_outputs
    }


def compile_external_execution_result(
    *,
    request_path: Path,
    sdk_summon_request_path: Path,
    sdk_summon_decision_path: Path,
    runtime_result_path: Path,
    reviewed_a2a_return_path: Path,
    runtime_profile_ref: Mapping[str, Any] | None = None,
    runtime_profile_path: Path | None = None,
    usage_pointer: str = "/usage_observation",
    usage_observation_ref: Mapping[str, Any] | None = None,
    usage_observation_path: Path | None = None,
    output_artifact_refs: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Compile one exact terminal, reviewed external execution chain."""

    _request_raw, request, _request_digest = _load(request_path, label="summon request")
    _sdk_request_raw, sdk_request, sdk_request_digest = _load(
        sdk_summon_request_path, label="SDK summon request"
    )
    _sdk_decision_raw, sdk_decision, sdk_decision_digest = _load(
        sdk_summon_decision_path, label="SDK summon decision"
    )
    _runtime_raw, runtime, runtime_artifact_digest = _load(
        runtime_result_path, label="runtime result"
    )
    _a2a_raw, reviewed_return, reviewed_return_digest = _load(
        reviewed_a2a_return_path, label="reviewed A2A return"
    )
    incarnation = _validate_external_request(request)
    _validate_sdk_chain(
        request,
        incarnation,
        sdk_request,
        sdk_request_digest,
        sdk_decision,
        sdk_decision_digest,
    )
    runtime["artifact_digest"] = runtime_artifact_digest
    runtime_ref, handles = _validate_runtime(runtime, request)
    usage_ref = _usage_ref(
        runtime,
        runtime_ref,
        usage_pointer=usage_pointer,
        usage_observation_ref=usage_observation_ref,
        usage_observation_path=usage_observation_path,
    )
    a2a_ref = _validate_reviewed_return(
        reviewed_return,
        request,
        runtime,
        reviewed_return_digest=reviewed_return_digest,
    )
    profile_ref = _runtime_profile_ref(
        runtime_profile_ref=runtime_profile_ref,
        runtime_profile_path=runtime_profile_path,
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
        "cohort_pattern": sdk_decision.get("cohort_pattern") or "solo",
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
            "parent_owner": _require_string(request.get("return_owner"), "request return owner"),
            "residual_risk": "Owner acceptance, publication, and stronger-owner artifact meaning remain outside aoa-summon.",
            "next_route": "aoa-agents:review-and-owner-acceptance",
        },
        "actual_effects": ["external-actor-runtime"],
        "stop_line": _require_string(request.get("child_stop_line"), "request stop line"),
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
    location.write_bytes(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
        + b"\n"
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--request", dest="request_path", type=Path, required=True)
    result.add_argument("--sdk-summon-request", type=Path, required=True)
    result.add_argument("--sdk-summon-decision", type=Path, required=True)
    result.add_argument("--runtime-result", type=Path, required=True)
    result.add_argument("--reviewed-a2a-return", type=Path, required=True)
    profile = result.add_mutually_exclusive_group(required=True)
    profile.add_argument("--runtime-profile", dest="runtime_profile_path", type=Path)
    profile.add_argument("--runtime-profile-ref", dest="runtime_profile_ref_path", type=Path)
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
        result = compile_external_execution_result(
            request_path=args.request_path,
            sdk_summon_request_path=args.sdk_summon_request,
            sdk_summon_decision_path=args.sdk_summon_decision,
            runtime_result_path=args.runtime_result,
            reviewed_a2a_return_path=args.reviewed_a2a_return,
            runtime_profile_ref=profile_ref,
            runtime_profile_path=args.runtime_profile_path,
            usage_pointer=args.usage_pointer,
            usage_observation_path=args.usage_observation_ref,
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
