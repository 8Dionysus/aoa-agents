# Codex Recursor Projection Boundary

## Rule

Codex projection candidates are not installed agents.

This seed may publish:

```text
config/codex_recursor_projection.candidate.json
generated/recursor_projection_candidates.min.json
```

It must not mutate:

```text
config/codex_subagent_wiring.v2.json
generated/codex_agents/agents/*.toml
generated/codex_agents/config.subagents.generated.toml
.codex/agents/
```

## Candidate-only posture

Projection candidates must set:

```json
{
  "projection_status": "candidate_only",
  "install_by_default": false,
  "requires_owner_review": true
}
```

## No hidden arena

Codex must not become a hidden arena. Agonic subjectivity, assistant governance,
arena eligibility, resistance posture, and formation-trial verdicts remain
source-owned actor surfaces, not automatic prompt behavior.
