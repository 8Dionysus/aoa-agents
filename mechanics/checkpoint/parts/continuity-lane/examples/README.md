# Self-Agency Continuity Examples

This directory contains inspectable examples for the `continuity-lane` part.

## Active Example

- [self-agency-continuity-window.example.json](self-agency-continuity-window.example.json)

The example illustrates a bounded continuity window. It is not live session
memory, a runtime checkpoint, or a permission to keep acting without re-entry.

## Validation

```bash
python scripts/validate_checkpoint_contracts.py
python scripts/validate_agents.py
```
