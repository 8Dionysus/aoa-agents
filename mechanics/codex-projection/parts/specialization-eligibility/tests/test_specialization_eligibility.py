from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = (
    REPO_ROOT
    / "mechanics"
    / "codex-projection"
    / "parts"
    / "specialization-eligibility"
)
SCHEMA_PATH = PART_ROOT / "schemas" / "specialization-eligibility.schema.json"
EXAMPLE_PATH = PART_ROOT / "examples" / "specialization-eligibility.example.json"
RECORDS_DIR = PART_ROOT / "records"
READINESS_PATH = PART_ROOT / "generated" / "specialization-eligibility-readiness.min.json"
VALIDATOR_PATH = PART_ROOT / "scripts" / "validate_specialization_eligibility.py"
BUILDER_PATH = PART_ROOT / "scripts" / "build_specialization_eligibility_readiness.py"
MANIFEST_PATH = REPO_ROOT / "generated" / "codex_agents" / "projection_manifest.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_validator_fixture(temp_root: Path) -> Path:
    temp_part_root = temp_root / PART_ROOT.relative_to(REPO_ROOT)

    shutil.copytree(PART_ROOT, temp_part_root)
    shutil.copytree(REPO_ROOT / "agents" / "roles", temp_root / "agents" / "roles")
    shutil.copytree(
        REPO_ROOT / "agents" / "operating-model" / "capabilities" / "packs",
        temp_root / "agents" / "operating-model" / "capabilities" / "packs",
    )
    temp_manifest_path = temp_root / MANIFEST_PATH.relative_to(REPO_ROOT)
    temp_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MANIFEST_PATH, temp_manifest_path)

    return temp_part_root


class SpecializationEligibilityTests(unittest.TestCase):
    def test_example_validates_against_schema(self) -> None:
        schema = load_json(SCHEMA_PATH)
        example = load_json(EXAMPLE_PATH)

        self.assertIsInstance(schema, dict)
        self.assertIsInstance(example, dict)

        errors = [error.message for error in Draft202012Validator(schema).iter_errors(example)]
        self.assertEqual(errors, [])

    def test_example_is_candidate_only_and_not_projected(self) -> None:
        example = load_json(EXAMPLE_PATH)
        manifest = load_json(MANIFEST_PATH)
        generated_names = {entry["name"] for entry in manifest["generated_agents"]}

        self.assertEqual(example["projection_scope"], "base_role_profiles_only")
        self.assertEqual(example["decision"]["status"], "candidate_only")
        self.assertEqual(example["codex_install"]["install_state"], "not_projected")
        self.assertNotIn(example["codex_install"]["proposed_agent_name"], generated_names)
        self.assertTrue(example["guardrails"]["no_generated_agent_change"])
        self.assertTrue(example["guardrails"]["no_workspace_install"])
        self.assertTrue(example["guardrails"]["no_runtime_activation"])

    def test_records_cover_every_role_specialization_without_projection(self) -> None:
        schema = load_json(SCHEMA_PATH)
        manifest = load_json(MANIFEST_PATH)
        generated_names = {entry["name"] for entry in manifest["generated_agents"]}
        specialization_ids = {
            load_json(path)["id"]
            for path in (REPO_ROOT / "agents" / "roles").glob("*/specializations/*/specialization.json")
        }
        record_paths = sorted(RECORDS_DIR.glob("*.eligibility.json"))
        records = [load_json(path) for path in record_paths]

        self.assertEqual({record["specialization_id"] for record in records}, specialization_ids)
        self.assertEqual(len(records), 5)
        for record in records:
            errors = [error.message for error in Draft202012Validator(schema).iter_errors(record)]
            self.assertEqual(errors, [])
            self.assertEqual(record["projection_scope"], "base_role_profiles_only")
            self.assertEqual(record["decision"]["status"], "candidate_only")
            self.assertEqual(record["codex_install"]["install_state"], "not_projected")
            self.assertNotIn(record["codex_install"]["proposed_agent_name"], generated_names)
            self.assertTrue(record["guardrails"]["no_generated_agent_change"])
            self.assertTrue(record["guardrails"]["no_workspace_install"])
            self.assertTrue(record["guardrails"]["no_runtime_activation"])

    def test_readiness_reader_summarizes_records(self) -> None:
        readiness = load_json(READINESS_PATH)
        record_ids = {
            load_json(path)["specialization_id"]
            for path in RECORDS_DIR.glob("*.eligibility.json")
        }

        self.assertEqual(readiness["projection_scope"], "base_role_profiles_only")
        self.assertEqual(readiness["counts"]["records"], len(record_ids))
        self.assertEqual(readiness["counts"]["by_decision_status"], {"candidate_only": len(record_ids)})
        self.assertEqual(readiness["counts"]["by_install_state"], {"not_projected": len(record_ids)})
        self.assertEqual({item["specialization_id"] for item in readiness["records"]}, record_ids)
        self.assertEqual(
            readiness["projection_boundary"],
            {
                "generated_surface_policy": "no_generated_change",
                "workspace_install_policy": "no_workspace_install",
                "runtime_activation_policy": "no_runtime_activation",
            },
        )

    def test_readiness_builder_accepts_generated_reader(self) -> None:
        result = subprocess.run(
            [sys.executable, str(BUILDER_PATH), "--check"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_validator_accepts_part(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_validator_reports_readiness_builder_failures_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            temp_part_root = copy_validator_fixture(temp_root)

            record_path = temp_part_root / "records" / "architect.topology-steward.eligibility.json"
            record = load_json(record_path)
            self.assertIsInstance(record, dict)
            del record["decision"]
            record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--root", str(temp_root)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("schema violation", result.stderr)
        self.assertIn("readiness reader could not be validated", result.stderr)
        self.assertIn("decision", result.stderr)

    def test_validator_reports_non_mapping_readiness_fields_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            temp_part_root = copy_validator_fixture(temp_root)

            record_path = temp_part_root / "records" / "architect.topology-steward.eligibility.json"
            record = load_json(record_path)
            self.assertIsInstance(record, dict)
            record["decision"] = None
            record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(VALIDATOR_PATH), "--root", str(temp_root)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("schema violation at decision", result.stderr)
        self.assertIn("readiness reader could not be validated", result.stderr)
        self.assertIn("invalid required field shape", result.stderr)


if __name__ == "__main__":
    unittest.main()
