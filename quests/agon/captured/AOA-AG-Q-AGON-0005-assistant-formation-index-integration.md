# AOA-AG-Q-AGON-0005: Assistant Formation Index Integration

## Repository

`aoa-agents`

## Goal

Make the assistant civil formation index visible to repo validation after owner review.

## Work

- review generated assistant index shape
- decide whether `scripts/validate_agents.py` should call `validate_assistant_civil_formation.py`
- decide whether `scripts/build_published_surfaces.py` should call `build_assistant_civil_formation_index.py`
- document that this is an actor-side formation surface, not protocol law

## Exit

- owner-reviewed validation route is explicit
- generated drift is checked in the chosen release path
