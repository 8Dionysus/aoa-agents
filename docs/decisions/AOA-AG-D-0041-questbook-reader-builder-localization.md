# 2026-05-26: Questbook Reader Builder Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0041
- Original date: 2026-05-26
- Surface classes: mechanic part, generated/readout
- Agent facets: mechanics atlas, quest/alpha
- Mechanic parents: questbook
- Guard families: part-local artifact, generated/read-model, quest dispatch
- Posture: accepted

## Context

The Questbook source-store repair correctly kept root `QUESTBOOK.md`, root
`quests/`, and root `generated/quest_*` readers outside the mechanic package.
One support script still lived in root `scripts/`:
`scripts/generate_questbook_readers.py`.

That script builds only the Questbook catalog and dispatch readers. In
`Agents-of-Abyss`, Questbook-specific builders live in
`mechanics/questbook/scripts/`; in `aoa-memo`, the pure quest projection
builder lives directly under the Questbook read-model part. `aoa-evals` keeps
its root catalog builder because it builds the whole eval catalog bundle, not
only Questbook readers.

## Decision

Move the dedicated Questbook catalog/dispatch builder to:

```text
mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py
```

Keep `generated/quest_catalog*.json` and `generated/quest_dispatch*.json`
root-published because their source truth remains root `quests/`.

Teach `scripts/validate_agents.py` that the former root builder path must stay
absent.

## Consequences

The support tool now sits beside the part whose projection contract it protects.
Root `scripts/` keeps repo-wide builders and validators; Questbook-specific
reader regeneration routes through the `dispatch-reader` part.

`generated/README.md` is a route/index doc, not generated data. The release
drift check excludes it together with `generated/AGENTS.md` while continuing to
check generated JSON output drift.

This follows the agent-instruction shape used by the external sources: clear
role, input, output, owner, tool, and validation routes instead of broad
negative prose or topic buckets.

## Validation

Verification routes through the focused owner checks and the repository release gate.
