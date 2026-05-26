# 2026-05-26: Provenance Bridge Operating Shape

## Status

Accepted.

## Context

The mechanics refactor already uses package-local `PROVENANCE.md` files as the
single active bridge into former-path accounting. After the active wording
cleanup, those bridge files still varied from the stronger `Agents-of-Abyss`
shape: they listed moved payloads, but did not consistently tell future agents
to start from current routes, avoid dragging archive inventories into active
cards, and update active parts before archive maps.

The user's `quests/` correction reinforced the same route law: source districts
and operation packages must stay distinct. A bridge can preserve accounting
without becoming the operating surface.

## Decision

Every mechanics package `PROVENANCE.md` now carries the same operating shape:

- `Current Route First`
- `Archive Route`
- dated accounting sections
- `Distillation Rule`

`validate_nested_agents.py` now enforces that shape for every mechanics package
bridge.

## Consequences

Future migrations should update the active part first, then the package
`PROVENANCE.md`, `legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md` only when
route accounting changes.

Active part docs should not grow per-source inventories. Former root paths,
raw receipts, and distillation history stay in the bridge/archive layer.
