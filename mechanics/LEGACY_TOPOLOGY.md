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

Most current `aoa-agents` mechanic payloads still live in root districts:
`docs/`, `schemas/`, `examples/`, `agents/`, `config/`, `generated/`,
`manifests/`, `quests/`, `scripts/`, and `tests/`.

Those root payloads are not automatically legacy. They remain current
source/support/generated districts until a package-local move changes their
lookup topology.

For this slice:

- each mechanic package gets a `parts/` lower route;
- each mechanic package gets a `PROVENANCE.md` bridge;
- each mechanic package gets a `legacy/` scaffold;
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
