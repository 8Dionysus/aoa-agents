#!/usr/bin/env python3
"""Prepare one obligation-derived external actor packet without starting it.

The input is a single semantic preparation specification.  The caller has
already decided that an independent obligation exists, selected an AoA role,
named the authority that selected one model-fit projection, and granted a
bounded effect posture.  This compiler resolves and content-addresses those
decisions through their owner surfaces.  It never detects an obligation,
selects a role or model, starts a process, or accepts a returned result.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


SUMMON_ROOT = Path(__file__).resolve().parents[1]
AGENT_SKILL_ROOT = SUMMON_ROOT.parent / "aoa-agents-skills"
REFERENCES = SUMMON_ROOT / "references"
ZERO_DIGEST = "sha256:" + "0" * 64
COMPLETED_WAKE_EVENT_KIND = "result.validated"
REVIEW_REQUIRED_WAKE_EVENT_KIND = "result.review_required"
DEFAULT_FORBIDDEN_EFFECTS = (
    "commit",
    "push",
    "pull_request",
    "merge",
    "tag",
    "release",
    "publication",
    "service_mutation",
    "secret_access",
    "global_config_mutation",
)
IMMUTABLE_EVIDENCE_REF_RE = re.compile(
    r"immutable:(?P<input_id>[a-z0-9]+(?:-[a-z0-9]+)*)#L[1-9][0-9]*(?:-L[1-9][0-9]*)?"
)


class PreparationError(ValueError):
    """One selected owner input or exact preparation relation is invalid."""


def _load(path: Path, *, label: str) -> dict[str, Any]:
    location = path.resolve()
    if path.is_symlink() or not location.is_file():
        raise PreparationError(f"{label} must be an exact regular file: {path}")
    try:
        value = json.loads(location.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PreparationError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise PreparationError(f"{label} must be a JSON object: {path}")
    return value


def _write(path: Path, value: Mapping[str, Any]) -> None:
    if path.exists() or path.is_symlink():
        raise PreparationError(f"refusing to overwrite preparation artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _raw_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _data_digest(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _concrete_return_owner_provenance(
    holder: Mapping[str, Any],
    owner_evidence: Mapping[str, Any],
) -> dict[str, str]:
    """Project the exact semantic holder into the SDK provenance shape."""

    return {
        "owner_repo": str(holder["owner_repo"]),
        "artifact_ref": str(holder["object_id"]),
        "source_ref": str(owner_evidence["source_ref"]),
        "artifact_digest": str(holder["digest"]),
        "schema_ref": "task-local/responsibility-holder-v1",
        "schema_version": str(holder["schema_version"]),
    }


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreparationError(
            f"cannot inspect exact Git owner root {root}: {' '.join(args)}"
        ) from exc


def _owner_head(root: Path) -> str:
    resolved = root.resolve(strict=True)
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != resolved:
        raise PreparationError(f"owner root is not an exact Git worktree root: {root}")
    return _git(root, "rev-parse", "HEAD")


def _module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise PreparationError(f"cannot load owner compiler: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _provenance(
    sdk: Any,
    path: Path,
    *,
    owner: str,
    artifact_ref: str,
    source_ref: str,
    schema_ref: str,
    schema_version: str,
) -> Any:
    return sdk.ProvenanceRef(
        owner_repo=owner,
        artifact_ref=artifact_ref,
        source_ref=source_ref,
        artifact_digest=_raw_digest(path),
        schema_ref=schema_ref,
        schema_version=schema_version,
    )


def _content_ref(
    sdk: Any,
    payload: Mapping[str, Any],
    *,
    object_field: str,
    digest_field: str,
    owner: str,
) -> Any:
    return sdk.ContentRef(
        object_id=str(payload[object_field]),
        owner_repo=owner,
        schema_version=str(payload["schema_version"]),
        digest=str(payload[digest_field]),
    )


def _selected_tool_profile(runtime_descriptor: Mapping[str, Any], profile_id: str) -> dict[str, Any]:
    matches = [
        item
        for item in runtime_descriptor.get("tool_profiles", [])
        if isinstance(item, dict) and item.get("profile_id") == profile_id
    ]
    if len(matches) != 1:
        raise PreparationError(f"runtime tool profile must resolve exactly once: {profile_id}")
    return matches[0]


def _domain_refs(paths: Sequence[Path]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for path in paths:
        payload = _load(path, label="domain procedure")
        values = (payload.get("procedure_id"), payload.get("owner"), payload.get("schema_version"))
        if not all(isinstance(value, str) and value for value in values):
            raise PreparationError(f"domain procedure identity is incomplete: {path}")
        result.append(
            {
                "object_id": str(payload["procedure_id"]),
                "owner_repo": str(payload["owner"]),
                "schema_version": str(payload["schema_version"]),
                "digest": _raw_digest(path),
            }
        )
    return result


def _assert_review_evidence_closure(
    evidence_inputs: Sequence[tuple[Mapping[str, Any], Path]],
) -> None:
    """Require writer evidence refs to survive into the reviewer namespace."""

    available_ids = {str(item["input_id"]) for item, _path in evidence_inputs}
    missing: dict[str, set[str]] = {}
    for item, path in evidence_inputs:
        input_id = str(item["input_id"])
        if input_id not in {"writer-report", "writer-selection"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise PreparationError(
                f"review evidence is not readable UTF-8: {input_id}"
            ) from exc
        unresolved = {
            match.group("input_id")
            for match in IMMUTABLE_EVIDENCE_REF_RE.finditer(content)
            if match.group("input_id") not in available_ids
        }
        if unresolved:
            missing[input_id] = unresolved
    if missing:
        rendered = "; ".join(
            f"{source} -> {','.join(sorted(input_ids))}"
            for source, input_ids in sorted(missing.items())
        )
        raise PreparationError(
            "independent review evidence closure is incomplete: " + rendered
        )


def _dag_topology(
    *,
    route_id: str,
    execution_posture: str,
    mandate: Mapping[str, Any],
    execution: Mapping[str, Any],
    named_outputs: Sequence[str],
    evidence_inputs: Sequence[tuple[Mapping[str, Any], Path]],
    runtime_profile_id: str,
) -> dict[str, Any]:
    actor_node = f"actor:{route_id}"
    if execution_posture == "independent_review":
        return {
            "nodes": [
                {
                    "id": actor_node,
                    "kind": "independent-review-obligation",
                    "binding": {
                        "role_id": mandate["role_binding"]["role_id"],
                        "permission_posture": "read_only",
                        "runtime_profile": runtime_profile_id,
                    },
                    "owner": {
                        "domain_owner": mandate["domain_owner"],
                        "return_owner": mandate["return_owner"],
                    },
                    "inputs": [str(item["input_id"]) for item, _path in evidence_inputs],
                    "outputs": list(named_outputs),
                    "effects": [execution["effect_class"]],
                    "verification": [
                        "distinct external CLI session",
                        "typed A2A result",
                        "transitively closed immutable review evidence",
                    ],
                    "termination": [mandate["authority"]["stop_line"]],
                    "availability": "bound-after-runtime-preflight",
                }
            ],
            "edges": [],
            "execution_stages": [[actor_node]],
            "checkpoints": [
                {
                    "node": actor_node,
                    "verifier": mandate["return_owner"]["object_id"],
                    "criteria": [
                        "review verdict returned",
                        "authority ceiling preserved",
                    ],
                }
            ],
            "external_target": actor_node,
        }

    reviewer_node = f"actor:{route_id}:independent-review"
    return {
        "nodes": [
            {
                "id": actor_node,
                "kind": "external-actor-obligation",
                "binding": {
                    "obligation_ref": mandate["obligation_ref"],
                    "mandate_ref": mandate["mandate_id"],
                    "role_id": mandate["role_binding"]["role_id"],
                    "runtime_profile": runtime_profile_id,
                },
                "owner": {
                    "domain_owner": mandate["domain_owner"],
                    "return_owner": mandate["return_owner"],
                },
                "inputs": ["obligation", "mandate", "model-fit", "domain-procedure"],
                "outputs": list(named_outputs),
                "effects": [execution["effect_class"]],
                "verification": [
                    "schema-valid runtime result",
                    "exact named-output set",
                ],
                "termination": [mandate["authority"]["stop_line"]],
                "availability": "bound-after-runtime-preflight",
            },
            {
                "id": reviewer_node,
                "kind": "independent-review-obligation",
                "binding": {
                    "role_id": "reviewer",
                    "permission_posture": "read_only",
                },
                "owner": {
                    "domain_owner": mandate["domain_owner"],
                    "return_owner": mandate["return_owner"],
                },
                "inputs": ["writer-runtime-result", *named_outputs],
                "outputs": ["independent-review", "a2a-child-result"],
                "effects": ["read_only"],
                "verification": [
                    "distinct external CLI session",
                    "typed A2A result",
                ],
                "termination": [
                    "Do not mutate the writer tree or claim owner acceptance."
                ],
                "availability": "after-admitted-writer-return",
            },
        ],
        "edges": [
            {
                "kind": "verification",
                "source": actor_node,
                "target": reviewer_node,
                "artifact_type": "external_codex_agent_result",
            }
        ],
        "execution_stages": [[actor_node], [reviewer_node]],
        "checkpoints": [
            {
                "node": actor_node,
                "verifier": mandate["return_owner"]["object_id"],
                "criteria": [
                    "all named outputs returned",
                    "authority ceiling preserved",
                ],
            },
            {
                "node": reviewer_node,
                "verifier": mandate["return_owner"]["object_id"],
                "criteria": ["writer evidence independently reviewed"],
            },
        ],
        "external_target": actor_node,
    }


def _validate_spec(spec: dict[str, Any]) -> None:
    schema = _load(REFERENCES / "actor-route-preparation-v1.schema.json", label="preparation schema")
    errors = sorted(
        Draft202012Validator(schema).iter_errors(spec),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    )
    if errors:
        where = ".".join(str(part) for part in errors[0].absolute_path)
        raise PreparationError(f"preparation spec is invalid at {where or '<root>'}: {errors[0].message}")


def _query_model_fit(spec: dict[str, Any], models_root: Path) -> dict[str, Any]:
    query = spec["model_fit"]
    command = [
        sys.executable,
        str(models_root / "scripts/query_model_fit.py"),
        "--root",
        str(models_root),
        "--task-family",
        spec["mandate"]["model_fit_relation"]["task_family"],
        "--runtime-product",
        query.get("runtime_product", "codex-cli"),
        "--runtime-version",
        query["runtime_version"],
        "--reasoning-effort",
        query["reasoning_effort"],
        "--sandbox-mode",
        query["sandbox_mode"],
    ]
    for tool in query["required_tools"]:
        command.extend(("--required-tool", tool))
    for server in query.get("required_mcp_servers", []):
        command.extend(("--required-mcp-server", server))
    command.append("--require-match")
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        payload = json.loads(result.stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise PreparationError("aoa-models fit query failed or returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise PreparationError("aoa-models fit query did not return an object")
    return payload


def _select_candidate(
    fit: Mapping[str, Any],
    models_root: Path,
    selected_ref: str,
    selection_authority: Mapping[str, Any],
) -> tuple[dict[str, Any], Path, Path]:
    if not selection_authority.get("object_id"):
        raise PreparationError("selected model-fit projection has no explicit selection authority")
    matches = [
        item
        for item in fit.get("candidates", [])
        if isinstance(item, dict)
        and item.get("projection_provenance", {}).get("artifact_ref") == selected_ref
    ]
    if len(matches) != 1:
        raise PreparationError("selected model-fit projection is absent or ambiguous in current query")
    candidate = matches[0]
    projection_path = (models_root / selected_ref).resolve(strict=True)
    realization_ref = candidate.get("realization_provenance", {}).get("artifact_ref")
    if not isinstance(realization_ref, str) or not realization_ref:
        raise PreparationError("selected fit candidate has no realization provenance")
    realization_path = (models_root / realization_ref).resolve(strict=True)
    if _raw_digest(projection_path) != candidate["projection_provenance"]["artifact_digest"]:
        raise PreparationError("selected fit projection bytes differ from query provenance")
    if _raw_digest(realization_path) != candidate["realization_provenance"]["artifact_digest"]:
        raise PreparationError("selected realization bytes differ from query provenance")
    return candidate, projection_path, realization_path


def compile_preparation(spec_path: Path, output_dir: Path) -> dict[str, Any]:
    spec = _load(spec_path, label="actor-route preparation spec")
    _validate_spec(spec)
    output_dir = output_dir.resolve()
    if output_dir.exists():
        raise PreparationError("output directory must not already exist")
    output_dir.mkdir(parents=True)

    roots = {name: Path(value).resolve(strict=True) for name, value in spec["owner_roots"].items()}
    agents_root = roots["aoa_agents"]
    models_root = roots["aoa_models"]
    sdk_root = roots["aoa_sdk"]
    release_root = roots["abyss_stack_release"]
    workspace = Path(spec["execution"]["workspace_path"]).resolve(strict=True)
    bind_executable = Path(spec["execution"]["runtime_bind_executable"]).resolve(strict=True)
    domain_paths = [Path(value).resolve(strict=True) for value in spec["domain_procedure_paths"]]
    evidence_inputs = [
        (item, Path(item["path"]).resolve(strict=True))
        for item in spec.get("evidence_inputs", [])
    ]
    if spec["execution"].get("execution_posture") == "independent_review":
        _assert_review_evidence_closure(evidence_inputs)

    agent_source_ref = _owner_head(agents_root)
    model_source_ref = _owner_head(models_root)
    sdk_source_ref = _owner_head(sdk_root)
    workspace_source_ref = _owner_head(workspace)

    actor_contract = _module(
        agents_root / "skills/aoa-agents-skills/scripts/compile_actor_contract.py",
        "aoa_agents_actor_contract",
    )
    role_resolver = _module(
        agents_root / "skills/aoa-agents-skills/scripts/resolve_role_binding.py",
        "aoa_agents_role_resolver",
    )
    obligation = actor_contract.compile_obligation(spec["obligation"])
    obligation_path = output_dir / "obligation.json"
    _write(obligation_path, obligation)
    selection = spec["role_selection"]
    role_resolution = role_resolver.resolve_role_binding(
        agents_root,
        role_id=selection["role_id"],
        tier_id=selection["tier_id"],
        specialization_id=selection.get("specialization_id"),
    )
    role_path = output_dir / "role-resolution.json"
    _write(role_path, role_resolution)
    mandate_semantic = dict(spec["mandate"])
    mandate_semantic["domain_procedure_refs"] = _domain_refs(domain_paths)
    mandate = actor_contract.compile_mandate(obligation, role_resolution, mandate_semantic)
    mandate_path = output_dir / "mandate.json"
    _write(mandate_path, mandate)

    fit = _query_model_fit(spec, models_root)
    fit_path = output_dir / "model-fit-query-result.json"
    _write(fit_path, fit)
    candidate, projection_path, realization_path = _select_candidate(
        fit,
        models_root,
        spec["model_fit"]["selected_projection_ref"],
        spec["model_fit"]["selection_authority_ref"],
    )

    sdk_src = str(sdk_root / "src")
    if sdk_src not in sys.path:
        sys.path.insert(0, sdk_src)
    import aoa_sdk.a2a.rebase as a2a  # type: ignore[import-not-found]
    import aoa_sdk.contracts.control_plane as cp  # type: ignore[import-not-found]
    import aoa_sdk.control_plane as sdk  # type: ignore[import-not-found]
    from aoa_sdk.runtime_adapters import (  # type: ignore[import-not-found]
        load_abyss_stack_external_codex_runtime_profile,
    )

    route_id = spec["route_id"]
    execution = spec["execution"]
    execution_posture = execution.get("execution_posture", "bounded_execution")
    review_required = execution.get("review_required", True)
    reviewed_artifact_path = mandate_path
    if execution_posture == "independent_review":
        reviewed_input_id = execution.get("reviewed_artifact_input_id")
        reviewed_matches = [
            path
            for item, path in evidence_inputs
            if item["input_id"] == reviewed_input_id
        ]
        if len(reviewed_matches) != 1:
            raise PreparationError(
                "independent review must bind one exact reviewed artifact input"
            )
        reviewed_artifact_path = reviewed_matches[0]
    named_outputs = [item["name"] for item in mandate["named_outputs"]]
    sdk_outputs = ["external_codex_agent_result", *named_outputs]
    incarnation_id = f"incarnation:{route_id}"
    continuation_id = f"continuation:{route_id}"
    correlation_id = f"actor-route:{route_id}"
    request = a2a.build_summon_request_payload(
        a2a.QuestPassport(
            difficulty=execution["difficulty"],
            risk=execution.get("risk", "r1_repo_local"),
            control_mode="codex_supervised",
            delegate_tier=mandate["role_binding"]["tier_id"],
            wrapper_class="external-cli-incarnation",
            route_anchor=obligation["goal_ref"]["object_id"],
            expected_artifacts=sdk_outputs,
        ),
        a2a.SummonIntent(
            desired_role=mandate["role_binding"]["role_id"],
            child_agent_id=incarnation_id,
            capability_refs=["aoa-summon:external-cli-incarnation"],
            expected_outputs=sdk_outputs,
            parent_task_id=execution["parent_task_id"],
            session_ref=execution["session_ref"],
            reviewed_artifact_path=str(reviewed_artifact_path),
            audit_refs=[str(fit_path)],
            review_required=review_required,
            transport_preference="a2a_remote",
            require_progression=False,
            workspace_root=str(workspace),
        ),
        expected_outputs=sdk_outputs,
    )
    sdk_request_path = output_dir / "sdk-summon-request.json"
    _write(sdk_request_path, request)
    assessed = a2a.assess_summon(
        a2a.QuestPassport(**request["quest_passport"]),
        a2a.SummonIntent(**request["summon_request"]),
    )
    if not assessed.allowed or assessed.execution_surface != "a2a_remote":
        raise PreparationError(f"aoa-sdk did not admit external transport: {assessed.reason_codes}")
    decision = {
        "schema_version": "urn:aoa-sdk:a2a:summon-result:v4",
        **a2a.build_summon_result_payload(assessed),
        "request_artifact_digest": _raw_digest(sdk_request_path),
        "decision_posture": "owner-sdk-transport-admission",
        "authority": "aoa-sdk transport decision only; no runtime effect",
    }
    sdk_decision_path = output_dir / "sdk-summon-decision.json"
    _write(sdk_decision_path, decision)

    source_graph = spec["task_local_dag_source_graph"]
    topology = _dag_topology(
        route_id=route_id,
        execution_posture=execution_posture,
        mandate=mandate,
        execution=execution,
        named_outputs=named_outputs,
        evidence_inputs=evidence_inputs,
        runtime_profile_id=(
            candidate["realization"]["configuration"]["tools"]["profile_ref"]
            if "realization" in candidate
            else _load(realization_path, label="model realization")["configuration"]["tools"]["profile_ref"]
        ),
    )
    external_target = topology.pop("external_target")
    dag_id = "dag-" + hashlib.sha256(route_id.encode("utf-8")).hexdigest()[:16]
    dag = {
        "schema_version": "aoa-task-local-dag-v2",
        "authority": False,
        "plan_id": dag_id,
        "request": {"query": obligation["duty"]},
        "source_graph": source_graph,
        "status": "ready",
        "selected_capabilities": ["skill.aoa-summon"],
        "nodes": topology["nodes"],
        "edges": topology["edges"],
        "external_inputs": [
            {"type": "workspace", "ref": str(workspace), "target": external_target},
            *({"type": "domain-procedure", "ref": str(path), "target": external_target} for path in domain_paths),
            *({"type": "evidence", "ref": str(path), "target": external_target} for _item, path in evidence_inputs),
        ],
        "execution_stages": topology["execution_stages"],
        "checkpoints": topology["checkpoints"],
        "terminal": {"lifetime": "task-local", "success_condition": "all selected nodes reached verified terminal conditions"},
        "warnings": [],
        "blockers": [],
    }
    dag_schema_path = release_root / "owners/aoa-skills/schemas/task_local_dag_v2.schema.json"
    errors = list(Draft202012Validator(_load(dag_schema_path, label="task-local DAG schema")).iter_errors(dag))
    if errors:
        raise PreparationError(f"task-local DAG is invalid: {errors[0].message}")
    dag_path = output_dir / "task-local-dag.json"
    _write(dag_path, dag)

    transfer = {
        "schema_version": "responsibility-transfer-v1",
        "transfer_id": f"responsibility-transfer:{route_id}",
        "state": "accepted",
        "obligation_ref": obligation["obligation_id"],
        "mandate_ref": mandate["mandate_id"],
        "task_local_dag_ref": dag["plan_id"],
        "holder_ids": [mandate["return_owner"]["object_id"], mandate["continuity"]["identity_key"]],
        "return_owner": mandate["return_owner"]["object_id"],
        "authority_ceiling": mandate["authority"]["stop_line"],
    }
    transfer_path = output_dir / "responsibility-transfer.json"
    _write(transfer_path, transfer)

    runtime_descriptor_path = release_root / "runtime/runtime-profile.v1.json"
    runtime_descriptor = _load(runtime_descriptor_path, label="runtime profile")
    runtime_profile = load_abyss_stack_external_codex_runtime_profile(runtime_descriptor_path)
    realization = _load(realization_path, label="model realization")
    profile_id = realization["configuration"]["tools"]["profile_ref"]
    tool_profile = _selected_tool_profile(runtime_descriptor, profile_id)
    if tool_profile["sandbox_mode"] != execution["sandbox_mode"] or tool_profile["allowed_effect_classes"] != [execution["effect_class"]]:
        raise PreparationError("selected runtime profile differs from granted permission posture")
    if set(tool_profile["required_tool_ids"]) != set(mandate["environment"]["required_tools"]):
        raise PreparationError("selected runtime tools differ from actor mandate")
    if set(tool_profile["required_mcp_server_ids"]) != set(mandate["environment"]["required_mcp_servers"]):
        raise PreparationError("selected runtime MCP servers differ from actor mandate")

    obligation_ref = _provenance(cp, obligation_path, owner="aoa-agents", artifact_ref=obligation["obligation_id"], source_ref=agent_source_ref, schema_ref="skills/aoa-agents-skills/references/agent-obligation-v1.schema.json", schema_version=obligation["schema_version"])
    mandate_ref = _provenance(cp, mandate_path, owner="aoa-agents", artifact_ref=mandate["mandate_id"], source_ref=agent_source_ref, schema_ref="skills/aoa-agents-skills/references/actor-mandate-v1.schema.json", schema_version=mandate["schema_version"])
    role_ref = _provenance(cp, role_path, owner="aoa-agents", artifact_ref=role_resolution["resolution_id"], source_ref=agent_source_ref, schema_ref="skills/aoa-agents-skills/references/role-resolution-v1.schema.json", schema_version=role_resolution["schema_version"])
    fit_ref = _provenance(cp, fit_path, owner="aoa-models", artifact_ref=fit["result_id"], source_ref=model_source_ref, schema_ref="schemas/model-fit-query-result.schema.json", schema_version=fit["schema_version"])
    projection_ref = cp.ProvenanceRef.model_validate(candidate["projection_provenance"])
    realization_ref = cp.ProvenanceRef.model_validate(candidate["realization_provenance"])
    dag_ref = _provenance(cp, dag_path, owner="aoa-skills", artifact_ref=dag["plan_id"], source_ref=source_graph["content_hash"], schema_ref="schemas/task_local_dag_v2.schema.json", schema_version=dag["schema_version"])
    transfer_ref = _provenance(cp, transfer_path, owner="aoa-agents", artifact_ref=transfer["transfer_id"], source_ref=agent_source_ref, schema_ref="task-local/responsibility-transfer-v1", schema_version=transfer["schema_version"])
    procedure_refs = tuple(
        _provenance(cp, path, owner=payload["owner"], artifact_ref=payload["procedure_id"], source_ref=payload.get("source_ref", "exact-owner-procedure"), schema_ref="task-local/owner-procedure-v1", schema_version=payload["schema_version"])
        for path, payload in ((path, _load(path, label="domain procedure")) for path in domain_paths)
    )
    evidence_refs = tuple(
        _provenance(
            cp,
            path,
            owner=item["owner_repo"],
            artifact_ref=item["artifact_ref"],
            source_ref=item["source_ref"],
            schema_ref=item["schema_ref"],
            schema_version=item["schema_version"],
        )
        for item, path in evidence_inputs
    )
    return_owner_matches = [
        ref
        for (item, _path), ref in zip(evidence_inputs, evidence_refs)
        if item["input_id"] == execution["return_owner_input_id"]
    ]
    if len(return_owner_matches) != 1:
        raise PreparationError("return owner input must resolve exactly once")
    return_owner_evidence_ref = return_owner_matches[0]
    if (
        return_owner_evidence_ref.owner_repo
        != mandate["return_owner"]["owner_repo"]
    ):
        raise PreparationError("return owner provenance differs from actor mandate")
    return_owner_ref = cp.ProvenanceRef.model_validate(
        _concrete_return_owner_provenance(
            mandate["return_owner"],
            return_owner_evidence_ref.model_dump(mode="json"),
        )
    )
    workspace_ref = cp.ProvenanceRef(owner_repo=f"task-local-workspace:{route_id}", artifact_ref=str(workspace), source_ref=workspace_source_ref, artifact_digest=_data_digest({"path": str(workspace), "head": workspace_source_ref}), schema_ref="task-local/git-workspace-v1", schema_version="task-local-git-workspace-v1")
    request_ref = _provenance(cp, sdk_request_path, owner="aoa-sdk", artifact_ref=f"task-local/{route_id}/sdk-summon-request.json", source_ref=sdk_source_ref, schema_ref="mechanics/checkpoint/parts/child-task-reentry/schemas/summon-request-v4.schema.json", schema_version="urn:aoa-sdk:a2a:summon-request:v4")
    sdk_summon_schema_path = sdk_root / request_ref.schema_ref
    sdk_summon_schema_ref = _provenance(
        cp,
        sdk_summon_schema_path,
        owner="aoa-sdk",
        artifact_ref=request_ref.schema_ref,
        source_ref=sdk_source_ref,
        schema_ref="https://json-schema.org/draft/2020-12/schema",
        schema_version=request_ref.schema_version,
    )
    decision_ref = _provenance(cp, sdk_decision_path, owner="aoa-sdk", artifact_ref=f"task-local/{route_id}/sdk-summon-decision.json", source_ref=sdk_source_ref, schema_ref="mechanics/checkpoint/parts/child-task-reentry/schemas/summon-result-v4.schema.json", schema_version="urn:aoa-sdk:a2a:summon-result:v4")

    wake_action = (
        "continue_without_parent"
        if mandate["continuity"]["posture"] == "role-continuity"
        else "wake_parent"
    )
    transition = execution["transition"]
    exact_transition_protocol = (
        f"transition.from_status={transition['from_status']}; "
        f"transition.owner={mandate['domain_owner']}; "
        f"transition.approval_posture={transition['approval_posture']}; "
        f"transition.rollback_reentry_route={transition['rollback_reentry_route']}; "
    )
    if execution_posture == "independent_review":
        if review_required:
            raise PreparationError(
                "an independent reviewer cannot require another automatic review"
            )
        return_protocol = (
            "\n\nRuntime return protocol (copy these task-owned values literally in the final "
            "external-codex report; they are ABI fields, not matters for actor judgment). "
            "If the reviewed result is sound: status=completed; decision=proceed; "
            f"transition.to_status={transition['target_status']}; "
            "reentry_request.condition_id=validated-completion. If a repairable blocker "
            "remains: status=review_required; decision=return_for_repair; "
            f"transition.to_status={transition['review_required_status']}; "
            "reentry_request.condition_id=validated-return. In either branch: "
            + exact_transition_protocol
            + f"reentry_request.proposed_action={wake_action}. Do not repair the writer "
            "source or report. Run the fixed validation suite last and do not issue a "
            "command or mutate the workspace afterward."
        )
    else:
        return_protocol = (
            "\n\nRuntime return protocol (copy these task-owned values literally in the final "
            "external-codex report; they are ABI fields, not matters for actor judgment): "
            "status=review_required; decision=submit_for_review; "
            f"transition.to_status={transition['target_status']}; "
            + exact_transition_protocol
            + "reentry_request.condition_id=validated-return; "
            f"reentry_request.proposed_action={wake_action}. The independent reviewer is "
            "activated by the caller after this writer return; do not invent or activate "
            "a reviewer inside the writer report. Produce every named output before fixed "
            "validation, run the fixed validation suite last and do not mutate the "
            "workspace afterward."
        )

    task = {
        "schema_version": "abyss_stack_external_codex_task_v1",
        "task_id": f"actor-task-{route_id}",
        "correlation_id": correlation_id,
        "continuation_id": continuation_id,
        "expected_incarnation_id": incarnation_id,
        "task_family": execution["task_family"],
        "execution_posture": execution_posture,
        "parent_task_id": execution["parent_task_id"],
        "objective": obligation["duty"] + return_protocol,
        "transition": transition,
        "target_owner": mandate["domain_owner"],
        "authority_scope": list(dict.fromkeys([mandate["domain_owner"], "codex-goal", "aoa-agents", "aoa-models", "aoa-sdk", "abyss-stack"])),
        "allowed_effect_class": execution["effect_class"],
        "indirect_command_policy": "sandbox_confined",
        "allowed_paths": execution["allowed_paths"],
        "source_evidence_paths": execution["source_evidence_paths"],
        "immutable_inputs": [],
        "done_state": obligation["expected_outcomes"],
        "validation_commands": execution.get("validation_commands", []),
        "expected_artifacts": named_outputs,
        "forbidden_effects": execution.get("forbidden_effects", list(DEFAULT_FORBIDDEN_EFFECTS)),
        "ambiguity_policy": "escalate",
        "review_required": review_required,
        "return_owner": mandate["return_owner"]["owner_repo"],
    }
    canonical_request_input_id = (
        "review-summon-request"
        if execution_posture == "independent_review"
        else "summon-request"
    )
    immutable = (
        (canonical_request_input_id, sdk_request_path, request_ref),
        ("summon-request-schema", sdk_summon_schema_path, sdk_summon_schema_ref),
        ("summon-decision", sdk_decision_path, decision_ref),
        ("agent-obligation", obligation_path, obligation_ref),
        ("actor-mandate", mandate_path, mandate_ref),
        ("role-resolution", role_path, role_ref),
        ("model-fit-query-result", fit_path, fit_ref),
        ("model-fit-projection", projection_path, projection_ref),
        ("task-local-dag", dag_path, dag_ref),
        ("responsibility-transfer", transfer_path, transfer_ref),
        *((f"domain-procedure-{index + 1}", path, ref) for index, (path, ref) in enumerate(zip(domain_paths, procedure_refs))),
        *((item["input_id"], path, ref) for (item, path), ref in zip(evidence_inputs, evidence_refs)),
    )
    task["immutable_inputs"] = [{"input_id": name, "local_path": str(path), "provenance": ref.model_dump(mode="json")} for name, path, ref in immutable]
    task_schema_path = release_root / "runtime/schemas/external-codex-task.schema.json"
    errors = list(Draft202012Validator(_load(task_schema_path, label="runtime task schema")).iter_errors(task))
    if errors:
        raise PreparationError(f"runtime task is invalid: {errors[0].message}")
    task_path = output_dir / "runtime-task.json"
    _write(task_path, task)
    task_ref = _provenance(cp, task_path, owner="abyss-stack", artifact_ref=f"task-local/{route_id}/runtime-task.json", source_ref=runtime_descriptor["source_ref"], schema_ref="runtime/schemas/external-codex-task.schema.json", schema_version=task["schema_version"])
    runtime_profile = runtime_profile.model_copy(update={"constraint_refs": (*runtime_profile.constraint_refs, task_ref)})

    compiler_ref = _provenance(
        cp,
        sdk_root / "src/aoa_sdk/control_plane/incarnation.py",
        owner="aoa-sdk",
        artifact_ref="src/aoa_sdk/control_plane/incarnation.py",
        source_ref=sdk_source_ref,
        schema_ref="mechanics/boundary-bridge/parts/agent-incarnation-binding/CONTRACT.md",
        schema_version="aoa_control_plane_v1",
    )
    summon_capability_ref = cp.CapabilityRef(
        capability_id="aoa-summon:external-cli-incarnation",
        capability_kind="execution-leaf",
        provenance=_provenance(
            cp,
            agents_root / "skills/aoa-summon/SKILL.md",
            owner="aoa-agents",
            artifact_ref="skills/aoa-summon/SKILL.md",
            source_ref=agent_source_ref,
            schema_ref="skills/aoa-summon/references/contract.yaml",
            schema_version="aoa-skill-contract-v1",
        ),
    )
    all_inputs = (request_ref, sdk_summon_schema_ref, decision_ref, task_ref, workspace_ref, obligation_ref, mandate_ref, role_ref, fit_ref, projection_ref, dag_ref, transfer_ref, *procedure_refs, *evidence_refs)
    result_schema_path = release_root / "runtime/schemas/external-codex-report.schema.json"
    result_schema_ref = _provenance(cp, result_schema_path, owner="abyss-stack", artifact_ref="runtime/schemas/external-codex-report.schema.json", source_ref=runtime_descriptor["source_ref"], schema_ref="runtime/schemas/external-codex-report.schema.json", schema_version="abyss_stack_external_codex_report_v1")
    plan = sdk.build_obligation_actor_run_plan(
        plan_id=f"run-plan:{route_id}", correlation_id=correlation_id,
        decision_ref=cp.ContentRef(object_id=f"sdk-summon-decision:{route_id}", owner_repo="aoa-sdk", schema_version=decision_ref.schema_version, digest=decision_ref.artifact_digest),
        scenario_binding_id=f"scenario-binding:{route_id}", scenario_id=f"scenario:{route_id}", task_local_dag_ref=dag_ref,
        role=cp.AgentRef(agent_id=mandate["role_binding"]["role_id"], provenance=mandate_ref), task_request_ref=request_ref,
        input_refs=all_inputs, expected_output_kinds=tuple(named_outputs), runtime_profile=runtime_profile,
        snapshot_id=f"plan-snapshot:{route_id}",
        abi_refs=(cp.ABIRef(abi_id="abyss-stack:external-codex-report", abi_version=result_schema_ref.schema_version, owner_repo="abyss-stack", schema_ref=result_schema_ref.schema_ref, source_ref=result_schema_ref.source_ref, artifact_digest=result_schema_ref.artifact_digest),),
        step_id=f"execute-{route_id}", effect_class=execution["effect_class"], producer_owner=mandate["domain_owner"],
        checkpoint_owner=dag_ref, rollback_owner=workspace_ref, closeout_owner=compiler_ref, provenance=compiler_ref,
        capability_refs=(summon_capability_ref,),
    )
    run_plan_path = output_dir / "run-plan.json"
    _write(run_plan_path, plan.model_dump(mode="json"))
    wake_conditions = (
        *(
            (
                sdk.WakeCondition(
                    condition_id="validated-completion",
                    event_kind=COMPLETED_WAKE_EVENT_KIND,
                    action=wake_action,
                    description=mandate["wake_policy"],
                ),
            )
            if execution_posture == "independent_review"
            else ()
        ),
        sdk.WakeCondition(condition_id="validated-return", event_kind=REVIEW_REQUIRED_WAKE_EVENT_KIND, action=wake_action, description=mandate["wake_policy"]),
        sdk.WakeCondition(condition_id="authority-needed", event_kind="run.authority_required", action="wake_parent", description="Return responsibility when the mandate ceiling is insufficient."),
    )
    binding = sdk.build_agent_incarnation_binding_v2(
        plan, binding_id=f"incarnation-binding:{route_id}", incarnation_id=incarnation_id, causation_id=obligation["obligation_id"], trace_id=f"trace:{route_id}", task_request_ref=request_ref,
        role_id=mandate["role_binding"]["role_id"], role_contract_ref=mandate_ref, model_realization_ref=realization_ref, workspace_source_ref=workspace_ref,
        permission_posture=sdk.IncarnationPermissionPosture(sandbox_mode=tool_profile["sandbox_mode"], approval_policy=tool_profile["approval_policy"], allowed_effect_classes=tuple(tool_profile["allowed_effect_classes"]), network_access=tool_profile["network_access"], secret_access=False, external_effects=tool_profile["external_effects"]),
        tool_profile=sdk.IncarnationToolProfile(profile_id=profile_id, profile_ref=runtime_profile.provenance, required_tool_ids=tuple(tool_profile["required_tool_ids"]), required_mcp_server_ids=tuple(tool_profile["required_mcp_server_ids"])),
        usage_metering=sdk.IncarnationUsageMetering(metering_regime="chatgpt_quota", dimensions=("input_tokens", "cached_input_tokens", "output_tokens", "active_wall_seconds", "turn_count", "output_bytes", "executed_commands")),
        stop_conditions=(sdk.IncarnationStopCondition(condition_id="authority-boundary", kind="authority_boundary", description=mandate["authority"]["stop_line"]),),
        expected_result_schema_ref=result_schema_ref,
        continuation=sdk.ContinuationObligation(continuation_id=continuation_id, parent_objective_ref=dag_ref, established_decision_refs=(decision_ref,), delegated_obligation=obligation["duty"], delegation_reason=f"Admitted {obligation['trigger']['strength']} obligation from {obligation['trigger']['authority_ref']['object_id']}.", exact_child_identity=incarnation_id, owner_scope=tuple(task["authority_scope"]), immutable_input_refs=all_inputs, expected_output=", ".join(named_outputs), validation_refs=(result_schema_ref, dag_ref), deferred_parent_decisions=("Accept, reject, or re-route the returned responsibility.",), invariants=(mandate["authority"]["stop_line"], "Usage is observed and counted; no pre-emptive token budget is enforced.", "The incarnation uses a separate CLI process and no built-in Codex subagents."), stop_condition_ids=("authority-boundary",), wake_condition_ids=tuple(item.condition_id for item in wake_conditions), return_owner=return_owner_ref, rollback_reentry_anchor=workspace_ref),
        wake_policy=sdk.WakeEscalationPolicy(default_action="stop", conditions=wake_conditions, escalation_conditions=("authority-needed",)),
        agent_obligation_ref=_content_ref(cp, obligation, object_field="obligation_id", digest_field="obligation_digest", owner="aoa-agents"),
        actor_mandate_ref=_content_ref(cp, mandate, object_field="mandate_id", digest_field="mandate_digest", owner="aoa-agents"),
        role_resolution_ref=_content_ref(cp, role_resolution, object_field="resolution_id", digest_field="resolution_digest", owner="aoa-agents"),
        model_fit_query_result_ref=_content_ref(cp, fit, object_field="result_id", digest_field="result_digest", owner="aoa-models"),
        model_fit_projection_ref=projection_ref, provenance=compiler_ref,
    )
    binding_path = output_dir / "incarnation-binding.json"
    _write(binding_path, binding.model_dump(mode="json"))

    launch_manifest = {
        "schema_version": "abyss_stack_external_actor_launch_manifest_v1", "launch_id": f"launch:{route_id}", "session_id": route_id.replace(":", "-"),
        "artifacts": {"plan": str(run_plan_path), "incarnation_binding": str(binding_path), "model_realization": str(realization_path), "task": str(task_path), "runtime_profile": str(runtime_descriptor_path), "role_contract": str(mandate_path), "result_schema": str(result_schema_path)},
        "owner_contract_paths": {"owner_execution_request_schema": str(release_root / "owners/aoa-agents/skills/aoa-summon/references/summon-request-v4.schema.json"), "task_local_dag_schema": str(dag_schema_path)},
        "workspace_path": str(workspace), "workspace_initial_posture": execution["workspace_initial_posture"], "workspace_manifest_input_id": execution["workspace_manifest_input_id"],
        "codex_executable": str(Path(execution["codex_executable"]).resolve(strict=True)), "codex_home": str(Path(execution["codex_home"]).resolve(strict=True)),
        "environment_allowlist": execution.get("environment_allowlist", ["HOME", "LANG", "PATH", "SSL_CERT_DIR", "TERM"]),
    }
    manifest_schema_path = release_root / "runtime/schemas/external-actor-launch-manifest.schema.json"
    errors = list(Draft202012Validator(_load(manifest_schema_path, label="launch manifest schema")).iter_errors(launch_manifest))
    if errors:
        raise PreparationError(f"launch manifest is invalid: {errors[0].message}")
    launch_manifest_path = output_dir / "launch-manifest.json"
    _write(launch_manifest_path, launch_manifest)
    runtime_launch_path = output_dir / "runtime-launch.json"
    try:
        subprocess.run([str(bind_executable), "--manifest", str(launch_manifest_path), "--output", str(runtime_launch_path)], check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreparationError("abyss-stack non-starting launch binding failed") from exc

    final_request_path = output_dir / "summon-request.json"
    external_compiler = _module(SUMMON_ROOT / "scripts/compile_external_execution_request.py", "aoa_agents_external_request")
    final_request = external_compiler.compile_external_execution_request(
        request_ref=execution["request_ref"], runtime_interface=execution["runtime_interface"], return_event_object_id=execution["return_event_object_id"],
        obligation_path=obligation_path, mandate_path=mandate_path, role_resolution_path=role_path, model_fit_query_result_path=fit_path,
        model_fit_projection_path=projection_path, task_local_dag_path=dag_path, incarnation_binding_path=binding_path,
        incarnation_binding_schema_path=sdk_root / "mechanics/boundary-bridge/parts/agent-incarnation-binding/schemas/agent-incarnation-binding-v2.schema.json",
        sdk_summon_request_path=sdk_request_path, sdk_summon_decision_path=sdk_decision_path, run_plan_path=run_plan_path,
        runtime_launch_path=runtime_launch_path, runtime_task_path=task_path, responsibility_transfer_path=transfer_path,
        domain_procedure_paths=domain_paths, return_event_schema_path=release_root / "runtime/schemas/external-codex-event.schema.json",
    )
    _write(final_request_path, final_request)
    manifest = {
        "schema_version": "actor-route-preparation-result-v1", "route_id": route_id, "lane": "external_cli_reviewed", "started": False,
        "selection_authority_ref": spec["model_fit"]["selection_authority_ref"],
        "artifacts": {name: {"path": str(path), "digest": _raw_digest(path)} for name, path in (
            ("obligation", obligation_path), ("role_resolution", role_path), ("mandate", mandate_path), ("model_fit_query_result", fit_path),
            ("task_local_dag", dag_path), ("responsibility_transfer", transfer_path), ("sdk_summon_request", sdk_request_path),
            ("sdk_summon_decision", sdk_decision_path), ("runtime_task", task_path), ("run_plan", run_plan_path),
            ("incarnation_binding", binding_path), ("launch_manifest", launch_manifest_path), ("runtime_launch", runtime_launch_path),
            ("summon_request", final_request_path),
        )},
        "next_route": "abyss-stack:external-codex-agent/start",
    }
    preparation_path = output_dir / "preparation-result.json"
    _write(preparation_path, manifest)
    return manifest


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--spec", type=Path, required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = compile_preparation(args.spec, args.output_dir)
    except (PreparationError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({"ok": True, **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
