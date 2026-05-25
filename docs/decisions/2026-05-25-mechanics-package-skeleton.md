# 2026-05-25: Mechanics Package Skeleton

## Status

Accepted.

## Context

`mechanics/` existed as an atlas, but the repeatable operations inside
`aoa-agents` were still implicit in large root payload districts:
`docs/`, `schemas/`, `examples/`, `agents/`, `tests/`, `scripts/`,
`generated/`, `quests/`, `manifests/`, and `config/`.

The root sweep showed dense operation clusters around Agon, assistant
experience, Titan, recurrence, runtime seam, Codex projection, checkpoint,
quest posture, progression, antifragility, boundary handoff, and release
support. At the same time, many payload paths are public contract anchors or
validator inputs, so moving them all into packages now would create a large
contract-sensitive topology change.

## Considered Options

- Keep `mechanics/` atlas-only until the next payload migration.
- Create a top-level `formation/` package for the visible formation work.
- Create topic folders for every dense filename cluster and move matching
  payloads immediately.
- Create operation-parent package skeletons now, and leave payloads in their
  current owner districts until package-local contracts and validators exist.

## Decision

Create package skeletons under `mechanics/` for the current repeatable
agent-layer mechanics:

- `agon/`
- `experience/`
- `titan/`
- `recurrence/`
- `runtime-seam/`
- `codex-projection/`
- `checkpoint/`
- `questbook/`
- `rpg/`
- `antifragility/`
- `boundary-bridge/`
- `release-support/`

Each package starts with `README.md` and `PARTS.md`. The skeletons name the
operation, current payload anchors, stronger-owner stop-lines, and validation
route. They do not move payloads from root districts.

Extend each package with:

- `parts/AGENTS.md` and `parts/README.md` as the active lower part route;
- child `parts/<part>/README.md` cards for each named current part, while
  payload anchors still remain in root districts;
- `PROVENANCE.md` as the active bridge into legacy;
- `legacy/AGENTS.md`, `legacy/README.md`, `legacy/INDEX.md`,
  `legacy/DISTILLATION_LOG.md`, and `legacy/raw/README.md` as provenance and
  old-route accounting scaffolds.

The legacy scaffolds start with empty raw inventories. Current root payloads
are not called legacy merely because they are waiting for a later
package-local move.

Formation routes through `mechanics/agon/` as a part, because Agon is the
parent operation. Assistant service, office, adoption, watch, and rollback
pressure routes through `mechanics/experience/`, because it is service
experience posture rather than the whole repository layer.

## Consequences

- Future mechanics work can start from a package card instead of reconstructing
  the topology from filename clusters.
- Future part work can start from `parts/README.md` after the parent package
  is selected, then enter the child part card before any payload move.
- Historical or old-path lookup starts from `PROVENANCE.md`, then enters
  `legacy/`; legacy is not the normal first route for current behavior.
- `docs/`, `schemas/`, `examples/`, `scripts/`, `tests/`, `generated/`,
  `config/`, `manifests/`, and `quests/` remain authoritative root districts
  for their current payload classes.
- A later payload move must be a smaller slice with package-local validation,
  compatibility handling, and a route note when lookup topology changes.
- The skeleton may grow or split, but it should stay operation-first rather
  than becoming a topic taxonomy.

## Verification

This decision is verified by:

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

`mechanics/PAYLOAD_RECON.md` records the root-folder sweep that shaped the
package set. `mechanics/LEGACY_TOPOLOGY.md` records the active/legacy split
used by the package scaffolds.
