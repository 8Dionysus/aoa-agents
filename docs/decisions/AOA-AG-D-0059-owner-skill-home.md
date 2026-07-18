# 2026-07-16: Agent Owner Skill Home

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0059
- Original date: 2026-07-16
- Surface classes: owner skill home, user projection
- Agent facets: progression, delegation, handoff
- Mechanic parents: rpg, titan
- Guard families: evidence boundary, runtime binding, closeout
- Posture: accepted

## Context

`aoa-session-progression-lift` and `aoa-summon` already existed as exported
copies authored elsewhere. Collapsing progression to a graph adapter removed
its procedure; treating summon as a workflow label removed host execution and
return state. Keeping copies under every repository also duplicates globally
installed names in Codex discovery.

## Decision

Admit both existing functions into the canonical `aoa-agents/skills/` owner
home. Progression lift consumes reviewed evidence and stops at an attributed
multi-axis candidate. Summon decides or executes one anchored child route,
requires explicit intent and real host binding, and preserves passport, gates,
runtime handle, typed return, and parent closeout.

Expose them once through `os-user-default`; remove the repository
`.agents/skills` catalog. Technique records remain optional provenance only.

## Evidence And Limits

Manual trials compared no-skill, prior exported skill, the consolidated shared
catalog, and the owner candidate. The owner progression skill selected the
correct route amid memo/eval/session neighbors, preserved tool and user
attribution, rejected live unreviewed growth, and changed no owner state. The
owner summon skill enforced the `d3+` split and, when host delegation returned
no usable thread binding, reported `blocked_binding_unavailable` instead of a
fake launch.

In a later bounded execute trial, the same summon package resolved its owner
source serially, launched exactly one child through the available host
delegation interface, observed the child move from running to completed,
received exactly the two named outputs, validated both against the parent
request, and left the inspected owner contract byte-identical. The returned
analysis correctly kept authorization, owner binding, rollback readiness, and
post-change verification outside the skill's enforcement authority.

This admits the procedures and discovery boundary. It does not prove cross-model
equivalence, central mastery, universal host availability, or successful child
execution on every runtime.

## Consequences

The semantic graph and KAG may index these owner contracts but cannot replace
them. Progression application remains a separate owner review. Runtime failure
or missing host binding remains visible. Raw trials and task-local state remain
outside the repository.
