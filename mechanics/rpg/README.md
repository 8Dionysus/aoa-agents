# RPG Mechanic

Status: skeleton.

`mechanics/rpg/` routes progression, mastery, unlock, and cohort posture for
agents. It is intentionally thin: the current payload is real, but it should
grow only where role progression becomes a repeatable operation rather than a
decorative metaphor.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent progression and mastery posture package |
| input | progression, mastery, unlock, cohort, quest-readable status, and growth pressure |
| output | bounded progression posture, cohort route, quest-readable handoff, or stronger-owner handoff |
| owner | this package for role progression routing |
| next route | `PARTS.md`, `mechanics/checkpoint/`, `mechanics/questbook/` |
| validation | affected cohort builders/tests plus repo validators |

## Agent Layer Owns

- agent progression model language
- cohort posture where it affects role capability and handoff
- quest-readable status where it remains an agent contract

## Stronger Owner Split

- Game mechanics implementation does not live here.
- Quest choreography belongs to `aoa-playbooks`.
- Stats and movement summaries belong to `aoa-stats`.
- Proof of mastery belongs to `aoa-evals`.

## Validation

```bash
python scripts/build_published_surfaces.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```
