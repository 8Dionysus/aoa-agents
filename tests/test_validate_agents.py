from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_agents


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def valid_memory_rights() -> dict[str, object]:
    return {
        "default_read_bands": ["core"],
        "default_write_bands": ["hot"],
        "allowed_recall_scopes": ["repo"],
        "promotion_rights": {
            "can_nominate": True,
            "can_confirm": True,
            "can_promote": True,
            "can_demote": False,
            "can_retire": False,
            "can_rescue": False,
            "allowed_transitions": ["hot_to_warm"],
        },
        "freeze_rights": {
            "can_recommend": True,
            "can_prepare": False,
            "can_finalize": False,
        },
    }


def transition_decision_schema() -> dict[str, object]:
    schema = validate_agents.read_json(
        REPO_ROOT / "schemas" / "artifact.transition_decision.schema.json"
    )
    assert isinstance(schema, dict)
    return schema


def valid_transition_return_payload() -> dict[str, object]:
    return {
        "artifact_type": "transition_decision",
        "decision": "return",
        "reason": "Verification detected scope drift and requires bounded re-entry.",
        "next_hop": "planner",
        "anchor_artifact": "bounded_plan",
        "reentry_note": "Re-enter from the last valid bounded plan without widening scope.",
    }


def registry_context() -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    agent_names = validate_agents.validate_registry()
    tiers_by_id = validate_agents.validate_model_tier_registry()
    cohort_patterns_by_id = validate_agents.validate_cohort_composition_registry(agent_names, tiers_by_id)
    bindings_by_phase = validate_agents.validate_runtime_seam_bindings(agent_names, tiers_by_id)
    return tiers_by_id, cohort_patterns_by_id, bindings_by_phase


def copy_reference_routes_tree(destination: Path) -> Path:
    shutil.copytree(REPO_ROOT / "examples" / "reference_routes", destination)
    return destination


def write_valid_playbooks_root(root: Path, cohort_patterns_by_id: dict[str, dict[str, object]]) -> None:
    payload = {
        "playbooks": [
            {
                "id": "AOA-P-0006",
                "participating_agents": cohort_patterns_by_id["checkpoint_cohort"]["allowed_role_sets"][0],
            },
            {
                "id": "AOA-P-0008",
                "participating_agents": cohort_patterns_by_id["orchestrated_loop"]["allowed_role_sets"][0],
                "expected_artifacts": list(validate_agents.RUNTIME_ARTIFACT_SCHEMA_PATHS),
            },
        ]
    }
    write_json(root / "generated" / "playbook_registry.min.json", payload)


def write_valid_evals_root(root: Path) -> None:
    payload = {
        "artifact_contract_refs": [
            "repo:aoa-evals/generated/eval_catalog.min.json",
            "repo:aoa-agents/docs/PUBLISHED_CONTRACT_COMPATIBILITY.md",
        ]
    }
    write_json(
        root / "examples" / "artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
        payload,
    )


def write_valid_memo_root(root: Path) -> None:
    write_json(
        root / "examples" / "checkpoint_to_memory_contract.example.json",
        {
            "artifact_refs": [
                "repo:aoa-agents/docs/AGENT_RUNTIME_SEAM.md",
                "repo:aoa-agents/generated/runtime_seam_bindings.json",
            ]
        },
    )

    for surface_file in validate_agents.MEMO_OBJECT_SURFACE_PATHS:
        write_json(root / surface_file, {"surface": surface_file})

    for contract_file, mode in validate_agents.MEMO_OBJECT_RECALL_CONTRACTS:
        payload: dict[str, object] = {
            "mode": mode,
            "inspect_surface": validate_agents.MEMO_OBJECT_INSPECT_SURFACE,
            "expand_surface": validate_agents.MEMO_OBJECT_EXPAND_SURFACE,
        }
        if mode in validate_agents.MEMO_CAPSULE_REQUIRED_MODES:
            payload["capsule_surface"] = validate_agents.MEMO_OBJECT_CAPSULE_SURFACE
        write_json(root / contract_file, payload)


def write_valid_routing_root(
    root: Path,
    tiers_by_id: dict[str, dict[str, object]],
    *,
    doctrine_modes: list[str] | None = None,
) -> None:
    if doctrine_modes is None:
        doctrine_modes = ["working", "semantic", "lineage"]
    object_contracts = {
        mode: contract_file for contract_file, mode in validate_agents.MEMO_OBJECT_RECALL_CONTRACTS
    }
    doctrine_capsule_surfaces_by_mode = {
        mode: validate_agents.ROUTING_MEMO_DOCTRINE_CAPSULE_SURFACE
        for mode in doctrine_modes
        if mode in validate_agents.MEMO_CAPSULE_REQUIRED_MODES
    }
    recall_payload: dict[str, object] = {
        "enabled": True,
        "supported_modes": doctrine_modes,
        "default_mode": "working",
        "contracts_by_mode": {
            "working": "examples/recall_contract.working.json",
            "semantic": "examples/recall_contract.semantic.json",
            "lineage": "examples/recall_contract.lineage.json",
        },
        "parallel_families": {
            validate_agents.ROUTING_MEMO_OBJECT_RECALL_FAMILY: {
                "inspect_surface": validate_agents.MEMO_OBJECT_INSPECT_SURFACE,
                "expand_surface": validate_agents.MEMO_OBJECT_EXPAND_SURFACE,
                "supported_modes": [mode for _, mode in validate_agents.MEMO_OBJECT_RECALL_CONTRACTS],
                "default_mode": "working",
                "contracts_by_mode": object_contracts,
                "capsule_surfaces_by_mode": {
                    "semantic": validate_agents.MEMO_OBJECT_CAPSULE_SURFACE,
                    "lineage": validate_agents.MEMO_OBJECT_CAPSULE_SURFACE,
                },
            }
        },
    }
    if doctrine_capsule_surfaces_by_mode:
        recall_payload["capsule_surfaces_by_mode"] = doctrine_capsule_surfaces_by_mode

    write_json(
        root / "generated" / "task_to_tier_hints.json",
        {
            "source_of_truth": {
                "tier_registry_repo": "aoa-agents",
                "tier_registry_path": "generated/model_tier_registry.json",
            },
            "hints": [
                {
                    "preferred_tier": "router",
                    "fallback_tier": "planner",
                    "output_artifact": tiers_by_id["router"]["artifact_requirement"],
                }
            ],
        },
    )

    write_json(
        root / validate_agents.ROUTING_TASK_TO_SURFACE_HINTS_PATH,
        {
            "hints": [
                {
                    "kind": "memo",
                    "actions": {
                        "inspect": {
                            "surface_file": validate_agents.ROUTING_MEMO_DOCTRINE_INSPECT_SURFACE
                        },
                        "expand": {
                            "surface_file": validate_agents.ROUTING_MEMO_DOCTRINE_EXPAND_SURFACE
                        },
                        "recall": recall_payload,
                    },
                }
            ]
        },
    )

    doctrine_queries = [
        {
            "verb": "recall",
            "target_surface": validate_agents.ROUTING_TASK_TO_SURFACE_HINTS_PATH,
            "match_key": "kind",
            "allowed_kinds": ["memo"],
        },
        {
            "verb": "recall",
            "target_surface": validate_agents.ROUTING_TASK_TO_SURFACE_HINTS_PATH,
            "match_key": "kind",
            "allowed_kinds": ["memo"],
            "recall_family": validate_agents.ROUTING_MEMO_OBJECT_RECALL_FAMILY,
        },
    ]
    starters: list[dict[str, object]] = []
    for mode in doctrine_modes:
        starters.append(
            {
                "verb": "recall",
                "target_surface": validate_agents.ROUTING_TASK_TO_SURFACE_HINTS_PATH,
                "match_key": "kind",
                "allowed_kinds": ["memo"],
                "target_kind": "memo",
                "target_value": "memo",
                "recall_mode": mode,
            }
        )
    for _, mode in validate_agents.MEMO_OBJECT_RECALL_CONTRACTS:
        starters.append(
            {
                "verb": "recall",
                "target_surface": validate_agents.ROUTING_TASK_TO_SURFACE_HINTS_PATH,
                "match_key": "kind",
                "allowed_kinds": ["memo"],
                "target_kind": "memo",
                "target_value": "memo",
                "recall_mode": mode,
                "recall_family": validate_agents.ROUTING_MEMO_OBJECT_RECALL_FAMILY,
            }
        )
    write_json(
        root / validate_agents.ROUTING_TINY_MODEL_ENTRYPOINTS_PATH,
        {
            "queries": doctrine_queries,
            "starters": starters,
        },
    )


class ValidateAgentsTests(unittest.TestCase):
    def test_validate_memory_rights_rejects_non_string_band_without_typeerror(self) -> None:
        memory_rights = valid_memory_rights()
        memory_rights["default_read_bands"] = [[]]

        with self.assertRaises(validate_agents.ValidationError) as ctx:
            validate_agents.validate_memory_rights("profiles[0]", memory_rights)

        self.assertIn(
            "profiles[0].memory_rights.default_read_bands must contain only strings",
            str(ctx.exception),
        )

    def test_validate_memory_rights_rejects_non_string_allowed_transition_without_typeerror(self) -> None:
        memory_rights = valid_memory_rights()
        promotion_rights = dict(memory_rights["promotion_rights"])
        promotion_rights["allowed_transitions"] = [["hot_to_warm"]]
        memory_rights["promotion_rights"] = promotion_rights

        with self.assertRaises(validate_agents.ValidationError) as ctx:
            validate_agents.validate_memory_rights("profiles[0]", memory_rights)

        self.assertIn(
            "profiles[0].memory_rights.promotion_rights.allowed_transitions must contain only strings",
            str(ctx.exception),
        )

    def test_resolve_aoa_agents_repo_ref_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "aoa-agents"
            repo_root.mkdir()
            (repo_root / "profiles").mkdir()
            (repo_root / "profiles" / "architect.profile.json").write_text("{}", encoding="utf-8")
            (repo_root.parent / "escape.json").write_text("{}", encoding="utf-8")

            with patch.object(validate_agents, "REPO_ROOT", repo_root):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.resolve_aoa_agents_repo_ref("repo:aoa-agents/../escape.json")

        self.assertIn("aoa-agents repo ref must stay inside this repository", str(ctx.exception))

    def test_optional_consumer_smoke_checks_ignore_non_aoa_agents_eval_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            evals_root = Path(tmp_dir) / "aoa-evals"
            payload = {
                "artifact_contract_refs": [
                    "repo:aoa-evals/generated/eval_catalog.min.json",
                    "repo:aoa-agents/docs/AGENT_PROFILE_SURFACE.md",
                ]
            }
            write_json(
                evals_root
                / "examples"
                / "artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json",
                payload,
            )

            with patch.dict(
                os.environ,
                {
                    "AOA_PLAYBOOKS_ROOT": "",
                    "AOA_EVALS_ROOT": str(evals_root),
                    "AOA_MEMO_ROOT": "",
                    "AOA_ROUTING_ROOT": "",
                },
                clear=False,
            ):
                checked = validate_agents.validate_optional_consumer_smoke_checks({}, {})

        self.assertEqual(checked, ["aoa-evals"])

    def test_transition_decision_schema_accepts_return_with_anchor_and_reentry(self) -> None:
        validate_agents.validate_instance_against_schema(
            valid_transition_return_payload(),
            transition_decision_schema(),
            "transition_decision",
        )

    def test_transition_decision_schema_rejects_return_without_anchor_artifact(self) -> None:
        payload = valid_transition_return_payload()
        del payload["anchor_artifact"]

        with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
            validate_agents.validate_instance_against_schema(
                payload,
                transition_decision_schema(),
                "transition_decision",
            )

        self.assertEqual(ctx.exception.code, "missing_required_field")
        self.assertIn("anchor_artifact", str(ctx.exception))

    def test_transition_decision_schema_rejects_return_without_reentry_note(self) -> None:
        payload = valid_transition_return_payload()
        del payload["reentry_note"]

        with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
            validate_agents.validate_instance_against_schema(
                payload,
                transition_decision_schema(),
                "transition_decision",
            )

        self.assertEqual(ctx.exception.code, "missing_required_field")
        self.assertIn("reentry_note", str(ctx.exception))

    def test_transition_decision_baseline_example_still_validates(self) -> None:
        payload = validate_agents.read_json(
            REPO_ROOT / "examples" / "runtime_artifacts" / "transition_decision.example.json"
        )
        self.assertIsInstance(payload, dict)
        validate_agents.validate_instance_against_schema(
            payload,
            transition_decision_schema(),
            "transition_decision.example",
        )

    def test_validate_runtime_artifact_examples_checks_supplemental_transition_examples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            examples_dir = temp_root / "examples"
            examples_dir.mkdir()
            write_json(
                examples_dir / "transition_decision.example.json",
                {
                    "artifact_type": "transition_decision",
                    "decision": "continue",
                    "reason": "Verification passed and the route can continue safely.",
                    "next_hop": "archivist",
                },
            )
            write_json(
                examples_dir / "transition_decision.return.example.json",
                {
                    "artifact_type": "transition_decision",
                    "decision": "return",
                    "reason": "Scope drift requires bounded re-entry.",
                    "next_hop": "planner",
                },
            )

            with patch.object(validate_agents, "RUNTIME_ARTIFACT_EXAMPLES_DIR", examples_dir):
                with patch.object(
                    validate_agents,
                    "RUNTIME_ARTIFACT_SCHEMA_PATHS",
                    {
                        "transition_decision": REPO_ROOT
                        / "schemas"
                        / "artifact.transition_decision.schema.json"
                    },
                ):
                    with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
                        validate_agents.validate_runtime_artifact_examples()

        self.assertEqual(ctx.exception.code, "missing_required_field")
        self.assertIn("anchor_artifact", str(ctx.exception))

    def test_validate_negative_runtime_artifact_examples_accepts_expanded_fixture_set(self) -> None:
        validate_agents.validate_negative_runtime_artifact_examples()

    def test_validate_registry_rejects_top_level_key_order_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "agent_registry.min.json"
            payload = read_json(REPO_ROOT / "generated" / "agent_registry.min.json")
            assert isinstance(payload, dict)
            drifted_payload = {
                "layer": payload["layer"],
                "version": payload["version"],
                "agents": payload["agents"],
            }
            write_json(path, drifted_payload)

            with patch.object(validate_agents, "REGISTRY_PATH", path):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.validate_registry()

        self.assertIn("stable order", str(ctx.exception))

    def test_validate_registry_rejects_renamed_published_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "agent_registry.min.json"
            payload = read_json(REPO_ROOT / "generated" / "agent_registry.min.json")
            assert isinstance(payload, dict)
            assert isinstance(payload["agents"], list)
            first_agent = dict(payload["agents"][0])
            renamed_agent: dict[str, object] = {}
            for key, value in first_agent.items():
                if key == "handoff_rule":
                    renamed_agent["handoff_policy"] = value
                else:
                    renamed_agent[key] = value
            payload["agents"][0] = renamed_agent
            write_json(path, payload)

            with patch.object(validate_agents, "REGISTRY_PATH", path):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.validate_registry()

        self.assertIn("stable order", str(ctx.exception))

    def test_validate_model_tier_registry_rejects_publication_order_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "model_tier_registry.json"
            payload = read_json(REPO_ROOT / "generated" / "model_tier_registry.json")
            assert isinstance(payload, dict)
            assert isinstance(payload["model_tiers"], list)
            payload["model_tiers"][0], payload["model_tiers"][1] = (
                payload["model_tiers"][1],
                payload["model_tiers"][0],
            )
            write_json(path, payload)

            with patch.object(validate_agents, "MODEL_TIER_REGISTRY_PATH", path):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.validate_model_tier_registry()

        self.assertIn("stable publication order", str(ctx.exception))

    def test_validate_reference_route_examples_rejects_role_set_outside_cohort_pattern(self) -> None:
        tiers_by_id, cohort_patterns_by_id, bindings_by_phase = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            reference_routes_dir = copy_reference_routes_tree(Path(tmp_dir) / "reference_routes")
            manifest_path = reference_routes_dir / "solo_bounded_route" / "manifest.json"
            manifest = read_json(manifest_path)
            assert isinstance(manifest, dict)
            manifest["role_set"] = ["architect", "coder"]
            write_json(manifest_path, manifest)

            with patch.object(validate_agents, "REFERENCE_ROUTES_DIR", reference_routes_dir):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.validate_reference_route_examples(
                        tiers_by_id, cohort_patterns_by_id, bindings_by_phase
                    )

        self.assertIn("allowed_role_sets", str(ctx.exception))

    def test_validate_reference_route_examples_rejects_tier_outside_pattern(self) -> None:
        tiers_by_id, cohort_patterns_by_id, bindings_by_phase = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            reference_routes_dir = copy_reference_routes_tree(Path(tmp_dir) / "reference_routes")
            manifest_path = reference_routes_dir / "pair_change_route" / "manifest.json"
            manifest = read_json(manifest_path)
            assert isinstance(manifest, dict)
            assert isinstance(manifest["steps"], list)
            manifest["steps"][0]["tier_id"] = "router"
            write_json(manifest_path, manifest)

            with patch.object(validate_agents, "REFERENCE_ROUTES_DIR", reference_routes_dir):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.validate_reference_route_examples(
                        tiers_by_id, cohort_patterns_by_id, bindings_by_phase
                    )

        self.assertIn("preferred_tier_ids", str(ctx.exception))

    def test_validate_reference_route_examples_rejects_invalid_phase(self) -> None:
        tiers_by_id, cohort_patterns_by_id, bindings_by_phase = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            reference_routes_dir = copy_reference_routes_tree(Path(tmp_dir) / "reference_routes")
            manifest_path = reference_routes_dir / "pair_change_route" / "manifest.json"
            manifest = read_json(manifest_path)
            assert isinstance(manifest, dict)
            assert isinstance(manifest["steps"], list)
            manifest["steps"][0]["phase"] = "ship"
            write_json(manifest_path, manifest)

            with patch.object(validate_agents, "REFERENCE_ROUTES_DIR", reference_routes_dir):
                with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
                    validate_agents.validate_reference_route_examples(
                        tiers_by_id, cohort_patterns_by_id, bindings_by_phase
                    )

        self.assertEqual(ctx.exception.code, "invalid_enum_value")
        self.assertIn("phase", str(ctx.exception))

    def test_validate_reference_route_examples_rejects_broken_artifact_path(self) -> None:
        tiers_by_id, cohort_patterns_by_id, bindings_by_phase = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            reference_routes_dir = copy_reference_routes_tree(Path(tmp_dir) / "reference_routes")
            manifest_path = reference_routes_dir / "checkpoint_self_change_route" / "manifest.json"
            manifest = read_json(manifest_path)
            assert isinstance(manifest, dict)
            assert isinstance(manifest["steps"], list)
            manifest["steps"][0]["artifact_path"] = "missing.json"
            write_json(manifest_path, manifest)

            with patch.object(validate_agents, "REFERENCE_ROUTES_DIR", reference_routes_dir):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.validate_reference_route_examples(
                        tiers_by_id, cohort_patterns_by_id, bindings_by_phase
                    )

        self.assertIn("does not resolve to an existing file", str(ctx.exception))

    def test_validate_reference_route_examples_rejects_schema_invalid_artifact(self) -> None:
        tiers_by_id, cohort_patterns_by_id, bindings_by_phase = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            reference_routes_dir = copy_reference_routes_tree(Path(tmp_dir) / "reference_routes")
            artifact_path = reference_routes_dir / "pair_change_route" / "work_result.json"
            write_json(
                artifact_path,
                {
                    "artifact_type": "work_result",
                    "summary": "Schema-invalid work result without verification notes.",
                    "state_delta": "Updated route pack fixture.",
                },
            )

            with patch.object(validate_agents, "REFERENCE_ROUTES_DIR", reference_routes_dir):
                with self.assertRaises(validate_agents.SchemaValidationError) as ctx:
                    validate_agents.validate_reference_route_examples(
                        tiers_by_id, cohort_patterns_by_id, bindings_by_phase
                    )

        self.assertEqual(ctx.exception.code, "missing_required_field")
        self.assertIn("verification_notes", str(ctx.exception))

    def test_optional_consumer_smoke_checks_validate_playbooks_root(self) -> None:
        tiers_by_id, cohort_patterns_by_id, _ = registry_context()
        del tiers_by_id

        with tempfile.TemporaryDirectory() as tmp_dir:
            playbooks_root = Path(tmp_dir) / "aoa-playbooks"
            write_valid_playbooks_root(playbooks_root, cohort_patterns_by_id)

            with patch.dict(
                os.environ,
                {
                    "AOA_PLAYBOOKS_ROOT": str(playbooks_root),
                    "AOA_EVALS_ROOT": "",
                    "AOA_MEMO_ROOT": "",
                    "AOA_ROUTING_ROOT": "",
                },
                clear=False,
            ):
                checked = validate_agents.validate_optional_consumer_smoke_checks({}, cohort_patterns_by_id)

        self.assertEqual(checked, ["aoa-playbooks"])

    def test_optional_consumer_smoke_checks_validate_evals_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            evals_root = Path(tmp_dir) / "aoa-evals"
            write_valid_evals_root(evals_root)

            with patch.dict(
                os.environ,
                {
                    "AOA_PLAYBOOKS_ROOT": "",
                    "AOA_EVALS_ROOT": str(evals_root),
                    "AOA_MEMO_ROOT": "",
                    "AOA_ROUTING_ROOT": "",
                },
                clear=False,
            ):
                checked = validate_agents.validate_optional_consumer_smoke_checks({}, {})

        self.assertEqual(checked, ["aoa-evals"])

    def test_optional_consumer_smoke_checks_validate_memo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            memo_root = Path(tmp_dir) / "aoa-memo"
            write_valid_memo_root(memo_root)

            with patch.dict(
                os.environ,
                {
                    "AOA_PLAYBOOKS_ROOT": "",
                    "AOA_EVALS_ROOT": "",
                    "AOA_MEMO_ROOT": str(memo_root),
                    "AOA_ROUTING_ROOT": "",
                },
                clear=False,
            ):
                checked = validate_agents.validate_optional_consumer_smoke_checks({}, {})

        self.assertEqual(checked, ["aoa-memo"])

    def test_optional_consumer_smoke_checks_validate_routing_root(self) -> None:
        tiers_by_id, _, _ = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            routing_root = Path(tmp_dir) / "aoa-routing"
            write_valid_routing_root(routing_root, tiers_by_id)

            with patch.dict(
                os.environ,
                {
                    "AOA_PLAYBOOKS_ROOT": "",
                    "AOA_EVALS_ROOT": "",
                    "AOA_MEMO_ROOT": "",
                    "AOA_ROUTING_ROOT": str(routing_root),
                },
                clear=False,
            ):
                checked = validate_agents.validate_optional_consumer_smoke_checks(tiers_by_id, {})

        self.assertEqual(checked, ["aoa-routing"])

    def test_optional_consumer_smoke_checks_allow_working_only_doctrine_without_capsules(self) -> None:
        tiers_by_id, _, _ = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            routing_root = Path(tmp_dir) / "aoa-routing"
            write_valid_routing_root(routing_root, tiers_by_id, doctrine_modes=["working"])

            with patch.dict(
                os.environ,
                {
                    "AOA_PLAYBOOKS_ROOT": "",
                    "AOA_EVALS_ROOT": "",
                    "AOA_MEMO_ROOT": "",
                    "AOA_ROUTING_ROOT": str(routing_root),
                },
                clear=False,
            ):
                checked = validate_agents.validate_optional_consumer_smoke_checks(tiers_by_id, {})

        self.assertEqual(checked, ["aoa-routing"])


if __name__ == "__main__":
    unittest.main()
