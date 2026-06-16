from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTOUR_PATH = REPO_ROOT / "docs" / "CURRENT_CONTOUR.md"


class RoadmapSurfaceAlignmentTestCase(unittest.TestCase):
    def test_roadmap_routes_inventory_to_current_contour(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        contour = CONTOUR_PATH.read_text(encoding="utf-8")
        subject_prep = (
            REPO_ROOT
            / "mechanics"
            / "agon"
            / "parts"
            / "formation"
            / "docs"
            / "subject-prep.md"
        ).read_text(encoding="utf-8")

        self.assertIn("v0.4.0", readme)
        self.assertIn("[0.4.0]", changelog)
        self.assertIn("v0.4.x", roadmap)
        self.assertIn("[CURRENT_CONTOUR](docs/CURRENT_CONTOUR.md)", roadmap)
        self.assertIn("roadmap drift", roadmap)
        self.assertIn("agonic/assistant kind split", roadmap)

        for relative_path in (
            "mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md",
            "mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md",
            "mechanics/codex-projection/parts/refresh-law/examples/subagent-refresh-law.example.json",
            "mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json",
            "generated/runtime_seam_bindings.json",
            "mechanics/antifragility/parts/stress-posture/docs/stress-posture.md",
            "mechanics/antifragility/parts/stress-posture/docs/stress-handoffs.md",
            "mechanics/questbook/parts/execution-passport/docs/quest-execution-passport.md",
            "mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json",
            "generated/quest_catalog.min.json",
            "generated/quest_dispatch.min.json",
            "generated/codex_agents/config.subagents.generated.toml",
            "mechanics/checkpoint/parts/growth-checkpoint/docs/workspace-checkpoint-growth-role-posture.md",
            "mechanics/agon/parts/formation/docs/subject-prep.md",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, contour)

        self.assertIn("Codex subagent projection", changelog)
        self.assertIn("self-agency continuity posture", changelog)
        self.assertIn("civil/service", subject_prep)
        self.assertIn("Agonic Actor Rechartering has now landed", subject_prep)
        self.assertIn("Assistant Civil Rechartering has now landed", subject_prep)
        self.assertIn("Formation Trial has now landed", subject_prep)
        self.assertIn("future additive adjunct", subject_prep)

    def test_current_contour_names_agonic_actor_recharter_turn(self) -> None:
        contour = CONTOUR_PATH.read_text(encoding="utf-8")

        self.assertIn("## Agonic Actor Rechartering", contour)
        self.assertIn("validation route", contour)
        self.assertIn("mechanics/agon/AGENTS.md", contour)

        for relative_path in (
            "mechanics/agon/parts/formation/docs/actor-rechartering.md",
            "mechanics/agon/parts/formation/docs/agonic-actor-rechartering-landing.md",
            "mechanics/agon/parts/formation/docs/kind-model.md",
            "mechanics/agon/parts/formation/docs/subjectivity-model.md",
            "mechanics/experience/parts/office-operations/docs/agent-office-model.md",
            "mechanics/agon/parts/arena-rank-school/docs/arena-eligibility-model.md",
            "mechanics/agon/parts/formation/docs/resistance-revision-posture.md",
            "mechanics/agon/parts/formation/schemas/agent-kind.schema.json",
            "mechanics/agon/parts/formation/schemas/subjectivity.schema.json",
            "mechanics/agon/parts/formation/schemas/office-overlay.schema.json",
            "mechanics/agon/parts/arena-rank-school/schemas/arena-eligibility.schema.json",
            "mechanics/agon/parts/formation/schemas/resistance-revision.schema.json",
            "generated/agent_agonic_formation_index.min.json",
            "mechanics/agon/parts/formation/examples/agent-agonic-formation.example.json",
            "mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py",
            "mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py",
            "mechanics/agon/parts/formation/tests/test_agent_agonic_formation.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, contour)

    def test_current_contour_names_assistant_civil_recharter_turn(self) -> None:
        contour = CONTOUR_PATH.read_text(encoding="utf-8")

        self.assertIn("## Assistant Civil Rechartering", contour)
        self.assertIn("mechanics/experience/AGENTS.md", contour)

        for relative_path in (
            "mechanics/experience/parts/assistant-civil-service/docs/civil-rechartering.md",
            "mechanics/agon/parts/formation/docs/assistant-civil-rechartering-landing.md",
            "mechanics/experience/parts/assistant-civil-service/docs/assistant-kind-model.md",
            "mechanics/experience/parts/assistant-civil-service/docs/service-identity-model.md",
            "mechanics/experience/parts/assistant-civil-service/docs/service-contract-model.md",
            "mechanics/experience/parts/assistant-civil-service/docs/service-governance-model.md",
            "mechanics/experience/parts/assistant-civil-service/docs/service-certification-model.md",
            "mechanics/experience/parts/arena-exclusion/docs/arena-exclusion-model.md",
            "mechanics/experience/parts/arena-exclusion/docs/escalation-to-agon.md",
            "mechanics/experience/parts/assistant-civil-service/schemas/assistant-variant.schema.json",
            "mechanics/experience/parts/assistant-civil-service/schemas/service-identity.schema.json",
            "mechanics/experience/parts/assistant-civil-service/schemas/service-contract.schema.json",
            "mechanics/experience/parts/assistant-civil-service/schemas/service-governance.schema.json",
            "mechanics/experience/parts/assistant-civil-service/schemas/service-certification.schema.json",
            "mechanics/experience/parts/assistant-civil-service/schemas/civil-formation.schema.json",
            "mechanics/experience/parts/arena-exclusion/schemas/arena-exclusion.schema.json",
            "generated/assistant_civil_formation_index.min.json",
            "mechanics/experience/parts/assistant-civil-service/examples/civil-formation.example.json",
            "mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py",
            "mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py",
            "mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py",
            "mechanics/experience/parts/assistant-civil-service/tests/test_assistant_civil_formation.py",
            "mechanics/experience/tests/test_experience_assistant_civil_contracts.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, contour)

    def test_current_contour_names_formation_trial_turn(self) -> None:
        contour = CONTOUR_PATH.read_text(encoding="utf-8")

        self.assertIn("## Formation Trial", contour)
        self.assertIn("mechanics/agon/AGENTS.md", contour)

        for relative_path in (
            "mechanics/agon/parts/formation/docs/formation-trial.md",
            "mechanics/agon/parts/pre-protocol-boundary/docs/pre-protocol-agent-boundary.md",
            "mechanics/agon/parts/pre-protocol-boundary/docs/formation-trial-readiness.md",
            "mechanics/codex-projection/parts/agon-boundary/docs/projection-agon-boundary.md",
            "mechanics/agon/parts/formation/docs/formation-trial-landing.md",
            "mechanics/agon/parts/formation/schemas/formation-trial.schema.json",
            "generated/agent_formation_trial.min.json",
            "mechanics/agon/parts/formation/examples/formation-trial.example.json",
            "mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py",
            "mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py",
            "mechanics/agon/parts/formation/tests/test_agent_formation_trial.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, contour)

    def test_current_contour_names_active_titan_projection_routes(self) -> None:
        contour = CONTOUR_PATH.read_text(encoding="utf-8")
        manifest = json.loads(
            (REPO_ROOT / "generated" / "titan_codex_agents" / "projection_manifest.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("## Titan Role Bearing", contour)
        for relative_path in (
            "mechanics/titan/parts/runtime-roster/docs/runtime-roster.md",
            "mechanics/titan/parts/runtime-roster/docs/appserver-bridge-boundary.md",
            "mechanics/titan/parts/runtime-roster/docs/agent-report-boundary.md",
            "mechanics/titan/parts/codex-projection/README.md",
            "mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py",
            "mechanics/titan/parts/codex-projection/tests/test_titan_codex_projection.py",
            "generated/titan_codex_agents/projection_manifest.json",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, contour)

        self.assertIn("generated/titan_codex_agents/agents/*.toml", contour)
        for agent in manifest["agents"]:
            relative_path = "generated/titan_codex_agents/" + agent["config_path"]
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).is_file())


if __name__ == "__main__":
    unittest.main()
