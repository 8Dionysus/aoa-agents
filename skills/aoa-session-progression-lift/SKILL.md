---
name: aoa-session-progression-lift
description: Lift closed, reviewed session evidence into a bounded multi-axis progression delta candidate for an AoA agent, with explicit baseline posture, attribution limits, holds or regressions, and small unlock hints. Use when meaningful mastery evidence needs owner review. Do not use on live impressions, to invent growth without a baseline, assign one universal score, mutate a role profile, grant authority, or turn progression into routing policy.
---

# aoa-session-progression-lift

## Intent

Make observed agent growth legible without turning one success, a mood, or a
generated summary into progression truth. The result is an owner-review
candidate; `aoa-agents` keeps progression authority and `aoa-evals` keeps proof.

## Owner-source return

Resolve the canonical `aoa-agents` root before any owner-relative read:

1. Record `<bundle_dir>` as the absolute directory containing the `SKILL.md`
   actually loaded; never resolve from the task working directory. Initialize
   one unresolved `<source_route>` and `<owner_root>`.
2. In one tool turn containing no other read or command, inspect exactly one
   same-bundle handle:
   `<bundle_dir>/.aoa-skill-source.json`. Await its result. If it is a regular
   file, set `<source_route>` to `source-handle` and require schema
   `aoa_skill_source_receipt_v1`, this bundle name, owner `aoa-agents`, an
   existing absolute `owner_root`, a safe relative `source_path`, and
   `<owner_root>/<source_path>/SKILL.md`. If the path exists but is invalid,
   mismatched, or not a regular file, return `blocked_missing_owner_source`;
   do not try another location.
3. Only when that exact same-bundle handle path does not exist, set
   `<source_route>` to `git` and run
   `git -C <bundle_dir> rev-parse --show-toplevel` exactly once. Require the
   returned root's `skills/port.manifest.json` to declare the expected owner,
   bundle, and path.
4. In the next tool turn, read only
   `<owner_root>/skills/port.manifest.json`; do not include an owner document,
   bundle reference, evidence read, or unrelated command in that tool turn.
   Await the manifest result. In the source-handle branch, require the same
   `owner_repo`, bundle name, and bundle `path` as the handle. In the git
   branch, require `aoa-agents`, this bundle name, and its actual bundle path.
   If the manifest read shared a tool batch with an owner document, the serial
   gate was not observed: return
   `blocked_owner_source_gate_not_observed` and do not use either result.
5. Only after the successful manifest result, use a later tool turn to read
   exactly the two named owner-model documents below. Then owner-source
   resolution is complete. Do not run or retry the other source branch,
   including after a later owner-document read fails. Any handle, git,
   manifest, path, or owner mismatch returns `blocked_missing_owner_source`
   and ends this invocation.
6. Never use `find`, `rg --files`, parent traversal, sibling scans, workspace
   conventions, temporary fixtures, `.system`, or another skill directory to
   discover a substitute owner root.

Treat handle ref, owner ref, dirty posture, and digest as install provenance,
not authority or current-parity proof. A
failed or non-serial resolution is terminal for this invocation; do not
synthesize an owner-dependent candidate from the installed copy alone. On
success, report `<source_route>`, `<owner_root>`, the handle or git action ref, the
manifest action ref, and the later owner-model action ref. Read exactly
`<owner_root>/mechanics/rpg/parts/progression-model/README.md` and
`<owner_root>/mechanics/rpg/parts/progression-model/docs/agent-progression-model.md`
as the owner model; do not search for substitutes.

## Trigger boundary

Use when a closed and explicitly reviewed session contains meaningful mastery,
regression, reanchoring, or unlock evidence tied to one `agent_id`.

Do not use when evidence is live/unreviewed, the agent or baseline posture is
unknown, only a single score is wanted, or the requested effect is direct role,
rank, authority, routing, quest, or proof mutation.

## Inputs and output

- input: one `reviewed-progression-evidence` packet with `agent_id`, current
  session boundary, evidence refs, attribution limits, baseline or explicit
  baseline state, and optional current progression object
- output: one `progression-delta-candidate` defined by
  `references/contract.yaml`; effect is `none` until separate owner review

## Procedure

1. Read `references/contract.yaml` and `references/lift.md` to EOF.
2. Reject live/unbounded evidence and classify every checkpoint, closeout,
   donor, generated, stale, or neighboring-session item as a hint until the
   reviewed packet corroborates it.
3. Execute the lift once. Do not apply the candidate to the owner progression
   object or chain automatically into summon, quest, stats, memo, or proof.

## Contracts

- progression is a multi-axis adjunct to `agent_id`, never a profile rewrite
- comparative movement requires an honest baseline posture
- tools, environment, prior context, and reviewer uncertainty remain visible
- rank and unlocks are reviewable hints; they grant no authority or route rights
- technique lineage is optional provenance, not a runtime dependency

## Verification

- trace every moved axis to reviewed refs and state attribution limits
- preserve zero, negative, contested, stale, and no-movement outcomes
- confirm the owner model was read, the candidate was not applied, and the
  nearest wrong route was rejected
