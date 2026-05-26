# 2026-05-26: Mechanics Package Route Cards

## Context

`aoa-agents` already had an active `mechanics/` atlas, package `README.md`
files, package `PARTS.md` files, part-local `parts/AGENTS.md` cards, and
legacy/provenance bridges. A source pass over `Agents-of-Abyss`, `aoa-memo`,
`aoa-evals`, `aoa-skills`, and `aoa-techniques` showed that refactored
mechanics packages also expose a nearest `mechanics/<package>/AGENTS.md`.

Without that layer, an agent entering `mechanics/questbook/`, `mechanics/agon/`,
or another package had to jump from the atlas directly to package README prose
or part-local cards. That made owner boundaries less discoverable than in the
source repositories.

## Decision

Add a package-local `AGENTS.md` to every active `mechanics/<package>/` route in
`aoa-agents`.

Each card records:

- package role
- input and output route
- owner split
- next route through `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part
  README, and `PROVENANCE.md`
- stronger-owner stop-lines
- narrow validation commands
- closeout expectations

`scripts/validate_nested_agents.py` now requires these package cards.

## Consequences

This is a navigation and route-law slice only. It does not move source,
support, generated, schema, example, script, or test payloads.

Future mechanics work should enter through the package card before editing
part-local surfaces. If a new mechanics package is added later, it should gain
its own `AGENTS.md` before payload movement.
