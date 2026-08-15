# Role-First Semantic Entry for External Actors

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0067
- Original date: 2026-08-15
- Surface classes: owner skill home, capability route, external actor lifecycle
- Agent facets: obligation, role contract, incarnation, responsibility return
- Mechanic parents: boundary-bridge, cross-mechanic
- Guard families: owner boundary, model fit, runtime binding, task-local DAG, wake ABI
- Posture: advertised organ with an internal semantic entry mode

## Context

The external actor contour already had owner compilers and a real aoa-summon
execution leaf, but a new Codex session still needed its master to assemble a
large preparation specification and to know the exact low-level command path.
That preserved the physical route while making the intended role-first entry
less usable than model-first or launcher-first habits.

## Options Considered

- Keep hand-building the obligation, mandate, fit, SDK, runtime, transfer, and
  summon packets for every Goal branch.
- Add a model-specific launcher or a monolithic runtime command that silently
  selects role, model, and authority.
- Add one explicit semantic mode to the existing aoa-agents-skills router
  that composes the current owner stages and keeps all low-level assembly
  internal to the owner compilers.

## Decision

Add role-first-entry inside the existing advertised aoa-agents-skills bundle.
Its caller-facing input is only role-first-intent-v1: Goal, independent duty,
authority envelope, and expected result. The mode normalizes that intent into
the existing goal-pressure-v1 path, performs the semantic role and
current-holder model-fit decisions, and then invokes the existing passive
compilers and stronger-owner runtime bindings. It may reach aoa-summon only
after the complete external packet and inspected runtime binding exist.

The mode does not choose a model by brand, mint a role, grant permissions,
launch a built-in child, own a domain procedure, or treat transport as A2A
responsibility. aoa-models remains fit authority, aoa-sdk remains RunPlan and
incarnation-v2 authority, abyss-stack remains process/session/state/event
authority, and the named domain owner remains procedure authority.

The route has an explicit preview/apply boundary. After owner compilation and
runtime inspection, the current holder receives the selected role, fit,
incarnation, permissions, effects, stop line, outputs, rollback, and return
owner as a task-local preview. The semantic request alone cannot launch the
external process; a separate current-holder apply confirmation is required.
Without it, the route returns `awaiting_apply` with no runtime mutation.

Because the semantic request intentionally omits a role ID, the source gate
admits one finite candidate read over the current role-house profiles and
role-local specialization files. The current holder compares those authored
candidates to the duty, records the semantic selection, and only then reads
the exact chosen sources. Generated readers remain navigation aids rather than
role authority, and the candidate read cannot widen into repository search.

## Consequences

- A new Codex session can start from a plain semantic request without knowing
  summon JSON, digests, owner roots, or a model-specific command.
- The route remains fail-closed at missing role, fit, runtime, authority,
  return, or review evidence.
- A prepared route is inspectable before execution, and runtime mutation cannot
  begin without explicit current-holder apply confirmation.
- The semantic entry is not itself proof that an actor launched or returned;
  separate process, session, continuation, effect, usage, review, and filtered
  return evidence remain required.
- The bundle version advances to 0.4.0; installed handles must be refreshed
  and checked through the user profile before claiming live parity.

## Source Surfaces

- skills/aoa-agents-skills/SKILL.md
- skills/aoa-agents-skills/references/role-first-entry.md
- skills/aoa-agents-skills/references/role-first-intent-v1.schema.json
- skills/aoa-agents-skills/references/contract.yaml
- capabilities/families/agent-lifecycle.yaml
- skills/port.manifest.json
- tests/test_aoa_agents_skill_tree.py

## Verification

Validate the semantic schema and source procedure, rebuild the owner
capability projection, run the focused contract/preparer tests and repository
validators, refresh the user-installed profile, and exercise a fresh
arbitrary-repository Codex session through the external runtime. Treat the
last exercise as live behavior evidence, not as a replacement for owner
source or CI evidence.
