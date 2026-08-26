# Goal Participant Relations Contract

## Purpose

The participant relation is the smallest `aoa-agents` owner surface that can
publish an exact assignment relation for a Goal/thread consumer. It is a
publisher-owned relation record, not a claim that a process is alive or that a
Goal has been accepted.

The relation scope has three separate exact endpoints:

- `goal_ref` — the owner-published Goal object;
- `goal_instance_ref` — the concrete Goal/session instance;
- `master_thread_ref` — the exact master thread.

A bare Goal identifier, a dashboard anchor, or a thread title cannot replace
these references.

## Independent dimensions

Each record carries five independent dimensions:

1. `identity` — an exact actor reference. A display reference, when allowed,
   is separate and is not a join key.
2. `obligation_role` — exact role and obligation references from the agent
   layer.
3. `task_assignment` — exact Goal/thread/task/assignment references from the
   app-server or SDK owner.
4. `model_realization` — exact model identity and realization references from
   `aoa-models`.
5. `runtime_incarnation` — exact runtime binding and incarnation references
   from `abyss-stack`.

The state of each dimension is one of `present`, `missing`, `unknown`, `stale`,
`deferred`, or `invalid`. A non-present state is preserved as-is. It cannot be
turned into an actor name, `Participant N`, `Working agent`, `Master`, a model
label, or an evidence-available flag.

## Admission and join law

Every admitted reference contains the owner repository, object identifier,
source reference, schema version, and content digest. A relation is admitted
only when the publisher supplies an opaque `relation_key` with its own exact
publisher reference and endpoint references. Consumers compare that key; they
do not recreate it from a name, role label, model slug, PID, working directory,
path, version, process ancestry, or bare Goal id.

The `relation_key.endpoint_refs` list makes the scope and present dimension
endpoints inspectable without making endpoint equality the consumer join rule.
Conflicting or malformed references are `invalid`; absent evidence remains
`missing`, `unknown`, or `deferred` according to the owner response.

## Typed publication and admission

The reusable producer input is
`aoa_agents_goal_participant_relation_publication_v1`. It is an explicit
owner-published envelope, not a discovery query. It must carry:

- the current `aoa-agents` contract ref, a distinct producer ref, and a
  producer-owned publication ref;
- exactly one `scope` containing `goal_ref`, `goal_instance_ref`, and
  `master_thread_ref` with full owner/schema/digest provenance;
- `currentness.state=current` with `observed_at`, no unadmitted pagination
  continuation, the exact privacy omission set, and a digest of canonical
  relation records;
- one or more `owner_published` relation records. Each record preserves its
  independent dimension states and has a publisher-owned relation-key digest.

`admit_goal_participant_publication.py` emits an
`aoa_agents_goal_participant_relation_admission_v1` receipt only after these
checks pass. The receipt proves local structural admission and binds the
producer ref, publication ref, payload digest, exact scope, relation IDs,
currentness, pagination, privacy omissions, and claim limit. It does not
verify the upstream contents behind external digests and does not establish
liveness, acceptance, or completion.
This admission receipt is not a participant, runtime, or Goal-acceptance
receipt.

The generated reader re-computes the receipt identity, requires that receipt
for every non-empty owner-published graph, binds it to the exact graph scope,
records, currentness, pagination, and privacy policy, and re-checks the
current contract/source references and their content digests before returning
the projection.

An admitted receipt can be handed to the explicit source publisher to replace
`empty_deferred`. Until the app-server/session, aoa-sdk, aoa-models,
abyss-stack, and aoa-agents owners provide the required exact records, the
checked-in source remains empty and deferred. No title, path, terminal,
version, model label, holder suffix, or single Goal read is a valid substitute.

## Currentness, pagination, and privacy

The source feed carries currentness separately from every participant
dimension. A feed with `has_more: true` and an exact next cursor remains
`deferred` until the continuation is admitted. A stale source does not become
current because a generated reader exists.

The source and generated surfaces preserve privacy omissions explicitly. The
baseline omits human display names, raw prompts, secrets, working directories,
paths, PIDs, terminal titles, and unreviewed model metadata. An omitted display
name is not an invalid participant and never triggers a substitute label.

## Owner split and claim limit

`aoa-agents` owns this contract, relation-key publication, role/obligation
references, and the derived reader. The app-server/session owners keep Goal,
Goal-instance, and master-thread truth; `aoa-models` keeps model truth; and
`abyss-stack` keeps runtime truth. Dashboard, session-memory, SDK, or runtime
consumers may compose these references only through this explicit seam.

The checked-in source feed is intentionally empty with deferred currentness.
It is not evidence that the target Goal has no participant; it records that no
exact owner-published relation was admitted into this source surface at this
capture. This part therefore makes no live presence, activation, liveness,
wake, return, acceptance, or completion claim.
