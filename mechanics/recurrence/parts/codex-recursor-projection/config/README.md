# Codex Recursor Projection Config

## Operating Card

| Field | Route |
| --- | --- |
| role | source candidate config for future Codex-visible recursor projection |
| input | reviewed candidate mapping from recursor roles to Codex names and safeguards |
| output | generated recursor projection candidate index |
| owner | `mechanics/recurrence/parts/codex-recursor-projection/` |
| next route | projection boundary docs, recursor readiness config, generated candidate reader |
| tools | `mechanics/recurrence/scripts/build_recursor_projection_candidates.py`, `mechanics/recurrence/scripts/validate_recursor_boundary.py` |
| validation | projection builder with `--check` plus recursor boundary validator |

## Active Config

- [projection-candidate.json](projection-candidate.json)

## Boundaries

This config is candidate-only and disabled by default. It must not modify Codex
subagent wiring, generated Codex agents, host `.codex/agents/`, or owner review
requirements.
