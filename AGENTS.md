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
2. `DESIGN.md`
3. `DESIGN.AGENTS.md` for design/topology work
4. [ROADMAP.md](ROADMAP.md)
5. `CHARTER.md`
6. `docs/BOUNDARIES.md`
7. `agents/README.md` when source-authored agent objects are in scope
8. `mechanics/README.md` when repeatable operation topology is in scope
9. `mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md` when Codex projection freshness or workspace subagent refresh is in scope
10. the target profile, model-tier, orchestrator, schema, or generated surface
11. neighboring repo docs when skills, memo, evals, playbooks, or routing are touched
12. `docs/AGENTS_ROOT_REFERENCE.md` for preserved full root branches


## AGENTS stack law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Memory route

For recall, continuity, compaction recovery, comparison with past work, or
preserved lessons, start with `aoa-memo` and the workspace memory map. Session
grounding routes through `.aoa`; local candidate writing routes through this
repository's `memo/` port when that port exists; durable reviewed memory lands
through `aoa-memo`.

## Route away when

- an agent profile starts becoming a skill, playbook, memory schema, proof doctrine, or runtime implementation
- progression becomes a universal score or live routing policy
- self-agent language skips approval, rollback, evidence, or handoff contracts

## GitHub landing workflow

Root `AGENTS.md` owns the repository-wide branch, PR, CI, and merge route.
`.github/AGENTS.md` owns the GitHub-native files that support it.

When the user asks to commit, push, and merge in this repository, use this route:

1. Start from a branch based on the current `origin/main`. If the worktree is already dirty, inventory it first and carry forward only the intended diff.
2. Commit the intended change with a message that names the changed surface.
3. Push the branch and open a pull request that states changed surfaces, validation run, skipped checks, and remaining risk.
4. Wait for GitHub `Repo Validation` and any required GitHub checks. If a check fails, fix the branch and wait for the new result.
5. Merge through GitHub after green validation. Use squash unless repository settings report a different required method; report the method that landed.
6. Return to `main`, fast-forward from `origin/main`, and confirm the worktree is clean before closeout.

If GitHub status or merge permissions cannot be observed, stop the landing route and report the exact blocker instead of guessing.

## Verify

Minimum source or generated-surface validation:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
python scripts/validate_codex_subagents.py --profiles-root agents/profiles --wiring config/codex_subagent_wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
```

Use optional federation smoke checks when sibling reachability matters.

## Report

State which profile, contract, schema, progression, checkpoint, or published surface changed, whether role boundaries or authority changed, and what validation ran.

## Full reference

`docs/AGENTS_ROOT_REFERENCE.md` preserves the former detailed root guidance, including branch docs for progression, recurrence, self-agent checkpoints, orchestrator classes, and Codex projection.
