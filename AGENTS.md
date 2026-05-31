# AGENTS.md

Root route card for `aoa-agents`.

## Applies To

This card applies to the whole repository unless a nearer nested `AGENTS.md`
narrows the lane.

## Role

This card keeps local work inside the `aoa-agents` role and persona layer,
names the nearest owner boundary, and routes wider claims to the owning surface.

It is the agent-facing route law for this repository. It does not replace
`README.md`, `CHARTER.md`, `DESIGN.md`, `DESIGN.AGENTS.md`,
`docs/BOUNDARIES.md`, source objects, mechanic packages, or local owner truth.

## Purpose

`aoa-agents` owns role-bearing actor meaning: profile structure, role
contracts, handoff posture, memory posture, evaluation posture, operating-model
surfaces, bounded cohort hints, role specializations, and generated
agent-layer consumer seams.

It does not implement runtime autonomy and does not own skill workflow truth,
technique truth, proof doctrine, memory objects, routing policy, playbook
scenario canon, KAG substrate semantics, stats summaries, or runtime workers.

## Operating Map

| Field | Route |
| --- | --- |
| input | role, persona, handoff, posture, projection, or agent-layer operation pressure |
| output | source role object, mechanic-local contract, generated companion, decision record, or stronger-owner handoff |
| owner | source objects under `agents/`, operation packages under `mechanics/`, and route docs under `docs/` |
| next route | nearest nested `AGENTS.md`, then the source surface, mechanic package, builder, validator, or sibling owner |
| validation | [Verify](#verify), plus the nearest local card |

## Read Before Editing

For first reading or outside orientation:

1. [README](README.md)
2. [CHARTER](CHARTER.md)
3. [DESIGN](DESIGN.md)
4. [agents](agents/README.md)
5. [mechanics](mechanics/README.md)
6. [BOUNDARIES](docs/BOUNDARIES.md)
7. [ROADMAP.md](ROADMAP.md)

For agent editing:

1. this `AGENTS.md`
2. nearest nested `AGENTS.md` for every touched path
3. the route-mode surface from the table below
4. nearest source file, package card, schema, builder, validator, test, or
   generated-source owner
5. the narrowest relevant validator before broader gates

For preserved legacy root branches, use
`docs/AGENTS_ROOT_REFERENCE.md` only as a reference. If a preserved rule still
governs current work, move it to the nearest owner surface rather than
re-bloating this card.

## Route Modes

| Route mode | Use when | First surface |
| --- | --- | --- |
| `first-reading` | you need the shortest honest overview | [README](README.md) |
| `authority-boundary` | repository authority, owner split, or role-layer claim changes | [CHARTER](CHARTER.md) and [BOUNDARIES](docs/BOUNDARIES.md) |
| `system-design` | repository shape, source/generated posture, or layer relationship changes | [DESIGN](DESIGN.md) |
| `agent-surface-design` | route-card shape, agent-facing guidance, or card mesh posture changes | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| `source-object` | role profiles, forms, specializations, tiers, capabilities, orchestrators, cohorts, or runtime-seam bindings change | [agents](agents/README.md) |
| `mechanic-change` | repeatable operation topology, package route, part-local contract, provenance, or validation changes | [mechanics](mechanics/README.md) |
| `codex-projection` | Codex custom-agent projection, specialization eligibility, workspace install, or freshness changes | [codex-projection](mechanics/codex-projection/README.md) and `mechanics/codex-projection/parts/refresh-law/docs/subagent-refresh-law.md` |
| `direction-change` | roadmap, release contour, future trigger, or repo-level direction changes | [ROADMAP.md](ROADMAP.md) |
| `current-contour` | shipped surface families or root discoverability change | [CURRENT_CONTOUR](docs/CURRENT_CONTOUR.md) |
| `generated-surface` | generated registries, readers, or projections change | source surface -> builder -> generated output -> validator |
| `local-memory-port` | repo-local memo candidate, receipt, export, or local note changes | [memo/AGENTS](memo/AGENTS.md) |

## AGENTS Stack Law

- Start with this root card, then follow the nearest nested `AGENTS.md` for every touched path.
- Root guidance owns repository identity, owner boundaries, route choice, and the shortest honest verification path.
- Nested guidance owns local contracts, local risk, exact files, and local checks.
- Authored source surfaces own meaning. Generated, exported, compact, derived, runtime, and adapter surfaces summarize, transport, or support meaning.
- Self-agency, recurrence, quest, progression, checkpoint, formation, or growth language must stay bounded, reviewable, evidence-linked, and reversible.
- Report what changed, what was verified, what was not verified, and where the next agent should resume.

## Memory Route

For recall, continuity, compaction recovery, comparison with past work, or
preserved lessons, start with `aoa-memo` and the workspace memory map. Session
grounding routes through `.aoa`; local candidate writing routes through this
repository's `memo/` port when that port exists; durable reviewed memory lands
through `aoa-memo`.

## Decision Review

After structural, ownership, workflow, route-law, validator-authority,
public-contract, projection, or topology changes, check whether future agents
need a decision record to understand why the path was chosen. Use
`docs/decisions/AGENTS.md` and `docs/decisions/README.md` for the local rule.

If no record is needed, say so in closeout.

## Route Away When

- an agent profile starts becoming a skill, playbook, memory schema, proof doctrine, route policy, or runtime implementation;
- progression becomes a universal score or live routing policy;
- formation, self-agent, checkpoint, Titan, quest, or recurrence language skips approval, rollback, evidence, or handoff contracts;
- generated or projected files are treated as stronger than source role objects or mechanic-local contracts.

## GitHub Landing Workflow

Root `AGENTS.md` owns the repository-wide branch, PR, CI, and merge route.
`.github/AGENTS.md` owns the GitHub-native files that support it.

When the user asks to commit, push, and merge in this repository, use this route:

1. Start from a branch based on the current `origin/main`. If the worktree is already dirty, inventory it first and carry forward only the intended diff.
2. Commit the intended change with a message that names the changed surface.
3. Push the branch and open a pull request that states changed surfaces, validation run, skipped checks, and remaining risk.
4. Wait for GitHub `Repo Validation` and any required GitHub checks. If a check fails, fix the branch and wait for the new result.
5. Merge through GitHub after green validation. Use squash unless repository settings report a different required method; report the method that landed.
6. Return to `main`, fast-forward from `origin/main`, and confirm the worktree is clean before closeout.

If GitHub status or merge permissions cannot be observed, stop the landing
route and report the exact blocker instead of guessing.

## Verify

For root docs, route-card, and current-contour changes, run:

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
python -m pytest -q tests
```

For source or generated-surface changes, add:

```bash
python scripts/build_published_surfaces.py
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
```

Use optional federation smoke checks only when sibling reachability matters.

## Report

State which role, source family, mechanic, projection, contour, or published
surface changed; whether role boundaries or authority changed; what validation
ran; what was skipped; decision review result; and where the next owner route
is.
