# Seed Manifest: Agon Wave II.5 / Formation Trial

This seed lands the first **Formation Trial** for `aoa-agents`.

It assumes Agon Wave I and Wave II have already landed:

- `generated/agent_agonic_formation_index.min.json`
- `generated/assistant_civil_formation_index.min.json`

Wave II.5 does not create new roles, new assistants, arena sessions, lawful moves, verdicts, scars, retention checks, runtime packets, or ToS promotion paths. It judges whether the actor forms created by Waves I and II are coherent enough to be read by the next wave.

## Landing target

Merge the contents of `repo/` into the root of `aoa-agents`.

## Added surfaces

```text
docs/AGENT_FORMATION_TRIAL.md
docs/AGON_PRE_PROTOCOL_AGENT_BOUNDARY.md
docs/FORMATION_TRIAL_READINESS.md
docs/CODEX_PROJECTION_AGON_BOUNDARY.md
docs/AGON_WAVE2_5_LANDING.md
schemas/agent_formation_trial_v1.json
generated/agent_formation_trial.min.json
scripts/build_agent_formation_trial.py
scripts/validate_agent_formation_trial.py
tests/test_agent_formation_trial.py
examples/agent_formation_trial.example.json
quests/AOA-AG-Q-AGON-0007-formation-trial.md
quests/AOA-AG-Q-AGON-0008-formation-trial-validation-integration.md
quests/AOA-AG-Q-AGON-0009-pre-protocol-agent-boundary.md
```

## Commands after merge

```bash
python scripts/build_agent_formation_trial.py --check
python scripts/validate_agent_formation_trial.py
python -m pytest -q tests/test_agent_formation_trial.py
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

It is permission for the next wave to design lawful movement against actor forms that are no longer vague.
