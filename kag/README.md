# aoa-agents Local KAG Provider

`kag/` exposes the current `aoa-agents` KAG provider packet as portable
source-linked records.

## Operating Card

| Field | Route |
| --- | --- |
| role | local KAG provider for agent role source-home, role registry, and capability pack registry surfaces |
| records | `nodes/`, `edges/`, `indexes/`, `projections/`, `receipts/` |
| manifest | `manifest.json` |
| source route | `agents/source_home.manifest.json` and `agents/README.md` |
| consumer route | `aoa-kag` registry/composition, `abyss-stack`, MCP resources |
| owner return | `agents/README.md` |

## Record Classes

| Class | Current record |
| --- | --- |
| node | source surface and owner-return route |
| edge | source surface returns to the owner route |
| index | source surface inventory over local records |
| projection | MCP-readable source-return packet |
| receipt | validation receipt for the current owner route |

Git holds compact provider records and source-return handles. Runtime graph,
vector, embedding, cache, and serving state stay with runtime owners.
