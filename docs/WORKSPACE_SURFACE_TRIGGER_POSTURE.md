# Workspace Surface Trigger Posture

## Purpose

This document records the bounded role-facing law for when a workspace session
should open additive `aoa surfaces detect` posture after ingress and mutation
gating are already explicit.

It exists so surface-awareness stays legible as agent posture rather than
remaining an operator habit or silently mutating into routing authority.

## Core rule

`aoa surfaces detect` is additive and read-only.

It may open a second look when workspace signals show route drift, owner-layer
ambiguity, proof need, recall need, role posture pressure, or a recurring
scenario. It does not replace `aoa skills enter`, `aoa skills guard`,
`aoa-routing`, `aoa-playbooks`, or owner-layer meaning.

`aoa-skills` remains the only immediate activation lane in this slice.
Non-skill surfaces stay advisory, candidate-shaped, or reviewed handoff-shaped.

## Trigger signals

Open additive `aoa surfaces detect` when one or more of these signals is
present:

- route drift: the current route no longer looks like one bounded skill or one
  already-known owner path
- owner-layer ambiguity: more than one neighboring AoA layer looks plausible
  and the next owner is no longer obvious
- proof need: the route starts needing explicit eval-facing inspection rather
  than generic confidence
- recall need: provenance, memory, or prior-session recall now matters to the
  next step
- role posture pressure: the current session needs to clarify whether the work
  is skill, memo, playbook, technique, agent, or closeout-shaped
- recurring scenario pressure: the route looks repeated enough that playbook or
  technique harvesting may soon matter

## Route

1. Choose the workspace root and primary `repo_root`.
2. Run `aoa skills enter <repo_root> --root /srv ...` before substantial work.
3. Before risky mutation, run `aoa skills guard <repo_root> --root /srv ...`.
4. If one or more trigger signals is present, run `aoa surfaces detect <repo_root> --root /srv ...`.
5. Treat shortlist hints, owner-layer notes, and ambiguity notes as advisory
   consumer guidance only.
6. Keep `aoa skills ...` skill-only and keep reviewed `aoa surfaces handoff`
   explicit rather than automatic.

## Consumer seam

- `aoa-sdk` owns the typed `aoa surfaces detect` and reviewed handoff seam
- `aoa-routing` may contribute shortlist hints and ambiguity signals, but it
  does not own surface meaning
- `aoa-stats` may later describe ambiguity frequency and candidate posture, but
  it does not decide promotion or owner truth
- `aoa-playbooks`, `aoa-memo`, `aoa-evals`, and `aoa-techniques` remain the
  owner homes when the route resolves there

## Boundaries to preserve

- do not treat this posture as routing policy
- do not treat this posture as playbook canon
- do not let `aoa surfaces detect` activate non-skill objects
- do not collapse `manual-equivalent` into `activated`
- do not let workspace trigger posture become a hidden default that skips
  ingress or mutation gate visibility

## Result

The surviving reusable law is small:

- enter the workspace explicitly
- gate risky mutation explicitly
- open `aoa surfaces detect` only when the role-facing signals justify a second
  look
- keep all resulting shortlist and family hints advisory until an owning layer
  or reviewed closeout handoff makes them durable
