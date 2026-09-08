---
name: aoa-summon
description: Decide or execute a complete summon-request-v4 for an independent external AoA actor and return a validated summon-result-v4. Use as the aoa-agents-skills execution leaf or to inspect an explicit legacy summon packet. Ordinary native Codex helpers do not use this leaf.
---

# aoa-summon

Execute an already settled actor route. This leaf does not form an obligation,
choose a role or model, select unresolved transport, or widen the caller's
authority. A plan is not a launch; execution needs an inspected host binding,
a real runtime handle, output validation, and responsibility closeout. This is
not the front door for generic delegation or native Codex helpers.

## Owner source

Resolve from the absolute directory containing the loaded `SKILL.md`, not
from the task working directory:

1. Inspect that bundle's `.aoa-skill-source.json`. An existing handle must be
   a regular non-symlink file with schema `aoa_skill_source_receipt_v1` or
   `aoa_skill_source_receipt_v2`, name `aoa-summon`, owner `aoa-agents`,
   a non-empty version, an existing absolute `owner_root`, and safe relative
   `source_path` containing `SKILL.md`. V2 also requires non-empty
   `digest`, `source_fingerprint`, `source_fingerprint_scope`, and
   `prompt_description_sha256`; preserve a non-empty `capability_graph_hash`
   when present.
2. Only if the handle is absent, use
   `git -C <bundle_dir> rev-parse --show-toplevel` to locate the source root.
3. Read `<owner_root>/skills/port.manifest.json`. Its owner, bundle name,
   path, and declared version must match the handle, or the source bundle's
   `references/contract.yaml` when using Git. An invalid handle or mismatched manifest returns
   `blocked_missing_owner_source`; do not search for a substitute checkout.

These are data dependencies, not separate-tool-turn requirements: dependent
reads may share one call when each result is checked before using it.
Record the resolved owner and source identity. Install digests and commit refs
are provenance, not proof of current parity or execution.

For summon-boundary meaning, read the resolved owner's
`mechanics/titan/parts/summon-boundary/README.md` and its
`docs/summon-boundary.md` and `docs/summon-protocol-v2.md`.
Schema and compiler mechanics remain in this bundle.

## Request and mode

The input is one literal `summon-request-v4` with `decide` or `execute`
intent. Transport is already `codex_local` or `external_cli`; SDK
`a2a_remote`/`either` requests must be resolved upstream.

- External execution needs the complete `external_incarnation` packet from
  `aoa-agents-skills`, including the admitted distinct-holder transfer.
- Only an explicitly supplied legacy Codex-local summon packet uses the local
  compatibility lane. It needs the exact owner-produced
  `responsibility_classification` with `not_independent` disposition.
  Its artifact, Goal, holder, execution epoch, and child-duty digest must bind
  to this request; a prose classification or old session context is not enough.
- Missing fields, inputs, named outputs, or authority return
  `blocked_missing_request_input`, `lane: null`, `allowed: false`, and
  runtime state `not_run`. Do not infer a complete packet from a route-shaped
  prompt. An input-free request explicitly carries `child_inputs: []`.

These local-ABI checks do not apply to ordinary native Codex delegation.
Do not construct a legacy summon packet solely to admit a native helper.

Use [lane-and-return.md](references/lane-and-return.md) for lane selection and
state-specific return requirements. Run
`scripts/validate_summon_request.py` before admission; supply the current
execution epoch from the routing/runtime owner for the local lane.
[contract.yaml](references/contract.yaml) and its named schemas define the ABI;
use them when inspecting or changing packet fields.

In `decide`, return the typed decision and stop without a host probe or
launch. An uninspected binding has `inspected: false`, `available: null`.

In `execute`, inspect the callable binding, launch one authorized runtime,
retain its handles, retrieve its result, validate every named output, and
return responsibility. If the binding is unavailable, return
`blocked_binding_unavailable`; do not silently substitute another transport.
An external actor requires a separate OS process and persistent CLI session,
resume/event handles, and disabled built-in subagents.

Start, wait, resume, and wake use the inspected runtime's supported interfaces.
Unavailable lifecycle support is a concrete binding blocker, not permission
to emulate a Goal transition or create another scheduler. Preserve an existing
actor's obligation and identity when continuing it.

## Use existing compilers

Use the [existing passive helpers](references/lane-and-return.md#existing-passive-helpers)
for request preparation, return compilation, and explicit receipt publication.
Keep semantic decisions with their owners; compiler failure returns the exact
missing or contradictory owner input without repairing authority locally.

## Return boundaries

Preserve the immutable request identity, selected role/model binding, exact
SDK/runtime/A2A/usage refs, actual effects, and concrete next holder.
Check the exact requested output set; never accept missing, extra, or
unreviewed outputs. Failed and narrowed executions also return explicitly.

Distinguish decided, launched, running, returned, and accepted using the
evidence for that state. Runtime traces and usage receipts do not establish
proof, memory truth, model fit, or owner acceptance. Usage is observation, not
a caller-created budget gate. Publication is a separate explicit action and
does not activate the stats runtime.

V3 request/result schemas are historical read contracts only. New decisions,
executions, and results use v4.
