# 2026-05-31: Canonical Decision IDs And Indexes

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0057
- Original date: 2026-05-31
- Surface classes: decision record, generated/readout, validation guard
- Agent facets: decision index
- Mechanic parents: cross-mechanic
- Guard families: decision index/read-model, docs route, release/tooling
- Posture: accepted

## Context

`aoa-agents` already used `docs/decisions/` as the durable route-law and
topology rationale surface, but records were addressed by date-prefixed
filenames and collected in a hand-maintained README list.

That worked while the set was small. It became weaker after the role layer grew
mechanic packages, Codex projection boundaries, specialization eligibility
records, generated readiness readers, and many local memo candidates that cite
decision refs. Future agents need stable handles and generated lookup paths that
can answer: which decision explains this role surface, mechanic parent, guard,
or projection boundary?

Sibling repositories now use canonical decision IDs and metadata-backed indexes,
but `aoa-agents` must adapt the pattern to the role/persona layer instead of
importing skill, eval, memo, or technique authority.

## Options Considered

- Keep date-prefixed filenames and continue maintaining the README by hand.
- Add generated indexes while preserving date-prefixed source filenames.
- Rename records to canonical `AOA-AG-D-####` IDs and generate lookup indexes
  from explicit metadata.

## Decision

Use canonical `AOA-AG-D-####` decision IDs and full canonical-ID filenames as
the active decision record addresses.

Each decision record owns an `## Index Metadata` block naming original date,
surface classes, agent facets, mechanic parents, guard families, and posture.
Generated indexes under `docs/decisions/indexes/` are read models derived from
that metadata.

The agent-layer facet index uses role-local categories such as source home, role
specialization, Codex projection, Titan role-bearing, assistant civil,
checkpoint/self-agent, recurrence, progression/cohort, quest/Alpha, stress
posture, mechanics atlas, and decision index. These labels make `aoa-agents`
decision lookup useful without turning the repo into the owner of skills,
proof, memory, routing, or runtime behavior.

Previous date-prefixed paths are retired as live files. They remain available
through git and PR history only.

## Rationale

Stable decision IDs make cross-surface references durable when files move or
when many decisions share the same date. Metadata-backed read models keep lookup
cheap for future agents while preserving decision notes as the only rationale
authority.

The generated indexes are deliberately weaker than both the decision notes and
the source surfaces they describe. They summarize route evidence; they do not
create agent behavior, Codex projection authority, memory truth, proof verdicts,
or runtime state.

## Consequences

- Decision records are now addressed as `docs/decisions/AOA-AG-D-####-*.md`.
- Generated indexes support lookup by number, date, source surface class, agent
  facet, mechanic parent, and guard family.
- `scripts/generate_decision_indexes.py --check` becomes part of release
  validation.
- Live refs inside specialization eligibility records and local memo candidates
  point at canonical decision paths.
- Old date-prefixed decision paths should not be recreated as compatibility
  aliases or lookup maps.

## Source Surfaces

- `docs/decisions/`
- `docs/decisions/indexes/`
- `scripts/decision_indexes.py`
- `scripts/generate_decision_indexes.py`
- `tests/test_decision_indexes.py`
- `scripts/release_check.py`

## Follow-Up Route

For future decision records, start from `docs/decisions/TEMPLATE.md`, choose the
next contiguous `AOA-AG-D-####` ID, regenerate indexes, and run the decision
index check before closeout.

## Verification

```bash
python scripts/generate_decision_indexes.py --check
python -m unittest tests.test_decision_indexes
python scripts/release_check.py
```
