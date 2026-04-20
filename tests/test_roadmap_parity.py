from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RoadmapParityTestCase(unittest.TestCase):
    def test_roadmap_matches_current_v0_2_release_surfaces(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        subject_prep = (REPO_ROOT / "docs" / "AGENT_SUBJECT_PREP.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("v0.2.2", readme)
        self.assertIn("[0.2.2]", changelog)
        self.assertIn("v0.2.x", roadmap)

        for relative_path in (
            "docs/CODEX_SUBAGENT_PROJECTION.md",
            "docs/CODEX_SUBAGENT_REFRESH_LAW.md",
            "config/codex_subagent_wiring.v2.json",
            "generated/runtime_seam_bindings.json",
            "docs/AGENT_STRESS_POSTURE.md",
            "docs/AGENT_STRESS_HANDOFFS.md",
            "docs/QUEST_EXECUTION_PASSPORT.md",
            "generated/quest_catalog.min.json",
            "generated/quest_dispatch.min.json",
            "generated/alpha_reference_routes.min.json",
            "generated/codex_agents/config.subagents.generated.toml",
            "docs/WORKSPACE_CHECKPOINT_GROWTH_ROLE_POSTURE.md",
            "docs/AGENT_SUBJECT_PREP.md",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)

        self.assertIn("Codex subagent projection", changelog)
        self.assertIn("self-agency continuity posture", changelog)
        self.assertIn("agonic/assistant kind split", roadmap)
        self.assertIn("civil/service", subject_prep)
        self.assertIn("Wave I Agonic Actor Rechartering has now landed", subject_prep)
        self.assertIn("Wave II Assistant Civil Rechartering has now landed", subject_prep)
        self.assertIn("future additive adjunct", subject_prep)
        self.assertIn("roadmap drift", roadmap)

    def test_roadmap_names_unreleased_wave1_agonic_actor_recharter(self) -> None:
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

        self.assertIn("## Unreleased next turn: Agonic Actor Rechartering", roadmap)
        self.assertIn("explicit Wave I validation lane", roadmap)

        for relative_path in (
            "docs/AGONIC_ACTOR_RECHARTERING.md",
            "docs/AGON_WAVE1_LANDING.md",
            "docs/AGENT_KIND_MODEL.md",
            "docs/AGENT_SUBJECTIVITY_MODEL.md",
            "docs/AGENT_OFFICE_MODEL.md",
            "docs/AGENT_ARENA_ELIGIBILITY_MODEL.md",
            "docs/AGENT_RESISTANCE_REVISION_POSTURE.md",
            "schemas/agent_kind_v1.json",
            "schemas/agent_subjectivity_v1.json",
            "schemas/agent_office_overlay_v1.json",
            "schemas/agent_arena_eligibility_v1.json",
            "schemas/agent_resistance_revision_v1.json",
            "generated/agent_agonic_formation_index.min.json",
            "examples/agent_agonic_formation.example.json",
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
            "docs/ASSISTANT_CIVIL_RECHARTERING.md",
            "docs/AGON_WAVE2_LANDING.md",
            "docs/ASSISTANT_KIND_MODEL.md",
            "docs/ASSISTANT_SERVICE_IDENTITY_MODEL.md",
            "docs/ASSISTANT_SERVICE_CONTRACT_MODEL.md",
            "docs/ASSISTANT_SERVICE_GOVERNANCE_MODEL.md",
            "docs/ASSISTANT_SERVICE_CERTIFICATION_MODEL.md",
            "docs/ASSISTANT_ARENA_EXCLUSION_MODEL.md",
            "docs/ASSISTANT_ESCALATION_TO_AGON.md",
            "schemas/assistant_variant_v1.json",
            "schemas/assistant_service_identity_v1.json",
            "schemas/assistant_service_contract_v1.json",
            "schemas/assistant_service_governance_v1.json",
            "schemas/assistant_service_certification_v1.json",
            "schemas/assistant_arena_exclusion_v1.json",
            "generated/assistant_civil_formation_index.min.json",
            "examples/assistant_civil_formation.example.json",
            "scripts/build_assistant_civil_formation_index.py",
            "scripts/validate_assistant_civil_formation.py",
            "tests/test_assistant_civil_formation.py",
        ):
            self.assertTrue((REPO_ROOT / relative_path).is_file())
            self.assertIn(relative_path, roadmap)


if __name__ == "__main__":
    unittest.main()
