# Agon Parts

## Current Parts

| Part | Operation | Current payload anchors |
| --- | --- | --- |
| `formation` | Wave I agonic actor, Wave II assistant civil posture, Wave II.5 formation trial | `agents/profiles/adjuncts/kind/`, `subjectivity/`, `office_overlay/`, `resistance_revision/`, `assistant_*`; `docs/AGENT_FORMATION_TRIAL.md`; `docs/AGON_WAVE1_LANDING.md`; `docs/AGON_WAVE2_LANDING.md`; `docs/AGON_WAVE2_5_LANDING.md`; `generated/agent_agonic_formation_index.min.json`; `generated/assistant_civil_formation_index.min.json`; `generated/agent_formation_trial.min.json` |
| `pre-protocol-boundary` | keep pre-protocol posture bounded before role promotion | `docs/AGON_PRE_PROTOCOL_AGENT_BOUNDARY.md`; `docs/FORMATION_TRIAL_READINESS.md`; `docs/CODEX_PROJECTION_AGON_BOUNDARY.md` |
| `arena-rank-school` | rank jurisdiction, school affiliation, school campaign posture, arena limits | `config/agon_agent_rank_jurisdiction.seed.json`; `config/agon_agent_school_campaign_posture.seed.json`; `docs/AGON_AGENT_RANK_JURISDICTION.md`; `docs/AGON_AGENT_SCHOOL_CAMPAIGN_POSTURE.md`; `docs/AGONIC_ACTOR_ARENA_ELIGIBILITY.md` |
| `epistemic-actor` | agent posture for concept, model-of-other, and epistemic actor limits | `config/agon_epistemic_actor_posture.seed.json`; `docs/AGON_EPISTEMIC_ACTOR_POSTURE.md`; `docs/AGON_CONCEPT_BOUNDARY.md`; `docs/AGON_MODEL_OF_OTHER_BOUNDARY.md` |
| `adoption-retention` | pattern adoption, shared scars, retention readiness after contest pressure | `docs/AGON_PATTERN_ADOPTION_TRIALS.md`; `docs/AGON_SHARED_SCAR_HARVEST.md`; `docs/AGON_RETENTION_READINESS.md`; assistant adoption examples and schemas cross-route through `experience/` |
| `recursor-boundary` | Agon-facing recursor and recurrence limits | `docs/AGON_RECURSOR_BOUNDARY.md`; `docs/AGON_RECURRENCE_ADAPTER.md`; `docs/AGON_TRIAL_RUNTIME_HOLDS.md`; recurrence payloads route through `mechanics/recurrence/` |

## Move Posture

Payloads stay in their current root districts. A later move should start with
`formation`, because it already has source adjuncts, generated indexes,
builders, validators, and route tests.
