# Validation map

This is the on-demand human map for repository validation. The executable
scripts and their source-owned contracts remain authoritative; command text
below is a route index, not a replacement for those owners.

## Repository and documentation

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
python -m pytest -q tests
python scripts/build_published_surfaces.py
python scripts/validate_agent_source_home.py
python scripts/release_check.py
python scripts/generate_decision_indexes.py --check
python scripts/validate_active_organ_agent_local_namespace.py
```

The generated-reader projection validation is owned by [Generated readers and projection outputs](#generated-readers-and-projection-outputs); the stats-port validation is owned by [Boundary, memo, quest, and stats ports](#boundary-memo-quest-and-stats-ports).

## Source, capability, and operating-model surfaces

```bash
python -m pip install -r requirements-dev.txt
PYTHONPATH=scripts python scripts/validate_capability_home_port.py --owner-root /path/to/aoa-agents
PYTHONPATH=scripts python scripts/build_capability_home_projection.py --owner-root /path/to/aoa-agents
PYTHONPATH=scripts python scripts/build_capability_home_projection.py --owner-root /path/to/aoa-agents --check
PYTHONPATH=scripts python scripts/validate_capability_home_port.py --owner-root /path/to/aoa-agents --check-generated
```

## Agon and assistant formation

```bash
python mechanics/agon/parts/formation/scripts/build_agent_agonic_formation_index.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_agonic_formation.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_agonic_formation.py
python mechanics/experience/parts/assistant-civil-service/scripts/build_assistant_civil_formation_index.py --check
python mechanics/experience/parts/assistant-civil-service/scripts/validate_assistant_civil_formation.py
python -m pytest -q mechanics/experience/parts/assistant-civil-service/tests/test_assistant_civil_formation.py
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_formation_trial.py
python mechanics/experience/scripts/validate_experience_assistant_civil_contracts.py
python mechanics/agon/parts/formation/scripts/validate_agon_formation_contracts.py
python mechanics/agon/scripts/validate_agon_rank_epistemic_contracts.py
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_rank_jurisdiction.py
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_school_campaign_posture_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_school_campaign_posture_registry.py
python mechanics/agon/parts/epistemic-actor/scripts/build_agon_epistemic_actor_posture_registry.py --check
python mechanics/agon/parts/epistemic-actor/scripts/validate_agon_epistemic_actor_posture.py
```

## Mechanic and runtime surfaces

```bash
python mechanics/antifragility/parts/stress-posture/scripts/validate_stress_posture.py
python -m unittest discover -s mechanics/antifragility/parts/stress-posture/tests -p "test_*.py"
python mechanics/experience/scripts/validate_adoption_boundary_contracts.py
python mechanics/checkpoint/scripts/validate_checkpoint_contracts.py
python mechanics/checkpoint/scripts/validate_reference_route_contracts.py
python -m unittest discover -s mechanics/codex-projection/parts/subagent-projection/tests -p "test_*.py"
python mechanics/codex-projection/parts/specialization-eligibility/scripts/build_specialization_eligibility_readiness.py --check
python mechanics/codex-projection/parts/specialization-eligibility/scripts/validate_specialization_eligibility.py
python -m unittest discover -s mechanics/codex-projection/parts/specialization-eligibility/tests -p "test_*.py"
python mechanics/codex-projection/parts/assistant-projection/scripts/validate_assistant_projection_resolver.py
python mechanics/codex-projection/parts/refresh-law/scripts/validate_codex_refresh_law_contracts.py
python -m unittest discover -s mechanics/experience/tests -p 'test_*.py'
python -m unittest discover -s mechanics/experience/parts/assistant-civil-service/tests -p 'test_*.py'
python mechanics/experience/scripts/validate_agent_service_contracts.py
python mechanics/recurrence/scripts/build_recursor_role_readiness.py --check
python mechanics/recurrence/scripts/build_recursor_projection_candidates.py --check
python mechanics/recurrence/scripts/validate_recursor_contracts.py
python mechanics/recurrence/scripts/validate_recursor_role_readiness.py
python mechanics/recurrence/scripts/validate_recursor_boundary.py
python mechanics/recurrence/parts/component-manifests/scripts/validate_recurrence_component_manifests.py
python mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py
python mechanics/runtime-seam/parts/artifact-contracts/scripts/validate_artifact_contracts.py
python mechanics/titan/scripts/validate_titan_lineage.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --ledger mechanics/titan/parts/lineage-ledger/config/ledger.v0.json
python mechanics/titan/scripts/validate_titan_schemas.py
python mechanics/titan/scripts/validate_titan_examples.py
python -m unittest discover -s mechanics/titan/tests -p "test_*.py"
python mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --out-dir generated/titan_codex_agents/agents --manifest generated/titan_codex_agents/projection_manifest.json --prune --check
python -m unittest discover -s mechanics/titan/parts/codex-projection/tests -p "test_*.py"
```

The Codex subagent projection build is owned by [Generated readers and projection outputs](#generated-readers-and-projection-outputs); assistant civil formation is owned by [Agon and assistant formation](#agon-and-assistant-formation).

## Boundary, memo, quest, and stats ports

```bash
python ../aoa-evals/scripts/validate_local_eval_port.py --target-root .
python mechanics/boundary-bridge/parts/participant-relations/scripts/build_goal_participant_graph.py --check
python mechanics/boundary-bridge/parts/participant-relations/scripts/validate_goal_participant_graph.py
python mechanics/boundary-bridge/parts/participant-relations/scripts/admit_goal_participant_publication.py --help
python -m unittest discover -s mechanics/boundary-bridge/parts/participant-relations/tests -p 'test_*.py'
python mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py --check
python mechanics/questbook/parts/alpha-reference-routes/scripts/generate_alpha_reference_routes.py --check
python mechanics/questbook/scripts/validate_alpha_reference_routes.py
python scripts/validate_local_stats_port.py
python -c 'import json, pathlib; p=json.loads(pathlib.Path("mechanics/codex-projection/parts/specialization-eligibility/generated/specialization-eligibility-readiness.min.json").read_text()); rows=p["records"]; eligible=sum(row["decision_status"] == "eligible" for row in rows); print({"population": len(rows), "eligible": eligible, "ratio": eligible / len(rows)})'
```

The stats-port validation is owned by [Boundary, memo, quest, and stats ports](#boundary-memo-quest-and-stats-ports).

Memo candidate and export routes use the local MCP helper. The `AOA_ABYSS_STACK_ROOT`
and `AOA_MEMO_ROOT` variables must be explicit; do not infer sibling checkouts.

```bash
AOA_ABYSS_STACK_ROOT="${AOA_ABYSS_STACK_ROOT:-$HOME/src/abyss-stack}"
PYTHONPATH="$AOA_ABYSS_STACK_ROOT/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli create-candidate \
  --repo aoa-agents \
  --evidence-ref README.md \
  --claim "aoa-agents memory should move through reviewed local candidates before aoa-memo landing."
PYTHONPATH="$AOA_ABYSS_STACK_ROOT/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli validate-candidate path/to/candidate.json
PYTHONPATH="$AOA_ABYSS_STACK_ROOT/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli pending-exports --repo aoa-agents
PYTHONPATH="$AOA_ABYSS_STACK_ROOT/mcp/services/aoa-memo-mcp/src" python -m aoa_memo_mcp.cli landing-plan --repo aoa-agents --export-ref exports/path.reviewed-intake.json --run-dry-run
: "${AOA_MEMO_ROOT:?Set AOA_MEMO_ROOT to your local aoa-memo checkout}"
python "$AOA_MEMO_ROOT/scripts/memory/validate_local_memo_port.py" --path memo
python "$AOA_MEMO_ROOT/scripts/memory/build_local_memo_port_index.py" --path memo --check
```

## Generated readers and projection outputs

```bash
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python mechanics/titan/parts/codex-projection/scripts/render_titan_codex_agents.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --out-dir generated/titan_codex_agents/agents --manifest generated/titan_codex_agents/projection_manifest.json --prune
```

Run the repository release gate for the complete executable contract. Do not
copy these commands into an `AGENTS.md` card; follow the nearest owner card
and return here when a human validation run is needed.
