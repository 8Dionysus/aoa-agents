# 2026-05-26: Mechanics Docs Part Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0003
- Original date: 2026-05-26
- Surface classes: mechanic part, generated/readout, docs route
- Agent facets: mechanics atlas
- Mechanic parents: cross-mechanic
- Guard families: part-local artifact, generated/read-model, docs route
- Posture: accepted

## Context

The 2026-05-25 mechanics package skeleton made the operation topology visible
but left mechanics-facing public docs in root `docs/`. That was a useful
holding shape, but it kept active behavior under legacy-style file names and
made each mechanic package depend on a distant docs inventory.

Mature AoA mechanics use active package routes first, then a single
`PROVENANCE.md` bridge into legacy lookup. The agent layer also needs compact
operational maps: role, input, output, owner, next route, tools, and
validation. Leaving active mechanics docs as flat root files worked against
both constraints.

## Decision

Move mechanics-facing public docs from root `docs/` into active part-local
routes under:

```text
mechanics/<mechanic>/parts/<part>/docs/
```

For each mechanic package:

- keep `README.md`, `PARTS.md`, and `parts/` as the active route;
- keep `PROVENANCE.md` as the only active bridge to former path accounting;
- populate `legacy/INDEX.md` with former `docs/*` path to active part route
  mappings;
- populate `legacy/DISTILLATION_LOG.md` with the slice accounting;
- keep `legacy/raw/` empty unless a future migration has real raw receipts to
  preserve.

Do not move schemas, examples, scripts, tests, generated readers, manifests,
quest files, config seeds, or agent source objects in this slice. Those remain
current owner/support/generated districts until a dedicated package-local
contract and validation route exists.

## Consequences

- Active mechanics docs now live near the part that owns their operation.
- Former root doc names become provenance facts, not active surface names.
- `docs/README.md` remains the human docs entrypoint, but it routes to
  part-local mechanics docs for operation surfaces.
- Generated readers and tests must reference the new active paths.
- Future non-doc payload moves should follow the same pattern: active route
  first, `PROVENANCE.md` as the bridge, `legacy/INDEX.md` for old-path lookup,
  and validators updated in the same slice.

## Verification

Verification routes through the focused owner checks and the repository release gate.

The release check should be run after generated files are staged, because it
uses the patch-integrity check to catch unstaged generated drift.
