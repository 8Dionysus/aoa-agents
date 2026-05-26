from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_agon_rank_epistemic_contracts.py"
sys.path.insert(0, str(ROOT / "scripts"))


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_agon_rank_epistemic_contracts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_agon_rank_epistemic_contracts_validate() -> None:
    validator = _load_validator()

    validator.validate_agon_rank_epistemic_contracts(ROOT)


def test_agon_rank_epistemic_contracts_are_part_local() -> None:
    former_paths = (
        Path("schemas") / ("agon-" + "agent-rank-jurisdiction.schema.json"),
        Path("schemas") / ("agon-" + "agent-school-campaign-posture.schema.json"),
        Path("schemas") / ("agon-" + "epistemic-actor-posture.schema.json"),
        Path("examples") / ("agon" + "_agent_rank_surface.example.json"),
        Path("examples") / ("agon" + "_epistemic_actor_posture.example.json"),
    )

    for relative_path in former_paths:
        assert not (ROOT / relative_path).exists()
