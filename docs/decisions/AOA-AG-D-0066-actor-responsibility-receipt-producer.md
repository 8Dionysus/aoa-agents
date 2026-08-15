# Add Owner-Local Actor Responsibility Receipt Producer

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0066
- Original date: 2026-08-14
- Surface classes: owner skill home, receipt payload, explicit publisher
- Agent facets: role contract, incarnation, responsibility return
- Mechanic parents: cross-mechanic, boundary-bridge
- Guard families: owner boundary, evidence identity, idempotent publication
- Posture: admitted passive observation route

## Context

The role-first external lane already returns an evidence-complete
`summon-result-v4`, and `aoa-stats` admits a distinct
`actor_responsibility_execution_receipt` event kind. The owner still lacked a
small producer that could turn one exact result and explicit observation
coordinates into that envelope without making stats, runtime, review, or
acceptance decisions.

## Options Considered

- Reuse a runtime, eval, or generic skill receipt and lose responsibility
  meaning.
- Add the payload or live source to `aoa-stats` and absorb stronger-owner
  authority.
- Compile an aoa-agents-owned strict payload and make publication a separate,
  validated, idempotent action.

## Decision

Add `actor-responsibility-execution-receipt.schema.json` and
`compile_actor_responsibility_receipt.py` under `skills/aoa-summon`. The
compiler accepts only a schema-valid external-lane `summon-result-v4`, keeps
the exact result-byte digest and stronger-owner references, requires an
explicit canonical ref for the exact result artifact plus observation
coordinates and the canonical receipt payload projection, and derives a
stable event ID from those exact inputs. The request ref remains a separate
field. Digest and event-ID assertions fail closed, so schema-valid payload
edits cannot retain a prior event ID.

Add `publish_actor_responsibility_receipts.py` as an explicit second action.
It validates inputs and all existing log lines before append, skips duplicate
event IDs, supports a test-local path, and defaults to the owner-local
`.aoa/live_receipts/actor-responsibility-execution-receipts.jsonl` path. The
default owner root resolves through the complete same-bundle source handle or
an explicit `--owner-root`; v2 handles must carry the bundle version and all
install-provenance identity dimensions before they can select an owner root.
Compilation does not publish. It acquires a POSIX
advisory exclusive lock at
`<log-path>.lock` before reading existing IDs and holds that lock through the
append, making the read/deduplicate/append sequence safe for independent
publisher processes that share the same path. A host without advisory-lock
support fails closed. Envelope validation also binds the emitted
`evidence_refs` to the payload's owner evidence, rejects symlink paths before
resolution, and preserves a JSONL line boundary when appending to a valid
unterminated file.

The compiler projects only the canonical `parent_owner`, `residual_risk`, and
`next_route` closeout fields into the strict receipt payload. Additional
closeout fields allowed by the summon-result source contract remain source
evidence and cannot widen the receipt schema.

The producer also follows the canonical execution-state reference contract:
returned and accepted results require runtime-result, reviewed A2A-return, and
usage refs; failed results require runtime-result and usage refs; launched and
running results carry no return refs yet. Optional null refs are not promoted
into the owner payload.

## Rationale

This is the smallest coherent topology that makes one owner-qualified actor
responsibility execution observable while keeping the payload with
`aoa-agents`. Exact refs remain evidence, not copied protocol authority, and
the publisher does not turn a workspace or feed entry into owner acceptance.

## Consequences

- The event can be counted by the already admitted generic stats surfaces.
- A missing feed entry remains unobserved, not zero execution.
- Benefit, model fit, task success, proof, review approval, and owner
  acceptance remain unknown unless separate owner evidence says otherwise.
- Live-feed append is explicit and remains outside compilation and this
  implementation task.
- The `.lock` sibling is owner-local runtime coordination, not receipt source
  data; callers must use this publisher contract when sharing a feed path.

## Source Surfaces

- `skills/aoa-summon/references/actor-responsibility-execution-receipt.schema.json`
- `skills/aoa-summon/scripts/compile_actor_responsibility_receipt.py`
- `skills/aoa-summon/scripts/publish_actor_responsibility_receipts.py`
- `skills/aoa-summon/SKILL.md`
- `skills/aoa-summon/references/lane-and-return.md`
- `tests/test_compile_actor_responsibility_receipt.py`
- `tests/test_publish_actor_responsibility_receipts.py`

## Follow-Up Route

Independent review must inspect this diff and validation evidence. A later
owner may activate the `aoa-stats` source only through its own source-owner
and live-observation route; this decision does not register a watcher or
activate a feed.

## Verification

Verification routes through focused compiler/publisher tests, summon-v4
generated-current checks, decision-index parity, semantic agent validation,
and the repository release gate.
