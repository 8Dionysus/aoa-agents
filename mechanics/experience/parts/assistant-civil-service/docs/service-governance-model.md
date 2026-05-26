# Assistant Service Governance Model

## Purpose

Governance prevents assistant drift.

The assistant does not become better by secretly rewriting itself.
It becomes better through external review, certification, and versioned reissue.

## Revision authority

Assistant persistent policy is externally governed.

The default authority is:

```text
revision_authority: operator_review
self_revision_allowed: false
persistent_policy_change_allowed: false
```

The assistant may propose a patch.
It may not install its own new constitution.

## Memory posture

The assistant may name receipt expectations and incident categories.

It must not store durable memory ledgers in `aoa-agents`.

Durable incident logs, revision ledgers, retention checks, and operational memory objects belong outside this repository.

## Rollback

Every assistant upgrade must remain rollback-aware.

A service actor that cannot be rolled back is already drifting toward opaque agency.

## Release governance

Assistant change is release-governed:

```text
proposal -> review -> certification -> versioned release -> rollback path
```

No shadow evolution.
