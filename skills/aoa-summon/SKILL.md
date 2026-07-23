---
name: aoa-summon
description: Decide, launch, and close one bounded child-agent route from an anchored parent task through quest-passport gates, host delegation, named outputs, return validation, and reviewed closeout. Use when the user asks to delegate or summon one narrower reviewer, evaluator, verifier, or leaf helper and a real parent anchor exists. Do not use without explicit delegation intent, with unresolved branch choice, unnamed outputs, d3+ unsplit work, or to bypass approval, proof, progression, stress, or owner boundaries.
---

# aoa-summon

## Intent

Preserve the existing summon function as an executable owner skill: a child is
not "summoned" merely because a plan names one. Execution requires a real host
binding, a runtime child handle, a bounded return, and parent-side closeout.

## Owner-source return

Resolve the canonical `aoa-agents` root before any owner-relative read:

1. Record `<bundle_dir>` as the absolute directory containing the `SKILL.md`
   actually loaded; never resolve from the task working directory. Initialize
   one unresolved `<source_route>` and `<owner_root>`.
2. In one tool turn containing no other read or command, inspect exactly one
   same-bundle handle:
   `<bundle_dir>/.aoa-skill-source.json`. Await its result. If it is a regular
   file, set `<source_route>` to `source-handle` and require schema
   `aoa_skill_source_receipt_v1` or `aoa_skill_source_receipt_v2`, this bundle
   name, owner `aoa-agents`, version `0.2.4`, an existing absolute
   `owner_root`, a safe relative `source_path`, and
   `<owner_root>/<source_path>/SKILL.md`. For v2 also require non-empty
   `digest`, `source_fingerprint`, `source_fingerprint_scope`, and
   `prompt_description_sha256`. When `capability_graph_hash` is present,
   require it to be a non-empty string and preserve it.
   If the path exists but is invalid, mismatched, or not a regular file,
   return `blocked_missing_owner_source`; do not try another location.
3. Only when that exact same-bundle handle path does not exist, set
   `<source_route>` to `git` and run
   `git -C <bundle_dir> rev-parse --show-toplevel` exactly once. Require the
   returned root's `skills/port.manifest.json` to declare the expected owner,
   bundle, and path.
4. In the next tool turn, read only
   `<owner_root>/skills/port.manifest.json`; do not include an owner document,
   bundle reference, evidence read, or unrelated command. Await the result. In
   the source-handle branch, require the same `owner_repo`, bundle name, and
   bundle `path` as the handle. In the git branch, require `aoa-agents`, this
   bundle name, and its actual bundle path. If the manifest shared a tool batch
   with an owner document, return
   `blocked_owner_source_gate_not_observed` and do not use either result.
5. Only after manifest success, read the three named owner documents below in
   a later tool turn. Then owner-source resolution is complete. Do not run or
   retry the other source branch, including after a later owner-document read
   fails. Any handle, git, manifest, path, or owner mismatch returns
   `blocked_missing_owner_source` and ends this invocation.
6. Never use `find`, `rg --files`, parent traversal, sibling scans, workspace
   conventions, temporary fixtures, `.system`, or another skill directory to
   discover a substitute owner root.

Treat handle schema, owner ref, dirty posture, digest, source fingerprint,
capability graph hash, and prompt-description hash as install provenance, not
authority or current-parity proof. A
failed or non-serial resolution is terminal for this invocation; do not
execute or decide an owner-dependent summon from the installed copy alone. On
success, report `<source_route>`, `<owner_root>`, the receipt schema and
identity dimensions or git action ref, the manifest action ref, and the later
owner-document action ref. Read exactly
`<owner_root>/mechanics/titan/parts/summon-boundary/README.md`,
`<owner_root>/mechanics/titan/parts/summon-boundary/docs/summon-boundary.md`,
and
`<owner_root>/mechanics/titan/parts/summon-boundary/docs/summon-protocol-v2.md`
as the owner summon boundary; do not search for substitutes.

## Trigger boundary

Use when the user explicitly requests delegation/summoning and the parent route
has one settled branch, real anchor, quest passport, named outputs, and return
owner. Use decision-only mode when the user asks whether delegation is lawful.

Do not use for implicit background agents, broad orchestration, unresolved
route forks, unanchored work, unnamed outputs, or a child used to widen
authority or evade a gate.

## Inputs and outputs

- input: `summon-request-v3` plus explicit intent `decide` or `execute`; see
  `references/summon-request-v3.schema.json` and `references/contract.yaml`
- output: `summon-result-v3` with decision, binding and runtime state, child
  handle when launched, return validation, closeout handoff, effects, and stop

## Procedure

1. Read `references/contract.yaml` and `references/lane-and-return.md` to EOF.
2. Validate the request and gates. `d3+` returns `split_required`; missing
   progression/self-agent/stress/approval evidence returns the matching gate.
3. In `decide`, stop after one typed decision and executable return plan.
4. In `execute`, require explicit user delegation intent and a callable host
   binding; launch exactly one bounded child, record its runtime handle, await
   or retrieve its terminal result, validate named outputs, and close the
   parent handoff. If the binding is absent, return `blocked_binding_unavailable`.

## Contracts

- local host delegation is the default; remote transport needs a real separate
  execution surface, not prestige
- child scope, tools, effects, authority, and stop line cannot exceed passport
- failed, blocked, or narrowed child results still return explicitly
- child traces are session aids, never proof, memory canon, or owner truth
- technique lineage is optional provenance, not a runtime dependency

## Verification

- confirm parent anchor, named outputs, selected lane, all required gates, and
  exact host binding before launch
- distinguish decided, launched, running, returned, accepted, blocked, and
  failed; a JSON plan is not runtime execution
- validate returned artifacts against the request and preserve residual risk,
  checkpoint/memo candidates, and owner closeout without promoting them
