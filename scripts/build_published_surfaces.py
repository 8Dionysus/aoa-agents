#!/usr/bin/env python3
from __future__ import annotations

import sys

from agent_profile_registry import BuildError, write_agent_registry
from cohort_registry import write_cohort_registry
from codex_subagent_projection import write_repo_projection_surfaces
from model_tier_registry import write_model_tier_registry
from orchestrator_class_registry import write_orchestrator_class_surfaces
from runtime_seam_registry import write_runtime_seam_registry


def main() -> int:
    try:
        agent_payload = write_agent_registry()
        tier_payload = write_model_tier_registry()
        cohort_payload = write_cohort_registry()
        orchestrator_catalog, _, _ = write_orchestrator_class_surfaces()
        seam_payload = write_runtime_seam_registry()
        codex_projection = write_repo_projection_surfaces()
    except BuildError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(
        "[ok] wrote published surfaces from source-authored layers: "
        f"{len(agent_payload['agents'])} agents, "
        f"{len(tier_payload['model_tiers'])} model tiers, "
        f"{len(cohort_payload['cohort_patterns'])} cohort patterns, "
        f"{len(orchestrator_catalog['orchestrator_classes'])} orchestrator classes, "
        f"{len(seam_payload['bindings'])} runtime seam bindings, "
        f"{len(codex_projection['generated_agents'])} Codex projected agents"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
