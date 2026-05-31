# Decision Records Index

This directory is the durable decision surface for `aoa-agents`.

Use it when a future contributor needs the rationale for a route, topology,
owner split, validator route, workflow boundary, agent-layer source surface,
mechanic package, generated read model, or Codex projection posture.

Ordinary edit summaries, generated output, runtime logs, private evidence,
memory objects, proof verdicts, and one-off planning thoughts route to their
owning surfaces instead.

## Operating Card

| Field | Route |
| --- | --- |
| role | durable decision rationale entrypoint and agent-facing index chooser |
| entry | use when a structural, topology, validation, public-contract, source/generated, role-boundary, mechanic, or projection change needs recoverable rationale |
| input | changed source surface, owner boundary, rejected option, validator guard, or cross-surface route pressure |
| output | canonical decision note, metadata-backed lookup index, and route back to the source surface |
| owner | `docs/decisions/AGENTS.md` for lane law; canonical decision notes for rationale; generated indexes for lookup only |
| next route | source surface first, then nearest route card, `CHARTER.md`, `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/BOUNDARIES.md`, generated lookup indexes, or the affected agent/mechanic owner |
| validation | `python scripts/generate_decision_indexes.py --check`, `git diff --check`, and the owning validator for the changed surface |

## Authority

Decision notes explain why a route was chosen.

They are weaker than the source surface they describe:

- repository authority stays in `CHARTER.md`;
- role/persona layer identity stays in `README.md`, `DESIGN.md`, and
  `DESIGN.AGENTS.md`;
- owner boundaries stay in `docs/BOUNDARIES.md` and nearest `AGENTS.md` cards;
- source-authored agent object meaning stays in `agents/`;
- mechanic shape stays in `mechanics/`, local route cards, and generated
  mechanic read models;
- generated readers stay derived from their builders;
- memo candidates stay local recall/writeback surfaces, not decision authority;
- sibling repositories keep their stronger truth for skills, techniques, evals,
  routing, memory objects, playbooks, stats, and runtime behavior.

Generated decision indexes are weaker than the decision notes. They exist to
make lookup cheaper for agents, not to carry decision rationale.

## Index Shape

Each decision owns:

- a canonical `Decision ID: AOA-AG-D-####`;
- a full canonical-ID filename, for example `AOA-AG-D-0001-*.md`;
- an `## Index Metadata` block naming original date, surface classes, agent
  facets, mechanic parents, guard families, and posture.

The lookup indexes under [indexes](indexes/README.md) are generated from that
metadata:

- [Decisions by canonical ID and number](indexes/by-number.md)
- [Decisions by date](indexes/by-date.md)
- [Decisions by surface class](indexes/by-surface.md)
- [Decisions by agent facet](indexes/by-agent-facet.md)
- [Decisions by mechanic parent](indexes/by-mechanic.md)
- [Decisions by validation or guard family](indexes/by-guard.md)

Use them in both directions:

- top down: repo route -> role/source surface -> agent facet -> mechanic parent
  -> guard family -> decision rationale;
- bottom up: changed source surface -> local route card or generated read model
  -> validator guard -> decision rationale -> stronger owner surface.

Regenerate the read models after decision metadata changes:

```bash
python scripts/generate_decision_indexes.py
```

Check generated parity before closeout:

```bash
python scripts/generate_decision_indexes.py --check
```

## Addressing

Full canonical-ID decision paths are the active source files:

- `docs/decisions/AOA-AG-D-0001-*.md`
- `docs/decisions/AOA-AG-D-0002-*.md`
- `docs/decisions/AOA-AG-D-####-*.md`

Canonical IDs remain the stable handles. Previous date-prefixed paths are not
live files and are not preserved as a repository lookup layer. Use git history,
PRs, or release notes when old path archaeology is actually needed.

Do not recreate date-named files or generated compatibility maps for retired
paths.

## Naming

Use the full canonical decision ID as the filename prefix:

`AOA-AG-D-0057-short-decision-slug.md`

Prefer short titles that name the route, not the whole debate.

## Template

Start from [TEMPLATE.md](TEMPLATE.md) for new decisions. Keep notes concise, but
include enough context, options, rationale, consequences, index metadata, and
validation for a future agent to avoid repeating the same route question.
