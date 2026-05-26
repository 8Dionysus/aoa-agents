from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_agents


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")


def registry_context() -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    agent_names = validate_agents.validate_registry()
    tiers_by_id = validate_agents.validate_model_tier_registry()
    cohort_patterns_by_id = validate_agents.validate_cohort_composition_registry(agent_names, tiers_by_id)
    bindings_by_phase = validate_agents.validate_runtime_seam_bindings(agent_names, tiers_by_id)
    return tiers_by_id, cohort_patterns_by_id, bindings_by_phase


def copy_reference_routes_tree(destination: Path) -> Path:
    shutil.copytree(
        REPO_ROOT / "mechanics" / "checkpoint" / "parts" / "reference-routes" / "examples",
        destination,
    )
    return destination


class ReferenceRouteContractTests(unittest.TestCase):
    def test_validate_reference_route_examples_rejects_role_set_outside_cohort_pattern(self) -> None:
        tiers_by_id, cohort_patterns_by_id, bindings_by_phase = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            reference_routes_dir = copy_reference_routes_tree(Path(tmp_dir) / "reference_routes")
            manifest_path = reference_routes_dir / "solo-bounded-route" / "manifest.json"
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
            manifest_path = reference_routes_dir / "pair-change-route" / "manifest.json"
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
            manifest_path = reference_routes_dir / "pair-change-route" / "manifest.json"
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
            manifest_path = reference_routes_dir / "checkpoint-self-change-route" / "manifest.json"
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
            artifact_path = reference_routes_dir / "pair-change-route" / "work_result.json"
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


if __name__ == "__main__":
    unittest.main()
