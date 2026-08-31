# 2026-08-30: Compact agent routes and on-demand guides

## Status

Accepted. This decision narrows the prompt-visible guidance posture established
by `AOA-AG-D-0047` and supersedes the requirement in `AOA-AG-D-0058` that
exact executable command blocks live in `AGENTS.md`.

## Index Metadata

- Decision ID: AOA-AG-D-0073
- Original date: 2026-08-30
- Surface classes: root/topology, docs route, AGENTS mesh, validation guard
- Agent facets: root clarity, prompt context, owner routing, human navigation
- Mechanic parents: cross-mechanic
- Guard families: docs route, AGENTS/mesh, validation guard, provenance
- Posture: accepted

## Context

The repository had 66 tracked `AGENTS.md` files and 209 tracked `README.md`
files. The AGENTS inheritance chains stayed below the workspace byte limit, but
46 route cards declared README reading as mandatory and pulled 76,108 bytes of
human-oriented README material into declared agent reading. Thirty-six AGENTS
files also carried executable command blocks, while several district cards
repeated complete schema, example, generated-reader, or package inventories.

The same census found placeholder-only README files: empty future eval lanes,
empty raw-receipt lanes, and child part directories whose only file repeated a
route already owned by `PARTS.md`. Treating every README as disposable would
remove useful public entrypoints, package maps, contract indexes, and schema or
example inventories. Keeping every placeholder would preserve topology that
has no source payload or validator owner.

## Options Considered

- Keep command blocks, inventories, and mandatory README reading in local
  AGENTS cards because the current chains fit the byte limit.
- Move most README content into AGENTS or delete README files by size,
  similarity, or paired-directory shape.
- Keep AGENTS as compact inherited routing and stop-line deltas; keep README as
  human/public explanation and usage; centralize executable validation
  procedure outside the automatic AGENTS chain; remove only placeholders whose
  unique function is already owned elsewhere.

## Decision

Use the following document boundary throughout `aoa-agents`:

- `AGENTS.md` owns the smallest local operational delta: role, input/output or
  route selection, owner boundary, stop-lines, validation route, and closeout.
- AGENTS cards do not contain executable command blocks, general inventories,
  or unconditional `README.md` reading. A README may be named as an on-demand
  route only when human/public explanation, usage, or a changed README surface
  is actually relevant.
- `README.md` remains the human/public directory entry, explanation, usage
  guide, or inspectable artifact index. Root and meaningful package, source,
  schema, example, generated, port, and provenance entrypoints remain.
- `VALIDATION.md` is the on-demand human validation map.
  `scripts/release_check.py` remains the executable repository gate and its
  command registry is stronger than prose copies.
- Source JSON, schemas, manifests, registries, builders, validators, and tests
  keep semantic or machine topology authority. Generated surfaces remain
  derived and are rebuilt from those sources.
- A placeholder README may be deleted only when it is the sole payload of an
  unmaterialized lane, carries no unique human/operator route, and an existing
  owner surface already preserves its route. Empty future lanes are created
  when their first real payload is admitted; empty raw-receipt lanes appear
  only with a real preserved receipt; unmaterialized mechanic parts stay named
  in `PARTS.md` without a placeholder directory.

## Rationale

This split reduces automatic context at the source instead of hiding useful
documentation. Agents receive owner routing and stop-lines through inheritance;
humans retain GitHub-rendered entrypoints and usage maps; executable validation
has one on-demand route and one code-owned full gate. Placeholder removal then
reflects actual source admission rather than a formatting preference.

The rule also makes wrong-owner routing visible. A route-only part points to
the existing owner part, root source, generated reader, or stronger repository
instead of materializing an empty local directory merely to hold a README.

## Consequences

- AGENTS chains become smaller and mandatory README fanout should fall to zero
  unless a future owner records a bounded exception.
- Contributors make one extra explicit hop to `VALIDATION.md` or the relevant
  README when they need commands, inventories, or human usage.
- Existing validators and tests must protect the boundary without freezing
  long prose or requiring placeholder paths.
- Decision records and historical provenance may continue to name removed
  paths as historical facts; active links and generated KAG views must be
  updated or regenerated.
- A later real eval packet, raw receipt, or mechanic payload may materialize a
  directory with its own README or nearer AGENTS card when the owner contract
  justifies it.

## Source Surfaces

- `AGENTS.md`
- `VALIDATION.md`
- `README.md`
- `DESIGN.AGENTS.md`
- `.github/AGENTS.md`
- `agents/**/AGENTS.md`
- `mechanics/**/AGENTS.md`
- `mechanics/**/README.md`
- `mechanics/**/PARTS.md`
- `scripts/release_check.py`
- `scripts/validate_nested_agents.py`
- `scripts/validate_semantic_agents.py`
- `tests/test_root_entrypoint_routes.py`

## Follow-Up Route

Future route-card changes start from the nearest AGENTS owner, but inventories
and usage land in the corresponding README, exact validation lands in
`VALIDATION.md` and executable validators, and machine topology stays in its
manifest, registry, schema, or builder. New empty skeleton directories require
payload admission rather than a placeholder README.

## Verification

Verification routes through the README/AGENTS corpus census, decision-index
parity, link and placeholder checks, semantic and nested AGENTS validators,
focused owner tests, and the repository release gate.
