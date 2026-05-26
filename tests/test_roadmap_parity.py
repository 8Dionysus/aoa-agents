from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_matches_current_v0_2_release_surfaces(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        subject_prep = (REPO_ROOT / "mechanics" / "agon" / "parts" / "formation" / "docs" / "subject-prep.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("v0.2.3", readme)
        self.assertIn("[0.2.3]", changelog)
        self.assertIn("v0.2.x", roadmap)

        for relative_path in (
            "mechanics/codex-projection/parts/subagent-projection/docs/subagent-projection.md",
            "mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md",
            "mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json",
            "generated/runtime_seam_bindings.json",
            "mechanics/antifragility/parts/stress-posture/docs/stress-posture.md",
            "mechanics/antifragility/parts/stress-posture/docs/stress-handoffs.md",
            "mechanics/questbook/parts/execution-passport/docs/quest-execution-passport.md",
            "generated/quest_catalog.min.json",
            "generated/quest_dispatch.min.json",
            "generated/alpha_reference_routes.min.json",
            "generated/codex_agents/config.subagents.generated.toml",
            "mechanics/checkpoint/parts/growth-checkpoint/docs/workspace-checkpoint-growth-role-posture.md",
            "mechanics/agon/parts/formation/docs/subject-prep.md",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)

        self.assertIn("Codex subagent projection", changelog)
        self.assertIn("self-agency continuity posture", changelog)
        self.assertIn("agonic/assistant kind split", roadmap)
        self.assertIn("civil/service", subject_prep)
        self.assertIn("Wave I Agonic Actor Rechartering has now landed", subject_prep)
        self.assertIn("Wave II Assistant Civil Rechartering has now landed", subject_prep)
        self.assertIn("Wave II.5 Formation Trial has now landed", subject_prep)
        self.assertIn("future additive adjunct", subject_prep)
        self.assertIn("roadmap drift", roadmap)

    def test_roadmap_names_unreleased_wave1_agonic_actor_recharter(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn("## Unreleased next turn: Agonic Actor Rechartering", roadmap)
        self.assertIn("explicit Wave I validation lane", roadmap)

        for relative_path in (
            "mechanics/agon/parts/formation/docs/actor-rechartering.md",
            "mechanics/agon/parts/formation/docs/wave1-landing.md",
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
            "scripts/build_agent_agonic_formation_index.py",
            "scripts/validate_agent_agonic_formation.py",
            "tests/test_agent_agonic_formation.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)

    def test_roadmap_names_unreleased_wave2_assistant_civil_recharter(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn("## Unreleased follow-on turn: Assistant Civil Rechartering", roadmap)
        self.assertIn("explicit Wave II validation lane", roadmap)

        for relative_path in (
            "mechanics/experience/parts/assistant-civil-service/docs/civil-rechartering.md",
            "mechanics/agon/parts/formation/docs/wave2-landing.md",
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
            "scripts/build_assistant_civil_formation_index.py",
            "scripts/validate_assistant_civil_formation.py",
            "scripts/validate_experience_assistant_civil_contracts.py",
            "tests/test_assistant_civil_formation.py",
            "tests/test_experience_assistant_civil_contracts.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)

    def test_roadmap_names_unreleased_wave2_5_formation_trial(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn("## Unreleased follow-on turn: Formation Trial", roadmap)
        self.assertIn("explicit Wave II.5 validation lane", roadmap)

        for relative_path in (
            "mechanics/agon/parts/formation/docs/formation-trial.md",
            "mechanics/agon/parts/pre-protocol-boundary/docs/pre-protocol-agent-boundary.md",
            "mechanics/agon/parts/pre-protocol-boundary/docs/formation-trial-readiness.md",
            "mechanics/codex-projection/parts/agon-boundary/docs/projection-agon-boundary.md",
            "mechanics/agon/parts/formation/docs/wave2-5-landing.md",
            "mechanics/agon/parts/formation/schemas/formation-trial.schema.json",
            "generated/agent_formation_trial.min.json",
            "mechanics/agon/parts/formation/examples/formation-trial.example.json",
            "scripts/build_agent_formation_trial.py",
            "scripts/validate_agent_formation_trial.py",
            "tests/test_agent_formation_trial.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)


if __name__ == "__main__":
    unittest.main()
