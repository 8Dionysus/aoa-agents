# AGENTS.md

Root route card for `aoa-agents`.

## Role

This repository owns role-bearing actor meaning: profile structure, role
contracts, handoff posture, memory posture, evaluation posture, operating-model
surfaces, bounded cohort hints, role specializations, and generated
agent-layer consumer seams. It also owns the meaning of agent-local
statistical questions and evidence references exposed through `stats/`.

It does not implement runtime autonomy and does not own skill workflow truth,
technique truth, proof doctrine, memory objects, routing policy, playbook
scenario canon, KAG substrate semantics, shared statistical grammar,
cross-owner statistical composition, or runtime workers.

This card supplies the repository-wide route. A nearer `AGENTS.md` narrows it
with a local delta; neither replaces authored source, public explanation, or a
named stronger-owner contract.

## Operating Map

| Field | Route |
| --- | --- |
| input | role, persona, handoff, posture, projection, or agent-layer operation pressure |
| output | source role object, mechanic-local contract, generated companion, decision record, or stronger-owner handoff |
| owner | source objects under `agents/`, operation packages under `mechanics/`, and route docs under `docs/` |
| next route | nearest nested `AGENTS.md`, then the source surface, mechanic package, builder, validator, or sibling owner |
| validation | [VALIDATION.md](VALIDATION.md), plus the nearest local card |

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
| `local-stats-port` | agent-local statistical question, contract, or reference packet changes | [stats/AGENTS](stats/AGENTS.md) |

The root card owns identity, owner boundaries, and route choice. Nested cards
own only local contracts, risk, stop-lines, and route selection. Authored
source owns meaning; generated, exported, compact, runtime, and adapter
surfaces are derived. Keep formation, autonomy, recurrence, quest,
progression, and growth claims bounded, evidence-linked, reversible, and
weaker than their owner contracts.

## Memory Route

Use `aoa-memo` for reviewed continuity or prior rationale. Session evidence,
local candidates, and durable reviewed memory remain distinct and do not
become role truth merely because they are recalled here.

## Decision Review

After a structural, ownership, route-law, validator-authority, public-contract,
projection, or topology change, use `docs/decisions/AGENTS.md` to decide
whether future agents need a durable rationale.

## Route Away When

- an agent profile starts becoming a skill, playbook, memory schema, proof doctrine, route policy, or runtime implementation;
- progression becomes a universal score or live routing policy;
- formation, self-agent, checkpoint, Titan, quest, or recurrence language skips approval, rollback, evidence, or handoff contracts;
- generated or projected files are treated as stronger than source role objects or mechanic-local contracts.

## Landing Route

Use [docs/RELEASING.md](docs/RELEASING.md) for branch, PR, CI, merge, tag, and
publication procedure. Root `AGENTS.md` retains the stop-line: do not claim or
perform a landing without observing required GitHub checks and current merge
authority. `.github/AGENTS.md` owns only the GitHub-native files that support
that route.

## Validation

Use the nearest owner route in [VALIDATION.md](VALIDATION.md). Overview,
contour, roadmap, decision, and AGENTS surfaces link to procedure owners rather
than duplicating commands.

For source or generated-surface changes, follow the source owner and its
builder before running the repository gate. Use optional federation smoke
checks only when sibling reachability matters.

## Report

State which role, source family, mechanic, projection, contour, or published
surface changed; whether role boundaries or authority changed; what validation
ran; what was skipped; decision review result; and where the next owner route
is.
