# Seed Manifest: Formation Trial

This seed lands the first **Formation Trial** for `aoa-agents`.

It assumes Agonic Actor Rechartering and Assistant Civil Rechartering have
already landed:

- `generated/agent_agonic_formation_index.min.json`
- `generated/assistant_civil_formation_index.min.json`

Formation Trial does not create new roles, new assistants, arena sessions,
lawful moves, verdicts, scars, retention checks, runtime packets, or ToS
promotion paths. It judges whether the actor forms created by Agonic Actor
Rechartering and Assistant Civil Rechartering are coherent enough to be read by
lawful-move design.

## Landing target

Merge the contents of `repo/` into the root of `aoa-agents`.

## Added surfaces

```text
mechanics/agon/parts/formation/docs/formation-trial.md
mechanics/agon/parts/pre-protocol-boundary/docs/pre-protocol-agent-boundary.md
mechanics/agon/parts/pre-protocol-boundary/docs/formation-trial-readiness.md
mechanics/codex-projection/parts/agon-boundary/docs/projection-agon-boundary.md
mechanics/agon/parts/formation/docs/formation-trial-landing.md
mechanics/agon/parts/formation/schemas/formation-trial.schema.json
generated/agent_formation_trial.min.json
mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py
mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
mechanics/agon/parts/formation/tests/test_agent_formation_trial.py
mechanics/agon/parts/formation/examples/formation-trial.example.json
quests/AOA-AG-Q-AGON-0007-formation-trial.md
quests/AOA-AG-Q-AGON-0008-formation-trial-validation-integration.md
quests/AOA-AG-Q-AGON-0009-pre-protocol-agent-boundary.md
```

## Commands after merge

```bash
python mechanics/agon/parts/formation/scripts/build_agent_formation_trial.py --check
python mechanics/agon/parts/formation/scripts/validate_agent_formation_trial.py
python -m pytest -q mechanics/agon/parts/formation/tests/test_agent_formation_trial.py
```

## Expected first verdict

The expected global verdict is:

```text
pass_pre_protocol_formation_trial
```

Expected counts:

- five base role homes
- five agonic actor forms
- five assistant variants
- three contestant candidates
- three witness candidates
- one judge candidate
- zero closer candidates
- zero summon initiator candidates
- zero assistant arena candidates

## Main invariant

A passed Formation Trial is not permission to open an arena.

It is permission for the next reviewed turn to design lawful movement against actor forms that are no longer vague.
