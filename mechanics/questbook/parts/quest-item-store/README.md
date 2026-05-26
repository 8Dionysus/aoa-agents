# Quest Item Store Part

This part owns the route to lane-first source quest records.

## Source Surface

- [quests](../../../../quests/README.md)

## Role

Keep quest source files in `quests/<lane>/<state>/`. Route YAML shape through
the external Questbook schema contract and local validation. Route Agon markdown
notes through the Agon lane before changing lifecycle state.

Use parent [PARTS](../../PARTS.md) for the full mechanic map and parent
[PROVENANCE](../../PROVENANCE.md) for former path accounting.
