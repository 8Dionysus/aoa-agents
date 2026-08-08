from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SUMMON_ROOT = REPO_ROOT / "skills" / "aoa-summon" / "references"
SHA256 = "sha256:" + "0" * 64


def content_ref(owner_repo: str, object_id: str, schema_version: str) -> dict[str, str]:
    return {
        "object_id": object_id,
        "owner_repo": owner_repo,
        "schema_version": schema_version,
        "digest": SHA256,
    }


def base_request(transport: str) -> dict[str, object]:
    return {
        "quest_passport": {
            "difficulty": "d2_slice",
            "risk": "low",
            "control_mode": "reviewed",
            "delegate_tier": "executor",
            "route_anchor": "goal://landing-proof",
        },
        "summon_request": {
            "desired_role": "coder.repo-refactor",
            "transport_preference": transport,
            "parent_task_id": "goal://landing-proof",
            "require_progression": False,
        },
        "expected_outputs": ["workspace-diff", "handoff"],
        "intent": "execute",
        "return_owner": "actor://goal-owner",
        "child_scope": {
            "task": "Prepare one bounded owner-local landing change.",
            "allowed_tools": ["shell-read", "workspace-write"],
            "allowed_effects": ["repo_mutation"],
            "authority_limit": "No commit, push, PR, merge, or external effect.",
        },
        "child_stop_line": "Stop at owner ambiguity or external effect.",
        "child_inputs": [],
        "request_ref": "task://landing-proof/summon-request",
        "request_digest": SHA256,
    }


def external_incarnation() -> dict[str, object]:
    return {
        "obligation_ref": content_ref("aoa-agents", "obligation:landing", "agent-obligation-v1"),
        "actor_mandate_ref": content_ref("aoa-agents", "mandate:landing-writer", "actor-mandate-v1"),
        "task_local_dag_ref": content_ref("aoa-skills", "dag:landing-proof", "aoa-task-local-dag-v2"),
        "incarnation_binding_ref": content_ref("aoa-sdk", "incarnation:landing-writer", "aoa_agent_incarnation_binding_v1"),
        "sdk_summon_request_ref": content_ref("aoa-sdk", "summon-request:landing-writer", "urn:aoa-sdk:a2a:summon-request:v4"),
        "sdk_summon_decision_ref": content_ref("aoa-sdk", "summon-decision:landing-writer", "urn:aoa-sdk:a2a:summon-result:v4"),
        "runtime_launch_ref": content_ref("abyss-stack", "launch:landing-writer", "abyss_stack_external_codex_launch_v1"),
        "runtime_interface": "abyss_stack_external_codex_agent_v1",
        "responsibility_from": "actor://goal-owner",
        "responsibility_to": "actor://landing-writer",
        "domain_procedure_refs": [
            content_ref("target-owner", "procedure:landing-preparation", "owner-procedure-v1")
        ],
        "continuity_ref": content_ref("aoa-sdk", "continuation:landing-writer", "continuation-obligation-v1"),
        "return_event_schema_ref": content_ref("abyss-stack", "schema:external-codex-event", "abyss_stack_external_codex_event_v1"),
        "launches_separate_os_process": True,
        "uses_builtin_codex_subagents": False,
        "separate_cli_session": True,
        "usage_metering": "observe_only_no_budget",
    }


def base_external_result() -> dict[str, object]:
    return {
        "allowed": True,
        "lane": "external_cli_reviewed",
        "execution_surface": "abyss_stack_external_codex_agent_v1",
        "cohort_pattern": "solo",
        "closeout_required": True,
        "decision_state": "allowed",
        "binding": {
            "interface": "abyss_stack_external_codex_agent_v1",
            "inspected": True,
            "available": True,
            "reason": None,
            "binding_kind": "external_cli_incarnation",
            "runtime_owner": "abyss-stack",
            "incarnation_binding_ref": content_ref("aoa-sdk", "incarnation:landing-writer", "aoa_agent_incarnation_binding_v1"),
            "sdk_summon_request_ref": content_ref("aoa-sdk", "summon-request:landing-writer", "urn:aoa-sdk:a2a:summon-request:v4"),
            "sdk_summon_decision_ref": content_ref("aoa-sdk", "summon-decision:landing-writer", "urn:aoa-sdk:a2a:summon-result:v4"),
            "runtime_profile_ref": content_ref("abyss-stack", "runtime-profile:external-codex", "abyss_stack_external_codex_runtime_profile_v1"),
            "uses_builtin_codex_subagents": False,
        },
        "runtime_state": {
            "state": "accepted",
            "child_handle": "compat://actor/landing-writer",
            "actor_handle": "actor://landing-writer",
            "process_handle": "process://external-codex/1001",
            "session_handle": "session://external-codex/landing-writer",
            "continuation_handle": "continuation://landing-writer/1",
            "runtime_result_ref": content_ref("abyss-stack", "result:landing-writer", "abyss_stack_external_codex_result_v1"),
            "runtime_a2a_return_ref": content_ref("abyss-stack", "a2a-return:landing-writer", "abyss_stack_external_codex_a2a_return_v1"),
            "usage_observation_ref": content_ref("abyss-stack", "usage:landing-writer", "abyss_stack_external_codex_usage_observation_v1"),
        },
        "return_validation": {
            "output_checks": {
                "workspace-diff": {"received": True, "artifact_ref": "artifact://workspace-diff", "accepted": True},
                "handoff": {"received": True, "artifact_ref": "artifact://handoff", "accepted": True},
            },
            "accepted": True,
        },
        "closeout_handoff": {
            "parent_owner": "actor://goal-owner",
            "residual_risk": "Independent review still required.",
            "next_route": "mode.agents.receive-return",
        },
        "actual_effects": ["external-actor-runtime"],
        "stop_line": "No external publication effect.",
        "request_ref": "task://landing-proof/summon-request",
        "request_digest": SHA256,
        "request_intent": "execute",
    }


class TestAoAAgentsSkillTreeContracts:
    @classmethod
    def setup_class(cls) -> None:
        cls.request_validator = Draft202012Validator(
            json.loads((SUMMON_ROOT / "summon-request-v3.schema.json").read_text())
        )
        cls.result_validator = Draft202012Validator(
            json.loads((SUMMON_ROOT / "summon-result-v3.schema.json").read_text())
        )

    def test_compatibility_child_request_does_not_require_external_packet(self) -> None:
        assert list(self.request_validator.iter_errors(base_request("codex_local"))) == []

    def test_external_cli_request_requires_complete_incarnation_packet(self) -> None:
        request = base_request("external_cli")
        assert list(self.request_validator.iter_errors(request))
        request["external_incarnation"] = external_incarnation()
        assert list(self.request_validator.iter_errors(request)) == []

    def test_external_cli_request_rejects_builtin_subagent_binding(self) -> None:
        request = base_request("external_cli")
        packet = external_incarnation()
        packet["uses_builtin_codex_subagents"] = True
        request["external_incarnation"] = packet
        assert list(self.request_validator.iter_errors(request))

    def test_external_result_requires_canonical_actor_runtime_handles(self) -> None:
        result = base_external_result()
        assert list(self.result_validator.iter_errors(result)) == []
        broken = copy.deepcopy(result)
        del broken["runtime_state"]["session_handle"]
        assert list(self.result_validator.iter_errors(broken))

    def test_external_decision_does_not_claim_runtime_effects_or_handles(self) -> None:
        result = base_external_result()
        result["request_intent"] = "decide"
        result["runtime_state"] = {"state": "decided", "child_handle": None}
        result["actual_effects"] = []
        result["return_validation"] = {
            "output_checks": {
                output: {
                    "received": False,
                    "artifact_ref": None,
                    "accepted": False,
                }
                for output in ("workspace-diff", "handoff")
            },
            "accepted": False,
        }
        assert list(self.result_validator.iter_errors(result)) == []

    def test_external_result_rejects_builtin_subagent_binding(self) -> None:
        result = base_external_result()
        result["binding"]["uses_builtin_codex_subagents"] = True
        assert list(self.result_validator.iter_errors(result))

    def test_external_accepted_result_requires_runtime_owned_return_refs(self) -> None:
        result = base_external_result()
        del result["runtime_state"]["runtime_a2a_return_ref"]
        assert list(self.result_validator.iter_errors(result))
