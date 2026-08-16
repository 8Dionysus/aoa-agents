from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SUMMON_ROOT = REPO_ROOT / "skills" / "aoa-summon" / "references"
SUMMON_SCRIPT_ROOT = REPO_ROOT / "skills" / "aoa-summon" / "scripts"
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
            "route_anchor": "goal:landing-proof",
            "execution_epoch": "epoch:landing-proof-1",
        },
        "summon_request": {
            "desired_role": "coder.repo-refactor",
            "transport_preference": transport,
            "parent_task_id": "goal:landing-proof",
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


def child_scope_digest(request: dict[str, object]) -> str:
    summon = request["summon_request"]
    assert isinstance(summon, dict)
    subject = {
        "desired_role": summon["desired_role"],
        "expected_outputs": request["expected_outputs"],
        "intent": request["intent"],
        "child_scope": request["child_scope"],
        "child_stop_line": request["child_stop_line"],
        "child_inputs": request["child_inputs"],
    }
    encoded = json.dumps(
        subject, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def external_incarnation() -> dict[str, object]:
    return {
        "obligation_ref": content_ref(
            "aoa-agents", "obligation:landing", "agent-obligation-v1"
        ),
        "actor_mandate_ref": content_ref(
            "aoa-agents", "mandate:landing-writer", "actor-mandate-v1"
        ),
        "task_local_dag_ref": content_ref(
            "aoa-skills", "dag:landing-proof", "aoa-task-local-dag-v2"
        ),
        "incarnation_binding_ref": content_ref(
            "aoa-sdk", "incarnation:landing-writer", "aoa_agent_incarnation_binding_v1"
        ),
        "sdk_summon_request_ref": content_ref(
            "aoa-sdk",
            "summon-request:landing-writer",
            "urn:aoa-sdk:a2a:summon-request:v4",
        ),
        "sdk_summon_decision_ref": content_ref(
            "aoa-sdk",
            "summon-decision:landing-writer",
            "urn:aoa-sdk:a2a:summon-result:v4",
        ),
        "runtime_launch_ref": content_ref(
            "abyss-stack",
            "launch:landing-writer",
            "abyss_stack_external_codex_launch_v1",
        ),
        "runtime_interface": "abyss_stack_external_codex_agent_v1",
        "responsibility_transfer_ref": {
            **content_ref(
                "aoa-agents",
                "transfer:goal-owner-to-landing-writer",
                "responsibility-transfer-v1",
            ),
            "admitted_state": "accepted",
            "holder_ids": ["actor://goal-owner", "actor://landing-writer"],
        },
        "domain_procedure_refs": [
            content_ref(
                "target-owner", "procedure:landing-preparation", "owner-procedure-v1"
            )
        ],
        "continuity_ref": content_ref(
            "aoa-sdk", "continuation:landing-writer", "continuation-obligation-v1"
        ),
        "return_event_schema_ref": content_ref(
            "abyss-stack",
            "schema:external-codex-event",
            "abyss_stack_external_codex_event_v1",
        ),
        "launches_separate_os_process": True,
        "uses_builtin_codex_subagents": False,
        "separate_cli_session": True,
        "usage_metering": "observe_only_no_budget",
    }


def external_incarnation_v4() -> dict[str, object]:
    packet = external_incarnation()
    packet.update(
        {
            "role_resolution_ref": content_ref(
                "aoa-agents",
                "role-resolution:coder:repo-refactor:executor",
                "aoa_role_resolution_v1",
            ),
            "model_fit_query_result_ref": content_ref(
                "aoa-models",
                "model-fit-query-result:landing-writer",
                "aoa_model_fit_query_result_v2",
            ),
            "model_fit_projection_ref": content_ref(
                "aoa-models",
                "model-fit-projection:luna-max-workspace-write",
                "aoa_model_fit_projection_v1",
            ),
            "model_realization_ref": content_ref(
                "aoa-models",
                "model-realization:luna-max-workspace-write",
                "aoa_model_realization_v1",
            ),
            "run_plan_ref": content_ref(
                "aoa-sdk",
                "run-plan:landing-writer",
                "aoa_control_plane_v1",
            ),
            "incarnation_binding_ref": content_ref(
                "aoa-sdk",
                "incarnation:landing-writer",
                "aoa_agent_incarnation_binding_v2",
            ),
        }
    )
    return packet


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
            "incarnation_binding_ref": content_ref(
                "aoa-sdk",
                "incarnation:landing-writer",
                "aoa_agent_incarnation_binding_v1",
            ),
            "sdk_summon_request_ref": content_ref(
                "aoa-sdk",
                "summon-request:landing-writer",
                "urn:aoa-sdk:a2a:summon-request:v4",
            ),
            "sdk_summon_decision_ref": content_ref(
                "aoa-sdk",
                "summon-decision:landing-writer",
                "urn:aoa-sdk:a2a:summon-result:v4",
            ),
            "runtime_profile_ref": content_ref(
                "abyss-stack",
                "runtime-profile:external-codex",
                "abyss_stack_external_codex_runtime_profile_v1",
            ),
            "uses_builtin_codex_subagents": False,
        },
        "runtime_state": {
            "state": "accepted",
            "child_handle": "compat://actor/landing-writer",
            "actor_handle": "actor://landing-writer",
            "process_handle": "process://external-codex/1001",
            "session_handle": "session://external-codex/landing-writer",
            "continuation_handle": "continuation://landing-writer/1",
            "runtime_result_ref": content_ref(
                "abyss-stack",
                "result:landing-writer",
                "abyss_stack_external_codex_result_v1",
            ),
            "runtime_a2a_return_ref": content_ref(
                "abyss-stack",
                "a2a-return:landing-writer",
                "abyss_stack_external_codex_a2a_return_v1",
            ),
            "usage_observation_ref": content_ref(
                "abyss-stack",
                "usage:landing-writer",
                "abyss_stack_external_codex_usage_observation_v1",
            ),
        },
        "return_validation": {
            "output_checks": {
                "workspace-diff": {
                    "received": True,
                    "artifact_ref": "artifact://workspace-diff",
                    "accepted": True,
                },
                "handoff": {
                    "received": True,
                    "artifact_ref": "artifact://handoff",
                    "accepted": True,
                },
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


def base_external_result_v4() -> dict[str, object]:
    result = copy.deepcopy(base_external_result())
    result["binding"].update(
        {
            "role_resolution_ref": content_ref(
                "aoa-agents",
                "role-resolution:coder:repo-refactor:executor",
                "aoa_role_resolution_v1",
            ),
            "model_fit_query_result_ref": content_ref(
                "aoa-models",
                "model-fit-query-result:landing-writer",
                "aoa_model_fit_query_result_v2",
            ),
            "model_fit_projection_ref": content_ref(
                "aoa-models",
                "model-fit-projection:luna-max-workspace-write",
                "aoa_model_fit_projection_v1",
            ),
            "model_realization_ref": content_ref(
                "aoa-models",
                "model-realization:luna-max-workspace-write",
                "aoa_model_realization_v1",
            ),
            "run_plan_ref": content_ref(
                "aoa-sdk",
                "run-plan:landing-writer",
                "aoa_control_plane_v1",
            ),
            "incarnation_binding_ref": content_ref(
                "aoa-sdk",
                "incarnation:landing-writer",
                "aoa_agent_incarnation_binding_v2",
            ),
            "runtime_profile_ref": content_ref(
                "abyss-stack",
                "runtime-profile:external-codex",
                "abyss_stack_external_codex_runtime_profile_v2",
            ),
        }
    )
    result["runtime_state"]["runtime_result_ref"] = content_ref(
        "abyss-stack",
        "result:landing-writer",
        "abyss_stack_external_codex_result_v2",
    )
    return result


class TestAoAAgentsSkillTreeContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.request_validator = Draft202012Validator(
            json.loads((SUMMON_ROOT / "summon-request-v3.schema.json").read_text())
        )
        cls.result_validator = Draft202012Validator(
            json.loads((SUMMON_ROOT / "summon-result-v3.schema.json").read_text())
        )
        cls.request_v4_validator = Draft202012Validator(
            json.loads((SUMMON_ROOT / "summon-request-v4.schema.json").read_text())
        )
        cls.result_v4_validator = Draft202012Validator(
            json.loads((SUMMON_ROOT / "summon-result-v4.schema.json").read_text())
        )

    def test_v4_schemas_are_current_from_byte_stable_v3_compatibility(self) -> None:
        import importlib.util

        path = SUMMON_SCRIPT_ROOT / "build_summon_v4_schemas.py"
        spec = importlib.util.spec_from_file_location("summon_v4_builder", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            spec.loader.exec_module(module)
        finally:
            sys.dont_write_bytecode = previous
        assert (
            json.loads((SUMMON_ROOT / "summon-request-v4.schema.json").read_text())
            == module.build_request_v4()
        )
        assert (
            json.loads((SUMMON_ROOT / "summon-result-v4.schema.json").read_text())
            == module.build_result_v4()
        )

    def test_external_request_compiler_is_passive_and_digest_exact(self) -> None:
        import importlib.util

        path = SUMMON_SCRIPT_ROOT / "compile_external_execution_request.py"
        source = path.read_text(encoding="utf-8")
        assert "import subprocess" not in source
        assert "codex exec" not in source
        spec = importlib.util.spec_from_file_location(
            "external_execution_request_compiler", path
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            spec.loader.exec_module(module)
        finally:
            sys.dont_write_bytecode = previous

        request = base_request("external_cli")
        request["external_incarnation"] = external_incarnation_v4()
        first = module.semantic_request_digest(request)
        request["request_digest"] = first
        assert module.semantic_request_digest(request) == first
        request["return_owner"] = "actor://another-owner"
        assert module.semantic_request_digest(request) != first

    def test_compatibility_child_request_does_not_require_external_packet(self) -> None:
        assert (
            list(self.request_validator.iter_errors(base_request("codex_local"))) == []
        )

    def test_external_cli_request_requires_complete_incarnation_packet(self) -> None:
        request = base_request("external_cli")
        assert list(self.request_validator.iter_errors(request))
        request["external_incarnation"] = external_incarnation()
        assert list(self.request_validator.iter_errors(request)) == []

    def test_v4_external_request_requires_evidence_complete_sdk_binding(self) -> None:
        request = base_request("external_cli")
        request["external_incarnation"] = external_incarnation_v4()
        assert list(self.request_v4_validator.iter_errors(request)) == []

        contradictory = copy.deepcopy(request)
        contradictory["responsibility_classification"] = {
            "disposition": "not_independent",
            "result_ref": content_ref(
                "aoa-agents",
                "classification:landing-proof",
                "responsibility-classification-v1",
            ),
            "artifact_path": "classification.json",
            "goal_ref": content_ref("aoa-agents", "goal:landing-proof", "goal-v1"),
            "current_holder_ref": content_ref(
                "aoa-agents", "actor://goal-owner", "holder-v1"
            ),
            "child_scope_digest": child_scope_digest(contradictory),
        }
        assert list(self.request_v4_validator.iter_errors(contradictory))

        for field in (
            "role_resolution_ref",
            "model_fit_query_result_ref",
            "model_fit_projection_ref",
            "model_realization_ref",
            "run_plan_ref",
        ):
            incomplete = copy.deepcopy(request)
            del incomplete["external_incarnation"][field]
            assert list(self.request_v4_validator.iter_errors(incomplete)), field

        legacy = copy.deepcopy(request)
        legacy["external_incarnation"]["incarnation_binding_ref"]["schema_version"] = (
            "aoa_agent_incarnation_binding_v1"
        )
        assert list(self.request_v4_validator.iter_errors(legacy))

    def test_v4_codex_local_request_carries_typed_not_independent_result(self) -> None:
        request = base_request("codex_local")
        assert list(self.request_v4_validator.iter_errors(request))

        request["responsibility_classification"] = {
            "disposition": "not_independent",
            "result_ref": content_ref(
                "aoa-agents",
                "classification:landing-proof",
                "responsibility-classification-v1",
            ),
            "artifact_path": "classification.json",
            "goal_ref": content_ref("aoa-agents", "goal:landing-proof", "goal-v1"),
            "current_holder_ref": content_ref(
                "aoa-agents", "actor://goal-owner", "holder-v1"
            ),
            "execution_epoch": "epoch:landing-proof-1",
            "child_scope_digest": child_scope_digest(request),
        }
        assert list(self.request_v4_validator.iter_errors(request)) == []

        missing_route_anchor = copy.deepcopy(request)
        del missing_route_anchor["quest_passport"]["route_anchor"]
        assert list(self.request_v4_validator.iter_errors(missing_route_anchor))

        missing_ref = copy.deepcopy(request)
        del missing_ref["responsibility_classification"]["result_ref"]
        assert list(self.request_v4_validator.iter_errors(missing_ref))

        wrong_ref = copy.deepcopy(request)
        wrong_ref["responsibility_classification"]["result_ref"] = content_ref(
            "aoa-sdk", "classification:landing-proof", "responsibility-classification-v1"
        )
        assert list(self.request_v4_validator.iter_errors(wrong_ref))

        either_request = base_request("either")
        assert list(self.request_v4_validator.iter_errors(either_request))
        either_request["responsibility_classification"] = copy.deepcopy(
            request["responsibility_classification"]
        )
        assert list(self.request_v4_validator.iter_errors(either_request))

        remote_request = base_request("a2a_remote")
        assert list(self.request_v4_validator.iter_errors(remote_request))

    def test_local_request_resolves_and_binds_exact_classification_artifact(self) -> None:
        import importlib.util

        compiler_path = (
            REPO_ROOT / "skills/aoa-agents-skills/scripts/compile_actor_contract.py"
        )
        compiler_spec = importlib.util.spec_from_file_location(
            "classification_compiler", compiler_path
        )
        assert compiler_spec is not None and compiler_spec.loader is not None
        compiler = importlib.util.module_from_spec(compiler_spec)
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            compiler_spec.loader.exec_module(compiler)
        finally:
            sys.dont_write_bytecode = previous

        semantic = {
            "classification_id": "classification:landing-proof",
            "goal_ref": content_ref("aoa-agents", "goal:landing-proof", "goal-v1"),
            "current_holder_ref": content_ref(
                "aoa-agents", "actor://goal-owner", "holder-v1"
            ),
            "execution_epoch": "epoch:landing-proof-1",
            "child_scope_digest": child_scope_digest(base_request("codex_local")),
            "reason": "The requested reviewer remains an ordinary local step.",
            "stop_line": "Stop if the local child gains independent authority.",
            "evidence_refs": [
                content_ref("aoa-agents", "evidence:landing-proof", "evidence-v1")
            ],
        }
        classification = compiler.compile_classification(semantic)

        validator_path = SUMMON_SCRIPT_ROOT / "validate_summon_request.py"
        validator_spec = importlib.util.spec_from_file_location(
            "summon_request_validator", validator_path
        )
        assert validator_spec is not None and validator_spec.loader is not None
        validator = importlib.util.module_from_spec(validator_spec)
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            validator_spec.loader.exec_module(validator)
        finally:
            sys.dont_write_bytecode = previous

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            classification_path = root / "classification.json"
            classification_path.write_text(
                json.dumps(classification, sort_keys=True), encoding="utf-8"
            )
            request = base_request("codex_local")
            request["responsibility_classification"] = {
                "disposition": classification["disposition"],
                "result_ref": content_ref(
                    "aoa-agents",
                    classification["classification_id"],
                    "responsibility-classification-v1",
                ),
                "artifact_path": "classification.json",
                "goal_ref": classification["goal_ref"],
                "current_holder_ref": classification["current_holder_ref"],
                "execution_epoch": classification["execution_epoch"],
                "child_scope_digest": classification["child_scope_digest"],
            }
            request["responsibility_classification"]["result_ref"]["digest"] = (
                classification["classification_digest"]
            )
            request["request_digest"] = validator.request_digest(request)
            request_path = root / "request.json"
            request_path.write_text(
                json.dumps(request, sort_keys=True), encoding="utf-8"
            )

            proof = validator.validate_request(request_path)
            assert proof["transport_preference"] == "codex_local"
            assert proof["classification"]["classification_ref"]["digest"] == (
                classification["classification_digest"]
            )

            tampered_passport = copy.deepcopy(request)
            tampered_passport["quest_passport"]["route_anchor"] = "goal:other"
            tampered_passport["request_digest"] = validator.request_digest(
                tampered_passport
            )
            request_path.write_text(
                json.dumps(tampered_passport, sort_keys=True), encoding="utf-8"
            )
            with self.assertRaisesRegex(validator.SummonRequestError, "route_anchor"):
                validator.validate_request(request_path)

            tampered = copy.deepcopy(request)
            tampered["responsibility_classification"]["goal_ref"] = content_ref(
                "aoa-agents", "goal:other", "goal-v1"
            )
            tampered["request_digest"] = validator.request_digest(tampered)
            request_path.write_text(
                json.dumps(tampered, sort_keys=True), encoding="utf-8"
            )
            with self.assertRaisesRegex(validator.SummonRequestError, "goal_ref"):
                validator.validate_request(request_path)

            tampered_scope = copy.deepcopy(request)
            tampered_scope["child_scope"]["task"] = "A different local duty."
            tampered_scope["request_digest"] = validator.request_digest(tampered_scope)
            request_path.write_text(
                json.dumps(tampered_scope, sort_keys=True), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                validator.SummonRequestError, "child_scope_digest"
            ):
                validator.validate_request(request_path)

            stale_epoch = copy.deepcopy(request)
            stale_epoch["quest_passport"]["execution_epoch"] = "epoch:landing-proof-2"
            stale_epoch["request_digest"] = validator.request_digest(stale_epoch)
            request_path.write_text(
                json.dumps(stale_epoch, sort_keys=True), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                validator.SummonRequestError, "execution_epoch"
            ):
                validator.validate_request(request_path)

    def test_not_independent_disposition_has_owner_schema_and_compiler(self) -> None:
        import importlib.util

        schema_path = (
            REPO_ROOT
            / "skills/aoa-agents-skills/references/responsibility-classification-v1.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        semantic = {
            "classification_id": "classification:landing-proof",
            "goal_ref": content_ref("aoa-agents", "goal:landing-proof", "goal-v1"),
            "current_holder_ref": content_ref(
                "aoa-agents", "holder:landing-proof", "holder-v1"
            ),
            "execution_epoch": "epoch:landing-proof-1",
            "child_scope_digest": child_scope_digest(base_request("codex_local")),
            "reason": "The requested reviewer is an ordinary local decomposition step.",
            "stop_line": "Stop if the local child request gains independent authority.",
            "evidence_refs": [
                content_ref("aoa-agents", "evidence:landing-proof", "evidence-v1")
            ],
        }
        compiler_path = (
            REPO_ROOT / "skills/aoa-agents-skills/scripts/compile_actor_contract.py"
        )
        spec = importlib.util.spec_from_file_location("actor_contract_compiler", compiler_path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            spec.loader.exec_module(module)
        finally:
            sys.dont_write_bytecode = previous

        result = module.compile_classification(semantic)
        assert list(Draft202012Validator(schema).iter_errors(result)) == []
        assert result["disposition"] == "not_independent"
        assert result["next_route"] == "codex_local"
        assert result["execution_epoch"] == "epoch:landing-proof-1"
        invalid = copy.deepcopy(result)
        invalid["disposition"] = "independent"
        assert list(Draft202012Validator(schema).iter_errors(invalid))

    def test_responsibility_classification_has_its_own_execution_contract(self) -> None:
        graph = yaml.safe_load(
            (
                REPO_ROOT / "capabilities/families/agent-lifecycle.yaml"
            ).read_text(encoding="utf-8")
        )
        nodes = {node["id"]: node for node in graph["nodes"]}
        detector = nodes["mode.agents.detect-obligation"]
        classifier = nodes["mode.agents.responsibility-classification"]

        assert classifier["execution"] != detector["execution"]
        assert classifier["execution"]["effects"] == ["none"]
        assert any(
            "one responsibility classification" in item
            for item in classifier["execution"]["termination"]
        )
        assert any(
            "selects no agent tool" in item
            for item in classifier["execution"]["verification"]
        )
        assert any(
            "transport implementation" in item
            and "codex_local compatibility route" in item
            for item in classifier["execution"]["verification"]
        )
        assert any(
            "execution epoch" in item
            for item in classifier["execution"]["verification"]
        )
        assert any(
            "compaction" in item for item in classifier["execution"]["failure_modes"]
        )

    def test_v3_compatibility_request_remains_byte_contract_v1(self) -> None:
        request = base_request("external_cli")
        request["external_incarnation"] = external_incarnation()

        assert list(self.request_validator.iter_errors(request)) == []
        assert list(self.request_v4_validator.iter_errors(request))

    def test_external_cli_request_rejects_builtin_subagent_binding(self) -> None:
        request = base_request("external_cli")
        packet = external_incarnation()
        packet["uses_builtin_codex_subagents"] = True
        request["external_incarnation"] = packet
        assert list(self.request_validator.iter_errors(request))

    def test_external_cli_request_rejects_stronger_owner_ref_drift(self) -> None:
        owner_fields = {
            "obligation_ref": "aoa-agents",
            "actor_mandate_ref": "aoa-agents",
            "task_local_dag_ref": "aoa-skills",
            "incarnation_binding_ref": "aoa-sdk",
            "sdk_summon_request_ref": "aoa-sdk",
            "sdk_summon_decision_ref": "aoa-sdk",
            "runtime_launch_ref": "abyss-stack",
            "continuity_ref": "aoa-sdk",
            "return_event_schema_ref": "abyss-stack",
            "responsibility_transfer_ref": "aoa-agents",
        }
        for field, expected_owner in owner_fields.items():
            request = base_request("external_cli")
            packet = external_incarnation()
            packet[field]["owner_repo"] = "unrelated-owner"
            request["external_incarnation"] = packet
            assert list(self.request_validator.iter_errors(request)), (
                field,
                expected_owner,
            )

    def test_external_cli_request_requires_admitted_holder_transition(self) -> None:
        for mutation in ("same-holder", "unadmitted", "wrong-owner"):
            request = base_request("external_cli")
            packet = external_incarnation()
            transfer = packet["responsibility_transfer_ref"]
            if mutation == "same-holder":
                transfer["holder_ids"] = [
                    "actor://goal-owner",
                    "actor://goal-owner",
                ]
            elif mutation == "unadmitted":
                transfer["admitted_state"] = "proposed"
            else:
                transfer["owner_repo"] = "unrelated-owner"
            request["external_incarnation"] = packet
            assert list(self.request_validator.iter_errors(request)), mutation

        stable_contract_fields = (
            "obligation_ref",
            "actor_mandate_ref",
            "task_local_dag_ref",
            "incarnation_binding_ref",
            "sdk_summon_request_ref",
            "sdk_summon_decision_ref",
            "runtime_launch_ref",
            "return_event_schema_ref",
        )
        for field in stable_contract_fields:
            request = base_request("external_cli")
            packet = external_incarnation()
            packet[field]["schema_version"] = "unrelated-contract-v1"
            request["external_incarnation"] = packet
            assert list(self.request_validator.iter_errors(request)), field

    def test_external_result_requires_canonical_actor_runtime_handles(self) -> None:
        result = base_external_result()
        del result["runtime_state"]["child_handle"]
        assert list(self.result_validator.iter_errors(result)) == []
        broken = copy.deepcopy(result)
        del broken["runtime_state"]["session_handle"]
        assert list(self.result_validator.iter_errors(broken))

    def test_v4_external_result_preserves_role_and_fit_refs(self) -> None:
        result = base_external_result_v4()
        assert list(self.result_v4_validator.iter_errors(result)) == []

        for field in (
            "role_resolution_ref",
            "model_fit_query_result_ref",
            "model_fit_projection_ref",
            "model_realization_ref",
            "run_plan_ref",
        ):
            incomplete = copy.deepcopy(result)
            del incomplete["binding"][field]
            assert list(self.result_v4_validator.iter_errors(incomplete)), field

        legacy = copy.deepcopy(result)
        legacy["binding"]["incarnation_binding_ref"]["schema_version"] = (
            "aoa_agent_incarnation_binding_v1"
        )
        assert list(self.result_v4_validator.iter_errors(legacy))

        legacy_runtime = copy.deepcopy(result)
        legacy_runtime["binding"]["runtime_profile_ref"]["schema_version"] = (
            "abyss_stack_external_codex_runtime_profile_v1"
        )
        assert list(self.result_v4_validator.iter_errors(legacy_runtime))

        legacy_result = copy.deepcopy(result)
        legacy_result["runtime_state"]["runtime_result_ref"]["schema_version"] = (
            "abyss_stack_external_codex_result_v1"
        )
        assert list(self.result_v4_validator.iter_errors(legacy_result))

    def test_v3_result_keeps_historical_runtime_profile_v1_contract(self) -> None:
        legacy = base_external_result()
        assert list(self.result_validator.iter_errors(legacy)) == []
        legacy["binding"]["runtime_profile_ref"]["schema_version"] = (
            "abyss_stack_external_codex_runtime_profile_v2"
        )
        assert list(self.result_validator.iter_errors(legacy))

        legacy = base_external_result()
        legacy["runtime_state"]["runtime_result_ref"]["schema_version"] = (
            "abyss_stack_external_codex_result_v2"
        )
        assert list(self.result_validator.iter_errors(legacy))

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

    def test_external_result_requires_the_abyss_stack_runtime_owner(self) -> None:
        result = base_external_result()
        result["binding"]["runtime_owner"] = "unrelated-owner"
        assert list(self.result_validator.iter_errors(result))

    def test_external_accepted_result_requires_runtime_owned_return_refs(self) -> None:
        result = base_external_result()
        del result["runtime_state"]["runtime_a2a_return_ref"]
        assert list(self.result_validator.iter_errors(result))

    def test_external_result_rejects_binding_ref_owner_or_contract_drift(self) -> None:
        fields = {
            "incarnation_binding_ref": "aoa-sdk",
            "sdk_summon_request_ref": "aoa-sdk",
            "sdk_summon_decision_ref": "aoa-sdk",
            "runtime_profile_ref": "abyss-stack",
        }
        for field, expected_owner in fields.items():
            result = base_external_result()
            result["binding"][field]["owner_repo"] = "unrelated-owner"
            assert list(self.result_validator.iter_errors(result)), (
                field,
                expected_owner,
            )

            result = base_external_result()
            result["binding"][field]["schema_version"] = "unrelated-contract-v1"
            assert list(self.result_validator.iter_errors(result)), field

    def test_external_result_rejects_runtime_ref_owner_or_contract_drift(self) -> None:
        fields = (
            "runtime_result_ref",
            "runtime_a2a_return_ref",
            "usage_observation_ref",
        )
        for field in fields:
            result = base_external_result()
            result["runtime_state"][field]["owner_repo"] = "unrelated-owner"
            assert list(self.result_validator.iter_errors(result)), field

            result = base_external_result()
            result["runtime_state"][field]["schema_version"] = "unrelated-contract-v1"
            assert list(self.result_validator.iter_errors(result)), field

    def test_result_compiler_contract_names_exact_role_resolution_input(self) -> None:
        contract = yaml.safe_load(
            (SUMMON_ROOT / "contract.yaml").read_text(encoding="utf-8")
        )
        input_chain = contract["result_compiler"]["input_chain"]
        assert (
            "exact aoa-agents aoa-role-resolution-v1 artifact selected by both "
            "the mandate and request"
        ) in input_chain

    def test_role_first_entry_exposes_only_semantic_caller_fields(self) -> None:
        intent_schema = json.loads(
            (
                REPO_ROOT
                / "skills/aoa-agents-skills/references/role-first-intent-v1.schema.json"
            ).read_text(encoding="utf-8")
        )
        valid = {
            "schema_version": "role-first-intent-v1",
            "execution_intent": "execute",
            "goal": "Land the owner-valid role-first entry surface",
            "independent_duty": "Form and run one external implementation actor",
            "authority": {
                "permissions": ["workspace-write"],
                "allowed_effects": ["repo-write"],
                "prohibited_effects": ["unrelated-repositories"],
                "stop_line": "Stop at owner ambiguity or outside-scope effects",
            },
            "expected_result": ["validated external return"],
        }
        assert list(Draft202012Validator(intent_schema).iter_errors(valid)) == []

        prepare = copy.deepcopy(valid)
        prepare["execution_intent"] = "prepare"
        assert list(Draft202012Validator(intent_schema).iter_errors(prepare)) == []

        invalid_intent = copy.deepcopy(valid)
        invalid_intent["execution_intent"] = "autospawn"
        assert list(Draft202012Validator(intent_schema).iter_errors(invalid_intent))

        low_level = copy.deepcopy(valid)
        low_level["owner_roots"] = {"aoa_agents": "/not-caller-facing"}
        assert list(Draft202012Validator(intent_schema).iter_errors(low_level))

        procedure = (
            REPO_ROOT / "skills/aoa-agents-skills/references/role-first-entry.md"
        ).read_text(encoding="utf-8")
        assert "role-first-intent-v1" in procedure
        assert "summon-request-v4" in procedure
        assert "built-in Codex child agents" in procedure
        assert "model-specific command" in procedure
        assert "explicit apply" in procedure
        assert "awaiting_apply" in procedure
        assert "complete direct imperative means" in procedure
        assert "supplies apply authority in the same request" in procedure
        assert "mere mention of an" in procedure
        assert "role-first-entry" in (
            REPO_ROOT
            / "skills/aoa-agents-skills/references/source-return.md"
        ).read_text(encoding="utf-8")
        source_return = (
            REPO_ROOT
            / "skills/aoa-agents-skills/references/source-return.md"
        ).read_text(encoding="utf-8")
        assert "agents/roles/*/profile.json" in source_return
        assert "specializations/*/specialization.json" in source_return
        assert "agents/operating-model/tiers/*.tier.json" in source_return
        assert "preferred_tier_ids" in source_return
        assert "exact capability-pack source" in source_return
        assert "capability_pack_ref" in source_return
        assert "After selecting the role, optional" in procedure
        assert "specialization, and tier" in procedure
        assert "do not scan for, infer, or invent a pack" in procedure
        assert "generated reader as role authority" in procedure

        prompt_surface = yaml.safe_load(
            (
                REPO_ROOT / "skills/aoa-agents-skills/agents/openai.yaml"
            ).read_text(encoding="utf-8")
        )
        prompt = prompt_surface["interface"]["default_prompt"]
        assert "routing control plane" in prompt
        assert "owner-local classification stage" in prompt
        assert "before any built-in Codex agent tool" not in prompt
        assert "external CLI actor" in prompt
        assert "explicit execution request as apply authority" in prompt

    def test_agent_tool_selection_routes_through_responsibility_first(self) -> None:
        root_skill = (
            REPO_ROOT / "skills/aoa-agents-skills/SKILL.md"
        ).read_text(encoding="utf-8")
        summon_skill = (
            REPO_ROOT / "skills/aoa-summon/SKILL.md"
        ).read_text(encoding="utf-8")
        summon_prompt = yaml.safe_load(
            (REPO_ROOT / "skills/aoa-summon/agents/openai.yaml").read_text(
                encoding="utf-8"
            )
        )["interface"]["default_prompt"]

        assert "## Agent-tool responsibility classification" in root_skill
        assert "aoa-sdk routing control plane or current holder explicitly presents" in root_skill
        assert "after compaction, resume, re-entry" in root_skill
        assert "typed `not_independent` disposition" in root_skill
        assert "responsibility-classification-v1" in root_skill
        assert "not a universal pre-tool hook" in root_skill
        assert "Generic requests for an agent" in summon_skill
        assert "before this skill or any built-in Codex tool" in summon_skill
        assert "after `aoa-agents-skills` returned `not_independent`" in summon_skill
        assert "after it has returned a typed not_independent disposition" in summon_skill
        assert "responsibility_classification" in summon_skill
        assert "typed `result_ref`" in summon_skill
        assert "$aoa-agents-skills must supply" in summon_prompt
        assert "return not_independent" in summon_prompt
        assert "exact responsibility classification artifact" in summon_prompt

        agents_prompt = yaml.safe_load(
            (REPO_ROOT / "skills/aoa-agents-skills/agents/openai.yaml").read_text(
                encoding="utf-8"
            )
        )["interface"]["default_prompt"]
        assert "routing control plane" in agents_prompt
        assert "owner-local classification stage" in agents_prompt
        assert "before any built-in Codex agent tool" not in agents_prompt

        summon_contract = yaml.safe_load(
            (REPO_ROOT / "skills/aoa-summon/references/contract.yaml").read_text(
                encoding="utf-8"
            )
        )
        assert "explicit delegation intent" not in summon_contract["applicability"]["positive"]
        assert "after aoa-agents-skills returned not_independent" in summon_contract[
            "applicability"
        ]["positive"]
        assert any(
            "responsibility_classification" in item
            for item in summon_contract["input_abi"]["required_additions"]
        )
        classification_contract = yaml.safe_load(
            (REPO_ROOT / "skills/aoa-agents-skills/references/contract.yaml").read_text(
                encoding="utf-8"
            )
        )
        assert (
            classification_contract["modes"]["responsibility-classification"][
                "output_abi"
            ]
            == "responsibility-classification-v1"
        )
        assert (
            classification_contract["modes"]["responsibility-classification"][
                "output_schema"
            ]
            == "responsibility-classification-v1.schema.json"
        )
