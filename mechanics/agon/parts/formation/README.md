# Formation Part

This part routes `formation` pressure inside `mechanics/agon/`.

## Active Docs

- [Agonic Actor Rechartering](docs/actor-rechartering.md)
- [Agent Formation Trial](docs/formation-trial.md)
- [Agent Kind Model](docs/kind-model.md)
- [Agent Resistance and Revision Posture](docs/resistance-revision-posture.md)
- [Agent Subject Prep](docs/subject-prep.md)
- [Agent Subjectivity Model](docs/subjectivity-model.md)
- [Agon Wave I Landing Notes](docs/wave1-landing.md)
- [Agon Wave II.5 Landing](docs/wave2-5-landing.md)
- [Agon Wave II Landing](docs/wave2-landing.md)

## Active Schemas

- [Agent Kind](schemas/agent-kind.schema.json)
- [Agent Subjectivity](schemas/subjectivity.schema.json)
- [Agent Office Overlay](schemas/office-overlay.schema.json)
- [Agent Resistance And Revision](schemas/resistance-revision.schema.json)
- [Formation Trial](schemas/formation-trial.schema.json)
- [Schema Route](schemas/README.md)

Arena eligibility is active in the adjacent
[arena-rank-school schema route](../arena-rank-school/schemas/arena-eligibility.schema.json).

## Active Examples

- [Agent Agonic Formation Example](examples/agent-agonic-formation.example.json)
- [Formation Trial Example](examples/formation-trial.example.json)
- [Example Route](examples/README.md)

## Generated Readers

- [`generated/agent_agonic_formation_index.min.json`](../../../../generated/agent_agonic_formation_index.min.json)
- [`generated/agent_formation_trial.min.json`](../../../../generated/agent_formation_trial.min.json)

These readers stay root-published because their source truth is the agent
source district under `agents/profiles/` and `agents/profiles/adjuncts/`, and
because the trial is a repo-wide role-readiness view. This part owns the Agon
formation contracts, examples, docs, and stop-lines around those readers; it
does not own the source adjunct records or turn generated readers into source
authority.

Validate local contracts with `python scripts/validate_agon_formation_contracts.py`.

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent [PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
