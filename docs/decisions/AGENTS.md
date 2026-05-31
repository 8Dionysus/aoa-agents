# AGENTS.md

## Applies To

This card applies to `docs/decisions/`.

## Role

`docs/decisions/` records structural, ownership, workflow, route-law, validator,
and topology decisions that future agents need to understand before continuing
the repository.

## Boundaries

- Keep decisions short and evidence-linked.
- Do not use decision notes as replacement docs for active source surfaces.
- Do not record tiny self-evident wording edits.
- When a decision changes a route, link the owning route card.
- Use canonical `AOA-AG-D-####` filenames for live decision records.
- Treat `indexes/` as generated lookup read models, not rationale authority.
- Do not recreate retired date-prefixed paths or compatibility maps for old
  decision names.

## Validation

For decision-only changes, run the narrow docs/topology validators:

```bash
python scripts/generate_decision_indexes.py --check
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
```
