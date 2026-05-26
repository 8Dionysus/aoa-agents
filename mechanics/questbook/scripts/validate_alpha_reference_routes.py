#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_agents


def main() -> int:
    try:
        validate_agents.validate_alpha_reference_route_schema_surface()
        agent_names = validate_agents.validate_registry()
        tiers_by_id = validate_agents.validate_model_tier_registry()
        cohort_patterns_by_id = validate_agents.validate_cohort_composition_registry(agent_names, tiers_by_id)
        validate_agents.validate_alpha_reference_routes(cohort_patterns_by_id)
    except validate_agents.ValidationError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[ok] validated questbook Alpha reference routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
