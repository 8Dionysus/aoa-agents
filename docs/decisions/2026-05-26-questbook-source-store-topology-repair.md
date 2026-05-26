# 2026-05-26: Questbook Source Store Topology Repair

## Status

Accepted.

## Context

The first Questbook payload localization treated root `QUESTBOOK.md` and
`quests/` as mechanics payloads and moved them under
`mechanics/questbook/parts/*`. A follow-up pass compared this with
`Agents-of-Abyss`, `aoa-memo`, `aoa-evals`, `aoa-skills`, and
`aoa-techniques`.

Those sources converge on a stronger split:

- root `QUESTBOOK.md` owns the human open-obligation index
- root `quests/` owns lane-first source quest records
- `mechanics/questbook/` owns source-store law, public-index route,
  lifecycle/projection contracts, and validation posture
- generated quest readers are derived read models, not source quest truth

## Decision

Restore `QUESTBOOK.md` as the root human index and restore `quests/` as the
lane-first source quest district:

```text
quests/agents/<state>/AOA-AG-Q-*.yaml
quests/agon/captured/*.md
```

Keep quest catalog and dispatch readers root-published under `generated/`
because they summarize root `quests/` for low-context consumers. Add a
dedicated Questbook reader builder/checker at
`scripts/generate_questbook_readers.py`.

Retire the part-local `quest-catalog` and `agon-quest-surfaces` source-store
shape in favor of `public-index`, `quest-item-store`, and `dispatch-reader`
parts that route to root-owned source/index/generated surfaces.

## Consequences

- `QUESTBOOK.md` is active root source for human open-obligation visibility.
- `quests/` is active root source for lane-first quest records.
- `mechanics/questbook/parts/public-index/` routes the root index.
- `mechanics/questbook/parts/quest-item-store/` routes root source records.
- `mechanics/questbook/parts/dispatch-reader/` routes root generated readers.
- `scripts/validate_agents.py` enforces `quests/agents/<state>/` for YAML
  records and checks generated reader drift.
- The earlier part-local source-store decision is superseded where it moved
  active quest source truth under `mechanics/questbook/parts/*`.

## Validation

```bash
python scripts/generate_questbook_readers.py --check
python scripts/validate_agents.py
python scripts/validate_nested_agents.py
python -m pytest -q tests/test_validate_agents.py tests/test_roadmap_parity.py
python scripts/release_check.py
```
