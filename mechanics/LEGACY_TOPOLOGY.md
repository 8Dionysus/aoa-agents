# Mechanics Legacy Topology

`legacy/` in a mechanic package is a provenance district. It is not the normal
first route for current behavior, and it is not a trash archive.

## Pattern From Mature Repositories

The established mechanics pattern is:

- active behavior lives in `README.md`, `PARTS.md`, and `parts/`;
- `PROVENANCE.md` is the active bridge into legacy;
- `legacy/README.md` explains archive-local use;
- `legacy/INDEX.md` maps old source or receipt paths to current active routes;
- `legacy/DISTILLATION_LOG.md` records source-to-active accounting;
- `legacy/raw/` preserves real raw receipts when they exist;
- an empty `legacy/raw/README.md` is better than placeholder receipts.

Legacy is entered only after the active route has identified the owning package
or part.

## Local Rule For aoa-agents

The 2026-05-26 docs landing moved mechanics-facing public docs from root
`docs/` into active part-local docs under `mechanics/*/parts/*/docs/`.

Former root doc paths are now legacy lookup facts, not active names. They are
accounted for in the target package `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`. Raw legacy files are not invented; git history
preserves the moved file bodies.

The 2026-05-26 config localization moved mechanic-specific source seed and
wiring payloads from root `config/` into active part-local config under
`mechanics/*/parts/*/config/`. Former root config paths are now legacy lookup
facts and are accounted for in the target package `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.

The 2026-05-26 manifest localization moved recurrence component and hook
manifests from root `manifests/` into active part-local manifests under
`mechanics/recurrence/parts/component-manifests/manifests/`. Former root
manifest paths are now legacy lookup facts and are accounted for in recurrence
`PROVENANCE.md`, `legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.

The 2026-05-26 questbook localization moved the root quest catalog doc and
quest source files into active part-local questbook routes. Former root
questbook and quest-source paths are now legacy lookup facts and are accounted
for in questbook `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`.

Other mechanic-adjacent payload classes still live in their owner districts:
`schemas/`, `examples/`, `agents/`, `generated/`, `scripts/`, and `tests/`.
They are not automatically legacy. They remain current source, support,
generated, or validation districts until a package-local move changes their
lookup topology.

For this landing:

- each mechanic package has a `parts/` lower route;
- each mechanic package has one active `PROVENANCE.md` bridge;
- each mechanic package has populated legacy lookup and distillation maps for
  moved payloads;
- no raw legacy receipts are invented;
- no payload is moved just because a filename matches a mechanic.

## When Payloads Move Later

When a later slice moves a payload into a mechanic package, update:

- parent package `PARTS.md`;
- target `parts/README.md` and any child part route;
- package `PROVENANCE.md`;
- `legacy/INDEX.md` when an old path needs lookup accounting;
- `legacy/DISTILLATION_LOG.md` for the move;
- validators/builders/tests that know the old path.

If the old path must remain for compatibility, keep a thin compatibility route
instead of duplicating authority.
