# Agent Obligation And Incarnation Skill Tree

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0061
- Original date: 2026-08-02
- Surface classes: owner skill home, capability topology, sibling-owner boundary, runtime consumer seam
- Agent facets: role contract, responsibility posture, incarnation, handoff
- Mechanic parents: cross-mechanic, runtime-seam, boundary-bridge
- Guard families: owner boundary, external incarnation, task-local DAG, return validation
- Posture: admitted challenger router with shadow model realization

## Context

Large goals repeatedly expose duties such as landing, CI, eval, memo, stats,
and independent review. Treating those duties as generic child tasks or starting
from a cheap model launcher loses the durable reason an actor exists: a
separate obligation needs a stable bearer of responsibility, authority,
continuity, and return posture.

The first practical pressure is a landing duty whose current candidate model
realization is Luna, but neither landing nor Luna is stable agent identity.
The existing `aoa-summon` preserves useful request, runtime-handle, named-output,
and return-validation evidence, yet its current admitted ABI is still bound to
explicit child delegation and built-in Codex lanes.

## Options Considered

- Start from a Luna launcher and wrap it in a globally installed skill.
- Treat every independent duty as a disposable built-in Codex child.
- Create one owner-local `aoa-agents-skills` tree that begins with obligation
  pressure, keeps model and runtime replaceable, and admits execution leaves
  only through typed responsibility and return contracts.

## Decision

Create `aoa-agents-skills` as the organ-level root bundle and owner-local
capability tree for:

```text
goal pressure or future duty
  -> independent obligation
  -> stable role mandate and required executor properties
  -> current model realization and specialized environment binding
  -> situational responsibility transfer
  -> separate CLI incarnation through an execution leaf
  -> filtered return, responsibility reassignment, or controlled wake
```

The semantic tree is durable discovery source. Typed relations describe
compatibility. Each goal's `aoa-task-local-dag-v2` remains ephemeral runtime
state and may grow during planning, execution, and closeout.

`aoa-summon` is a leaf of this tree only where it can consume the exact
incarnation and responsibility packet and launch a separately addressable CLI
process/session. Its built-in Codex child lanes remain compatibility surfaces
and do not satisfy the external-incarnation proof. If that ABI cannot evolve
without corrupting its existing contract, another external execution leaf must
carry the route.

The leaf's owner-local request/result receipt does not replace the canonical
`aoa-sdk` A2A request/decision or the `abyss-stack` terminal and reviewed-return
artifacts. It binds them by exact owner-qualified digest and owns only the
actor-execution and responsibility-closeout view needed by `aoa-agents`.

The capability home and `aoa-agents-skills` root bundle are admitted as a
prompt-visible challenger router. This admission is deliberately narrower than
admission of any model realization or domain route: it establishes the organ's
ability to detect an independent obligation, preserve a role mandate, bind
stronger-owner evidence, transfer responsibility to an external execution
leaf, and filter a reviewed return.

This corrects the earlier decision text, which conflated admission of the
obligation-to-actor router with admission of the Luna/landing realization. The
installed vertical evidence now includes a real separate Luna CLI session with
workspace-write authority, an independently addressable reviewer session, an
exact reviewed A2A return, exact parent-thread re-entry on a significant return,
filtering of a non-significant event, and an ambiguity stop. These observations
are sufficient to expose the bounded router as a challenger. They do **not**
establish general Luna task fit, cross-model equivalence, net benefit, or
permission for an unreviewed effect. The Luna/landing realization therefore
remains shadow evidence owned by `aoa-models`, `aoa-sdk`, `abyss-stack`, and the
landing procedure owner.

## Rationale

This direction starts from an obligation rather than available compute, keeps
role identity stable while model and process bodies change, and lets the task
DAG express real responsibility movement without turning a launcher into A2A.
It also preserves existing owner boundaries: domain owners retain procedures,
`aoa-models` retains fit evidence, `aoa-sdk` retains runtime planning and
incarnation binding, and `abyss-stack` retains external CLI execution.

## Consequences

- Any future model can replace Luna without renaming the role or root skill.
- A persistent office may survive while no process is running; continuation
  and wake remain explicit contracts.
- Trigger strengths distinguish notice, required plan branch, master decision,
  and an exact pre-authorized reflex.
- The root is present in the global advertised profile as a challenger router;
  its mutation paths remain gated by exact stronger-owner bindings and explicit
  apply authority.
- Existing child-oriented `aoa-summon` consumers retain compatibility while an
  external CLI lane provides the independently addressable execution leaf.
- The first vertical proof may use landing preparation and independent release
  review, but remote publication remains with its domain owner.
- A model realization, domain procedure, or effect route cannot inherit
  admission from the root skill. Each keeps its own evidence and owner gate.

## Source Surfaces

- `skills/aoa-agents-skills/`
- `skills/aoa-summon/`
- `capabilities/port.manifest.json`
- `capabilities/families/agent-lifecycle.yaml`
- `skills/port.manifest.json`
- `agents/roles/`
- `agents/operating-model/`

## Follow-Up Route

Install the admitted challenger root through the owner-skill profile and verify
its discovery in a fresh Codex session. Keep the Luna/landing route in shadow
while `aoa-evals` and the model owner test held-out duties, failure boundaries,
comparative cost, and net benefit. Promote a model/domain/effect route only
through its own owner decision; do not revise the stable role around the
current winning realization.

## Verification

Build and validate the owner capability projection, run owner skill-home and
repository validators, and verify fresh-session discovery after profile
installation. The bounded execution evidence for challenger admission is:

- writer result
  `/srv/abyss-machine/tmp/ai/external-codex-landing-study-20260802/runtime-state-installed-workspace-write-018/sessions/970ee8de9a548219782a139be93c6f01/result.json`
  (`sha256:bcbc2609e8760c4fc2002e1278cf5f5932872d962cd93055463e8b53431aed32`);
- independent reviewer result
  `/srv/abyss-machine/tmp/ai/external-codex-landing-study-20260802/runtime-state-installed-workspace-write-018-reviewer/sessions/bd95f403a0c1955b7dd6d433b3291cda/result.json`
  (`sha256:ae0b85bef322e338fd3d5adf798d79ef88e0d3e88623422e262a71a6bee08c5d`);
- reviewed A2A return
  `/srv/abyss-machine/tmp/ai/external-codex-landing-study-20260802/a2a-return-installed-runtime-workspace-write-018.json`
  (`sha256:6126ee0bb58bb93fe4fddb143a18d963060e2bd40be3fad412599c030d4e7cb8`);
- controlled re-entry and event filtering
  `/srv/abyss-machine/tmp/ai/external-codex-landing-track-20260801/l2-reentry-closeout-v2.json`.

The same packet counts 2,616,871 input tokens, 2,372,096 cached input tokens,
30,058 output tokens, 611.381005 active seconds, 104 commands, and 834,221
output bytes. These are observations, not a token budget or a net-benefit
verdict.
