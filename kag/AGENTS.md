# AGENTS.md

## Applies to

This card applies to `aoa-agents/kag/` and every nested path until a nearer card
narrows the lane.

## Role

`kag/` is the local KAG provider home for `aoa-agents`. It exposes compact,
source-linked records over `agent roles and capability pack registries` for `aoa-kag` registry,
composition, and MCP consumers.

## Read before editing

Read the root `AGENTS.md`, this card, `kag/README.md`, `kag/manifest.json`,
`agents/source_home.manifest.json`, and `agents/README.md` before
changing provider records.

## Boundaries

Keep authored meaning with `aoa-agents` source surfaces. Keep shared KAG schema,
registry, composition, and provider validation with `aoa-kag`. Keep runtime
serving state with `abyss-stack` or the runtime owner named by the consumer.

## Validation

Use the owner validator named in `manifest.json`, then validate this provider
through the `aoa-kag` local subtree validator.

## Closeout

Report provider records changed, source-return route changed, owner validation,
`aoa-kag` validation, and the next MCP consumer route.
