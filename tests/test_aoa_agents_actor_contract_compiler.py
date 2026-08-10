from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = ROOT / "skills" / "aoa-agents-skills" / "scripts"


def _load_module(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


COMPILER = _load_module(
    "aoa_agents_actor_contract_compiler", SCRIPT_ROOT / "compile_actor_contract.py"
)
RESOLVER = _load_module(
    "aoa_agents_role_resolver_for_compiler", SCRIPT_ROOT / "resolve_role_binding.py"
)


def _ref(owner: str, object_id: str, schema: str) -> dict[str, str]:
    return {
        "object_id": object_id,
        "owner_repo": owner,
        "schema_version": schema,
        "digest": "sha256:" + "1" * 64,
    }


def _obligation_semantic() -> dict[str, object]:
    holder = _ref("aoa-agents", "holder:goal-master", "actor-holder-v1")
    return {
        "obligation_id": "obligation:landing-preparation",
        "goal_ref": _ref("aoa-goals", "goal:external-actors", "goal-v1"),
        "phase": "execution",
        "duty": "Prepare a bounded repository change for landing",
        "domain_owner": "landing-owner",
        "current_holder": holder,
        "responsibility_boundary": "Own preparation and local proof only",
        "missed_consequence": "The parent goal retains an unlanded change",
        "independence_findings": {
            "positive_signals": ["independent reviewable return"],
            "negative_signals": ["same parent goal"],
            "rejected_ordinary_step": "The duty has its own return and proof boundary",
        },
        "trigger": {
            "strength": "master_decision",
            "authority_ref": holder,
        },
        "expected_outcomes": ["landing candidate", "local proof receipt"],
        "return_owner": holder,
        "lifecycle_posture": "task-instance",
        "stop_line": "Do not publish, merge, or widen the selected repository scope",
        "evidence_refs": [],
        "uncertainty": ["Remote CI remains with the landing owner"],
        "next_route": "form_actor",
    }


def _mandate_semantic(holder: dict[str, str]) -> dict[str, object]:
    return {
        "mandate_id": "mandate:landing-preparation-coder",
        "identity_posture": "task-instance",
        "domain_procedure_refs": [
            _ref("aoa-skills", "skill:landing", "aoa-skill-contract-v1")
        ],
        "required_executor_properties": [
            {
                "property_id": "procedure-discipline",
                "requirement": "Follow the supplied landing procedure exactly",
                "verification_route": "Review the named handoff and local receipts",
            },
            {
                "property_id": "scope-control",
                "requirement": "Keep repository effects inside the admitted worktree",
                "verification_route": "Inspect Git status and the returned diff",
            },
        ],
        "model_fit_relation": {
            "task_family": "landing",
            "relation_to_duty": "Landing preparation is the bounded write-bearing part of the broader landing family",
            "relation_authority_ref": holder,
        },
        "authority": {
            "permissions": ["read-owner-sources", "write-isolated-worktree"],
            "allowed_effects": ["workspace-write"],
            "prohibited_effects": ["remote-publication", "merge"],
            "stop_line": "Do not publish, merge, or widen the selected repository scope",
        },
        "environment": {
            "sandbox_mode": "workspace-write",
            "workspace_requirement": "One isolated owner repository worktree",
            "required_tools": ["git", "shell"],
            "required_mcp_servers": [],
            "state_root_posture": "Runtime-owned persistent external CLI state",
        },
        "continuity": {
            "posture": "task-instance",
            "identity_key": "landing-preparation-coder",
            "state_ref": None,
        },
        "named_outputs": [
            {
                "name": "landing-candidate",
                "description": "Bounded prepared repository change",
                "acceptance_route": "Landing owner review",
            },
            {
                "name": "proof-receipt",
                "description": "Exact local validation evidence",
                "acceptance_route": "Parent closeout validation",
            },
        ],
        "review_policy": "Independent landing-owner review before publication",
        "refusal_policy": "Return blocked when owner truth or scope is ambiguous",
        "wake_policy": "No automatic wake for this task-instance actor",
        "review_after": "Review on the first terminal return",
        "uncertainty": ["Model fit remains a stronger-owner decision"],
    }


def _compiled_inputs():  # type: ignore[no-untyped-def]
    obligation = COMPILER.compile_obligation(_obligation_semantic())
    resolution = RESOLVER.resolve_role_binding(
        ROOT,
        role_id="coder",
        specialization_id="coder.repo-refactor",
        tier_id="executor",
    )
    semantic = _mandate_semantic(obligation["current_holder"])
    return obligation, resolution, semantic


def test_compiles_explicit_duty_to_fit_family_without_selecting_compute() -> None:
    obligation, resolution, semantic = _compiled_inputs()
    mandate = COMPILER.compile_mandate(obligation, resolution, semantic)

    assert mandate["obligation_ref"]["digest"] == obligation["obligation_digest"]
    assert mandate["role_resolution_ref"]["digest"] == resolution["resolution_digest"]
    assert mandate["role_binding"]["specialization_id"] == "coder.repo-refactor"
    assert mandate["model_fit_relation"]["task_family"] == "landing"
    assert mandate["environment"]["sandbox_mode"] == "workspace-write"
    assert mandate["compiler_authority"] == {
        "obligation_detection_performed": False,
        "role_selection_performed": False,
        "model_selection_performed": False,
        "runtime_activation_performed": False,
    }
    encoded = json.dumps(mandate).lower()
    assert "luna" not in encoded
    assert "token_budget" not in encoded
    COMPILER._assert_digest(mandate, "mandate_digest", label="actor mandate")


def test_rejects_implicit_fit_relation_authority() -> None:
    obligation, resolution, semantic = _compiled_inputs()
    semantic["model_fit_relation"]["relation_authority_ref"] = _ref(  # type: ignore[index]
        "aoa-agents", "holder:other", "actor-holder-v1"
    )

    with pytest.raises(COMPILER.ActorContractError, match="current obligation holder"):
        COMPILER.compile_mandate(obligation, resolution, semantic)


def test_rejects_lifecycle_or_stop_line_widening() -> None:
    obligation, resolution, semantic = _compiled_inputs()
    semantic["identity_posture"] = "persistent-office"
    with pytest.raises(COMPILER.ActorContractError, match="lifecycle posture"):
        COMPILER.compile_mandate(obligation, resolution, semantic)

    semantic = _mandate_semantic(obligation["current_holder"])
    semantic["authority"]["stop_line"] = "Do anything needed"  # type: ignore[index]
    with pytest.raises(COMPILER.ActorContractError, match="stop line"):
        COMPILER.compile_mandate(obligation, resolution, semantic)


def test_rejects_duplicate_output_identity_and_digest_tampering() -> None:
    obligation, resolution, semantic = _compiled_inputs()
    semantic["named_outputs"][1]["name"] = "landing-candidate"  # type: ignore[index]
    with pytest.raises(COMPILER.ActorContractError, match="identities must be unique"):
        COMPILER.compile_mandate(obligation, resolution, semantic)

    obligation["duty"] = "Tampered duty"
    with pytest.raises(COMPILER.ActorContractError, match="digest mismatch"):
        COMPILER.compile_mandate(
            obligation,
            resolution,
            _mandate_semantic(obligation["current_holder"]),
        )


def test_semantic_inputs_cannot_smuggle_model_or_budget_fields() -> None:
    obligation, resolution, semantic = _compiled_inputs()
    semantic["model_slug"] = "gpt-5.6-luna"
    semantic["token_budget"] = 1000

    with pytest.raises(COMPILER.ActorContractError, match="extra=.*model_slug"):
        COMPILER.compile_mandate(obligation, resolution, semantic)
