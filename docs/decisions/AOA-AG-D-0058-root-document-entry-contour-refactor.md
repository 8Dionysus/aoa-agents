# 2026-05-31: Root Document Entry And Contour Refactor

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0058
- Original date: 2026-05-31
- Surface classes: root/topology, docs route, validation guard
- Agent facets: root clarity, mechanics atlas, codex projection, agon formation, assistant civil, stress posture
- Mechanic parents: cross-mechanic, agon, experience, codex-projection, antifragility, boundary-bridge, questbook, runtime-seam, titan
- Guard families: docs route, source topology, generated/read-model, validation guard
- Posture: accepted

## Context

The root documents in `aoa-agents` had started to carry too many direct deep
links, current-surface inventories, validator paths, and shipped-surface lists.
That made `README.md`, `docs/README.md`, and `ROADMAP.md` useful as archives but
weak as entrypoints.

Sibling repositories that already went through root-document refactors use a
clearer split: README introduces, AGENTS routes agents, CHARTER authorizes,
DESIGN preserves shape, ROADMAP points direction, docs maps choose owners, and
separate contour or generated surfaces carry inventories.

The agent-layer version of that pattern must not hide role-layer shipped
surfaces. It must keep formation, projection, stress, quest, Titan, runtime
seam, and generated reader routes discoverable without making root docs a path
warehouse.

## Options Considered

- Keep all shipped deep links in `README.md`, `docs/README.md`, and `ROADMAP.md`.
- Delete the detailed route lists without replacing their discoverability.
- Move shipped surface inventories to a dedicated docs contour while keeping
  root docs short and owner-routed.

## Decision

Use `docs/CURRENT_CONTOUR.md` as the current shipped-surface route map for
`aoa-agents`.

Keep root surfaces role-bound:

- `README.md` is the public front door.
- `AGENTS.md` is operational route law.
- `CHARTER.md` is repository authority boundary.
- `DESIGN.md` is system form.
- `ROADMAP.md` is direction and horizon posture.
- `docs/README.md` is the docs/source-of-truth chooser.
- `docs/BOUNDARIES.md` is the owner-boundary map.

Update tests and validation so they check that detailed shipped paths are
discoverable through `docs/CURRENT_CONTOUR.md`, rather than requiring
`README.md` or `ROADMAP.md` to carry the full inventory.

## Rationale

The refactor follows the same source-of-truth layout used by the recently
cleaned sibling repositories while preserving the local `aoa-agents` truth:
role-bearing source objects and mechanic packages remain the authority, and the
contour doc is only a route map.

This keeps low-context entry cheap for humans and agents. It also prevents
tests from encoding root bloat as a contract.

## Consequences

- Root docs become shorter and clearer, but readers have one more explicit hop
  for detailed shipped surface lists.
- Tests now protect the desired topology: root routes to contour, contour keeps
  detailed paths discoverable, and source/mechanic surfaces retain authority.
- Future shipped-surface additions should update `docs/CURRENT_CONTOUR.md` only
  when the addition changes discoverability across root/docs entry.
- Local package READMEs, generated readers, and route cards remain the stronger
  homes for package-local detail.

## Source Surfaces

- `README.md`
- `AGENTS.md`
- `CHARTER.md`
- `ROADMAP.md`
- `docs/README.md`
- `docs/BOUNDARIES.md`
- `docs/CURRENT_CONTOUR.md`
- `scripts/validate_agents.py`
- `tests/test_roadmap_surface_alignment.py`
- `tests/test_agon_formation_route_surfaces.py`
- `tests/test_assistant_civil_route_surfaces.py`
- `tests/test_formation_trial_route_surfaces.py`
- `tests/test_published_consumer_feeds.py`
- `mechanics/antifragility/parts/stress-posture/tests/test_stress_posture.py`
- `mechanics/codex-projection/parts/refresh-law/tests/test_codex_subagent_refresh_law.py`

## Follow-Up Route

When a new shipped surface family needs root-level discoverability, update
`docs/CURRENT_CONTOUR.md` and the narrow discoverability test. Do not add the
full inventory back to `README.md` or `ROADMAP.md`.

## Verification

Verification ran through the root `AGENTS.md` route: decision-index check,
semantic and nested AGENTS validation, repo validation, and the root test suite.
Exact executable command blocks belong in `AGENTS.md`, not in this decision
record.
