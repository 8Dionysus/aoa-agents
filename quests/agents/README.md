# Agents Quest Lane

This lane holds schema-backed `AOA-AG-Q-*.yaml` source records for
agent-layer obligations.

Use lifecycle directories directly:

```text
quests/agents/<state>/AOA-AG-Q-*.yaml
```

The YAML `state` field must match the directory name. Generated catalog and
dispatch readers are rebuilt from these records through
`mechanics/questbook/parts/dispatch-reader/scripts/generate_questbook_readers.py`.
