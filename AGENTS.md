# AGENTS.md

Root route card for `aoa-agents`.

## Purpose

`aoa-agents` is the role and persona layer of AoA.
It stores explicit agent profiles, role contracts, handoff posture, memory and evaluation posture, model-tier surfaces, bounded cohort hints, progression overlays, recurrence discipline, and self-agent checkpoint contract posture.
It does not implement runtime autonomy.

## Owner lane

This repository owns:

- profile structure and role-contract wording
- handoff, memory, evaluation, model-tier, orchestrator-class, and cohort-pattern posture at the agent layer
- progression, recurrence, mastery-axis, unlock, and self-agent checkpoint contract surfaces when defined here
- generated registries and published agent-layer consumer seams

It does not own:

- skills, techniques, proof verdicts, routing policy, memory-object schemas, playbook scenarios, KAG substrate semantics, stats summaries, or live runtime checkpoint execution

## Start here

1. `README.md`
2. `ROADMAP.md`
3. `CHARTER.md`
4. `docs/BOUNDARIES.md`
5. `docs/CODEX_SUBAGENT_REFRESH_LAW.md` when Codex projection freshness or workspace subagent refresh is in scope
6. the target profile, model-tier, orchestrator, schema, or generated surface
7. neighboring repo docs when skills, memo, evals, playbooks, or routing are touched
8. `docs/AGENTS_ROOT_REFERENCE.md` for preserved full root branches


## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Route away when

- an agent profile starts becoming a skill, playbook, memory schema, proof doctrine, or runtime implementation
- progression becomes a universal score or live routing policy
- self-agent language skips approval, rollback, evidence, or handoff contracts

## Verify

Minimum source or generated-surface validation:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agents.py
python scripts/validate_codex_subagents.py --profiles-root profiles --wiring config/codex_subagent_wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
```

Use optional federation smoke checks when sibling reachability matters.

## Report

State which profile, contract, schema, progression, checkpoint, or published surface changed, whether role boundaries or authority changed, and what validation ran.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including branch docs for progression, recurrence, self-agent checkpoints, orchestrator classes, and Codex projection.
