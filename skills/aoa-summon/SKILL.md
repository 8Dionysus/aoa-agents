---
name: aoa-summon
description: Execute one bounded actor route from an anchored goal, including compatibility child lanes or an independently bound external CLI incarnation, named outputs, return validation, and responsibility closeout. Use when the user explicitly delegates or when aoa-agents-skills selects this leaf from a complete task-local actor DAG. An incomplete request must block. Do not use for generic implicit spawning, unresolved branching, unnamed outputs, unsplit deep work, or to bypass obligation, mandate, incarnation, approval, owner, or proof boundaries.
---

# aoa-summon

## Intent

Preserve summon as the execution leaf, not the source of actor meaning. A route
is not executed merely because a plan names a child, actor, model, or launcher.
Execution requires a real inspected host binding, runtime handle, bounded
return, and responsibility closeout. `child` remains compatibility vocabulary
for the existing Codex-local lanes; the external lane uses an actor identity
and separate CLI process/session.

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
   name, owner `aoa-agents`, version `0.4.0`, an existing absolute
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

Use through either of two exact authorities:

- the user explicitly requests delegation/summoning and the anchored route has
  one settled branch, quest passport, named outputs, and return owner; or
- `aoa-agents-skills` has produced one complete task-local execution-leaf
  packet with obligation, actor mandate, incarnation binding, an owner-qualified
  admitted responsibility-transfer ref with distinct previous/current holders,
  domain procedures, separate CLI runtime launch, outputs, return, continuation,
  and stop refs.

Use decision-only mode when the caller asks whether either route is lawful.

Do not use for generic implicit background agents, keyword autospawn, broad
orchestration, unresolved route forks, unanchored work, unnamed outputs, or an
actor used to widen authority or evade a gate. A source-authorized task-local
leaf is not permission to infer any missing field.

## Inputs and outputs

- input: `summon-request-v4` plus intent `decide` or `execute`; the
  `external_cli` transport additionally requires the complete
  `external_incarnation` extension; see
  `references/summon-request-v4.schema.json` and `references/contract.yaml`
- output: `summon-result-v4` with decision, binding and runtime state, canonical
  actor/process/session/continuation handles for the external lane,
  compatibility child handle where material, exact SDK summon request and
  decision refs, runtime-owned terminal/result/usage refs, immutable request
  identity and intent, one validation record per named output, closeout
  handoff, effects, and stop. This owner-local receipt does not replace or
  rename the `aoa-sdk` A2A schemas or the `abyss-stack` runtime return.

## Procedure

1. Read `references/contract.yaml` and `references/lane-and-return.md` to EOF.
2. Validate the literal supplied request against `summon-request-v4` and the
   additions in `references/contract.yaml` before deciding a lane. A
   route-shaped description is not a request packet: if required objects,
   fields, input refs, or bounded task content are absent, return
   `blocked_missing_request_input` with `lane: null`, `allowed: false`, and
   runtime state `not_run`; never infer or mint them. An input-free child must
   carry an explicit empty `child_inputs` array. Only then evaluate gates.
   The request carries one immutable `request_ref` and a `request_digest`
   computed as SHA-256 over canonical JSON with `request_digest` omitted.
   `d3+` returns `split_required`; missing
   progression/self-agent/stress/approval evidence returns the matching gate.
3. In `decide`, stop after one typed decision and executable return plan. Do
   not probe the host merely to strengthen a decision-only answer. When the
   binding was not actually inspected, return `binding.inspected: false` and
   `binding.available: null`; an allowed lane is not a claim that launch is
   currently available.
4. In `execute`, require either explicit user delegation or a complete
   source-authorized `aoa-agents-skills` external-incarnation packet, plus a
   callable inspected host binding. Launch exactly one bounded runtime, record
   its canonical handles, await or retrieve its terminal result, validate named
   outputs, and close the responsibility handoff. If the binding is absent,
   return `blocked_binding_unavailable`. Copy the request ref, digest, and
   intent into the result; execute intent may never terminate as a
   decision-only `decided` state.
5. For `external_cli_reviewed`, require the host binding to consume the exact
   `aoa-sdk` incarnation, summon request, summon decision, and `abyss-stack`
   launch refs, launch a separate OS process and separate persistent CLI
   session, disable built-in Codex subagents, expose resume and event handles,
   and return observe-only usage receipts. On terminal reviewed return,
   preserve the runtime-owned result and A2A-return refs and validate the
   requested outputs from those exact bytes. Do not ask `abyss-stack` to emit
   `summon-result-v4`: that receipt belongs to this leaf and references the
   stronger SDK/runtime artifacts. Do not substitute `codex_local_*` or
   `remote_reviewed` when the external contract is unavailable.

## Contracts

- existing local child delegation remains the compatibility default only for
  explicit child requests; external actor execution selects
  `external_cli_reviewed` and a real separate execution surface
- scope, tools, effects, authority, and stop line cannot exceed the passport,
  actor mandate, incarnation binding, or responsibility transfer
- failed, blocked, or narrowed actor results still return explicitly
- runtime traces are session aids, never proof, memory canon, or owner truth
- technique lineage is optional provenance, not a runtime dependency

## Verification

- confirm goal/parent anchor, named outputs, selected lane, all required gates, and
  exact host binding before launch
- never report binding availability from configuration, catalog presence, or
  assumption; only a real host-interface inspection may set
  `binding.inspected: true`
- confirm every required request field and input ref was literally supplied
  before returning `allowed`; a task with no inputs must say so through an
  explicit empty `child_inputs` array
- distinguish decided, launched, running, returned, accepted, blocked, and
  failed; a JSON plan is not runtime execution
- require failed execution to preserve the inspected binding and canonical
  runtime handles just like every other post-launch state; external execution
  preserves `external-actor-runtime`, while compatibility child execution
  preserves `child-agent-runtime`; reject the retired result-side
  `expected_outputs` field
- validate returned artifacts against the request and preserve residual risk,
  checkpoint/memo candidates, and owner closeout without promoting them
- build `return_validation.output_checks` as an object keyed by every request
  `expected_outputs` name and no others; the key is the output identity, so
  duplicates cannot exist; accept only when every value is received,
  artifact-linked, and accepted
- resolve `request_ref`, verify `request_digest`, and compare the request
  `expected_outputs` set exactly with the result `output_checks` keys before
  aggregate acceptance; no missing or extra key may advance parent work
- keep gate decisions and lanes bidirectionally aligned; aggregate acceptance
  is true only in the accepted runtime state, and every allowed route requires
  parent closeout
- preserve immutable request identity, request intent, concrete responsibility
  return owner, and next route in every allowed result; executable states must
  carry the actual host execution effect
- preserve the SDK summon request/decision and runtime result/A2A-return as
  exact owner-qualified refs; never copy their fields into a competing A2A ABI
- preserve the exact role-resolution, model-fit query, selected fit projection,
  and incarnation-binding-v2 refs through request, runtime binding, and return;
  a model name or runtime profile cannot substitute for this evidence chain
- treat `summon-request-v3` and `summon-result-v3` as frozen historical read
  contracts only; they may be validated to inspect old receipts, but no new
  execution may launch from v3 or emit a new v3 result
