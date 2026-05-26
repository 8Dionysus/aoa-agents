# 2026-05-26: Root Agent Schema Posture

## Status

Accepted.

## Context

After the mechanic-specific schema localizations, the remaining root schemas
were:

```text
schemas/agent-profile.schema.json
schemas/agent-registry.schema.json
schemas/model-tier.schema.json
schemas/model-tier-registry.schema.json
schemas/orchestrator-class.schema.json
schemas/cohort-pattern.schema.json
schemas/cohort-composition-registry.schema.json
schemas/runtime-seam-binding.schema.json
schemas/runtime-seam-bindings.schema.json
```

Sibling source comparison shows that root schema districts remain active when
they constrain repo-wide source families and generated readers, while
mechanic-specific schemas move under the owning mechanic part.

In `aoa-agents`, these remaining schemas constrain `agents/` source objects and
root generated registries. They are not mechanic payloads.

## Decision

Keep the remaining root schemas under `schemas/`.

Add `schemas/README.md` as the root schema district index, update
`schemas/AGENTS.md`, and clarify the `agents/` route card plus mechanics
topology notes so future moves distinguish repo-wide agent contracts from
mechanic-local contracts.

Do not create legacy old-path accounting because no path moved.

## Consequences

Source object edits still start under the owning `agents/<family>/` directory,
but schema shape changes route through root `schemas/` when the contract is
shared across agent source families, generated registries, tests, and public
consumers.

Mechanic-specific schemas remain part-local once the owning mechanic part has
route cards and validators. Mechanics should not absorb root agent schemas only
because their names include role, tier, class, cohort, or runtime-seam language.

## Validation

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/release_check.py
```
