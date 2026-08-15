### Mode: form-actor

Turn one admitted obligation into a bounded role mandate. Preserve the role's
stable meaning separately from its replaceable model and process body.

## Input

Require one `agent-obligation-v1` plus exact owner refs for the selected base
role, optional specialization, tier, capability pack, and domain procedures.
For a role-first request those refs are produced internally by its bounded
candidate-source phase: the tier must come from the selected base role's
`preferred_tier_ids`, and a specialization's capability pack must be read from
that source's exact authored `capability_pack_ref`. Missing domain procedure
truth is a handoff, not permission for `aoa-agents` to invent it. After the
semantic chain selection, use the bundled passive resolver to prove the
selected base role, specialization, tier, and implied capability pack form one
clean content-addressed owner chain:

```bash
python <bundle_dir>/scripts/resolve_role_binding.py \
  --root <owner_root> \
  --role-id <base-role-id> \
  --specialization-id <optional-specialization-id> \
  --tier-id <tier-id>
```

The resolver does not choose or rank roles. Its `aoa_role_resolution_v1`
output is exact source evidence for the choice already made by this mode.

## Procedure

1. Resolve the smallest existing base role that can bear the obligation. Make
   this semantic choice before invoking the passive exact-ref resolver.
2. Add an existing specialization and capability pack when they narrow the
   mandate. Create neither merely to name the current task.
3. State required executor properties behaviorally: procedure discipline,
   initiative, scope control, handoff quality, tool competence, context span,
   latency, or other testable properties. Do not name a vendor or model.
4. Attach the domain skill or procedure by exact owner ref. It remains owned
   by that domain.
5. Define authority, permissions, effects, stop lines, named outputs, review,
   refusal, escalation, return, and wake posture.
6. Decide continuity posture:
   - `task-instance`: no identity beyond this obligation;
   - `role-continuity`: role identity and accumulated context may survive;
   - `persistent-office`: stable duty and relationships survive while process
     and model instances may disappear and later be restored.
7. Name the broader `aoa-models` task family that should receive the mandate's
   behavioral requirements and explain its relation to the exact duty. This is
   an explicit semantic relation authorized by the current obligation holder,
   not a string-equality heuristic and not a model choice.
8. Bind the mandate to the exact obligation and `aoa_role_resolution_v1`
   digests with the bundled compiler. Return an `actor-mandate-v1`. Do not bind
   a model or start a process.

```bash
python <bundle_dir>/scripts/compile_actor_contract.py mandate \
  --obligation <agent-obligation-v1.json> \
  --role-resolution <aoa-role-resolution-v1.json> \
  --input <semantic-mandate.json>
```

The compiler verifies exact input digests, lifecycle and stop-line
preservation, unique property/output identities, and current-holder authority
for the duty-to-fit-family relation. It makes none of those semantic choices.

## Output

The mandate records obligation and goal refs, actor identity posture, base role,
specialization, tier, capability packs, domain procedure refs, required
executor properties, authority/effects, specialized-environment requirements,
continuity and state roots, named outputs, return owner, review/refusal/wake
rules, expiry/review posture, uncertainty, stop line, and an explicit
duty-to-model-fit-family relation.

For the first landing proof, existing `coder.repo-refactor` with
`repo-refactor.workspace-write` may bear bounded repo-local preparation, while
`evaluator.release-readiness` with `release-readiness.readonly` provides an
independent review. Neither becomes a permanent `landing-agent`, and remote
publication remains with its domain owner.
