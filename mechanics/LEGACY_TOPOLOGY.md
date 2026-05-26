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

The 2026-05-26 Questbook source-store repair restored root `QUESTBOOK.md`,
root `quests/`, and root quest generated readers as active source/read-model
districts. Former flat quest source paths are now lane/state lookup facts and
are accounted for in questbook `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`.

The 2026-05-26 Titan example localization moved schema-backed Titan examples
into active part-local Titan `examples/` routes. Former root Titan example
paths are now legacy lookup facts and are accounted for in Titan
`PROVENANCE.md`, `legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.

The 2026-05-26 Titan schema localization moved Titan-specific schemas into
active part-local Titan `schemas/` routes. Former root Titan schema paths are
now legacy lookup facts and are accounted for in Titan `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`. Stable schema `$id`
values remain public contract identifiers, not active repo paths.

The 2026-05-26 antifragility stress localization moved stress-posture schemas
and examples into active part-local antifragility routes. Former root stress
schema and example paths are now legacy lookup facts and are accounted for in
antifragility `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`. Stable schema `$id` values remain public contract
identifiers, not active repo paths.

The 2026-05-26 RPG progression localization moved the adjunct progression
schema and example into active part-local RPG routes. Former root progression
schema and example paths are now legacy lookup facts and are accounted for in
RPG `PROVENANCE.md`, `legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.
Stable schema `$id` values remain public contract identifiers, not active repo
paths.

The 2026-05-26 assistant projection resolver localization moved assistant
projection resolver schemas and example into active part-local Codex projection
routes. Former root projection schema and example paths are now legacy lookup
facts and are accounted for in Codex projection `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`. Stable schema `$id` values
remain public contract identifiers, not active repo paths.

The 2026-05-26 runtime artifact contract localization moved runtime artifact
schemas, examples, and invalid fixtures into active part-local runtime-seam
routes. Former root runtime artifact schema and example paths are now legacy
lookup facts and are accounted for in Runtime Seam `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`. Stable schema `$id` values
remain public contract identifiers, not active repo paths.

The 2026-05-26 checkpoint contract localization moved self-agent checkpoint
and continuity-window schemas/examples into active part-local checkpoint
routes. Former root checkpoint schema and example paths are now legacy lookup
facts and are accounted for in Checkpoint `PROVENANCE.md`, `legacy/INDEX.md`,
and `legacy/DISTILLATION_LOG.md`. Stable schema `$id` values remain public
contract identifiers, not active repo paths.

The 2026-05-26 recursor contract localization moved recurrence recursor
schemas/examples into active part-local recurrence routes. Former root
recursor schema and example paths are now legacy lookup facts and are
accounted for in Recurrence `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`. Stable schema `$id` values remain public
contract identifiers, not active repo paths.

The 2026-05-26 Agon rank/epistemic contract localization moved rank,
jurisdiction, school/campaign, and epistemic actor schemas/examples into
active part-local Agon routes. Former root Agon rank/epistemic schema and
example paths are now legacy lookup facts and are accounted for in Agon
`PROVENANCE.md`, `legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.

The 2026-05-26 Agon formation contract localization moved Wave I agonic
formation and Wave II.5 formation-trial schemas/examples into active
part-local Agon routes. Former root Agon formation schema and example paths
are now legacy lookup facts and are accounted for in Agon `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`. Stable schema `$id`
values remain public contract identifiers, not active repo paths.

The 2026-05-26 Experience assistant civil contract localization moved Wave II
assistant civil schemas/examples into active part-local Experience routes.
Former root assistant civil schema and example paths are now legacy lookup
facts and are accounted for in Experience `PROVENANCE.md`, `legacy/INDEX.md`,
and `legacy/DISTILLATION_LOG.md`. Stable schema `$id` values remain public
contract identifiers, not active repo paths.

The 2026-05-26 Codex refresh-law example localization moved the Codex subagent
projection refresh-law example into the active part-local Codex projection
route. The former root example path is now a legacy lookup fact and is
accounted for in Codex Projection `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`.

The 2026-05-26 adoption/boundary contract localization moved adoption,
retention, office, and boundary bridge schemas/examples into active
part-local Experience, Agon, and Boundary Bridge routes. Former root schema
and example paths are now legacy lookup facts and are accounted for in the
target package `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`. Stable schema `$id`, `kind`, and
`schema_id`/`schema_version` values remain public contract identifiers, not
active repo paths.

The 2026-05-26 agent service contract localization moved assistant service,
office, release, watch, rollback, governance, runtime-readable
authority-claim, and release-hold schemas/examples into active part-local
Experience, Runtime Seam, and Release Support routes. Former root schema and
example paths are now legacy lookup facts and are accounted for in the target
package `PROVENANCE.md`, `legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.
Stable schema `$id`, `kind`, and identifier values remain public contract
identifiers, not active repo paths.

The 2026-05-26 reference-route contract localization moved reference-route and
Alpha reference-route schemas/examples into active part-local Checkpoint and
Questbook routes. Former root schema and example paths are now legacy lookup
facts and are accounted for in the target package `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`. Stable schema `$id` and
manifest `route_id` values remain public contract identifiers, not active repo
paths.

The 2026-05-26 Alpha reference-route generated reader localization moved the
derived Alpha reader into the active Questbook part-local `generated/` route.
The former root generated path is now a legacy lookup fact and is accounted for
in Questbook `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`.

The 2026-05-26 Agon rank/school/epistemic generated reader localization moved
candidate-only generated registries into active Agon part-local `generated/`
routes. Former root generated paths are now legacy lookup facts and are
accounted for in Agon `PROVENANCE.md`, `legacy/INDEX.md`, and
`legacy/DISTILLATION_LOG.md`.

The 2026-05-26 recursor generated reader localization moved Recurrence
readiness, pair, projection-candidate, and Agon boundary readers into active
Recurrence part-local `generated/` routes. Former root generated paths are now
legacy lookup facts and are accounted for in Recurrence `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.

Quest catalog and dispatch readers remain active root generated surfaces; they
are not legacy paths in this topology.

Other mechanic-adjacent payload classes still live in their owner districts:
remaining shared non-Titan, non-runtime-artifact, non-checkpoint,
non-Agon-rank/epistemic, non-Agon-formation, and
non-Experience-assistant-civil, non-adoption/boundary, non-agent-service,
non-reference-route
`schemas/`,
remaining non-Titan, non-runtime-artifact, non-checkpoint,
non-Agon-rank/epistemic, non-Agon-formation, and
non-Experience-assistant-civil, non-Codex-refresh-law,
non-adoption/boundary, non-agent-service, non-reference-route `examples/`, `agents/`,
remaining non-Alpha, non-Agon-rank/epistemic, non-recursor, non-Questbook
`generated/`, `scripts/`, and
`tests/`. They are not automatically legacy.
They remain current source, support, generated, or validation districts until
a package-local move changes their lookup topology.

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
