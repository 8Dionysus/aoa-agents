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

### 2026-07-25 - Block incomplete summon requests before lane admission

A fresh installed-profile trial supplied explicit delegation intent, a parent
anchor, and named outputs, but described two "named" child inputs without
actually supplying their identifiers or a complete `summon-request-v3`.
The correct owner skill was selected and no child launched, yet decision mode
returned `allowed`.

Version `0.2.6` now validates the literal request ABI before lane selection.
Missing required objects, fields, bounded task content, or input refs returns
`blocked_missing_request_input`; the skill may not infer or mint them. This
correction is justified by the observed negative case and still requires a
fresh rerun; it does not broaden delegation authority or prove general routing
lift.

### 2026-07-25 - Make pre-admission blocking representable

Review of the correction found that version `0.2.6` named bounded task content
and child input refs only as prose additions; `summon-request-v3` could not
represent them. It also blocked before lane selection while
`summon-result-v3` required a concrete lane, forcing either invalid output or
an invented route.

Version `0.2.7` makes intent, return owner, bounded child scope, stop line, and
typed child input refs required request fields. An input-free child is explicit
as `child_inputs: []`. The result schema now carries the full declared output
additions and permits `lane: null` only for a blocked, not-run pre-admission
result. Null is absence of a route, not a new execution lane.

This closes the representability defect. Existing validators and fresh manual
blocked and complete-request trials must still confirm the schema and behavior;
the schema does not itself prove a lawful delegation outcome.

### 2026-07-25 - Keep decision-only binding availability unknown

The first complete-request rerun selected `codex_local_leaf` correctly and did
not launch a child, but it returned `binding.available: true` without
inspecting the host interface. That turned a lawful route decision into an
unsupported runtime-currentness claim.

Version `0.2.8` requires every result to state whether the binding was actually
inspected. An uninspected decision reports `available: null`; only a real host
probe may report true or false, and live runtime states require inspected,
available binding. The same complete request must be rerun to prove the
behavioral correction.

### 2026-07-25 - Close contradictory result states

Review of the corrected result ABI found three remaining contradictions:
`allowed` could accompany a gate-only lane, `lane: null` did not itself require
the missing-request reason, and an inspected binding could still report
unknown availability.

Version `0.2.9` limits allowed results to executable lanes, makes a null lane
and `blocked_missing_request_input` imply one another, and requires boolean
availability after inspection. These schema invariants encode the already
stated procedure; they do not prove that a particular delegation is lawful or
that a host binding is available.

### 2026-07-26 - Require an executable and closeable live result

Version `0.2.10` closes the remaining one-way implications in the result ABI.
An allowed decision now requires `allowed: true` plus concrete execution
surface and cohort fields; live child states require a real interface and
child handle; and `accepted` requires successful return validation, received
output, and a concrete parent closeout route. These are contract consistency
invariants, not evidence that a host launch or returned artifact actually
occurred.

### 2026-07-26 - Exclude phantom execution from non-run states

Version `0.2.11` makes the pre-execution side of the state machine equally
explicit. Blocked and gate decisions remain `not_run`, `decided` and
`not_run` cannot carry a child handle, and an inspected unavailable binding
must include a concrete reason. This prevents a gate, plan, or failed binding
probe from masquerading as runtime identity.

### 2026-07-26 - Make output acceptance complete and non-run evidence empty

Version `0.2.12` replaces aggregate expected-versus-received lists with one
ordered validation record per requested output. An accepted result requires
every record to be received, artifact-linked, and accepted; the procedure
requires the records to match the request names exactly. Decision-only and
non-run results carry no output checks, accepted return, or actual effects.
These invariants prevent partial child returns and pre-execution plans from
masquerading as completed execution.

### 2026-07-26 - Close acceptance, lane, binding, and closeout implications

Version `0.2.13` makes aggregate return acceptance imply the accepted runtime
state, binds split and human-gate decisions to their matching lanes in both
directions, requires an inspected available binding to name its interface, and
requires every allowed decision to preserve parent closeout. Per-output records
also reject impossible received, artifact, and acceptance combinations. These
are state-machine consistency rules; they do not prove that a delegation or
artifact is valid in the environment.

### 2026-07-26 - Make executable intent closeable before launch

Version `0.2.14` requires every allowed result to preserve its unique named
outputs and a concrete parent owner and next route before execution. Gate lanes
carry no execution target, launched/running states carry no premature return
checks, and every live child state records the `child-agent-runtime` effect.
This keeps decision, launch, return, and closeout evidence aligned without
claiming that the host effect itself proves a valid result.

### 2026-07-26 - Use one canonical output identity map

Version `0.2.15` removes the duplicated expected-output list from the result.
`return_validation.output_checks` is now the single result-side output set,
keyed by the names from the request, so duplicate names are structurally
impossible. Allowed decisions carry the complete unreceived map; acceptance
requires every value to be received, artifact-linked, and accepted. The same
revision makes a null lane clear both execution targets, reserves `not_run` for
non-allowed results, and clears failure reason from an available binding.

### 2026-07-26 - Bind result acceptance to one immutable request

Version `0.2.16` gives every request and result the same immutable request ref,
digest, and intent. Expected outputs exist only once in the request. Aggregate
acceptance requires resolving that request, verifying its digest, and manually
checking exact equality between its expected-output set and the result's keyed
output map. The result schema also prevents an allowed `execute` request from
terminating as the decision-only `decided` state.
