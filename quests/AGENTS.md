# AGENTS.md

## Applies To

`quests/` and all descendant quest source records.

## Role

`quests/` is the lane-first source quest district for durable `aoa-agents`
obligations. `QUESTBOOK.md` is the human open-obligation index.
`mechanics/questbook/` owns the Questbook operation package, source-store route,
execution passport posture, and generated reader contract.

## Route Rules

- Source quest records live under `quests/<lane>/<state>/`.
- YAML agent-layer records live under `quests/agents/<state>/AOA-AG-Q-*.yaml`.
- Agon markdown notes live under `quests/agon/<state>/`.
- The lifecycle directory must match the YAML `state` field when a YAML record
  has one.
- Generated quest readers in `generated/` are derived read models. Rebuild them
  from source records; do not hand-author reader truth.
- Quest files are durable obligations, not hidden task dumps, roadmap copies,
  proof verdicts, or live runtime authority.

## Read Before Editing

1. root `AGENTS.md`
2. `QUESTBOOK.md`
3. `quests/README.md`
4. `mechanics/questbook/README.md`
5. the nearest lane README

## Validation

After changing YAML source records or generated quest readers, run:

```bash
python scripts/generate_questbook_readers.py --check
python scripts/validate_agents.py
```

Run broader repo validation when route docs, generated surfaces, or mechanics
maps change.
