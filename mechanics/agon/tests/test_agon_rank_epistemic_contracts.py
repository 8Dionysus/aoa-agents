from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "mechanics" / "agon" / "scripts" / "validate_agon_rank_epistemic_contracts.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_agon_rank_epistemic_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AgonRankEpistemicContractsTestCase(unittest.TestCase):
    def test_agon_rank_epistemic_contracts_validate(self) -> None:
        validator = _load_validator()
        validator.validate_agon_rank_epistemic_contracts(ROOT)

    def test_agon_rank_epistemic_contracts_are_part_local(self) -> None:
        former_paths = (
            Path("schemas") / ("agon-" + "agent-rank-jurisdiction.schema.json"),
            Path("schemas") / ("agon-" + "agent-school-campaign-posture.schema.json"),
            Path("schemas") / ("agon-" + "epistemic-actor-posture.schema.json"),
            Path("examples") / ("agon" + "_agent_rank_surface.example.json"),
            Path("examples") / ("agon" + "_epistemic_actor_posture.example.json"),
            Path("generated") / ("agon" + "_agent_rank_jurisdiction_registry.min.json"),
            Path("generated") / ("agon" + "_epistemic_actor_posture_registry.min.json"),
            Path("scripts") / "build_agon_agent_rank_jurisdiction_registry.py",
            Path("scripts") / "validate_agon_agent_rank_jurisdiction.py",
            Path("scripts") / "build_agon_agent_school_campaign_posture_registry.py",
            Path("scripts") / "validate_agon_agent_school_campaign_posture_registry.py",
            Path("scripts") / "build_agon_epistemic_actor_posture_registry.py",
            Path("scripts") / "validate_agon_epistemic_actor_posture.py",
            Path("scripts") / "validate_agon_rank_epistemic_contracts.py",
            Path("tests") / "test_agon_agent_rank_jurisdiction.py",
            Path("tests") / "test_agon_agent_school_campaign_posture_registry.py",
            Path("tests") / "test_agon_epistemic_actor_posture.py",
            Path("tests") / "test_agon_rank_epistemic_contracts.py",
        )

        for relative_path in former_paths:
            self.assertFalse((ROOT / relative_path).exists(), str(relative_path))


if __name__ == "__main__":
    unittest.main()
