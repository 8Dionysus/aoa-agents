---
name: aoa-summon
description: Execute one bounded actor route only after aoa-agents-skills has classified responsibility and supplied a complete external execution leaf, or after it has returned a typed not_independent disposition for an explicitly requested disposable Codex-local child whose complete anchored packet carries the resolved classification artifact and child-duty digest, names outputs, and names a return owner. This leaf consumes only a resolved summon-request-v4 with transport_preference codex_local or external_cli; unresolved aoa-sdk a2a_remote/either requests and generic delegation must remain with their owning routing control plane. Generic requests for an agent, sub-agent, worker, reviewer, researcher, delegation, parallel work, or background work must route to aoa-agents-skills before this skill or any built-in Codex tool such as spawn_agent. Use the external CLI lane for an independently bound incarnation. An incomplete request must block.
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

- `aoa-agents-skills` has produced one complete task-local execution-leaf
  packet with obligation, actor mandate, incarnation binding, an owner-qualified
  admitted responsibility-transfer ref with distinct previous/current holders,
  domain procedures, separate CLI runtime launch, outputs, return, continuation,
  and stop refs; or
- the user explicitly requests a disposable Codex-local child and the anchored
  route already has one settled local branch, quest passport, named outputs,
  and return owner after `aoa-agents-skills` returned `not_independent`.

A generic request to delegate to an agent, sub-agent, worker, reviewer,
researcher, parallel lane, or background role is not direct authority for this
leaf. Route it to `aoa-agents-skills` before this skill or any built-in Codex
tool such as `spawn_agent`.

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
- a `codex_local` request must carry the exact owner-produced
  `responsibility_classification` with `disposition: not_independent`, its
  typed `result_ref` to `responsibility-classification-v1`, and a digest of the
  complete local-child duty subject; this result is part of the request ABI,
  not session-only context
- output: `summon-result-v4` with decision, binding and runtime state, canonical
  actor/process/session/continuation handles for the external lane,
  compatibility child handle where material, exact SDK summon request and
  decision refs, the runtime-owned refs required by the observed state (all
  result/A2A/usage refs for returned or accepted, result/usage refs for failed,
  and no return refs yet for launched or running), immutable request identity
  and intent, one validation record per named output, closeout
  handoff, effects, and stop. This owner-local receipt does not replace or
  rename the `aoa-sdk` A2A schemas or the `abyss-stack` runtime return.

## Procedure

1. Read `references/contract.yaml` and `references/lane-and-return.md` to EOF.
2. Validate the literal supplied request against `summon-request-v4` and the
   additions in `references/contract.yaml` before deciding a lane. For a
   `codex_local` lane, require the carried typed
   `responsibility_classification.disposition: not_independent`, its
   owner-qualified `result_ref` to `responsibility-classification-v1`, the
   exact `artifact_path`, the copied Goal/current-holder refs, and the
   classification's `execution_epoch` bound to `quest_passport.execution_epoch`
   and `quest_passport.route_anchor` bound to the classification Goal, together
   with its `child_scope_digest` bound to this request's desired role, intent,
   expected outputs, child scope, stop line, and child inputs. Run
   `scripts/validate_summon_request.py` to resolve the artifact, validate its
   owner schema and semantic digest, and bind its Goal to `parent_task_id`,
   child duty to this request, and holder to `return_owner`; do not reconstruct
   the classification from prompt
   history, compaction context, or a prose mention. A
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
4. In `execute`, require either a complete source-authorized
   `aoa-agents-skills` external-incarnation packet or an explicitly requested
   disposable Codex-local child packet following a carried typed
   `not_independent` disposition and the exact classification artifact
   resolution above, plus a callable inspected host binding. Launch exactly
   one bounded runtime, record
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

For the external lane,
`scripts/compile_external_execution_request.py` may compile the final
`summon-request-v4` from already complete obligation, mandate, exact role
resolution, model-fit query and projection, SDK binding/request/decision/plan,
task-local DAG, runtime task/launch/event schema, responsibility transfer, and
domain procedure files. It performs no semantic selection, host inspection,
launch, or effect. The SDK request may retain `a2a_remote` or `either` before
this leaf is reached; the compiler translates that SDK-owned choice to the
physical `external_cli` leaf and removes the SDK's duplicate nested output
list. The emitted aoa-summon request is resolved and contains `external_cli`,
never an unresolved SDK transport.
Before emitting that request, it also validates the complete SDK permission
posture, enforces its external-effect, read-only-sandbox, and secret-approval
cross-field invariants, and requires the effect ceiling to equal both the
runtime task and actor mandate. It also requires the selected binding tool and
MCP ceilings to equal the actor-mandate environment, forbids inherited user
configuration, and binds the tool profile to the same runtime-profile ref.
It also preserves the originating obligation goal in the mandate and SDK
route anchor, and preserves the obligation lifecycle in mandate identity and
continuity posture. It preserves the obligation domain owner and exact duty in
the mandate/continuation chain, binds the mandate stop line to the obligation
stop line and model-fit authority to its current holder, and requires the SDK decision to select
`a2a_remote` explicitly. The complete incarnation binding must pass the exact
aoa-sdk v2 owner schema and semantic self-digest before field-level relations
are admitted; the schema content digest is pinned and a caller-supplied `$id`
does not establish owner authority. The SDK run plan likewise passes the
complete generated `RunPlan` schema pinned by canonical content, and both its
snapshot and plan semantic digests are recomputed before a decision snapshot
can authorize launch.
Invalid authority therefore stops before
responsibility reaches the runtime rather than waiting for closeout.

After a runtime has already returned, `scripts/compile_external_execution_result.py`
may compile one `summon-result-v4` from the exact owner request, SDK request and
decision, exact agent-obligation-v1, actor-mandate-v1,
aoa-role-resolution-v1, and
incarnation-binding-v2 artifacts, terminal
`abyss-stack` result, runtime-profile ref, reviewed A2A return, and the exact
review summon-request artifact named by that return. It is a passive closeout
adapter:
it verifies the immutable request
digest and schema, requires the complete owner summon body and passport to be
the SDK request with only the documented `a2a_remote` or `either` to
`external_cli` transport translation, and preserves
role, fit, incarnation, runtime, A2A, and usage
evidence as refs, and derives the four external handles from the supplied
runtime evidence. The mandate goal and request route anchor must equal the
exact obligation goal, and mandate identity plus continuity posture must
preserve its lifecycle. The mandate domain owner and delegated continuation
duty must remain equal to the exact obligation, and the SDK decision must
select `a2a_remote`. The mandate stop line and model-fit authority must remain
bound to the exact obligation stop line and current holder. Its complete role
binding, including specialization, tier, and provenance refs, must equal the
independently loaded exact role-resolution artifact. The request authority limit and stop line must equal the
exact obligation boundary and mandate stop line. Both responsibility holders
must equal the selected return owner and mandate continuity identity, and the
SDK continuation must retain the same concrete return-holder identity,
digest, owner, and schema. The binding permission posture must satisfy the
aoa-sdk cross-field invariants. A
reviewed return must carry runtime-owned A2A schema
provenance, bind its reviewed writer-result digest to the exact terminal
runtime result, bind `remote_task.task_id` and `remote_task.agent_id` exactly
to the terminal runtime `task_id` and `incarnation_id`, and be paired with the canonical
`result.validated`/`validated-completion` wake event. Its independently loaded
review request must have the exact returned digest, source itself from that
terminal result, route a distinct read-only verifier over the same writer
path/task/digest, retain the same audit and output closures, and authorize
that exact output closure through its quest passport. The SDK
decision must carry its actual nonempty cohort pattern; closeout never invents
a local fallback. An embedded usage
observation is accepted only at the exact `/usage_observation` JSON pointer
and must retain the runtime-owned observation shape: `complete` has no gaps,
while `partial` has at least one canonical gap. An optional
`--usage-observation-ref` is only an assertion of that exact runtime-owned
JSON-pointer ref; it must match its object identity and subtree digest and
cannot replace the embedded observation. There is no separately minted usage
artifact on this owner-local surface. Actor-safe immutable input
envelopes are addressed by their exact derivative bytes; their embedded source
digest is not elevated to stronger-owner identity without a separate trusted
attestation. Every envelope must retain a nonempty source schema ref, and its
provenance schema version must agree with the
unwrapped payload schema version, or with the explicit expected owner schema
version when that owner payload is intentionally schema-less. The reviewed A2A return binds the complete original SDK
summon-request ref, not only its digest. The output path must be new and is
never overwritten. The terminal runtime's owner-admission ref must bind both
the exact owner-request identity and bytes, and therefore that request's exact
runtime-launch, continuity, task, and effect chain. The supplied incarnation
binding must match its request ref, incarnation and continuity identities,
exact child identity, obligation, mandate, role resolution, model-fit query
and projection, SDK task request, effect posture, and exact runtime-profile
ref. It must also retain the complete strict owner-v2 shape and semantic
binding digest, including its run-plan and model-realization refs; the model
realization and fit projection must share one aoa-models source. The exact
run-plan and model-realization content refs must also be carried by the owner
request and match the binding, so recomputed local digests cannot substitute
another plan or realization. The exact
mandate must authorize the same obligation, role resolution, selected role,
and domain-procedure sequence carried by the request and binding. A
syntactically valid unrelated or truncated owner ref, mandate, or profile
cannot be substituted. The logical continuation identity remains in the exact
request/binding chain; the physical Codex continuation handle is the runtime
`thread_id` and must equal every admitted invocation's `thread_id`.
Returned artifacts are an
exact, duplicate-free closure over the request's named outputs; path basenames
are not inferred as output identities. The compiler does not launch, review,
select, repair, or mint an SDK, runtime, A2A, stats, proof, or owner-acceptance
artifact.

When the obligation, role choice, mandate, model-fit selection, domain
procedure, permission posture, task-local source graph, and exact owner roots
are already settled, `scripts/prepare_external_actor.py` may compile the whole
non-starting route packet. It resolves the selected role and model projection
through their owners, asks `aoa-sdk` for transport admission and incarnation
binding, asks the installed `abyss-stack` binder for a launch artifact, and
then emits the final `summon-request-v4`. It does not detect an obligation,
choose a role or model, launch a process, accept a result, or own the domain
procedure. `independent_review` packets must carry the exact reviewed artifact
and every immutable evidence object referenced transitively by writer report
or output anchors; their task-local DAG terminates at that reviewer rather than
inventing review-of-review.

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
- require the request tool scope to equal the binding tool ceiling, and require
  the mandate environment, effect, MCP, and sandbox ceilings to agree with that
  same binding rather than trusting a recomputed request digest
- return responsibility only when the mandate and request name the same holder,
  the transfer names that holder as its prior holder, and the SDK continuation
  retains the same owner repository
- bind a successful independent-review completion to the runtime's canonical
  `result.validated` event and keep repair returns on `result.review_required`;
  a structurally valid report with an unbound wake event must fail closed
- treat `summon-request-v3` and `summon-result-v3` as frozen historical read
  contracts only; they may be validated to inspect old receipts, but no new
  execution may launch from v3 or emit a new v3 result

## Actor responsibility observation

`scripts/compile_actor_responsibility_receipt.py` is a passive owner-local
observation adapter. It accepts one exact schema-valid
`urn:aoa-agents:aoa-summon:result:v4` artifact from the external lane plus
explicit canonical `result_artifact_ref`, `observed_at`, `run_ref`,
`session_ref`, `actor_ref`, and `object_ref` inputs. It retains the exact
result-byte digest, selected role/model/SDK references, state-appropriate
runtime/A2A/usage references, effects, review/output posture, closeout
handoff, and stop line in the strict
`aoa_actor_responsibility_execution_receipt_v1` payload. Its event ID is
derived from the exact result digest, canonical payload projection, and those
observation inputs; supplied digest or event-ID assertions must match exactly.
The projected `execution.runtime_state` must equal
`owner_evidence.runtime_state.state`, and source `blocked_actions` and
`reason_codes` arrays are compacted by dropping empty strings and later
duplicates while preserving first-seen order before strict payload validation.

For a live usage report, the same passive adapter may receive an exact
`--runtime-result` plus `--expected-runtime-result-digest`. It verifies the
terminal runtime-result bytes (including an exact actor-safe runtime envelope),
the A2A task identity independently from an optional result identity, the usage
pointer, and the canonical usage-observation digest before adding the bounded
`aoa_actor_usage_observation_projection_v1` snapshot. This remains
observe-only data: it does not replace stronger runtime refs or infer model
fit, benefit, success, proof, review approval, owner acceptance, budget, or
limiting policy. `--supersedes` appends a repaired observation as a new event
while preserving the earlier receipt. Absent runtime fields remain null and are
listed in `unknown_fields`; the adapter never fills them from neighboring
receipts or from policy. The observation status/gap law is strict: `complete`
requires no gaps and `partial` requires at least one canonical gap. Likewise,
`cost_status=reported` requires numeric `cost_usd`, while non-reported statuses
keep it null. The projection's retained runtime and usage refs must
continue to equal the owner evidence refs when a receipt is validated for
publication.

`scripts/publish_actor_responsibility_receipts.py` is a separate explicit
publisher. It validates the complete envelope and owner payload before
appending to `.aoa/live_receipts/actor-responsibility-execution-receipts.jsonl`,
resolving the owner root through the same-bundle source handle or explicit
`--owner-root`. It skips duplicate event IDs, validates existing feed lines in
order, requires every `supersedes` target to be an existing or earlier event in
that order, and fails closed on malformed existing logs. Tests use a temporary
`--log-path`; compilation never publishes
automatically. The publisher takes a POSIX advisory exclusive lock at
`<log-path>.lock` before reading existing IDs and holds it through the append,
so independent sessions using the same log path serialize deduplication. The
lock file is owner-local runtime coordination, not a receipt, source artifact,
or automatic feed activation; hosts without advisory-lock support fail closed.

This route consumes the admitted `aoa-stats` envelope and event-kind meaning
without modifying or activating `aoa-stats`. Receipt presence is an
observation only: it does not infer benefit, model fit, task success, proof,
review approval, or owner acceptance.
