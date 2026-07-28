# SDK Routing Consumer Succession

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0060
- Original date: 2026-07-27
- Surface classes: sibling-owner boundary, federation consumer seam, validator
- Agent facets: model tier, memo posture, runtime seam
- Mechanic parents: boundary-bridge, recurrence, runtime-seam
- Guard families: owner succession, canonical producer admission, compatibility ABI, consumer-zero
- Posture: accepted

## Context

`aoa-sdk` became the canonical routing producer while retaining `aoa-routing`
as the compatibility namespace, ABI, and runtime layer name. `aoa-agents`
still treated the predecessor repository as the routing owner and optionally
read generated routing surfaces directly from `AOA_ROUTING_ROOT`.

That shape made a predecessor checkout operationally relevant after producer
authority had moved. A path-only smoke check also could not distinguish an
SDK-canonical bundle from an unadmitted copy of the same stable ABI.

## Options Considered

- Keep the predecessor checkout as the optional smoke-check root.
- Read generated files from the `aoa-sdk` source checkout.
- Read an SDK-produced canonical bundle or runtime mirror after fail-closed
  producer, receipt, ABI, and digest admission.

## Decision

Route current navigation, dispatch, and routing-policy ownership to the
`aoa-sdk` routing control plane. Preserve `aoa-routing` as the stable
compatibility namespace, artifact ABI, and runtime layer name.

The optional routing consumer check uses `AOA_SDK_ROUTING_BUNDLE_ROOT`. Before
reading tier or memo entrypoints, it must admit either an SDK canonical bundle
or an SDK-canonical runtime mirror and verify:

- `aoa-sdk` is the canonical producer;
- the G5 owner-switch receipt and SDK routing ABI are exact;
- the receipt digest matches its admitted summary;
- every declared file digest resolves inside and matches the bundle.

Historical decisions, stable artifact identifiers, and predecessor rollback
provenance remain unchanged. Removing the predecessor checkout dependency is
not archive authorization.

## Rationale

This preserves one routing producer without moving routing meaning into
`aoa-agents`. It also keeps the stable consumer ABI independent of repository
layout while making producer identity and artifact integrity explicit.

## Consequences

- `aoa-agents` no longer requires `AOA_ROUTING_ROOT` or an `aoa-routing`
  checkout for current validation.
- Model-tier and memo-recall compatibility checks continue against the same
  stable generated artifact names.
- Synthetic tests must carry SDK canonical admission metadata rather than only
  place JSON files under a directory named after the predecessor.
- Portable role-registry proof may accept the exact fail-closed
  `required_artifact_subject_store_not_verified` verdict before local
  materialization, but must still require a full allow after materialization;
  ambient host subject-store contents are not a test precondition.
- Archive, rollback retirement, and compatibility-window exit remain separate
  operator decisions.

## Source Surfaces

- `scripts/validate_agents.py`
- `scripts/validate_abyss_machine_role_registry_bundle.py`
- `tests/test_repo_validator.py`
- `tests/test_published_consumer_feeds.py`
- `mechanics/boundary-bridge/parts/federation-consumer-seams/docs/federation-consumer-seams.md`
- `mechanics/runtime-seam/parts/role-tier-bindings/docs/agent-runtime-seam.md`
- `docs/BOUNDARIES.md`

## Follow-Up Route

Consumer-zero and compatibility-exit evidence route to the `aoa-sdk` routing
succession owner surface. Runtime mirror lifecycle stays with `abyss-stack`.

## Verification

Verification routes through the focused owner checks, the live SDK-canonical
runtime mirror smoke check, and the repository release gate.
