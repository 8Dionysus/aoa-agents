# Mechanics Provenance Topology

This note keeps the active-to-archive route small.

## Pattern From Mature Repositories

The established mechanics pattern is:

- active behavior lives in `README.md`, `AGENTS.md`, `PARTS.md`, and `parts/`;
- `PROVENANCE.md` is the active bridge for former-path and source-accounting
  lookup;
- archive-local indexes preserve old path maps and distillation receipts;
- raw receipts are preserved only when they are real source evidence;
- empty archive inventories are better than invented receipts.

Archive accounting is entered only after the active route has identified the
owning package or part.

## Local Rule For aoa-agents

When a payload moves from a root district into a mechanic package, the active
route changes to the owning package, part, builder, and validator. Former-path
lookup belongs in the package `PROVENANCE.md` bridge and its archive-local
indexes.

The current moved payload families include:

- mechanics-facing public docs moved into part-local `docs/`;
- mechanic-specific config moved into part-local `config/`;
- recurrence component manifests moved into the component-manifest part;
- Questbook source-store topology was repaired back to root `QUESTBOOK.md`,
  root `quests/`, and root quest generated readers;
- Titan examples and schemas moved into Titan parts;
- antifragility stress contracts moved into antifragility parts;
- RPG progression contracts moved into RPG parts;
- assistant projection resolver contracts moved into Codex projection parts;
- runtime artifact contracts moved into runtime-seam parts;
- checkpoint contracts moved into checkpoint parts;
- recursor contracts and generated readers moved into recurrence parts;
- Agon rank, school, epistemic, and formation contracts moved into Agon parts;
- assistant civil and service contracts moved into Experience, Runtime Seam,
  and Release Support parts;
- reference-route contracts moved into Checkpoint and Questbook parts;
- Alpha reference-route, Agon rank/school/epistemic, and recursor generated
  readers moved into their part-local generated routes.

Quest catalog and dispatch readers remain active root generated surfaces. They
summarize root quest records and are not archive paths.

Other mechanic-adjacent payload classes still live in their owner districts:
shared schemas, shared examples, source agent objects, root-published generated
readers, scripts, tests, and repo-level docs. They remain current source,
support, generated, or validation districts until a package-local move changes
their lookup topology.

## Current Landing Standard

Each mechanic package should have:

- an active package `AGENTS.md`;
- a package `PARTS.md`;
- active part cards under `parts/`;
- one package `PROVENANCE.md` bridge for former-path lookup;
- archive-local indexes for moved payloads;
- validators, builders, or tests that know the active route.

No payload should move only because its filename matches a mechanic.

## When Payloads Move Later

When a later slice moves a payload into a mechanic package, update:

- parent package `PARTS.md`;
- target part README and any child part route;
- package `PROVENANCE.md`;
- archive-local path and distillation indexes when old lookup is needed;
- validators, builders, and tests that know the old path.

If the old path must remain for compatibility, keep a thin compatibility route
instead of duplicating authority.
