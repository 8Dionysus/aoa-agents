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

## Validation

For decision-only changes, run the narrow docs/topology validators:

```bash
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
```

