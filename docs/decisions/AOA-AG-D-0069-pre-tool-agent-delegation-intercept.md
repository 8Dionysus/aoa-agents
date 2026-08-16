# Pre-Tool Agent Delegation Intercept

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0069
- Original date: 2026-08-15
- Surface classes: owner skill home, capability route, external actor lifecycle
- Agent facets: obligation, responsibility transfer, incarnation
- Mechanic parents: boundary-bridge, summon-boundary
- Guard families: trigger precedence, owner boundary, runtime binding
- Posture: role-first pre-tool routing

## Context

Fresh and compacted Codex sessions repeatedly selected built-in agent tools
before the external actor route could acquire responsibility. The advertised
root skill described an already visible independent obligation, while
`aoa-summon` advertised itself for any explicit delegation. The executable
tool was therefore easier to select than the semantic owner route, and a prior
correction could disappear as session context drifted.

The role-first entry also required a second apply message even when the
current holder's complete imperative already authorized execution. That added
friction at exactly the point where an immediately available built-in tool
competed with the intended route.

## Options Considered

- Rely on operator correction whenever a session chooses a built-in tool.
- Disable Codex-local child tools globally.
- Make `aoa-agents-skills` the pre-tool semantic intercept, keep local child
  lanes available after classification, and narrow `aoa-summon` to an
  execution leaf.

## Decision

`aoa-agents-skills` runs before any built-in Codex agent, sub-agent,
collaboration, or delegation tool whenever a request or plan proposes another
agent, worker, reviewer, researcher, parallel lane, background role, or
delegated duty. It classifies whether responsibility moves before any
transport is selected. Independent duties route to a separately addressable
external CLI actor. Ordinary local splits return `not_independent` before a
Codex-local compatibility lane may be considered.

The intercept repeats after compaction, resume, re-entry, or material plan
change when a new agent-tool decision appears. Prior correction in the same
session does not replace a fresh responsibility classification.

`aoa-summon` is not the generic delegation trigger. It executes only a
complete leaf supplied by `aoa-agents-skills`, or an explicitly requested
disposable Codex-local child whose complete anchored packet follows a
`not_independent` disposition.

`role-first-intent-v1` admits optional `prepare` or `execute` intent. A
planning or inspection request prepares and returns `awaiting_apply`. A
complete direct current-holder imperative to form, assign, launch, or delegate
the actor supplies explicit apply authority in that same request after the
compiled preview is checked against its authority. This narrowly supersedes
the always-separate apply clause in AOA-AG-D-0067; it does not weaken preview,
owner, effect, stop-line, runtime, return, or proof gates.

## Rationale

The semantic trigger must arrive before tool availability decides the route.
This preserves the useful Codex-local child mechanism for actual local
decomposition while making responsibility, not convenience or model
availability, determine when an external actor is required. Same-request
execute authority removes redundant ceremony without inventing permission.

## Consequences

- Fresh and compacted sessions receive the routing rule in the advertised
  skill description before choosing an agent tool.
- Generic delegation no longer activates `aoa-summon` ahead of the organ
  router.
- Explicit execution can proceed in one turn when its semantic authority is
  complete; exploratory pressure remains prepare-only.
- Built-in child tools remain available after a typed local-duty disposition.
- Source and prompt validation can prove trigger precedence is advertised;
  long-session behavior still requires fresh live exercises.

## Source Surfaces

- `skills/aoa-agents-skills/SKILL.md`
- `skills/aoa-agents-skills/agents/openai.yaml`
- `skills/aoa-agents-skills/references/role-first-entry.md`
- `skills/aoa-agents-skills/references/role-first-intent-v1.schema.json`
- `skills/aoa-summon/SKILL.md`
- `skills/aoa-summon/agents/openai.yaml`
- `capabilities/families/agent-lifecycle.yaml`
- `skills/port.manifest.json`

## Follow-Up Route

Exercise positive independent-duty, explicit local-child, no-delegation, and
post-compaction prompts in fresh installed sessions. Route behavioral findings
to aoa-evals without treating prompt exposure as a live verdict.

## Verification

Validate both skills, rebuild capability and decision projections, run the
focused skill-tree and repository suites, install the merged profile, inspect
the model-visible prompt, and then collect fresh-session routing evidence.
