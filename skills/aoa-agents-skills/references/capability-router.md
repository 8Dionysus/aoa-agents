# aoa-agents capability router

Generated from owner capability contracts. This card is a retrieval read model, not procedure or proof authority.

Source graph hash: `34017bac74d3d378751ff27d23164796e539c22afda54d662b6e48c824702533`
Federation: `aoa-agents` specializes `aoa-skills:operations`.

| skill | visibility | use when | do not use when | version | fingerprint |
|---|---|---|---|---|---|
| `aoa-agents-skills` | advertised | Before any decision to call a built-in Codex agent, sub-agent, collaboration, or delegation tool.; A request or plan proposes an agent, worker, reviewer, researcher, parallel lane, background role, or delegated duty whose responsibility boundary is not yet classified.; Goal planning, execution, or closeout exposes a duty that may need an independently addressable responsibility bearer.; An existing persistent role may need rebinding, return filtering, or controlled wake. | No agent-tool decision, delegation pressure, or independent-duty pressure exists. | 0.5.0 | `095f6dcad25980db` |
| `aoa-session-progression-lift` | advertised | Closed reviewed evidence shows attributable movement or regression for one agent with a baseline. | Evidence is live; no baseline exists; or the request would mutate a role; grant authority; or set routing policy. | 0.2.5 | `5b795c438a553cbb` |
| `aoa-summon` | advertised | aoa-agents-skills selects this execution leaf from a complete task-local actor DAG with an admitted transfer and return owner.; The user explicitly requests a disposable Codex-local child and aoa-agents-skills has classified it not_independent before a complete anchored local-child packet is supplied. | The request is incomplete; implicit; unsplit deep work; or intended to widen authority. | 0.4.0 | `831555e31db0450c` |

Load the named `SKILL.md` for procedure. Use the full generated graph for ABI, effects, failures, relations, and composition; do not infer invocation or benefit from selection alone.
