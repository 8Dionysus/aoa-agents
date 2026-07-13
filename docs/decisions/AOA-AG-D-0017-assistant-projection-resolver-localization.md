# 2026-05-26: Assistant Projection Resolver Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0017
- Original date: 2026-05-26
- Surface classes: mechanic part
- Agent facets: mechanics atlas, assistant civil, codex projection
- Mechanic parents: experience, codex-projection
- Guard families: part-local artifact, projection guard
- Posture: accepted

## Context

The Codex projection mechanic already has an `assistant-projection` part, but
the assistant projection resolver schemas and public example still lived in
root `schemas/` and `examples/`.

Those payloads describe a Codex-facing assistant projection contract and
no-self-rewrite posture. They are not shared profile schemas and not generated
Codex agents. The active owner is the `assistant-projection` part.

## Decision

Move the assistant projection resolver schemas and example into
`mechanics/codex-projection/parts/assistant-projection/{schemas,examples}/`
using part-local names. Keep stable schema `$id` values unchanged because they
are public contract identifiers, not active repository path authority.

Add a validator and wire it into `scripts/validate_agents.py` so the active
file set, schema validity, example validation, doc references, and old-route
absence are checked explicitly. A later check-localization slice moved that
validator into `mechanics/codex-projection/parts/assistant-projection/scripts/`
and moved the focused resolver test beside the part.

Preserve former root lookup only through Codex projection `PROVENANCE.md` and
`legacy/`.

## Consequences

- The `assistant-projection` part now owns the resolver schemas, example,
  validator, and focused tests.
- Root `schemas/` and `examples/` remain active for shared or not-yet-localized
  contracts.
- Existing schema `$id` values remain stable for consumers.
- Old root assistant projection names remain historical lookup facts only.

## Verification

Verification routes through the focused owner checks and the repository release gate.
