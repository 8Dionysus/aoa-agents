# aoa-agents Memo Port

This is the role-layer local memory port for `aoa-agents`.

Use it for candidates, receipts, exports, and local notes that should be visible
to future agents without making `aoa-agents` the central memory authority.

| Path | Use |
|---|---|
| `PORT.yaml` | role-layer port contract |
| `INDEX.md` / `index.min.json` | generated local read model over packets |
| `candidates/` | proposed memory claims with evidence refs |
| `receipts/` | accept, reject, validate, or forward traces |
| `exports/` | reviewed-intake packets for `aoa-memo` |
| `local/` | role-layer memory notes that should remain local |

Default write mode: `write_candidate_only`.
