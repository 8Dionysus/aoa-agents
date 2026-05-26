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


class AlphaReferenceRouteTests(unittest.TestCase):
    def test_validate_alpha_reference_routes_rejects_playbook_id_name_mismatch(self) -> None:
        _, cohort_patterns_by_id, _ = registry_context()

        with tempfile.TemporaryDirectory() as tmp_dir:
            alpha_routes_dir = Path(tmp_dir) / "alpha_reference_routes"
            shutil.copytree(
                REPO_ROOT / "mechanics" / "questbook" / "parts" / "alpha-reference-routes" / "examples",
                alpha_routes_dir,
            )
            first_path = alpha_routes_dir / "local-stack-diagnosis.example.json"
            second_path = alpha_routes_dir / "self-agent-checkpoint-rollout.example.json"
            first = read_json(first_path)
            second = read_json(second_path)
            assert isinstance(first, dict)
            assert isinstance(second, dict)
            first["playbook_name"], second["playbook_name"] = (
                second["playbook_name"],
                first["playbook_name"],
            )
            write_json(first_path, first)
            write_json(second_path, second)

            with patch.object(validate_agents, "ALPHA_REFERENCE_ROUTES_DIR", alpha_routes_dir):
                with self.assertRaises(validate_agents.ValidationError) as ctx:
                    validate_agents.validate_alpha_reference_routes(cohort_patterns_by_id)

        self.assertIn("pairs playbook_id", str(ctx.exception))
        self.assertIn("expected 'local-stack-diagnosis'", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
