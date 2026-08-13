#!/usr/bin/env python3
"""Compile one evidence-complete aoa-summon v4 external execution request.

All semantic selections and stronger-owner bindings must already exist.  This
compiler checks their exact relationship and emits no runtime effect.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


SUMMON_ROOT = Path(__file__).resolve().parents[1]
AGENT_REFERENCES = SUMMON_ROOT.parent / "aoa-agents-skills" / "references"
REQUEST_SCHEMA = SUMMON_ROOT / "references" / "summon-request-v4.schema.json"
ZERO_DIGEST = "sha256:" + "0" * 64
SDK_BINDING_V2_SCHEMA_DIGEST = (
    "sha256:e62e4b27fcb8d76ad80e1f7b9e66b510d8e076de77c1714988daac4d98deb529"
)


class ExternalExecutionRequestError(ValueError):
    """One required owner artifact or exact relationship is invalid."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def semantic_request_digest(value: Mapping[str, Any]) -> str:
    candidate = dict(value)
    candidate.pop("request_digest", None)
    return digest_bytes(canonical_bytes(candidate))


def semantic_self_digest(value: Mapping[str, Any], field: str) -> str:
    return digest_bytes(canonical_bytes(dict(value) | {field: ZERO_DIGEST}))


def sdk_semantic_excluding_digest(value: Mapping[str, Any], field: str) -> str:
    """Match aoa-sdk canonical_digest(..., exclude={field}) exactly."""

    candidate = dict(value)
    candidate.pop(field, None)
    encoded = json.dumps(
        candidate,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return digest_bytes(encoded)


def _load(path: Path, *, label: str) -> tuple[bytes, dict[str, Any]]:
    location = path.resolve()
    if path.is_symlink() or not location.is_file():
        raise ExternalExecutionRequestError(
            f"{label} must be an exact regular non-symlink file: {path}"
        )
    try:
        raw = location.read_bytes()
        payload = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalExecutionRequestError(f"{label} is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise ExternalExecutionRequestError(f"{label} must be a JSON object")
    return raw, payload


def _validate(payload: dict[str, Any], schema_path: Path, *, label: str) -> None:
    try:
        schema = json.loads(schema_path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalExecutionRequestError(
            f"{label} schema is unavailable: {schema_path}"
        ) from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path)
        where = f" at {path}" if path else ""
        raise ExternalExecutionRequestError(
            f"{label} violates {schema_path.name}{where}: {errors[0].message}"
        )


def _semantic_ref(
    payload: Mapping[str, Any],
    *,
    object_field: str,
    owner_repo: str,
    schema_version: str,
    digest_field: str,
    label: str,
) -> dict[str, str]:
    if payload.get("schema_version") != schema_version:
        raise ExternalExecutionRequestError(f"{label} must use {schema_version}")
    expected = semantic_self_digest(payload, digest_field)
    if payload.get(digest_field) != expected:
        raise ExternalExecutionRequestError(f"{label} semantic digest mismatch")
    object_id = payload.get(object_field)
    if not isinstance(object_id, str) or not object_id:
        raise ExternalExecutionRequestError(f"{label} object identity is absent")
    return {
        "object_id": object_id,
        "owner_repo": owner_repo,
        "schema_version": schema_version,
        "digest": expected,
    }


def _raw_ref(
    raw: bytes,
    payload: Mapping[str, Any],
    *,
    object_field: str,
    owner_repo: str,
    schema_version: str,
    label: str,
) -> dict[str, str]:
    if payload.get("schema_version") != schema_version:
        raise ExternalExecutionRequestError(f"{label} must use {schema_version}")
    object_id = payload.get(object_field)
    if not isinstance(object_id, str) or not object_id:
        raise ExternalExecutionRequestError(f"{label} object identity is absent")
    return {
        "object_id": object_id,
        "owner_repo": owner_repo,
        "schema_version": schema_version,
        "digest": digest_bytes(raw),
    }


def _content_from_provenance(value: Mapping[str, Any]) -> dict[str, str]:
    return {
        "object_id": str(value["artifact_ref"]),
        "owner_repo": str(value["owner_repo"]),
        "schema_version": str(value["schema_version"]),
        "digest": str(value["artifact_digest"]),
    }


def _require_equal(actual: Any, expected: Any, *, label: str) -> None:
    if actual != expected:
        raise ExternalExecutionRequestError(
            f"{label} differs from its exact owner binding"
        )


def _validate_permission_posture(
    binding: Mapping[str, Any],
    runtime_task: Mapping[str, Any],
    mandate: Mapping[str, Any],
) -> None:
    """Validate the SDK posture and bind it to both owner effect ceilings."""

    permission = binding.get("permission_posture")
    if not isinstance(permission, Mapping):
        raise ExternalExecutionRequestError(
            "incarnation binding permission posture is absent"
        )
    required = {
        "sandbox_mode",
        "approval_policy",
        "allowed_effect_classes",
        "network_access",
    }
    allowed = required | {"external_effects", "secret_access"}
    if required - set(permission) or set(permission) - allowed:
        raise ExternalExecutionRequestError(
            "incarnation binding permission posture shape is invalid"
        )
    if permission.get("sandbox_mode") not in {
        "read_only",
        "workspace_write",
        "danger_full_access",
    }:
        raise ExternalExecutionRequestError(
            "incarnation binding sandbox mode is invalid"
        )
    if permission.get("approval_policy") not in {
        "never",
        "on_request",
        "on_failure",
        "untrusted",
    }:
        raise ExternalExecutionRequestError(
            "incarnation binding approval policy is invalid"
        )
    if permission.get("network_access") not in {
        "disabled",
        "allowlisted",
        "enabled",
    }:
        raise ExternalExecutionRequestError(
            "incarnation binding network access is invalid"
        )

    effects = permission.get("allowed_effect_classes")
    if (
        not isinstance(effects, list)
        or not effects
        or any(not isinstance(item, str) or not item for item in effects)
        or len(effects) != len(set(effects))
        or not set(effects)
        <= {"read_only", "repo_mutation", "runtime_mutation", "external"}
    ):
        raise ExternalExecutionRequestError(
            "incarnation binding allowed effect classes are invalid"
        )
    for field in ("external_effects", "secret_access"):
        if field in permission and not isinstance(permission[field], bool):
            raise ExternalExecutionRequestError(
                f"incarnation binding {field} is invalid"
            )

    external_effects = permission.get("external_effects", False)
    secret_access = permission.get("secret_access", False)
    if external_effects != ("external" in effects):
        raise ExternalExecutionRequestError(
            "incarnation binding external-effects flag differs from its effect ceiling"
        )
    if permission.get("sandbox_mode") == "read_only" and set(effects) != {
        "read_only"
    }:
        raise ExternalExecutionRequestError(
            "incarnation binding read-only sandbox admits non-read-only effects"
        )
    if secret_access and permission.get("approval_policy") == "never":
        raise ExternalExecutionRequestError(
            "incarnation binding secret access cannot use approval_policy=never"
        )

    runtime_effect = runtime_task.get("allowed_effect_class")
    mandate_effects = mandate.get("authority", {}).get("allowed_effects")
    if (
        runtime_effect not in {"read_only", "repo_mutation"}
        or not isinstance(mandate_effects, list)
        or not mandate_effects
        or any(not isinstance(item, str) or not item for item in mandate_effects)
        or len(mandate_effects) != len(set(mandate_effects))
        or set(effects) != {runtime_effect}
        or set(effects) != set(mandate_effects)
    ):
        raise ExternalExecutionRequestError(
            "incarnation effect posture differs from runtime task or actor mandate"
        )


def _validate_tool_profile(
    binding: Mapping[str, Any],
    mandate: Mapping[str, Any],
) -> None:
    """Bind the SDK tool profile to the actor mandate before runtime launch."""

    tool_profile = binding.get("tool_profile")
    if not isinstance(tool_profile, Mapping):
        raise ExternalExecutionRequestError(
            "incarnation binding tool profile is absent"
        )
    required = {"profile_id", "profile_ref", "required_tool_ids"}
    allowed = required | {
        "required_mcp_server_ids",
        "inherit_user_configuration",
    }
    if required - set(tool_profile) or set(tool_profile) - allowed:
        raise ExternalExecutionRequestError(
            "incarnation binding tool profile shape is invalid"
        )
    if not isinstance(tool_profile.get("profile_id"), str) or not tool_profile[
        "profile_id"
    ]:
        raise ExternalExecutionRequestError(
            "incarnation binding tool profile identity is invalid"
        )
    profile_ref = tool_profile.get("profile_ref")
    runtime_profile_ref = binding.get("runtime_profile_ref")
    if not isinstance(profile_ref, Mapping) or profile_ref != runtime_profile_ref:
        raise ExternalExecutionRequestError(
            "incarnation tool profile ref differs from runtime profile ref"
        )
    if (
        "inherit_user_configuration" in tool_profile
        and tool_profile["inherit_user_configuration"] is not False
    ):
        raise ExternalExecutionRequestError(
            "incarnation binding cannot inherit user configuration"
        )

    environment = mandate.get("environment")
    if not isinstance(environment, Mapping):
        raise ExternalExecutionRequestError("actor mandate environment is absent")

    def require_strings(
        value: Any,
        *,
        label: str,
        nonempty: bool,
    ) -> list[str]:
        if (
            not isinstance(value, list)
            or (nonempty and not value)
            or any(not isinstance(item, str) or not item for item in value)
            or len(value) != len(set(value))
        ):
            raise ExternalExecutionRequestError(f"{label} is invalid")
        return value

    binding_tools = require_strings(
        tool_profile.get("required_tool_ids"),
        label="incarnation binding required tool ids",
        nonempty=True,
    )
    mandate_tools = require_strings(
        environment.get("required_tools"),
        label="actor mandate required tools",
        nonempty=True,
    )
    if set(binding_tools) != set(mandate_tools):
        raise ExternalExecutionRequestError(
            "incarnation tool ceiling differs from actor mandate"
        )

    binding_mcp = require_strings(
        tool_profile.get("required_mcp_server_ids", []),
        label="incarnation binding required MCP server ids",
        nonempty=False,
    )
    mandate_mcp = require_strings(
        environment.get("required_mcp_servers"),
        label="actor mandate required MCP servers",
        nonempty=False,
    )
    if set(binding_mcp) != set(mandate_mcp):
        raise ExternalExecutionRequestError(
            "incarnation MCP ceiling differs from actor mandate"
        )


def _validate_obligation_mandate_chain(
    obligation: Mapping[str, Any],
    mandate: Mapping[str, Any],
    sdk_request: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> None:
    """Keep the formed obligation's goal and lifecycle exact before launch."""

    obligation_goal = obligation.get("goal_ref")
    mandate_goal = mandate.get("goal_ref")
    if not isinstance(obligation_goal, Mapping) or not isinstance(
        mandate_goal, Mapping
    ):
        raise ExternalExecutionRequestError(
            "obligation or mandate goal ref is absent"
        )
    _require_equal(
        mandate_goal,
        obligation_goal,
        label="mandate goal and originating obligation goal",
    )

    quest_passport = sdk_request.get("quest_passport")
    if not isinstance(quest_passport, Mapping):
        raise ExternalExecutionRequestError("SDK request quest passport is absent")
    _require_equal(
        quest_passport.get("route_anchor"),
        obligation_goal.get("object_id"),
        label="SDK route anchor and originating obligation goal",
    )

    lifecycle_posture = obligation.get("lifecycle_posture")
    if not isinstance(lifecycle_posture, str) or not lifecycle_posture:
        raise ExternalExecutionRequestError(
            "originating obligation lifecycle posture is absent"
        )
    _require_equal(
        mandate.get("identity_posture"),
        lifecycle_posture,
        label="mandate identity and obligation lifecycle posture",
    )
    continuity = mandate.get("continuity")
    if not isinstance(continuity, Mapping):
        raise ExternalExecutionRequestError("actor mandate continuity is absent")
    _require_equal(
        continuity.get("posture"),
        lifecycle_posture,
        label="mandate continuity and obligation lifecycle posture",
    )
    _require_equal(
        mandate.get("domain_owner"),
        obligation.get("domain_owner"),
        label="mandate and obligation domain owner",
    )
    binding_continuation = binding.get("continuation")
    if not isinstance(binding_continuation, Mapping):
        raise ExternalExecutionRequestError("incarnation continuation is absent")
    _require_equal(
        binding_continuation.get("delegated_obligation"),
        obligation.get("duty"),
        label="delegated and originating obligation duty",
    )


def _validate_sdk_decision(
    sdk_decision: Mapping[str, Any],
    *,
    sdk_request_digest: str,
) -> None:
    """Require the SDK to select the exact remote execution surface."""

    if (
        sdk_decision.get("schema_version")
        != "urn:aoa-sdk:a2a:summon-result:v4"
        or sdk_decision.get("allowed") is not True
        or sdk_decision.get("capability_execution_claimed") is not False
        or sdk_decision.get("request_artifact_digest") != sdk_request_digest
    ):
        raise ExternalExecutionRequestError("SDK summon decision is not admitted")
    if sdk_decision.get("execution_surface") != "a2a_remote":
        raise ExternalExecutionRequestError(
            "SDK summon decision does not select the remote execution surface"
        )
    cohort_pattern = sdk_decision.get("cohort_pattern")
    if not isinstance(cohort_pattern, str) or not cohort_pattern:
        raise ExternalExecutionRequestError(
            "SDK summon decision cohort pattern is absent"
        )


def _validate_incarnation_binding_artifact(
    binding: dict[str, Any],
    *,
    schema_path: Path,
) -> None:
    """Admit the complete SDK v2 artifact and its semantic self-digest."""

    try:
        schema_raw = schema_path.resolve(strict=True).read_bytes()
        schema = json.loads(schema_raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalExecutionRequestError(
            f"incarnation binding schema is unavailable: {schema_path}"
        ) from exc
    if digest_bytes(schema_raw) != SDK_BINDING_V2_SCHEMA_DIGEST:
        raise ExternalExecutionRequestError(
            "incarnation binding schema differs from the pinned SDK v2 owner contract"
        )
    if schema.get("$id") != "urn:aoa-sdk:agent-incarnation-binding:v2":
        raise ExternalExecutionRequestError(
            "incarnation binding schema is not the SDK v2 owner contract"
        )
    errors = sorted(
        Draft202012Validator(schema).iter_errors(binding),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path)
        where = f" at {path}" if path else ""
        raise ExternalExecutionRequestError(
            f"incarnation binding violates SDK v2 owner contract{where}: "
            f"{errors[0].message}"
        )
    _validate_incarnation_binding_semantic_digest(binding)


def _validate_incarnation_binding_semantic_digest(
    binding: Mapping[str, Any],
) -> None:
    if binding.get("binding_digest") != sdk_semantic_excluding_digest(
        binding,
        "binding_digest",
    ):
        raise ExternalExecutionRequestError(
            "incarnation binding semantic digest mismatch"
        )


def compile_external_execution_request(
    *,
    request_ref: str,
    runtime_interface: str,
    return_event_object_id: str,
    obligation_path: Path,
    mandate_path: Path,
    role_resolution_path: Path,
    model_fit_query_result_path: Path,
    model_fit_projection_path: Path,
    task_local_dag_path: Path,
    incarnation_binding_path: Path,
    incarnation_binding_schema_path: Path,
    sdk_summon_request_path: Path,
    sdk_summon_decision_path: Path,
    run_plan_path: Path,
    runtime_launch_path: Path,
    runtime_task_path: Path,
    responsibility_transfer_path: Path,
    domain_procedure_paths: Sequence[Path],
    return_event_schema_path: Path,
) -> dict[str, Any]:
    """Compile exact supplied artifacts; never select or launch an actor."""

    if not request_ref or not runtime_interface or not return_event_object_id:
        raise ExternalExecutionRequestError(
            "request, runtime-interface, and return-event identities are required"
        )
    if not domain_procedure_paths:
        raise ExternalExecutionRequestError("at least one domain procedure is required")

    obligation_raw, obligation = _load(obligation_path, label="agent obligation")
    mandate_raw, mandate = _load(mandate_path, label="actor mandate")
    role_raw, role_resolution = _load(role_resolution_path, label="role resolution")
    query_raw, model_fit_query = _load(
        model_fit_query_result_path, label="model-fit query result"
    )
    projection_raw, model_fit_projection = _load(
        model_fit_projection_path, label="model-fit projection"
    )
    dag_raw, task_local_dag = _load(task_local_dag_path, label="task-local DAG")
    binding_raw, binding = _load(incarnation_binding_path, label="incarnation binding")
    sdk_request_raw, sdk_request = _load(
        sdk_summon_request_path, label="SDK summon request"
    )
    sdk_decision_raw, sdk_decision = _load(
        sdk_summon_decision_path, label="SDK summon decision"
    )
    _plan_raw, run_plan = _load(run_plan_path, label="SDK run plan")
    launch_raw, runtime_launch = _load(runtime_launch_path, label="runtime launch")
    _task_raw, runtime_task = _load(runtime_task_path, label="runtime task")
    transfer_raw, transfer = _load(
        responsibility_transfer_path, label="responsibility transfer"
    )
    event_schema_raw, _event_schema = _load(
        return_event_schema_path, label="return-event schema"
    )

    _validate(
        obligation,
        AGENT_REFERENCES / "agent-obligation-v1.schema.json",
        label="agent obligation",
    )
    _validate(
        mandate,
        AGENT_REFERENCES / "actor-mandate-v1.schema.json",
        label="actor mandate",
    )
    _validate(
        role_resolution,
        AGENT_REFERENCES / "role-resolution-v1.schema.json",
        label="role resolution",
    )
    _validate_incarnation_binding_artifact(
        binding,
        schema_path=incarnation_binding_schema_path,
    )

    obligation_ref = _semantic_ref(
        obligation,
        object_field="obligation_id",
        owner_repo="aoa-agents",
        schema_version="agent-obligation-v1",
        digest_field="obligation_digest",
        label="agent obligation",
    )
    mandate_ref = _semantic_ref(
        mandate,
        object_field="mandate_id",
        owner_repo="aoa-agents",
        schema_version="actor-mandate-v1",
        digest_field="mandate_digest",
        label="actor mandate",
    )
    role_resolution_ref = _semantic_ref(
        role_resolution,
        object_field="resolution_id",
        owner_repo="aoa-agents",
        schema_version="aoa_role_resolution_v1",
        digest_field="resolution_digest",
        label="role resolution",
    )
    query_ref = _semantic_ref(
        model_fit_query,
        object_field="result_id",
        owner_repo="aoa-models",
        schema_version="aoa_model_fit_query_result_v2",
        digest_field="result_digest",
        label="model-fit query result",
    )

    _require_equal(
        mandate["obligation_ref"], obligation_ref, label="mandate obligation"
    )
    _require_equal(
        mandate["role_resolution_ref"],
        role_resolution_ref,
        label="mandate role resolution",
    )
    _require_equal(
        mandate["role_binding"]["role_id"],
        role_resolution["role_id"],
        label="mandate role identity",
    )
    for field in (
        "base_role_ref",
        "specialization_ref",
        "tier_ref",
        "capability_pack_refs",
    ):
        _require_equal(
            mandate["role_binding"][field],
            role_resolution[field],
            label=f"mandate role {field}",
        )

    if binding.get("schema_version") != "aoa_agent_incarnation_binding_v2":
        raise ExternalExecutionRequestError(
            "external execution requires aoa_agent_incarnation_binding_v2"
        )
    for field, expected in (
        ("agent_obligation_ref", obligation_ref),
        ("actor_mandate_ref", mandate_ref),
        ("role_resolution_ref", role_resolution_ref),
        ("model_fit_query_result_ref", query_ref),
    ):
        _require_equal(binding.get(field), expected, label=f"incarnation {field}")

    projection_provenance = binding.get("model_fit_projection_ref")
    if not isinstance(projection_provenance, dict):
        raise ExternalExecutionRequestError("incarnation has no model-fit projection")
    projection_ref = _content_from_provenance(projection_provenance)
    if projection_ref["digest"] != digest_bytes(projection_raw):
        raise ExternalExecutionRequestError(
            "model-fit projection transport digest mismatch"
        )
    if projection_ref["schema_version"] != "aoa_model_fit_projection_v1":
        raise ExternalExecutionRequestError("model-fit projection schema is invalid")
    realization_provenance = binding.get("model_realization_ref")
    if not isinstance(realization_provenance, dict):
        raise ExternalExecutionRequestError("incarnation has no model realization")
    realization_ref = _content_from_provenance(realization_provenance)
    if (
        realization_ref["owner_repo"] != "aoa-models"
        or realization_ref["schema_version"] != "aoa_model_realization_v1"
    ):
        raise ExternalExecutionRequestError("model realization provenance is invalid")

    fit_family = mandate["model_fit_relation"]["task_family"]
    candidates = [
        item
        for item in model_fit_query.get("candidates", [])
        if item.get("projection_provenance") == projection_provenance
        and item.get("realization_provenance") == binding.get("model_realization_ref")
    ]
    if (
        model_fit_query.get("query", {}).get("task_family") != fit_family
        or len(candidates) != 1
        or model_fit_projection.get("schema_version") != "aoa_model_fit_projection_v1"
        or model_fit_projection.get("subject_realization_ref")
        != candidates[0].get("realization_ref")
    ):
        raise ExternalExecutionRequestError("model-fit evidence chain is inconsistent")

    if digest_bytes(mandate_raw) != binding.get("role_contract_ref", {}).get(
        "artifact_digest"
    ):
        raise ExternalExecutionRequestError(
            "mandate transport differs from role contract"
        )
    task_request_ref = binding.get("task_request_ref")
    if (
        not isinstance(task_request_ref, dict)
        or task_request_ref.get("owner_repo") != "aoa-sdk"
        or task_request_ref.get("schema_version") != "urn:aoa-sdk:a2a:summon-request:v4"
        or task_request_ref.get("artifact_digest") != digest_bytes(sdk_request_raw)
    ):
        raise ExternalExecutionRequestError(
            "SDK summon request differs from incarnation"
        )
    sdk_summon = sdk_request.get("summon_request")
    if not isinstance(sdk_summon, dict) or sdk_summon.get(
        "transport_preference"
    ) not in {"a2a_remote", "either"}:
        raise ExternalExecutionRequestError(
            "SDK request must authorize an external A2A transport"
        )
    _validate_obligation_mandate_chain(obligation, mandate, sdk_request, binding)

    run_plan_ref = binding.get("run_plan_ref")
    if (
        not isinstance(run_plan_ref, dict)
        or run_plan_ref.get("owner_repo") != "aoa-sdk"
        or run_plan_ref.get("schema_version") != "aoa_control_plane_v1"
        or run_plan.get("plan_id") != run_plan_ref.get("object_id")
        or run_plan.get("plan_digest") != run_plan_ref.get("digest")
    ):
        raise ExternalExecutionRequestError("incarnation names another SDK run plan")
    decision_digest = digest_bytes(sdk_decision_raw)
    decision_matches = [
        item
        for item in run_plan.get("snapshot", {}).get("source_refs", [])
        if item.get("owner_repo") == "aoa-sdk"
        and item.get("schema_version") == "urn:aoa-sdk:a2a:summon-result:v4"
        and item.get("artifact_digest") == decision_digest
    ]
    if len(decision_matches) != 1:
        raise ExternalExecutionRequestError(
            "SDK decision is not one exact run-plan snapshot input"
        )
    _validate_sdk_decision(
        sdk_decision,
        sdk_request_digest=digest_bytes(sdk_request_raw),
    )
    sdk_decision_ref = _content_from_provenance(decision_matches[0])

    if task_local_dag.get("schema_version") != "aoa-task-local-dag-v2" or (
        task_local_dag.get("status") != "ready"
        or task_local_dag.get("authority") is not False
    ):
        raise ExternalExecutionRequestError("task-local DAG is not ready")
    dag_ref = _raw_ref(
        dag_raw,
        task_local_dag,
        object_field="plan_id",
        owner_repo="aoa-skills",
        schema_version="aoa-task-local-dag-v2",
        label="task-local DAG",
    )
    if runtime_launch.get("schema_version") != "abyss_stack_external_codex_launch_v1":
        raise ExternalExecutionRequestError("runtime launch schema is invalid")
    launch_ref = _raw_ref(
        launch_raw,
        runtime_launch,
        object_field="launch_id",
        owner_repo="abyss-stack",
        schema_version="abyss_stack_external_codex_launch_v1",
        label="runtime launch",
    )

    if transfer.get("schema_version") != "responsibility-transfer-v1" or transfer.get(
        "state"
    ) not in {"accepted", "narrowed", "launched"}:
        raise ExternalExecutionRequestError("responsibility transfer is not admitted")
    _require_equal(
        transfer.get("obligation_ref"),
        obligation_ref["object_id"],
        label="transfer obligation",
    )
    _require_equal(
        transfer.get("mandate_ref"), mandate_ref["object_id"], label="transfer mandate"
    )
    _require_equal(
        transfer.get("task_local_dag_ref"),
        dag_ref["object_id"],
        label="transfer task-local DAG",
    )
    holders = transfer.get("holder_ids")
    if not isinstance(holders, list) or len(holders) != 2 or len(set(holders)) != 2:
        raise ExternalExecutionRequestError(
            "responsibility transfer holders are invalid"
        )
    return_owner = mandate.get("return_owner")
    current_holder = obligation.get("current_holder")
    obligation_return_owner = obligation.get("return_owner")
    continuity = mandate.get("continuity")
    if not all(
        isinstance(item, Mapping)
        for item in (return_owner, current_holder, obligation_return_owner, continuity)
    ):
        raise ExternalExecutionRequestError(
            "responsibility transfer owner chain is incomplete"
        )
    _require_equal(
        current_holder,
        obligation_return_owner,
        label="obligation current and return holder",
    )
    _require_equal(
        return_owner,
        obligation_return_owner,
        label="mandate and obligation return owner",
    )
    _require_equal(
        holders[0],
        return_owner.get("object_id"),
        label="transfer prior holder",
    )
    _require_equal(
        holders[1],
        continuity.get("identity_key"),
        label="transfer current holder",
    )
    transfer_ref = {
        **_raw_ref(
            transfer_raw,
            transfer,
            object_field="transfer_id",
            owner_repo="aoa-agents",
            schema_version="responsibility-transfer-v1",
            label="responsibility transfer",
        ),
        "admitted_state": transfer["state"],
        "holder_ids": holders,
    }

    procedure_refs: list[dict[str, str]] = []
    for index, path in enumerate(domain_procedure_paths):
        raw, procedure = _load(path, label=f"domain procedure {index + 1}")
        procedure_id = procedure.get("procedure_id")
        owner = procedure.get("owner")
        schema_version = procedure.get("schema_version")
        if not all(
            isinstance(item, str) and item
            for item in (procedure_id, owner, schema_version)
        ):
            raise ExternalExecutionRequestError(
                "domain procedure identity is incomplete"
            )
        procedure_refs.append(
            {
                "object_id": procedure_id,
                "owner_repo": owner,
                "schema_version": schema_version,
                "digest": digest_bytes(raw),
            }
        )
    _require_equal(
        mandate["domain_procedure_refs"],
        procedure_refs,
        label="mandate domain procedures",
    )

    if runtime_task.get("schema_version") != "abyss_stack_external_codex_task_v1":
        raise ExternalExecutionRequestError("runtime task schema is invalid")
    _validate_permission_posture(binding, runtime_task, mandate)
    _validate_tool_profile(binding, mandate)
    if (
        runtime_task.get("parent_task_id") != sdk_summon.get("parent_task_id")
        or runtime_task.get("target_owner") != mandate["domain_owner"]
        or runtime_task.get("expected_incarnation_id") != binding.get("incarnation_id")
        or runtime_task.get("continuation_id")
        != binding.get("continuation", {}).get("continuation_id")
    ):
        raise ExternalExecutionRequestError(
            "runtime task identity differs from actor binding"
        )

    expected_outputs = sdk_request.get("expected_outputs")
    if not isinstance(expected_outputs, list) or not expected_outputs:
        raise ExternalExecutionRequestError("SDK request has no named outputs")
    required_outputs = {
        "external_codex_agent_result",
        *runtime_task.get("expected_artifacts", []),
        *(item["name"] for item in mandate["named_outputs"]),
    }
    if not required_outputs.issubset(set(expected_outputs)):
        raise ExternalExecutionRequestError(
            "SDK request omits mandate or runtime named outputs"
        )

    owner_summon = dict(sdk_summon)
    owner_summon.pop("expected_outputs", None)
    owner_summon["transport_preference"] = "external_cli"
    binding_provenance = binding.get("provenance", {})
    binding_ref = {
        "object_id": str(binding_provenance.get("artifact_ref", "")),
        "owner_repo": "aoa-sdk",
        "schema_version": "aoa_agent_incarnation_binding_v2",
        "digest": digest_bytes(binding_raw),
    }
    if not binding_ref["object_id"]:
        raise ExternalExecutionRequestError("incarnation binding identity is absent")

    request: dict[str, Any] = {
        "quest_passport": sdk_request["quest_passport"],
        "summon_request": owner_summon,
        "expected_outputs": expected_outputs,
        "intent": "execute",
        "request_ref": request_ref,
        "request_digest": ZERO_DIGEST,
        "return_owner": mandate["return_owner"]["object_id"],
        "child_scope": {
            "task": runtime_task["objective"],
            "allowed_tools": mandate["environment"]["required_tools"],
            "allowed_effects": [runtime_task["allowed_effect_class"]],
            "authority_limit": obligation["responsibility_boundary"],
        },
        "child_stop_line": mandate["authority"]["stop_line"],
        "child_inputs": [
            {"kind": "contract", "ref": item["object_id"]} for item in procedure_refs
        ],
        "external_incarnation": {
            "obligation_ref": obligation_ref,
            "actor_mandate_ref": mandate_ref,
            "role_resolution_ref": role_resolution_ref,
            "model_fit_query_result_ref": query_ref,
            "model_fit_projection_ref": projection_ref,
            "model_realization_ref": realization_ref,
            "run_plan_ref": dict(run_plan_ref),
            "task_local_dag_ref": dag_ref,
            "incarnation_binding_ref": binding_ref,
            "sdk_summon_request_ref": _content_from_provenance(task_request_ref),
            "sdk_summon_decision_ref": sdk_decision_ref,
            "runtime_launch_ref": launch_ref,
            "runtime_interface": runtime_interface,
            "responsibility_transfer_ref": transfer_ref,
            "domain_procedure_refs": procedure_refs,
            "continuity_ref": {
                "object_id": binding["continuation"]["continuation_id"],
                "owner_repo": "aoa-sdk",
                "schema_version": "continuation-obligation-v1",
                "digest": digest_bytes(binding_raw),
            },
            "return_event_schema_ref": {
                "object_id": return_event_object_id,
                "owner_repo": "abyss-stack",
                "schema_version": "abyss_stack_external_codex_event_v1",
                "digest": digest_bytes(event_schema_raw),
            },
            "launches_separate_os_process": True,
            "uses_builtin_codex_subagents": False,
            "separate_cli_session": True,
            "usage_metering": "observe_only_no_budget",
        },
    }
    request["request_digest"] = semantic_request_digest(request)
    _validate(request, REQUEST_SCHEMA, label="aoa-summon external request")
    return request


def _write(path: Path, payload: Mapping[str, Any]) -> None:
    location = path.resolve()
    if path.is_symlink() or not location.parent.is_dir() or location.exists():
        raise ExternalExecutionRequestError(
            "output must be a new regular file under an existing directory"
        )
    location.write_bytes(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode(
            "utf-8"
        )
        + b"\n"
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--request-ref", required=True)
    result.add_argument("--runtime-interface", required=True)
    result.add_argument("--return-event-object-id", required=True)
    for name in (
        "obligation",
        "mandate",
        "role-resolution",
        "model-fit-query-result",
        "model-fit-projection",
        "task-local-dag",
        "incarnation-binding",
        "incarnation-binding-schema",
        "sdk-summon-request",
        "sdk-summon-decision",
        "run-plan",
        "runtime-launch",
        "runtime-task",
        "responsibility-transfer",
        "return-event-schema",
    ):
        result.add_argument(f"--{name}", type=Path, required=True)
    result.add_argument("--domain-procedure", type=Path, action="append", required=True)
    result.add_argument("--output", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        request = compile_external_execution_request(
            request_ref=args.request_ref,
            runtime_interface=args.runtime_interface,
            return_event_object_id=args.return_event_object_id,
            obligation_path=args.obligation,
            mandate_path=args.mandate,
            role_resolution_path=args.role_resolution,
            model_fit_query_result_path=args.model_fit_query_result,
            model_fit_projection_path=args.model_fit_projection,
            task_local_dag_path=args.task_local_dag,
            incarnation_binding_path=args.incarnation_binding,
            incarnation_binding_schema_path=args.incarnation_binding_schema,
            sdk_summon_request_path=args.sdk_summon_request,
            sdk_summon_decision_path=args.sdk_summon_decision,
            run_plan_path=args.run_plan,
            runtime_launch_path=args.runtime_launch,
            runtime_task_path=args.runtime_task,
            responsibility_transfer_path=args.responsibility_transfer,
            domain_procedure_paths=args.domain_procedure,
            return_event_schema_path=args.return_event_schema,
        )
        _write(args.output, request)
    except (ExternalExecutionRequestError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(
        json.dumps(
            {
                "ok": True,
                "output": str(args.output.resolve()),
                "request_ref": request["request_ref"],
                "request_digest": request["request_digest"],
                "started": False,
                "next_route": "abyss-stack:external-codex-agent/preflight",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
