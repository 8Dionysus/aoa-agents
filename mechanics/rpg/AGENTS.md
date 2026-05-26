# AGENTS.md

## Applies To

This card applies to `mechanics/rpg/` and descendants until a nearer
`AGENTS.md` narrows the route.

## Role

`mechanics/rpg/` routes progression, mastery, unlock, cohort, and
quest-readable status posture for agents. It should grow only where role
progression is a repeatable operation rather than decorative metaphor.

## Operating Card

| Field | Route |
| --- | --- |
| role | agent progression and mastery posture package |
| input | progression, mastery, unlock, cohort, quest-readable status, and growth pressure |
| output | bounded progression posture, cohort route, quest-readable handoff, or stronger-owner handoff |
| owner | this package for role progression routing |
| next route | `README.md`, `PARTS.md`, `parts/AGENTS.md`, target part README, `PROVENANCE.md`, `mechanics/checkpoint/`, `mechanics/questbook/` |
| tools | published surface builder, RPG progression validator, repo validators |
| validation | affected cohort/progression checks plus repo validators |

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `mechanics/AGENTS.md`
4. this package `README.md`
5. `PARTS.md`
6. `parts/AGENTS.md` and the target part README
7. `PROVENANCE.md` for provenance accounting
8. stronger owner routes for playbook, stats, proof, or runtime pressure

## Boundaries

- Game mechanics implementation does not live here.
- Quest choreography belongs to `aoa-playbooks`.
- Stats and movement summaries belong to `aoa-stats`.
- Proof of mastery belongs to `aoa-evals`.

## Validation

```bash
python mechanics/rpg/parts/progression-model/scripts/validate_rpg_progression.py
python scripts/build_published_surfaces.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
```

## Closeout

Report the changed RPG part, progression or cohort surface affected, checks
run, checks skipped, and any playbook, stats, or proof handoff.
